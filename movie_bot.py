import os
import re
import asyncio
import time

from telethon import TelegramClient, events, sync
from telethon.tl.functions.messages import SearchRequest
from telethon.tl.types import InputMessagesFilterDocument

api_id = os.getenv("API_ID", "optional-default")
api_hash = os.getenv("API_HASH", "optional-default")


channel_names = ["HEVC_MOVIES_SERIES", "Qualitymovies", "MM_HEVC_Movies", "CC_x265", "koreanmovieshub", "TAMILROCKERS", "MM_Old"]

client = TelegramClient("Movie Bot", api_id, api_hash)
client.start()


movies = []




async def get_movies(name_of_the_movie):
    for channel_name in channel_names:
        print("I am here")
        if len(movies) >= 3:
            break
        print("searching in "+channel_name)
        channel_obj = await client.get_entity(channel_name)
        print("got channel")
        filter = InputMessagesFilterDocument()
        posts = await client(SearchRequest(
            peer=channel_obj,      # On which chat/conversation
            q=name_of_the_movie,      # What to search for
            filter=filter,  # Filter to use (maybe filter for media)
            min_date=None,  # Minimum date
            max_date=None,  # Maximum date
            offset_id=0,    # ID of the message to use as offset
            add_offset=0,   # Additional offset
            limit=10,       # How many results
            max_id=0,       # Maximum message ID
            min_id=0,       # Minimum message ID
            from_id=None,    # Who must have sent the message (peer)
            hash=0
        ))
        messages = posts.messages
        for message in messages:
            movies.append(message.media)

async def Sending_File(movie_list, event):
    for movie in movie_list:
        print("sending the file")
        await event.reply(file=movie)





@client.on(events.NewMessage(("Anu Sis")))
async def my_event_handler(event):
    if '@movie_finder' in event.raw_text:
        print("got search request")
        raw_string = event.raw_text
        new_string = re.sub('@movie_finder ', '', raw_string)
        print("edited the request")
        print("Trying to fetch the movies") 
        await get_movies(new_string)
        if len(movies) == 0:
            print("No movies found")
            await event.reply("Sorry No Movies Found!")
        else:
            print("sending movies")
            await Sending_File(movies, event)
            movies.clear()
            print("Completed sending the files")
            time.sleep(60)

client.run_until_disconnected()







