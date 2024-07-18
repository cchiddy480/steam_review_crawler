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

    def generate_unique_id(self, review):
        # review_string = review['author']['steamid'] + review['review']
        # return
        pass
    
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