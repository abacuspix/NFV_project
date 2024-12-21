import urllib.request
import urllib.parse
import json
import os

TOKEN = os.getenv("BITLY_API_TOKEN", "cc922578a7a1c6065a2aa91bc62b02e41a99afdb")
ROOT_URL = "https://api-ssl.bitly.com"
SHORTEN = "/v3/shorten?access_token={}&longUrl={}"


class BitlyHelper:

    def shorten_url(self, longurl):
        try:
            # Encode the long URL to ensure it is properly formatted
            encoded_url = urllib.parse.quote(longurl, safe="")
            url = ROOT_URL + SHORTEN.format(TOKEN, encoded_url)

            # Make the API request
            with urllib.request.urlopen(url) as response:
                data = response.read().decode('utf-8')
                jr = json.loads(data)

            # Check if the response contains the expected data
            if jr.get('status_code') == 200:
                return jr['data']['url']
            else:
                print(f"Error shortening URL: {jr.get('status_txt')}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
