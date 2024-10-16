
import os
import requests
from dotenv import load_dotenv

load_dotenv()
TomTomAPI_KEY = os.environ.get('TomTomAPI_KEY')

def get_location(location: str):
    if location is None:
        raise ValueError('No location provided')
    
    try:
        response = requests.get(f"https://api.tomtom.com/search/2/geocode/{location}.json?key={TomTomAPI_KEY}")
        response = response.json()
        long = response['results'][0]['position']['lat']
        lat = response['results'][0]['position']['lon']
        return long, lat
    except Exception as e:
        print(f"Could not get coordinates for {location} due to error: {e}")
