# Spotify-Downloader
Código para download automático de playlists e músicas do Spotify

As seguintes bibliotecas devem ser instaladas para o funcionamento do código:
- PIL
- requests
- customtkinter
- python-dotenv
- music-tag
- pytube
- youtube_search
- o FFMPEG deve estar instalado no computador

O programa utiliza a API do Spotify para listar cada música da playlist dada pelo usuário, extrai a foto do álbum, o nome dos artistas, o nome das músicas, e os álbuns, e guarda tudo em um array onde cada elemento é um dicionário respectivo de cada música. Depois, usa a biblioteca youtube_search para encontrar o primeiro resultado da busca no youtube com a query "[Música] [Artista] official audio", o que praticamente acerta sempre as músicas.

Então ele baixa cada música através da biblioteca "pytube" em formato mp4, pois ao baixar em mp3 não era possível editar as tags do arquivo. Depois, usa o FFMPEG para converter em mp3, e então, usa a biblioteca "music_tag" para colocar os nomes da música e artista, o álbum, e a foto em suas respectivas tags do arquivo. Todas as mmúsicas são baixadas na pasta selecionada pela variável "self.path" da classe Core, no arquivo "main.py". Também é necessário passar uma pasta onde as imagens poderão ser baixadas, definida na variável "self.img_path" da classe Core, no arquivo "main.py".

Por fim, é necessário configurar a API do Spotify, para isso é necessário usar o site oficial, e basta seguir qualquer tutorial no youtube, então, devem ser alteradas as constants CLIENT_ID e CLIENT_SECRET no arquivo ".env" para os códigos gerados pela API.

Com tudo isso feito, é só executar e baixar as músicas!
