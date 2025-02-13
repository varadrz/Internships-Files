import requests
import json
import instaloader
from googleapiclient.discovery import build

# Function to get YouTube data
def get_youtube_data(channel_id):
    youtube = build('youtube', 'v3', developerKey='YOUR_YOUTUBE_API_KEY')  # Replace with your API Key
    request = youtube.channels().list(part="snippet,contentDetails,statistics", id=channel_id)
    response = request.execute()
    return {
        'channel_name': response['items'][0]['snippet']['title'],
        'followers': response['items'][0]['statistics']['subscriberCount'],
        'views': response['items'][0]['statistics']['viewCount'],
        'videos': response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    }

# Function to get Instagram data
def get_instagram_data(username):
    L = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(L.context, username)
    followers = profile.get_followers()
    posts = profile.get_posts()
    
    post_urls = [post.url for post in posts]
    
    return {
        'username': profile.username,
        'followers': followers,
        'posts': post_urls
    }

# Function to scrape data based on URL
def scrape_data(url):
    if "youtube" in url:
        channel_id = url.split('/')[-1]
        return get_youtube_data(channel_id)
    
    elif "instagram" in url:
        username = url.split('/')[-1]
        return get_instagram_data(username)
    
    else:
        print("Invalid URL. Please provide a valid YouTube or Instagram URL.")
        return None

# Function to save data in a JSON file
def save_data(data, filename='scraped_data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Main execution
if __name__ == "__main__":
    # Example URL Inputs
    url = input("Enter the YouTube or Instagram URL to scrape: ")
    
    # Scrape data
    scraped_data = scrape_data(url)
    
    if scraped_data:
        print("Scraped Data:", scraped_data)
        save_data(scraped_data)  # Save data to a JSON file
        print(f"Data saved to 'scraped_data.json'.")
    else:
        print("No data scraped.")
