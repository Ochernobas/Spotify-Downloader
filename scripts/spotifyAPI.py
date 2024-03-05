from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json


class Spotify:
    def __init__(self):
        load_dotenv()

        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.texto = ""


    #Pega o token para uso da API do Spotify
    #Código original de Tech with Tim
    #Link original - https://www.youtube.com/watch?v=WAmEZBEeNmg
    def getToken(self):
        auth_string = self.client_id + ":" + self.client_secret
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}

        result = post(url, headers=headers, data=data)
        json_result = json.loads(result.content)
        token = json_result["access_token"]

        return token

    def get_auth_header(self, token):
        return {"Authorization": "Bearer " + token}


    #Procura por uma playlist em específico
    def search_for_playlist(self, token, playlist_id):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        headers = self.get_auth_header(token)

        result = get(url, headers=headers)
        json_result = json.loads(result.content)

        return json_result


    #Procura por uma música em específico
    def search_for_music(self, link):
        id = link.split("track/")[1].split("?")[0]
        url = f"https://api.spotify.com/v1/tracks/{id}"

        token = self.getToken()
        headers = self.get_auth_header(token)

        result = get(url, headers=headers)
        json_result = json.loads(result.content)
        return json_result


    #Função principal da classe
    def iniciando(self, playlist, pl):
        pl_id = playlist
        token = self.getToken()
        if pl:
            result = self.search_for_playlist(token, pl_id)
        else:
            result = self.search_for_music(pl_id)

        return result