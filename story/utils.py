import datetime
from firebase_admin import storage
import requests
import soundfile as sf
import os
import random
from story.models import SystemSettings

def get_token(key):
    obj = SystemSettings.objects.filter(key=key).first()

    if obj:
        return obj.value

    return os.getenv(key)


def upload_file(story_id, img_url):
        avatar_response = requests.get(img_url)
        avatar_content_type = "audio/mpeg"
        avatar_data = avatar_response.content

        filename = f"{story_id}_{str(datetime.datetime.now().timestamp())}.mp3"
        path = "openVNU/" + filename

        bucket = storage.bucket()
        blob = bucket.blob(path)
        blob.upload_from_string(
            avatar_data, content_type=avatar_content_type
        )

        avatar_url = (
            "https://firebasestorage.googleapis.com/v0/b/gokag-19eac.appspot.com/o/openVNU%2F"
            + filename
            + "?alt=media"
        )

        return avatar_url

def fetch_and_check_audio_length(audio_url):
    print(audio_url)
    audio_response = requests.get(audio_url, stream=True)
    print(audio_response)

    if audio_response.status_code == 200:
        audio_data = audio_response.content

        with open("temp_audio.mp3", "wb") as f:
            f.write(audio_data)

        audio_data, sample_rate = sf.read("temp_audio.mp3")

        audio_duration = len(audio_data) / sample_rate
        print(audio_duration)

        os.remove("temp_audio.mp3")

        return audio_duration
    else:
        print("Failed to fetch audio from the provided URL")
        return 0

def shuffle_array(arr):
    while True:
        random.shuffle(arr)

        has_consecutive_duplicates = any(arr[i] == arr[i + 1] for i in range(len(arr) - 1))

        if not has_consecutive_duplicates:
            return arr
