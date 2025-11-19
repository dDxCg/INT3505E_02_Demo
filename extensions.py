# extensions.py
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

cache = Cache()

redis_uri = os.getenv("REDIS_URI", "redis://:<password>@redis-16478.crce185.ap-seast-1-1.ec2.cloud.redislabs.com:16478/0")

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=redis_uri
)