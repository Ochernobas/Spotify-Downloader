import pytube

class Download:
    def __init__(self):
        pass


    def downloadVideo(self, link, path, name):
        print("BAIXANDO")
        yt = pytube.YouTube(link)
        yt = yt.streams.filter(only_audio=True).first()

        filename = f"{name}.mp3"
        new_filename = filename.replace("?", "")

        arquivo = yt.download(path)
        print("DOWNLOAD CONCLUÍDO")
        print(f"ARQUIVO - {arquivo}")
        return arquivo
