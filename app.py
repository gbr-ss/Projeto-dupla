import streamlit as st
import random
import requests

st.set_page_config(
    page_title="Descubra o Pokemon",
    page_icon="❓️"
)

def pega_lista_de_pokemons():
    url = "https://pokeapi.co/api/v2/generation/1"
    try:
        resposta = requests.get(url, timeout=5)
        resposta.raise_for_status()
        dados = resposta.json()
        return [p['name'] for p in dados['pokemon_species']]
    except:
        st.error("Vish, deu ruim pra pegar a lista de Pokémons!")
        return []

def pega_foto_do_pokemon(nome):
    try:
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{nome.lower()}", timeout=5)
        r.raise_for_status()
        return r.json()['sprites']['front_default']
    except:
        return None

st.markdown("""
<style>
.emoji-box {display:inline-flex;justify-content:center;align-items:center;width:2.5em;height:2.5em;font-weight:bold;font-size:1.2em;color:white;margin:2px;border-radius:5px;}
.green {background:#6aaa64;}
.yellow {background:#c9b458;}
.gray {background:#787c7e;}
</style>
""", unsafe_allow_html=True)

if 'lista_de_pokemons' not in st.session_state:
    st.session_state.lista_de_pokemons = pega_lista_de_pokemons()

if 'pokemon_secreto' not in st.session_state:
    st.session_state.pokemon_secreto = random.choice(st.session_state.lista_de_pokemons) if st.session_state.lista_de_pokemons else None

if 'historico_de_chutes' not in st.session_state:
    st.session_state.historico_de_chutes = []
    
st.title("Qual é o Pokémon? (1ª geração)")

chute_do_player = st.selectbox(
    "Escolha um pokemon para tentar acertar:",
    st.session_state.lista_de_pokemons,
    index=None
)

if chute_do_player:
    reacao = []
    letras_do_alvo = list(st.session_state.pokemon_secreto)
    letras_do_chute = list(chute_do_player)

    for i in range(len(letras_do_chute)):
        if i < len(letras_do_alvo) and letras_do_chute[i] == letras_do_alvo[i]:
            reacao.append(("green", letras_do_chute[i].upper()))
            letras_do_alvo[i] = None
        else:
            reacao.append((None, letras_do_chute[i].upper()))

    for i, (cor, letra) in enumerate(reacao):
        if cor is None:
            if letra.lower() in letras_do_alvo:
                reacao[i] = ("yellow", letra)
                letras_do_alvo[letras_do_alvo.index(letra.lower())] = None
            else:
                reacao[i] = ("gray", letra)

    st.session_state.historico_de_chutes.append((chute_do_player, reacao, pega_foto_do_pokemon(chute_do_player)))

    if chute_do_player == st.session_state.pokemon_secreto:
        st.success(f"Aee! Na mosca, era **{st.session_state.pokemon_secreto.upper()}**")
        foto_final = pega_foto_do_pokemon(st.session_state.pokemon_secreto)
        st.balloons()
        if foto_final:
            st.image(foto_final, width=150)
        if st.button("Jogar de novo"):
            st.session_state.pokemon_secreto = random.choice(st.session_state.lista_de_pokemons)
            st.session_state.historico_de_chutes = []
    else:
        st.info("Quase! Tente de novo.")

for chute_historico, reacao_historico, foto_historico in st.session_state.historico_de_chutes:
    cols = st.columns([0.8, 0.2])
    with cols[0]:
        html = "".join([f"<div class='emoji-box {cor}'>{letra}</div>" for cor, letra in reacao_historico])
        st.markdown(html, unsafe_allow_html=True)
    with cols[1]:
        if foto_historico:
            st.image(foto_historico, width=50)
    st.markdown("---")
