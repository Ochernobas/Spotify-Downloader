from youtube_search import YoutubeSearch

class Youtube:
    def __init__(self):
        pass


    def getURL(self, q):
        result = YoutubeSearch(f"{q} official audio", max_results=1).to_dict()
        url = f"www.youtube.com{result[0]["url_suffix"]}"
        return url