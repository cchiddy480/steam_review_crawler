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