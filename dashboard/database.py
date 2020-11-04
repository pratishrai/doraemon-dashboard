import pymongo
from pymongo import MongoClient
# import os
import env_file

token = env_file.get()
client = MongoClient(token["URI"])
# client = MongoClient(os.environ["URI"])
db = client.doraemonbot
profiles = db.guild_profiles

def guilds():
	guild = list(db.guild_profiles.find({}))
	return guild


def find_guild(guild):
	guild = profiles.find_one({"guild_id": guild})
	return guild

find_guild(709321533654433792)
