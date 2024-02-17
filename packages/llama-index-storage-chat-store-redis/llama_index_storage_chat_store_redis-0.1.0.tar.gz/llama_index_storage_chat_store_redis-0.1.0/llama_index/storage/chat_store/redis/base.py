import json
import logging
import sys
from typing import Any, List, Optional
from urllib.parse import urlparse

from llama_index.core.bridge.pydantic import Field
from llama_index.core.llms import ChatMessage
from llama_index.core.storage.chat_store.base import BaseChatStore

import redis
from redis import Redis
from redis.cluster import RedisCluster


# Convert a ChatMessage to a json object for Redis
def _message_to_dict(message: ChatMessage) -> dict:
    return {"type": message.role, "content": message.content}


# Convert the json object in Redis to a ChatMessage
def _dict_to_message(d: dict) -> ChatMessage:
    return ChatMessage(role=d["type"], content=d["content"])


class RedisChatStore(BaseChatStore):
    """Redis chat store."""

    redis_client: Any = Field(description="Redis client.")
    ttl: Optional[int] = Field(default=None, description="Time to live in seconds.")

    def __init__(
        self,
        redis_url: str = "redis://localhost:6379",
        redis_client: Optional[Any] = None,
        ttl: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize."""
        redis_client = redis_client or self._get_client(redis_url, **kwargs)
        super().__init__(redis_client=redis_client, ttl=ttl)

    @classmethod
    def class_name(cls) -> str:
        """Get class name."""
        return "RedisChatStore"

    def set_messages(self, key: str, messages: List[ChatMessage]) -> None:
        """Set messages for a key."""
        self.redis_client.delete(key)
        for message in messages:
            self.add_message(key, message)

        if self.ttl:
            self.redis_client.expire(key, self.ttl)

    def get_messages(self, key: str) -> List[ChatMessage]:
        """Get messages for a key."""
        items = self.redis_client.lrange(key, 0, -1)
        if len(items) == 0:
            return []

        items_json = [json.loads(m.decode("utf-8")) for m in items]
        return [_dict_to_message(d) for d in items_json]

    def add_message(
        self, key: str, message: ChatMessage, idx: Optional[int] = None
    ) -> None:
        """Add a message for a key."""
        if idx is None:
            item = json.dumps(_message_to_dict(message))
            self.redis_client.rpush(key, item)
        else:
            self._insert_element_at_index(key, idx, message)

        if self.ttl:
            self.redis_client.expire(key, self.ttl)

    def delete_messages(self, key: str) -> Optional[List[ChatMessage]]:
        """Delete messages for a key."""
        self.redis_client.delete(key)
        return None

    def delete_message(self, key: str, idx: int) -> Optional[ChatMessage]:
        """Delete specific message for a key."""
        current_list = self.redis_client.lrange(key, 0, -1)
        if 0 <= idx < len(current_list):
            removed_item = current_list.pop(idx)

            self.redis_client.delete(key)
            self.redis_client.lpush(key, *current_list)
            return removed_item
        else:
            return None

    def delete_last_message(self, key: str) -> Optional[ChatMessage]:
        """Delete last message for a key."""
        return self.redis_client.rpop(key)

    def get_keys(self) -> List[str]:
        """Get all keys."""
        return [key.decode("utf-8") for key in self.redis_client.keys("*")]

    def _insert_element_at_index(
        self, key: str, index: int, message: ChatMessage
    ) -> List[ChatMessage]:
        # Step 1: Retrieve the current list
        current_list = self.get_messages(key)
        # Step 2: Insert the new element at the desired index in the local list
        current_list.insert(index, message)

        # Step 3: Push the modified local list back to Redis
        self.redis_client.delete(key)  # Remove the existing list
        self.set_messages(key, current_list)
        return self.get_messages(key)

    def _redis_cluster_client(self, redis_url: str, **kwargs: Any) -> "Redis":
        return RedisCluster.from_url(redis_url, **kwargs)  # type: ignore

    def _check_for_cluster(self, redis_client: "Redis") -> bool:
        try:
            cluster_info = redis_client.info("cluster")
            return cluster_info["cluster_enabled"] == 1
        except redis.exceptions.RedisError:
            return False

    def _redis_sentinel_client(self, redis_url: str, **kwargs: Any) -> "Redis":
        """
        Helper method to parse an (un-official) redis+sentinel url
        and create a Sentinel connection to fetch the final redis client
        connection to a replica-master for read-write operations.

        If username and/or password for authentication is given the
        same credentials are used for the Redis Sentinel as well as Redis Server.
        With this implementation using a redis url only it is not possible
        to use different data for authentication on booth systems.
        """
        parsed_url = urlparse(redis_url)
        # sentinel needs list with (host, port) tuple, use default port if none available
        sentinel_list = [(parsed_url.hostname or "localhost", parsed_url.port or 26379)]
        if parsed_url.path:
            # "/mymaster/0" first part is service name, optional second part is db number
            path_parts = parsed_url.path.split("/")
            service_name = path_parts[1] or "mymaster"
            if len(path_parts) > 2:
                kwargs["db"] = path_parts[2]
        else:
            service_name = "mymaster"

        sentinel_args = {}
        if parsed_url.password:
            sentinel_args["password"] = parsed_url.password
            kwargs["password"] = parsed_url.password
        if parsed_url.username:
            sentinel_args["username"] = parsed_url.username
            kwargs["username"] = parsed_url.username

        # check for all SSL related properties and copy them into sentinel_kwargs too,
        # add client_name also
        for arg in kwargs:
            if arg.startswith("ssl") or arg == "client_name":
                sentinel_args[arg] = kwargs[arg]

        # sentinel user/pass is part of sentinel_kwargs, user/pass for redis server
        # connection as direct parameter in kwargs
        sentinel_client = redis.sentinel.Sentinel(
            sentinel_list, sentinel_kwargs=sentinel_args, **kwargs
        )

        # redis server might have password but not sentinel - fetch this error and try
        # again without pass, everything else cannot be handled here -> user needed
        try:
            sentinel_client.execute_command("ping")
        except redis.exceptions.AuthenticationError:
            exception_info = sys.exc_info()
            exception = exception_info[1] or None
            if exception is not None and "no password is set" in exception.args[0]:
                logging.warning(
                    msg="Redis sentinel connection configured with password but Sentinel \
    answered NO PASSWORD NEEDED - Please check Sentinel configuration"
                )
                sentinel_client = redis.sentinel.Sentinel(sentinel_list, **kwargs)
            else:
                raise

        return sentinel_client.master_for(service_name)

    def _get_client(self, redis_url: str, **kwargs: Any) -> "Redis":
        """
        Get a redis client from the connection url given. This helper accepts
        urls for Redis server (TCP with/without TLS or UnixSocket) as well as
        Redis Sentinel connections.

        Redis Cluster is not supported.

        Before creating a connection the existence of the database driver is checked
        an and ValueError raised otherwise

        To use, you should have the ``redis`` python package installed.

        Example:
            .. code-block:: python

                redis_client = get_client(
                    redis_url="redis://username:password@localhost:6379"
                )

        To use a redis replication setup with multiple redis server and redis sentinels
        set "redis_url" to "redis+sentinel://" scheme. With this url format a path is
        needed holding the name of the redis service within the sentinels to get the
        correct redis server connection. The default service name is "mymaster". The
        optional second part of the path is the redis db number to connect to.

        An optional username or password is used for booth connections to the rediserver
        and the sentinel, different passwords for server and sentinel are not supported.
        And as another constraint only one sentinel instance can be given:

        Example:
            .. code-block:: python

                redis_client = get_client(
                    redis_url="redis+sentinel://username:password@sentinelhost:26379/mymaster/0"
                )
        """
        # Initialize with necessary components.
        redis_client: "Redis"
        # check if normal redis:// or redis+sentinel:// url
        if redis_url.startswith("redis+sentinel"):
            redis_client = self._redis_sentinel_client(redis_url, **kwargs)
        elif redis_url.startswith(
            "rediss+sentinel"
        ):  # sentinel with TLS support enables
            kwargs["ssl"] = True
            if "ssl_cert_reqs" not in kwargs:
                kwargs["ssl_cert_reqs"] = "none"
            redis_client = self._redis_sentinel_client(redis_url, **kwargs)
        else:
            # connect to redis server from url, reconnect with cluster client if needed
            redis_client = redis.from_url(redis_url, **kwargs)
            if self._check_for_cluster(redis_client):
                redis_client.close()
                redis_client = self._redis_cluster_client(redis_url, **kwargs)
        return redis_client
