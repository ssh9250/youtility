from web.crawling.models import Story

BASE_URL = "https://hacker-news.firebaseio.com/v0"

def fetch_top_stories(limit=30)->list[dict]:
    ...

def fetch_comments(story: Story)->None:
    ...