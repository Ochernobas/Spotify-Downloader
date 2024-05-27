from spotifyAPI import Spotify
from ytSearcher import Youtube
from ytDownloader import Download
from tagger import TagEditor
from PIL import Image
import requests
import subprocess
import os
import customtkinter

class Core:
    def __init__(self):
        self.spotify = Spotify()
        self.youtube = Youtube()
        self.downloader = Download()
        self.tagEditor = TagEditor()
        self.playlist = None

        #COLOQUE AQUI A PASTA ONDE DEVERÃO SER COLOCADAS AS MÚSICAS
        self.path = "C:\\Users\\pacot\\PycharmProjects\\SpotipyFinal\\files\\music"

        #COLOQUE AQUI QUALQUER PASTA PARA QUE SEJAM BAIXADAS AS IMAGENS DAS MÚSICAS
        self.img_path = "C:\\Users\\pacot\\PycharmProjects\\SpotipyFinal\\files\\images"

        self.mus = None
        self.musica = None
        self.img = None
        self.name = None
        self.artist = ""
        self.album = ""
        self.tags = {"title": None,
                "artist": None,
                "artwork": None,
                "album": None}


    #Gera a query que será pesquisada no Youtube
    def geraQuery(self, track):
        query = f"{track["track"]["name"]} {track["track"]["artists"][0]["name"]}"
        return query


    #Converte o arquivo mp4 em mp3 usando o FFMPEG
    def convert_video_to_audio(self, path, nome):
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", f"{self.path}\\{path}",
            "-vn",
            "-acodec", "libmp3lame",
            "-ab", "192k",
            "-ar", "44100",
            "-y",
            f"{self.path}\\{nome}.mp3"
        ]

        try:
            subprocess.run(ffmpeg_cmd, check=True)
            print("ARQUIVO CONVERTIDO")
        except subprocess.CalledProcessError as e:
            print("ERRO NA CONVERSÃO")


    #Pega o json com a música lá do SpotifyAPI.py
    def listaMusica(self, link):
        ms = self.spotify.iniciando(link, False)

        return ms


    #Igual a função acima, só que pra playlists
    def listadeMusicas(self, link):
        self.playlist = link
        pl_id = self.playlist.split("playlist/")[1].split("?")[0]
        pl = self.spotify.iniciando(pl_id, True)

        return pl #JSON da Playlist


    #Baixa todas as músicas da playlist
    def baixaPL(self, playlist):
        for track in playlist: #Para cada música da playlist

            #Define variáveis para as tags
            self.name = track["nome"]
            self.img = track["imagemURL"]
            self.album = track["album"]
            self.artist = track["artista"]

            #Pega a url da música no youtube
            url = self.youtube.getURL(f"{self.name} {self.artist}")
            print(url)

            #Baixa a música em mp3
            arquivo = self.downloader.downloadVideo(url, self.path, self.name)
            novo_arquivo = arquivo.split('music\\')[1]

            #Pega a imagem de cover do álbum
            response = requests.get(self.img)
            filename = f"{self.name}.mp3"
            new_filename = filename.replace("?", "")
            with open(f"{self.img_path}\\{new_filename}.jpg", "wb") as f:
                f.write(response.content)

            #Converte o mp4 para mp3
            self.convert_video_to_audio(novo_arquivo, self.name)

            #Edita as tags
            self.tags["title"] = self.name
            self.tags["artist"] = self.artist
            self.tags["artwork"] = f"{self.img_path}\\{new_filename}.jpg"
            self.tags["album"] = self.album
            self.tagEditor.editarTags(f"{self.path}\\{self.name}.mp3", self.tags)

            #Apaga os arquivos temporários (Imagens e mp4)
            os.remove(arquivo)
            os.remove(f"{self.img_path}\\{new_filename}.jpg")


    #Baixa a música selecionada
    def baixaMusica(self, musica):
        self.mus = musica

        #Pega a URL da música no youtube
        url = self.youtube.getURL(f"{self.mus["nome"]} {self.mus["artista"]}")

        #Baixa a música em mp4
        arquivo = self.downloader.downloadVideo(url, self.path, self.mus["nome"])
        novo_arquivo = arquivo.split('music\\')[1]

        #Pega a imagem de cover do album
        response = requests.get(self.mus["imagemURL"])
        filename = f"{self.mus["nome"]}.mp3"
        new_filename = filename.replace("?", "")
        with open(f"{self.img_path}\\{new_filename}.jpg", "wb") as f:
            f.write(response.content)

        #Converte o mp4 para mp3
        self.convert_video_to_audio(novo_arquivo, self.mus["nome"])

        #Edita as tags da música
        self.tags["title"] = self.mus["nome"]
        self.tags["artist"] = self.mus["artista"]
        self.tags["artwork"] = f"{self.img_path}\\{new_filename}.jpg"
        self.tags["album"] = self.mus["album"]
        self.tagEditor.editarTags(f"{self.path}\\{self.mus["nome"]}.mp3", self.tags)

        # Apaga os arquivos temporários (Imagens e mp4)
        os.remove(arquivo)
        os.remove(f"{self.img_path}\\{new_filename}.jpg")


#Interface do frame onde aparecem as músicas
class Frame1(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.core = Core()
        self.musicas = []
        self.image = customtkinter.CTkImage(Image.open(r"C:\Users\pacot\PycharmProjects\SpotipyFinal\src\img\delete_FILL0_wght400_GRAD0_opsz24.png"))
        self.image1 = customtkinter.CTkImage(Image.open(r"C:\Users\pacot\PycharmProjects\SpotipyFinal\src\img\download_FILL0_wght400_GRAD0_opsz24.png"))
        self.image2 = customtkinter.CTkImage(Image.open(r"C:\Users\pacot\PycharmProjects\SpotipyFinal\src\img\edit_24dp_FILL0_wght400_GRAD0_opsz24.png"))
        self.top_levelwindow = None


    #Pega os dados de uma música só
    def pegaMusica(self, link):
        track = self.core.listaMusica(link)
        musica = {
            "nome": None,
            "artista": [],
            "album": None,
            "imagemURL": None
        }

        self.inputNome = []
        self.inputArtista = []
        self.inputAlbum = []
        self.buttons1 = []
        self.buttons2 = []

        musica["nome"] = track["name"]
        musica["album"] = track["album"]["name"]
        musica["imagemURL"] = track["album"]["images"][0]["url"]

        for artist in track["artists"]:
            musica["artista"].append(artist["name"])

        self.musicas.append(musica)

        musica = {
            "nome": None,
            "artista": [],
            "album": None,
            "imagemURL": None
        }

        self.mostraMusicas()


    #Pega os dados de todas as músicas de uma playlist
    def pegaMusicas(self, link):
        json = self.core.listadeMusicas(link)["tracks"]["items"]
        musica = {
            "nome": None,
            "artista": [],
            "album": None,
            "imagemURL": None
        }

        self.inputNome = []
        self.inputArtista = []
        self.inputAlbum = []
        self.buttons1 = []
        self.buttons2 = []
        self.buttons3 = []

        for track in json:
            musica["nome"] = track["track"]["name"]
            musica["album"] = track["track"]["album"]["name"]
            musica["imagemURL"] = track["track"]["album"]["images"][0]["url"]

            for artist in track["track"]["artists"]:
                musica["artista"].append(artist["name"])

            self.musicas.append(musica)

            musica = {
                "nome": None,
                "artista": [],
                "album": None,
                "imagemURL": None
            }

        self.mostraMusicas()


    #Desenha a Tela
    def mostraMusicas(self):
        self.downloadALL = customtkinter.CTkButton(self, text="Baixar Todos", width=60, height=40, corner_radius=20,
                                                   fg_color="#908080", hover_color="#423939", command=self.baixaTodos)
        self.downloadALL.grid(row=0, padx=20, pady=10, sticky="nsew")

        for i, musica in enumerate(self.musicas):
            self.musica = customtkinter.CTkEntry(self, placeholder_text="", fg_color="transparent", border_color="#000000", placeholder_text_color="#000000",
                                                 width=150)
            self.artista = customtkinter.CTkEntry(self, placeholder_text="", fg_color="transparent", border_color="#000000", placeholder_text_color="#000000",
                                                  width=240)
            self.album = customtkinter.CTkEntry(self, placeholder_text="", fg_color="transparent", border_color="#000000", placeholder_text_color="#000000",
                                                width=200)

            self.grid_rowconfigure(i, weight=1, pad=20)
            self.grid_columnconfigure(i, weight=0)

            self.musica.insert(0,musica["nome"])
            self.artista.insert(0, musica["artista"])
            self.album.insert(0, musica["album"])

            self.inputNome.append(self.musica)
            self.inputArtista.append(self.artista)
            self.inputAlbum.append(self.album)

            self.musica.grid(row=i+1, column=0, padx=20, pady=10, sticky="nsew")
            self.artista.grid(row=i+1, column=1, padx=20, pady=10, sticky="nsew")
            self.album.grid(row=i+1, column=2, padx=20, pady=10, sticky="nsew")

            self.buttons1.append(customtkinter.CTkButton(self, image=self.image1, text="", width=15, height=15,
                                                  fg_color="transparent", hover_color="#9B9A9A", command=lambda text=i:self.baixaMusica(text)))
            self.buttons1[i].grid(row=i+1, column=3, padx=5, pady=10, sticky="nsew")

            self.buttons2.append(customtkinter.CTkButton(self, image=self.image, text="", fg_color="transparent", width=15,
                                                   height=15, hover_color="#9B9A9A", command=lambda text=i:self.apagaMusica(text)))
            self.buttons2[i].grid(row=i+1, column=4, padx=5, pady=10, sticky="nsew")

            self.buttons3.append(customtkinter.CTkButton(self, image=self.image2, text="", fg_color="transparent", width=15,
                                                         height=15, hover_color="#9B9A9A", command=lambda text=i: self.openTopLevel(text)))
            self.buttons3[i].grid(row=i + 1, column=5, padx=5, pady=10, sticky="nsew")

            self.musica = None
            self.artista = None
            self.album = None


    def openTopLevel(self):
        if self.top_levelwindow is None or not self.top_levelwindow.winfo_exists():
            self.top_levelwindow = TopLevel(self)  # create window if its None or destroyed
        else:
            self.top_levelwindow.focus()


    #Apaga uma música da tela e dos arrays (Lixeira)
    def apagaMusica(self, i):
        self.pegaValores()
        self.musicas.pop(i)
        self.buttons1 = []
        self.buttons2 = []
        self.inputNome = []
        self.inputAlbum = []
        self.inputArtista = []

        for widget in self.winfo_children():
            widget.destroy()

        self.mostraMusicas()


    #Baixa individualmente uma música
    def baixaMusica(self, i):
        self.pegaValores(i)
        self.core.baixaMusica(self.musicas[i])


    #Baixa todas as músicas ao mesmo tempo
    def baixaTodos(self):
        self.pegaValores()
        self.core.baixaPL(self.musicas)


    #Pega a música referente a cada botão individual de download, para ser possível baixar elas individualmente
    #Os kwargs aqui podem ser sómente um inteiro, o index do botão referente a música que deve ser baixada
    def pegaValores(self, *args):
        print(args)
        if len(args) > 0:
            self.musicas[args[0]]["nome"] = self.inputNome[args[0]].get()
            self.musicas[args[0]]["artista"] = self.inputArtista[args[0]].get().replace("{", "").replace("}", "")
            self.musicas[args[0]]["album"] = self.inputAlbum[args[0]].get()
            print(self.musicas[args[0]])
        else:
            for i, musica in enumerate(self.musicas):
                self.musicas[i]["nome"] = self.inputNome[i].get()
                self.musicas[i]["artista"] = self.inputArtista[i].get()
                self.musicas[i]["album"] = self.inputAlbum[i].get()
                print(self.musicas[i])


class TopLevel(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="ToplevelWindow")
        self.label.pack(padx=20, pady=20)

#Frame superior da tela, onde pode ser digitado o link
class Frame0(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.core = Core()
        self.texto = ""
        self.master = master

        self.link = customtkinter.CTkEntry(self, placeholder_text="Coloque o Link", width=650, border_color="#000000", placeholder_text_color="#000000")
        self.link.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        self.linkButton = customtkinter.CTkButton(self, text="Procurar", width=60, height=40, corner_radius=20, fg_color="#908080", hover_color="#423939", command=self.confereLink)
        self.linkButton.grid(row=0, column=1, padx=20, pady=20, sticky="e")


    #Confere se o link entregue é de uma playlist ou música do spotify
    def confereLink(self):
        self.texto = self.link.get()

        if self.texto.split(".com")[0] == "https://open.spotify":
            texto = self.texto.split(".com/")[1].split("/")[0]
            if texto == "playlist":
                self.master.frame1.pegaMusicas(self.texto)
            elif texto == "intl-pt":
                self.master.frame1.pegaMusica(self.texto)
        else: print("URL INVÁLIDA")


#Cria a tela
class Tela(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("910x780")
        self.resizable(width=5.0, height=1.0)
        self.minsize(width=910, height=760)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.frame0 = Frame0(master=self, width=850, height=10)
        self.frame1 = Frame1(master=self, width=850, height=500)

        self.frame0.grid(row=0, column=0, padx=20, pady=20, sticky="n")
        self.frame1.grid(row=1, column=0, padx=20, pady=20, sticky="n")


#Gera a Tela
tela = Tela()
tela.mainloop()