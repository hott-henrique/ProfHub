import requests, os
import streamlit as st

from model import Register
from streamlit_option_menu import option_menu
from datetime import date
from api.endpoint import auth

@st.dialog("Entrar")        
def login():
    email = st.text_input(label="E-mail")
    password = st.text_input(label="Senha", type="password")
    
    login_button = st.button("Entrar", use_container_width=True)
            
    if login_button:
        print("login")

@st.dialog("Cadastrar")
def cadastro():
    name          = st.text_input(label = "Nome")
    birthdate     = st.date_input(label = "Data de nascimento", format='DD/MM/YYYY', min_value=date(1900, 1, 1))
    email         = st.text_input(label= "E-mail")
    phone         = st.text_input(label= "Telefone", )
    github        = st.text_input(label= "Github")
    password      = st.text_input(label = "Senha", type = "password")
        
    data = {
        "email": email,
        "password": password,
        "name": name,
        "phone": phone,
        "github": github,
        "birthdate": birthdate
    }   
    
    submit = st.button("Cadastrar", use_container_width=True)
    
    if submit:
        try:
            new_user = Register.Register(**data)
            auth.register(new_user)
            st.success("Usuário cadastrado com sucesso!")
        except Exception as e:
            st.error(f"Erro de cadastro: {e}")

def main():
    st.set_page_config(page_title='ProfHub', page_icon=':material/person:')
    st.sidebar.image("app/images/profhub-logo7.png")

    with st.sidebar:
        selected = option_menu(
            menu_title=None,
            options=["Início", "Login", "Cadastro"],
            icons=["house", "door-open", "building"],
            default_index=0,
            orientation="horizontal",
        )
        

    if selected == "Login":
        login()
    elif selected == "Cadastro":
        cadastro()

    response: requests.Response = requests.get(os.environ["API_URL"] + "/ping")

    message: str = f"API Server response: {response.json()}." if response.ok else "API Server is offline."

    st.markdown(message)
if __name__ == "__main__":
    main()
