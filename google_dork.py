import os
import time
import requests
from googleapiclient.discovery import build

import config

class GoogleDork:
    def __init__(self, keyword):
        self.keyword = keyword
        self.num_keys = 4
        self.api_keys = [getattr(config, f"GOOGLE_API_KEY_{i}") for i in range(1, self.num_keys + 1)]
        self.cse_ids = [getattr(config, f"CSE_ID_{i}") for i in range(1, self.num_keys + 1)]
        self.current_key_index = 0
        self.consecutive_429_count = 0 

        self.API_SEARCH_URL = 'https://www.googleapis.com/customsearch/v1'
        self.GOOGLE_URL = "https://www.google.com/search?q=site%3A"

    def rotate_api_key_and_cse(self):
        print(f'Rotating key from keys {self.current_key_index+1} to {self.current_key_index + 2}')
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)

    def query_url(self, query):
        apikey = self.api_keys[self.current_key_index]
        cse_id = self.cse_ids[self.current_key_index]

        params = {
            'q': query,
            'key': apikey,
            'cx': cse_id
        }

        response = requests.get(self.API_SEARCH_URL, params=params)

        if response.status_code == 429:
            self.consecutive_429_count += 1 
            if self.consecutive_429_count >= 100:
                print("Reached 100 consecutive 429 errors. Exiting the application.")
                exit()
            self.rotate_api_key_and_cse()
            return self.query_url(query)
        elif response.status_code != 200:
            print(response)
            return None
        else:
            self.consecutive_429_count = 0  # Reset consecutive 429 error count
            return response.json()

    def generate_raw_links(self):
        active_links = []
        no_hit_links = []

        try:
            with open(f"google_keywords.txt", "r") as keywords_file:
                for line in keywords_file:
                    if line.strip():
                        query = f"site:{self.keyword} {line}"

                        result = self.query_url(query)

                        search_line = line.strip().replace(" ", "+")
                        google_search_url = f"{self.GOOGLE_URL}{self.keyword}+{search_line}"

                        if int(result['searchInformation']['totalResults']) > 0:
                            print(f'Hit found! {google_search_url}')
                            active_links.append(google_search_url)
                        else:
                            no_hit_links.append(google_search_url)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.save_links(active_links, no_hit_links)

    def save_links(self, active_links, no_hit_links):
        active_link_file = f"google_dork_links_{self.keyword}_active.txt"
        no_hit_link_file = f"google_dork_links_{self.keyword}_no_hit.txt"

        with open(active_link_file, "w") as active_file:
            for link in active_links:
                active_file.write(link + "\n")

        with open(no_hit_link_file, "w") as no_hit_file:
            for link in no_hit_links:
                no_hit_file.write(link + "\n")
