import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

# 1. Configuração da Página
st.set_page_config(page_title="Unitmetrics", page_icon="📊")

# --- CONEXÃO SEGURA COM SECRETS ---
try:
    CLIENT_ID = st.secrets["CLIENT_ID"]
    CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
except:
    st.error("🚨 Configure as chaves nos Secrets do Streamlit!")
    st.stop()

@st.cache_resource
def iniciar_spot(cid, csec):
    auth_manager = SpotifyClientCredentials(client_id=cid, client_secret=csec)
    return spotipy.Spotify(auth_manager=auth_manager)

sp = iniciar_spot(CLIENT_ID, CLIENT_SECRET)

# --- CABEÇALHO ---
col_logo, col_titulo = st.columns([0.2, 0.8])
with col_logo:
    # Busca a logo na pasta do GitHub (tenta várias extensões)
    for f in ["logo.jpg", "logo.png", "logo.jpeg", "logo"]:
        if os.path.exists(f):
            st.image(f, width=80)
            st.markdown("<style>[data-testid='stImage'] img {mix-blend-mode: screen;}</style>", unsafe_allow_html=True)
            break
with col_titulo:
    st.markdown("<h1 style='margin-top: -10px;'>Unitmetrics</h1>", unsafe_allow_html=True)

# --- BUSCA ---
nome = st.text_input("Buscar Artista:", value="Orochi")

if nome:
    try:
        busca = sp.search(q=nome, type='artist', limit=1)
        items = busca['artists']['items']
        
        if items:
            # AQUI ESTÁ A CORREÇÃO: Pegamos o primeiro item da lista
            artista = items[0] 
            
            c1, c2 = st.columns([0.3, 0.7])
            with c1:
                # Verifica se o artista tem imagem e pega a URL da primeira
                if artista.get('images'):
                    st.image(artista['images'][0]['url'], width=150)
            with c2:
                st.header(artista['name'])
                generos = artista.get('genres', [])
                if generos:
                    st.caption(f"Gêneros: {', '.join(generos)}")
            
            st.divider()
            
            # --- ÁLBUNS E CRÉDITOS ---
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
        else:
            st.warning("Artista não encontrado.")
    except Exception as e:
        st.error(f"Erro na busca: {e}")
