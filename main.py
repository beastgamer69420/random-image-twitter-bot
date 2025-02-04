import tweepy
import os
import random
import io
import schedule
import time
from configs import client,api
from datetime import datetime, timedelta

FOLDER_PATH = "YOUR_FOLDER_PATH_HERE" # ok u can guess what this 
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif")  # Valid image extensions
TWEET_INTERVAL = 15 # this is in seconds

def get_random_image(folder_path):
    image_files = [
        file
        for file in os.listdir(folder_path)
        if file.lower().endswith(IMAGE_EXTENSIONS)
    ]
    if image_files:
        random_image = random.choice(image_files)
        image_path = os.path.join(folder_path, random_image)
        return image_path, random_image
    else:
        return None, None
    
def tweet_action(): 
    image_path, random_image = get_random_image(FOLDER_PATH)

    if image_path:
        with open(image_path, "rb") as file:
            image_content = file.read()

        image_io = io.BytesIO(image_content)
        media = api.media_upload(filename=random_image, file=image_io)

        client.create_tweet(media_ids=[media.media_id])

schedule.every(TWEET_INTERVAL).seconds.do(tweet_action)

while True:
    schedule.run_pending()
    time.sleep(1)
