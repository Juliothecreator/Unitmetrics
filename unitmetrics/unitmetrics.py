import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# --- CONFIGURAÇÃO ---
CLIENT_ID = 'SEU_ID_AQUI'
CLIENT_SECRET = 'SEU_SECRET_AQUI'

auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# 1. Busca Interativa (Onde o programa pergunta o nome)
nome_do_artista = input("Digite o nome do artista para analisar no Unitmetrics: ")

# AQUI ESTÁ O SEGREDO: Fazemos a busca e salvamos em 'busca'
busca = sp.search(q=nome_do_artista, type='artist', limit=1)

# E aqui definimos o 'items' que o seu código estava sentindo falta
items = busca['artists']['items']

if items:
    artista = items[0] 
    print(f"\n--- UNITMETRICS: FICHA TÉCNICA DE {artista['name'].upper()} ---")
    
    # 2. Busca os Álbuns
    albuns = sp.artist_albums(artista['id'], album_type='album', limit=2)
    
    for album in albuns['items']:
        print(f"\nDisco: {album['name']}")
        
        # 3. Busca as faixas e participantes
        tracks = sp.album_tracks(album['id'], limit=5)
        for track in tracks['items']:
            participantes = [a['name'] for a in track['artists']]
            print(f"  - Faixa: {track['name']}")
            print(f"    Créditos: {', '.join(participantes)}")
else:
    print("Artista não encontrado.")
