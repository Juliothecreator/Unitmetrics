import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

# 1. Configuração da Página
st.set_page_config(page_title="Unitmetrics", page_icon="📊")

# --- SUAS CHAVES ---
CLIENT_ID = ""
CLIENT_SECRET = ""

@st.cache_resource
def conectar_spotify(cid, csec):
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cid, client_secret=csec))

sp = conectar_spotify(CLIENT_ID, CLIENT_SECRET)

# --- CABEÇALHO COM LOGO ---
col_l, col_t = st.columns([0.15, 0.85])

with col_l:
    arquivos_na_pasta = os.listdir(".")
    logo_encontrada = None
    for f in arquivos_na_pasta:
        if f.lower().startswith("logo"):
            logo_encontrada = f
            break
    
    if logo_encontrada:
        st.image(logo_encontrada, width=80)
        st.markdown("<style>[data-testid='stImage'] img {mix-blend-mode: screen;}</style>", unsafe_allow_html=True)
    else:
        st.write("🔴")

with col_t:
    st.markdown("<h1 style='margin-top: -10px;'>Unitmetrics</h1>", unsafe_allow_html=True)

# --- BUSCA ---
nome_procurado = st.text_input("Buscar Artista:", value="Orochi")

if nome_procurado:
    try:
        resultado = sp.search(q=nome_procurado, type='artist', limit=1)
        artistas_encontrados = resultado['artists']['items']
        
        if artistas_encontrados:
            dados_artista = artistas_encontrados[0]
            
            c1, c2 = st.columns([0.3, 0.7])
            with c1:
                if 'images' in dados_artista and dados_artista['images']:
                    st.image(dados_artista['images'][0]['url'], width=150)
            with c2:
                st.header(dados_artista['name'])
                st.caption(f"Gêneros: {', '.join(dados_artista.get('genres', []))}")

            st.divider()
            
            # --- LISTAGEM DE ÁLBUNS COM ANO E TOTAL DE FAIXAS ---
            albuns = sp.artist_albums(dados_artista['id'], album_type='album', limit=5)
            for alb in albuns['items']:
                ano = alb['release_date'][:4]
                total_faixas = alb['total_tracks']
                
                with st.expander(f"💿 {alb['name']} ({ano}) — {total_faixas} faixas"):
                    mscs = sp.album_tracks(alb['id'])
                    for m in mscs['items']:
                        participantes = ", ".join([a['name'] for a in m['artists']])
                        st.write(f"**{m['name']}**")
                        st.caption(f"Créditos: {participantes}")
                        st.divider()
        else:
            st.warning("Artista não encontrado.")
            
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
