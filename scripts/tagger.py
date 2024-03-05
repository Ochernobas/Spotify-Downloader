import music_tag

class TagEditor:
    def __init__(self):
        pass

    def editarTags(self, arquivo, tags):
        f = music_tag.load_file(arquivo)
        f["title"] = tags["title"]
        f["artist"] = tags["artist"]
        f["album"] = tags["album"]

        with open(tags["artwork"], "rb") as img_in:
            f["artwork"] = img_in.read()
        f.save()
