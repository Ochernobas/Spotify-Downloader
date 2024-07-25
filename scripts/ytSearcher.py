from youtube_search import YoutubeSearch
from youtubesearchpython import VideosSearch

class Youtube:
    def __init__(self):
        pass


    def getURL(self, q):
        result = VideosSearch(f"{q} official audio", limit=1).result()
        url = result["result"][0]["link"]
        return url