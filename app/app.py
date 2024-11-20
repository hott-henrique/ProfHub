import streamlit as st
import time

from datetime import date
from streamlit_option_menu import option_menu
from model.Register import Register
from model.Login import Login
from sdk.AuthAPI import AuthAPI
from streamlit_lottie import st_lottie
from sdk.UserAPI import UserAPI

@st.dialog("Entrar")
def login():
    if 'user' not in st.session_state: st.session_state['user'] = None

    email    = st.text_input(label="E-mail")
    password = st.text_input(label="Senha", type="password")

    login_button = st.button("Entrar", use_container_width=True)

    data = {
        'email' : email,
        'password' : password
    }

    if login_button:
        try:
            user_data = AuthAPI.login(Login(**data))
            st.session_state['user'] = user_data
            st.switch_page("pages/home.py")
        except Exception as e:
            st.error(f"Erro de login: {e}")

@st.dialog("Cadastrar")
def cadastro():
    name          = st.text_input(label = "Nome")
    birthdate     = st.date_input(label = "Data de nascimento", format='DD/MM/YYYY', min_value=date(1900, 1, 1))
    email         = st.text_input(label= "E-mail")
    phone         = st.text_input(label= "Telefone", )
    github        = st.text_input(label= "Github")
    password      = st.text_input(label = "Senha", type = "password")
    confirm       = st.text_input(label = "Confirme a senha", type = "password")

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
        if password == confirm:
            try:
                AuthAPI.register(Register(**data))
                st.success("Usuário cadastrado com sucesso!")
                time.sleep(2)
                st.rerun()
            except Exception as e:
                st.error(f"Erro de cadastro: {e}")
        else:
            st.error("As senhas divergem, verifique.")

@st.dialog("Busca")
def search(prompt):
    response = UserAPI.search_by_text(prompt)
    num = len(response)
    container_list = []

    for exp in range(num):
        container_list.append(st.container(border=True, key="container" + str(exp)))
    
    for index, container in enumerate(container_list):
        with container:
            c1, c2, c3 = st.columns(3, vertical_alignment="center")
            
            c1.write(f"{response[index]['name']}")
            b = c3.button("Visualizar", key="button" + str(index))

            if b:
                st.session_state['view_user'] = response[index]
                st.switch_page("pages/preview.py")

def main():
    st.set_page_config(page_title='ProfHub', page_icon=':material/person:')
    st.sidebar.image("app/images/profhub-logo.png")

    with st.sidebar:
        selected = option_menu(
            menu_title=None,
            options=["Início", "Login", "Cadastro"],
            icons=["house", "door-open", "building"],
            default_index=0,
            orientation="horizontal",
        )

        if selected == "Início":
            prompt = st.chat_input(placeholder="Faça sua busca")
            if prompt: search(prompt)
        if selected == "Login":
            login()
        elif selected == "Cadastro":
            cadastro()

    st.title("_:red[Prof]Hub_, sua vitrine profissional ", anchor=False)

    col1, col2, col3 = st.tabs(['O ProfHub', 'O Profissional', 'A empresa'])

    with col1:
        st.subheader("O ProfHub conecta profissionais e empresas.")
        c1, c2 = st.columns(spec=2)

        with c1:
            st.markdown("""
                <div style="text-align: justify;">
                    <br>O <span style="color: red;">Prof</span><span style="color: black;">Hub</span>
                    nasceu com a ideia de destacar de simplificar a conexão entre profissionais de
                    tecnologia e empresas contratantes, oferecendo ferramentas para o profissional
                    se destacar e opções para que as empresas encontrem os melhores profissionais.
                </div>
            """, unsafe_allow_html=True)

        with c2:
            st_lottie("https://lottie.host/8220a679-4cae-4d7a-88d4-d55c7a84ecda/WJ56RWIOqP.json",
                      key="ProfHub",
                      quality='high',
                      speed=0.1,
                      height=220)

    with col2:
        st.subheader("Construa seu currículo e destaque-se para o mercado.")
        c1, c2 = st.columns(spec=2)

        with c1:
            st.markdown("""
                <div style="text-align: justify;">
                    <br>O profissional conta com as melhores ferramentas para destacar seu currículo,
                    no <span style="color: red;">Prof</span><span style="color: black;">Hub</span>
                    ele pode apresentar suas experiências, cursos, certificações,
                    idiomas e formação acadêmica. Suas competências cadastradas serão
                    apresentadas em filtos, para aqueles que quiserem encontrar um profissional com
                    determinado perfil.
                </div>
            """, unsafe_allow_html=True)

        with c2:
            st_lottie("https://lottie.host/809d4498-47e6-41ba-8af3-5fb59ff21ab7/3rqDNPsG5k.json",
                      key="Profissional",
                      quality='high',
                      speed=0.1,
                      height=250)
    with col3:
        st.subheader("Encontre os melhores profissionais para sua empresa.")
        c1, c2 = st.columns(spec=2)

        with c1:
            st.markdown("""
                <div style="text-align: justify;">
                As empresas podem buscar os melhores profissionais de acordo com os requisitos do seu
                negócio, é possível quaisquer características na ferramenta de busca geral.
                Além de visualizar os currículos dos profissionais buscados o
                <span style="color: red;">Prof</span><span style="color: black;">Hub</span> também
                oferece um relatório personalizado dos profissionais que possuem mais certificações por
                formação acadêmica.
                </div>
            """, unsafe_allow_html=True)

        with c2:
            st_lottie("https://lottie.host/475b7a1c-b0ce-4b70-a721-1210e7dca8e7/elMtyxh915.json",
                      key="Empresa",
                      quality='high',
                      speed=0.1,
                      height=220)

if __name__ == "__main__":
    main()
