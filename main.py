import requests
import json
import uuid
from datetime import datetime 

class SteamReviewCrawler:
    def __init__(self, franchsie, game_name, source, app_id):
        