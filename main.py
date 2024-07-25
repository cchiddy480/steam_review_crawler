import requests
import json
import uuid
import hashlib
from datetime import datetime 

class SteamReviewCrawler:
    def __init__(self, franchise, game_name, source, app_id):
        self.franchise = franchise # Attribute
        self.game_name = game_name # Attribute
        self.source = source       # Attribute
        self.app_id = app_id       # Attribute
        self.reviews = []          # Attribute to store reviews 

    # Generates unique ID for each review using ther MD5 hash of the authors 
    # steamid and review content 
    def generate_unique_id(self, review):
        review_string = review['author']['steamid'] + review['review']
        return hashlib.md5(review_string.encode()).hexdigest()
        
    # Hashes the authors information using uuid    
    def hash_author(self, author_id):
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, author_id))
    
    # Formatting the review data according to specified JSON structure
    def format_review(self, review):
        return {
            "id" : self.generate_unique_id(review),
            "author" : self.hash_author(review['author']['steamid']),
            "date" : review['timestamp_created'],
            "hours" : review.get('author', {}).get('playtime_forever', 0),
            "content" : review['review'],
            "comments" : review.get['comment_count', 0],
            "source" : self.source,
            "helpful" : review.get('votes_up', 0),
            "funny" : review.get('votes_funny', 0),
            "recommended" : review['voted_up'],
            "franchsie" : self.franchise,
            "gameName" : self.game_name
        }

    def fetch_reviews(self, params):
        url = f'https://store.steampowered.com/appreviews/{self.app_id}'
        params['num_per_page'] = 100
        cursor = '*'
        total_reviews = 0
        while total_reviews < 5000:
            params['cursor'] = cursor
            response = requests.get(url, params = params)
            data = response.json()
            reviews = data.get('reviews', [])
            if not reviews:
                break
            self.reviews.extend(reviews)
            total_reviews += len(reviews)
            cursor = data.get('cursor', '*')
            if len(reviews) < 100: # No more reviews to retreive
                break
        return data 
    
    def save_reviews_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.reviews, file, indent = 4)

# Sample Usage 
if __name__ == "__main__":
    crawler = SteamReviewCrawler("Franchise", "Game Name", "steam", "1382330")
    params = {
        'json' : 1,
        'filter' : 'recent',
    }
    crawler.fetch_reviews(params)
    crawler.save_reviews_to_file('reviews.json')