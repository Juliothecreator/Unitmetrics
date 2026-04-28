import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

st.set_page_config(page_title="Unitmetrics", page_icon="📊")

# --- CONEXÃO SEGURA COM TRATAMENTO DE ERRO ---
try:
    # O código tenta pegar as chaves do "cofre" do Streamlit
    CLIENT_ID = st.secrets["CLIENT_ID"]
    CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
except Exception:
    st.error("🚨 ERRO: Chaves não encontradas nos Secrets do Streamlit!")
    st.info("Vá em Settings > Secrets e cole as chaves no formato CLIENT_ID = '...' ")
    st.stop()

@st.cache_resource
def iniciar_spot(cid, csec):
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cid, client_secret=csec))

sp = iniciar_spot(CLIENT_ID, CLIENT_SECRET)

# --- CABEÇALHO ---
col_logo, col_titulo = st.columns([0.2, 0.8])
with col_logo:
    # Tenta achar a logo na pasta do GitHub
    for f in ["logo.jpg", "logo.png", "logo"]:
        if os.path.exists(f):
            st.image(f, width=80)
            st.markdown("<style>[data-testid='stImage'] img {mix-blend-mode: screen;}</style>", unsafe_allow_html=True)
            break
with col_titulo:
    st.title("Unitmetrics")

# --- BUSCA ---
nome = st.text_input("Buscar Artista:", value="Orochi")

if nome:
    try:
        busca = sp.search(q=nome, type='artist', limit=1)
        items = busca['artists']['items']
        if items:
            artista = items
            c1, c2 = st.columns([0.3, 0.7])
            with c1:
                if artista.get('images'):
                    st.image(artista['images']['url'], width=150)
            with c2:
                st.header(artista['name'])
                st.caption(f"Gêneros: {', '.join(artista.get('genres', []))}")
            
            st.divider()
            
            albuns = sp.artist_albums(artista['id'], album_type='album', limit=5)
            for alb in albuns['items']:
                ano = alb['release_date'][:4]
                with st.expander(f"💿 {alb['name']} ({ano})"):
                    tracks = sp.album_tracks(alb['id'])
                    for t in tracks['items']:
                        part = ", ".join([a['name'] for a in t['artists']])
                        st.write(f"**{t['name']}**")
                        st.caption(f"Créditos: {part}")
                        st.divider()
    except Exception as e:
        st.error(f"Erro na busca: {e}")
