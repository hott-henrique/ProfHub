import streamlit as st
import time

from datetime import date
from streamlit_option_menu import option_menu
from sdk.UserAPI import UserAPI
from model.User import User
from sdk.AuthAPI import AuthAPI
from model.Login import Login
from model.UpdatePassword import UpdatePassword

def main():
    st.set_page_config(page_title='ProfHub', page_icon=':material/person:')
    st.sidebar.image("app/images/profhub-logo.png")
    user = st.session_state['user'] if 'user' in st.session_state else st.switch_page("app.py")

    with st.sidebar:
        selected = option_menu(
            menu_title=None,
            options=["Visualizar currículo", "Busca avançada", "Sair"],
            icons=["file-earmark-text", "search", "escape"],
            default_index=0,
        )

        if selected == "Busca avançada":
            st.switch_page("pages/busca.py")
        elif selected == "Sair":
            st.session_state['user'] = None
            st.switch_page("app.py")
    
    st.title("olá, " + user['name'], anchor=False)
    
    with st.expander("Informações pessoais"):
        container = st.container(border=True, key='container-infos')
        container.write(f"Nome: {user['name']}")
        container.write(f"E-mail: {user['email']}")
        container.write(f"Github: {user['github']}")
        container.write(f"Telefone: {user['phone']}")
        container.write(f"Aniversário: {user['birthdate'].split('T')[0]}")

        left, middle, right = st.columns(3, vertical_alignment="bottom")

        left.button("Editar perfil", key='editar-perfil', use_container_width=True, on_click=edit_user)
        middle.button("Alterar senha", key='alterar-senha', use_container_width=True, on_click=edit_password)
        right.button("Apagar conta", key='apagar-conta', use_container_width=True, on_click=delete_account)
    with st.expander("Experiências profissionais"):
        st.write("Em breve...")
    
    with st.expander("Formação acadêmica"):
        st.write("Em breve...")
    
    with st.expander("Cursos"):
        st.write("Em breve...")
    
    with st.expander("Certificações"):
        st.write("Em breve...")

    with st.expander("Idiomas"):
        st.write("Em breve...")
    
@st.dialog("Editar informações pessoais")
def edit_user():
    user = st.session_state['user']
    b_data = user['birthdate'].split("T")[0].split("-")
    
    name          = st.text_input(label = "Nome", value=user['name'])
    birthdate     = st.date_input(label = "Data de nascimento", format='DD/MM/YYYY', min_value=date(1900, 1, 1), value=date(int(b_data[0]), int(b_data[1]), int(b_data[2])))
    email         = st.text_input(label= "E-mail", value=user['email'])
    phone         = st.text_input(label= "Telefone", value=user['phone'])
    github        = st.text_input(label= "Github", value=user['github'])
    
    editar = st.button("Atualizar", use_container_width=True, key='salvar-user')    
    
    data = {
        "email": email,
        "name": name,
        "phone": phone,
        "github": github,
        "birthdate": birthdate
    }

    if editar:
        try:
            response = UserAPI.update(user['id'], User(**data))
            st.session_state['user'] = response
            st.success("Informações atualiadas.")
            time.sleep(2)
            st.rerun()
        except Exception as e:
            st.error(f"Erro de atualização: {e}")
        
@st.dialog("Alterar senha")
def edit_password():
    user = st.session_state['user']

    atual      = st.text_input(label = "Senha atual", type = "password")
    nova       = st.text_input(label = "Nova senha", type = "password")
    confirm    = st.text_input(label = "Confirmação de senha", type = "password")

    conf = st.button("Alterar senha", key="confirm-edit-password")

    data = {
        'email' : user['email'],
        'old_password' : atual,
        'new_password' : nova
    }

    if conf:
        if nova == confirm:
            try:
                AuthAPI.update_password(UpdatePassword(**data))
                st.success("Senha alterada.")
                time.sleep(2)
                st.rerun()
            except Exception as e:
                st.error(f"Erro: {e}")
        else:
            st.error("As senhas divergem, confira.")

@st.dialog("Excluir conta")
def delete_account():
    user = st.session_state['user']

    texto      = st.text_input(label = "Digite: 'eu quero excluir minha conta :('")
    password   = st.text_input(label = "Digite sua senha.", type = "password")
    
    conf = st.button("Excluir conta", key="confirm-delete-account")

    data = {
        'email' : user['email'],
        'password' : password
    }

    if conf:
        if texto == 'eu quero excluir minha conta :(':
            try:
                AuthAPI.login(Login(**data))
                response = UserAPI.delete(user['id'])

                st.success(response)

                progress_text = "Apagando sua conta.. tchauu :("
                my_bar = st.progress(0, text=progress_text)

                for percent_complete in range(100):
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1, text=progress_text)
                
                time.sleep(1)
                my_bar.empty()
                time.sleep(2)

                
                st.switch_page("app.py")
            except Exception as e:
                st.error(f"Erro: {e}")
        else:
            st.error("Texto incorreto, verifique.")

@st.dialog("Editar experiência profissional")
def edit_experience():
    #buscar valores do usuario e acrescentar em value
    função = st.text_input(label = "Função", value="Analista de dados")
    cargo = st.text_input(label = "Cargo", value="Estagiario")
    empresa = st.text_input(label = "Empresa", value="Vexpenses")
    inicio = st.date_input(label = "Início", min_value=date(1900, 1, 1), value=date(2024, 1, 1))
    ate = st.date_input(label = "Até", min_value=date(1900, 1, 1))
    descricao = st.text_area(label="Descrição", value="analistar dados, etc, etc")
    
    editar = st.button("Atualizar", use_container_width=True, key='editar-exp')
    #editar informações via api

@st.dialog("Adicionar experiência profissional")
def add_experience():
    #buscar valores do usuario e acrescentar em value
    função = st.text_input(label = "Função")
    cargo = st.text_input(label = "Cargo")
    empresa = st.text_input(label = "Empresa")
    inicio = st.date_input(label = "Início", min_value=date(1900, 1, 1))
    ate = st.date_input(label = "Até", min_value=date(1900, 1, 1))
    descricao = st.text_area(label="Descrição")
    
    adicionar = st.button("Adicionar", use_container_width=True, key='add-exp')
    #adicionar informações via api

@st.dialog("Remover experiência profissional")
def rmv_experience():
    #pegar a lista de experiencias por nome da empresa
    exps = ['exp1', 'exp2', 'exp3']
    
    selects = st.multiselect(label="Selecione as experiências", options=exps, default=None)
    
    remover = st.button("Remover", use_container_width=True, key='remover-exp')
    #remover informações via api

if __name__ == "__main__":
    main()