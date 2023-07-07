import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = 'AIzaSyDmHVppYFI-q7dy4BjdNHdQagVGDSNHD2I'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def get_comments(video_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    comments = []
    results = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        maxResults=100
    ).execute()

    for item in results["items"]:
        comment = item["snippet"]["topLevelComment"]
        text = comment["snippet"]["textDisplay"]
        comments.append(text)

    return comments

# Input the YouTube URL
url = input("Enter a YouTube URL to check: ")

# Send a GET request to the URL and parse the HTML content of the response using BeautifulSoup
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find the video title using the "title" tag
video_title = soup.find("title").text
print(f"Checking video: {video_title}")

# Check if the video title contains the keywords
title_lower = video_title.lower()
if "never gonna give you up" in title_lower or "rick roll" in title_lower:
    print(f"Found 'never gonna give you up' or 'rick roll' in video title: {video_title}")
else:
    print("No 'never gonna give you up' or 'rick roll' found in video title.")

# Find the video ID from the URL
video_id = url.split("=")[-1]

# Retrieve comments using the YouTube Data API
comments = get_comments(video_id)
num_comments = len(comments)
print(f"Checking the first {num_comments} comments...")

rickroll_count = 0
for comment in comments[:50]:  # Check the first 50 comments
    text = comment.lower()
    if "rick roll" in text or "rick astley" in text:
        print(f"Found 'rick roll' or 'rick astley' in comment: {text}")
        rickroll_count += 1

if rickroll_count > 0:
    print(f"Found {rickroll_count} comment(s) containing 'rick roll' or 'rick astley'. This might be a Rickroll!")
else:
    print("No comments containing 'rick roll' or 'rick astley' found.")
