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
        