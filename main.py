import cv2  
import numpy as np
import streamlit as st
import random
import imutils

st.set_page_config(page_title="Ponderada Periquito", layout="centered")
st.title("Ultra modificador de Imagens Periquito 1.1")
# Filtros dos botões: Não se aplica ao redimencionamento e rotação.
# Provavelmente porque fiz em dois dias diferentes e fiquei com preguiça de seguir o padrão
def apply_filter(img, tag):
    if tag == "Cinza":
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif tag == "Inversão":
        return cv2.bitwise_not(img)
    elif tag == "Contraste":
        return cv2.convertScaleAbs(img, alpha=1.5, beta=0)
    elif tag == "Blur":
        return cv2.blur(img, (5, 5))
    elif tag == "Sharpen":
        kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
        return cv2.filter2D(img, -1, kernel)
    elif tag == "Bordas":
        return cv2.Canny(img, 100, 200)
    elif tag == "Psycho":
        img = img.copy()
        random_red = random.randrange(1,5)
        random_green = random.randrange(1,5)
        random_blue = random.randrange(1,5)
        img[:, :, 0] = np.clip(img[:, :, 0] * random_blue, 0, 255)
        img[:, :, 1] = np.clip(img[:, :, 1] * random_green, 0, 255)
        img[:, :, 2] = np.clip(img[:, :, 2] * random_red, 0, 255)
        return img.astype(np.uint8)
    elif tag == "Reset":
        print("Reset")
        st.session_state["mod"] = st.session_state["original"].copy()
        st.session_state['Cinza'] = False
        return st.session_state["original"]
       
uploaded_file = st.file_uploader("Upar imagem", type=["png", "jpg", "jpeg", "webp"])
if uploaded_file is not None:
    raw = uploaded_file.read()
    # Transformando a imagem em RGB, quem que em sã consciência usa BGR?
    img_brg = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img_brg, cv2.COLOR_BGR2RGB)
    if st.session_state.get("raw") != raw:
        st.session_state["raw"] = raw      
        st.session_state["original"] = img_rgb  
        st.session_state["mod"] = img_rgb
        st.session_state["Cinza"] = False
    file_bytes = None
    button_cols = st.columns(4, gap="small")
    button_tag = ["Cinza", "Inversão", 'Contraste', 'Blur']
    data = np.frombuffer(uploaded_file.read(), np.uint8)
    for col, tag in zip(button_cols, button_tag):
        with col:
            disable_now = st.session_state['Cinza'] if tag == "Cinza" else False or st.session_state["Cinza"] if tag == "Psycho" else False
            if st.button(tag, use_container_width=True, disabled=disable_now):
                st.session_state["mod"] = apply_filter(st.session_state["mod"], tag)
                if(tag == "Cinza" or tag == "Bordas"):
                    st.session_state['Cinza'] = True
                st.rerun()
    button_tag =  ['Sharpen', "Bordas", "Psycho", "Reset"]
    for col, tag in zip(button_cols, button_tag):
        with col:
            disable_now = st.session_state['Cinza'] if tag == "Cinza" else False or st.session_state["Cinza"] if tag == "Psycho" else False
            if st.button(tag, use_container_width=True, disabled=disable_now):
                st.session_state["mod"] = apply_filter(st.session_state["mod"], tag)
                if(tag == "Cinza" or tag == "Bordas"):
                    st.session_state['Cinza'] = True
                st.rerun()
    # Slider de redimencionamento
    #Ficou meio torto mas front não é fácil
    left, right = st.columns([1,1], gap="small")
    with left:
        st.slider("Ajuste de tamanho", 0,4096, 1024, 1, key="slider")
    with right:
        if st.button("Resize"):
            sizex = st.session_state["slider"]
            sizey = int(sizex/st.session_state["mod"].shape[1] * st.session_state["mod"].shape[0])
            st.session_state["mod"] = cv2.resize(st.session_state["mod"], (sizex, sizey))
            st.rerun()
    # Display das imagens
    # Honestamente eu não sei se seria possível manter as duas imagens nas colunas iguais as de cima, mas preferi separar para garantir
    left, right = st.columns([1, 1])
    with left:
        st.image(img_rgb, use_container_width=True, caption="Imagem Original")
    with right:
        st.image(st.session_state['mod'], use_container_width=True, caption="Imagem Modificada")
    #Sim, tem muitas dessas separações de colunas. Eu também não estou feliz com isso, mas postergar é complicado
    left, right = st.columns([1, 1])
    with left:
        st.number_input("Rotação", 0, 360, 0, 1, key="rotacao")
    with right:
        # Link bem interessante sobre rotações: https://pyimagesearch.com/2021/01/20/opencv-rotate-image/
        if st.button("Rotacionar"):
            st.session_state["mod"] = imutils.rotate_bound(st.session_state["mod"], st.session_state["rotacao"])
            st.rerun()
    # Girar a imagem fora dos múltiplos de 90 graus faz a imagem ser constantemente "reduzida", mesmo que a imagem em sí esteja aumentando.
    # Como o sistema tenta encaixar a imagem, girando 45 graus por exemplo resulta no tamanho da imagem aumentando, chegando no ponto em que o sistema pode se recusar a realizar operações por ter pixels demais.
    st.text("*Não recomendado rotacionar fora de multiplos de 90 graus várias vezes seguidas")
    file_bytes = cv2.cvtColor(st.session_state["mod"], cv2.COLOR_RGB2BGR)
    file_bytes = cv2.imencode(".png", file_bytes)[1].tobytes()
    st.download_button(label="Baixar imagem", data=file_bytes, file_name="imagem_modificada.png", mime="image/png")
else:
    # Você não acreditaria o que tinha aqui durante o desenvolvimento :skull:
    # Emoji n funciona mas o importante é a intenção
    st.info("Por favor, faça o upload de uma imagem para começar.")
    st.text("Desenvolvido pelo Periquito, com amor, carinho, pressa, um toque de procrastinação e muita cafeína")