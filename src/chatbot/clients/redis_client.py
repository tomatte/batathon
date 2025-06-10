import redis
from typing import Optional, Any
import logging

logger = logging.getLogger(__name__)

class RedisClient:
    def __init__(self, host: str = "redis", port: int = 6379, db: int = 0):
        """
        Initialize Redis client.
        
        Args:
            host: Redis host (default: "redis" - the service name in docker network)
            port: Redis port (default: 6379)
            db: Redis database number (default: 0)
        """
        self._client: Optional[redis.Redis] = None
        self._host = host
        self._port = port
        self._db = db

    @property
    def client(self) -> redis.Redis:
        """Get Redis client instance, creating it if it doesn't exist."""
        if self._client is None:
            try:
                self._client = redis.Redis(
                    host=self._host,
                    port=self._port,
                    db=self._db,
                    decode_responses=True  # Automatically decode responses to strings
                )
                # Test connection
                self._client.ping()
                logger.info("Successfully connected to Redis")
            except redis.ConnectionError as e:
                logger.error(f"Failed to connect to Redis: {e}")
                raise
        return self._client

    def set(self, key: str, value: Any, ex: Optional[int] = None) -> bool:
        """
        Set a key-value pair in Redis.
        
        Args:
            key: The key to set
            value: The value to set
            ex: Optional expiration time in seconds
            
        Returns:
            bool: True if successful
        """
        return self.client.set(key, value, ex=ex)

    def get(self, key: str) -> Optional[str]:
        """
        Get a value from Redis by key.
        
        Args:
            key: The key to get
            
        Returns:
            Optional[str]: The value if found, None otherwise
        """
        return self.client.get(key)

    def delete(self, key: str) -> int:
        """
        Delete a key from Redis.
        
        Args:
            key: The key to delete
            
        Returns:
            int: Number of keys deleted
        """
        return self.client.delete(key)

    def exists(self, key: str) -> bool:
        """
        Check if a key exists in Redis.
        
        Args:
            key: The key to check
            
        Returns:
            bool: True if key exists
        """
        return bool(self.client.exists(key))

    def close(self) -> None:
        """Close the Redis connection."""
        if self._client is not None:
            self._client.close()
            self._client = None
            logger.info("Redis connection closed")
