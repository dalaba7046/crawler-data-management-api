import configparser
import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

CONFIG_PATH = Path(__file__).with_name("database.cfg")


def _mongodb_url_from_cfg():
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH)
    if not parser.has_section("MONGO_DEV"):
        return None

    mongo = parser["MONGO_DEV"]
    username = mongo.get("MONGODB_USERNAME")
    password = mongo.get("MONGODB_PASSWORD")
    host = mongo.get("MONGO_HOST", "localhost")
    port = mongo.get("MONGO_PORT", "27017")
    database = mongo.get("MONGO_DATABASE", "spider")

    if username and password:
        return f"mongodb://{username}:{password}@{host}:{port}/{database}?authSource=admin"
    return f"mongodb://{host}:{port}/{database}"


MONGO_DATABASE = os.getenv("MONGO_DATABASE", "spider")
MONGODB_URL = os.getenv("MONGODB_URL") or _mongodb_url_from_cfg()

if not MONGODB_URL:
    raise ValueError("MongoDB setting failed")

mongo_client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=3000)
mongo_db = mongo_client[MONGO_DATABASE]
