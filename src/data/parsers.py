from typing import Optional, Union
from google_images_search import GoogleImagesSearch
from abc import ABC, abstractmethod
import numpy as np
import praw
import requests
import yaml
import cv2 
import hashlib
import os 

class Parser(ABC):  

    yaml_path = None

    @abstractmethod
    def parse(self):
        pass
    
    @abstractmethod
    def __len__(self):
        pass

    @staticmethod
    def _load_yaml(yaml_path):

        with open(yaml_path, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        return config

class SubredditImagesParser(Parser):
    def __init__(self) -> None:

        credentials = self._load_yaml(Parser.yaml_path)["Reddit"]
        self._reddit_instance = praw.Reddit(
            client_id = credentials["client_id"],
            client_secret = credentials["client_secret"],
            user_agent = credentials["user_agent"],
            username = credentials["username"],
            password = credentials["password"],
        )
        self._images_counter = 0

    def parse(self, subreddits_list: Union[set, str], path_to_save: str, valid_formats: Union[set, str], n_posts: Optional[int] = 1e3) -> None:
        self.valid_formats = {valid_formats} if isinstance(valid_formats, str) else valid_formats
        self.subreddits = {subreddits_list} if isinstance(subreddits_list, str) else subreddits_list

        for subreddit in self.subreddits:
            print(f"Parsing {subreddit}")
            subreddit_instance = self._reddit_instance.subreddit(subreddit)
            for submission in subreddit_instance.new(limit = n_posts):
                submission_url = submission.url.lower()
                image_format = submission_url.split(".")[-1]
                if image_format in self.valid_formats:
                    response = requests.get(submission_url)
                    img = np.array(bytearray(response.content), dtype="uint8")
                    decoded_image = cv2.imdecode(img, cv2.IMREAD_COLOR)
                    hash_code = hashlib.md5(decoded_image.tobytes()).hexdigest()
                    cv2.imwrite(os.path.join(path_to_save, f"{hash_code}.png"), decoded_image)
                    self._images_counter += 1

    def __len__(self) -> int:
        return self._images_counter
    
class GoogleImagesParser(Parser):
    def __init__(self) -> None:
        credentials = self._load_yaml(Parser.yaml_path)["Google"]
        self.google_instance = GoogleImagesSearch(credentials["dev_api_key"], 
                                        credentials["project_cx"], validate_images=False)   
        self._images_counter = 0

    def parse(self, query: Union[set, str], path_to_save: str, valid_formats: Union[set, str], n_images: Optional[int] = 10**3) -> None:
        self.valid_formats = {valid_formats} if isinstance(valid_formats, str) else valid_formats
        self.queries = {query} if isinstance(query, str) else query

        _search_params = {
        'q': query,
        'num': n_images,
        'fileType': "|".join(self.valid_formats),
        }

        for query in self.queries:
            _search_params["q"] = query
            self.google_instance.search(search_params=_search_params) 
            for image in self.google_instance.results():
                raw_image = image.get_raw_data()
                img = np.array(bytearray(raw_image), dtype="uint8")
                decoded_image = cv2.imdecode(img, cv2.IMREAD_COLOR)

                if decoded_image is None:
                    continue

                hash_code = hashlib.md5(decoded_image.tobytes()).hexdigest()
                cv2.imwrite(os.path.join(path_to_save, f"{hash_code}.png"), decoded_image)
                self._images_counter += 1     
                
    def __len__(self):
        return self._images_counter
