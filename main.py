import requests
import json
import uuid
from datetime import datetime 

class SteamReviewCrawler:
    def __init__(self, franchise, game_name, source, app_id):
        self.franchise = franchise # Attribute
        self.game_name = game_name # Attribute
        self.source = source       # Attribute
        self.app_id = app_id       # Attribute
        self.reviews = []          # Attribute to store reviews 
    
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