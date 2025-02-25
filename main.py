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
            "date" : datetime.fromtimestamp(review['timestamp_created']).strftime('%y-%m-%d'),
            "hours" : review.get('author', {}).get('playtime_forever', 0),
            "content" : review['review'],
            "comments" : review.get('comment_count', 0),
            "source" : self.source,
            "helpful" : review.get('votes_up', 0),
            "funny" : review.get('votes_funny', 0),
            "recommended" : review['voted_up'],
            "franchise" : self.franchise,
            "gameName" : self.game_name, 
        }
    
    # Fetching and storing reviews from the stean review API in a loop
    def fetch_reviews(self, params, start_date=None, end_date=None):
        url = f'https://store.steampowered.com/appreviews/{self.app_id}'
        params['num_per_page'] = 100
        cursor = '*'
        total_reviews = 0
        start_timestamp = datetime.strptime(start_date, '%y-%m-%d').timestamp() if start_date else None
        end_timestamp = datetime.strptime(end_date, '%y-%m-%d').timestamp() if end_date else None
        while total_reviews < 5000:
            params['cursor'] = cursor
            response = requests.get(url, params = params)
            data = response.json()
            reviews = data.get('reviews', [])
            if not reviews:
                break
            for review in reviews:
                review_timestamp = review['timestamp_created']
                if (start_timestamp and review_timestamp < start_timestamp) or (end_timestamp and review_timestamp > end_timestamp):
                    continue
                formatted_reviews = [self.format_review(review) for review in reviews]
                self.reviews.extend(formatted_reviews)
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
    crawler = SteamReviewCrawler("Persona", "Persona 5 Strikers", "steam", "1382330")
    params = {
        'json' : 1,
        'filter' : 'recent',
    }
    crawler.fetch_reviews(params)
    crawler.save_reviews_to_file('reviews.json')

    # Testing for the correct number of reviews saved to the reviews.json file 
    # Does not exceed 5000
    # reviews_data = open('reviews.json')
    # review_count_data = json.load(reviews_data)
    # print(len(review_count_data))