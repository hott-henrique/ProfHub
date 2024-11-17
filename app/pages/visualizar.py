import streamlit as st

from datetime import date
from streamlit_option_menu import option_menu

def main():
    st.set_page_config(page_title='ProfHub', page_icon=':material/person:')
    st.sidebar.image("app/images/profhub-logo.png")

    st.sidebar.title(f"olá, {st.session_state['user']}")
    
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
    
        st.chat_input(placeholder="Faça sua busca")
    
    st.title(st.session_state['user'], anchor=False)
    #st.toast para cadastro de informações
    
    with st.expander("Informações pessoais"):
        container = st.container(border=True, key='container-infos')
        container.write(f"Nome: Matheus")
        container.write("E-mail: matheus@gmail.com")
        container.write("Github: github.com/robotheus")
        container.write("Telefone: 31981180164")
        container.write("Aniversário: 07/11/2003")

        st.button("Editar", use_container_width=True, on_click=edit_user)
    
    with st.expander("Experiências profissionais"):
        #obter uma lista de experiencias
        num_exps = 2
        container_list = []

        for exp in range(num_exps):
            container_list.append(st.container(border=True, key="container" + str(exp)))
        
        for container in container_list:
            container.write("Função: Analista de dados")
            container.write("Cargo: Estagiário")
            container.write("Empresa: Vexpenses")
            container.write("Inicio: 01/2024")
            container.write("Até: Atualmente")
            container.write("Descrição: Analisar dados")
            
        left, middle, right = st.columns(3, vertical_alignment="bottom")

        left.button("Adicionar", key='adicionar-experiencia', use_container_width=True, on_click=add_experience)
        middle.button("Editar", key='editar-experiencia', use_container_width=True, on_click=edit_experience)
        right.button("Apagar", key='apagar-experiencia', use_container_width=True, on_click=rmv_experience)
    
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
    #buscar valores do usuario e acrescentar em value
    name          = st.text_input(label = "Nome", value="Matheus")
    birthdate     = st.date_input(label = "Data de nascimento", format='DD/MM/YYYY', min_value=date(1900, 1, 1), value=date(2003, 11, 7))
    email         = st.text_input(label= "E-mail", value="matheus@gmail.com")
    phone         = st.text_input(label= "Telefone", value="31981180164")
    github        = st.text_input(label= "Github", value="github.com/robotheus")
    
    editar = st.button("Atualizar", use_container_width=True, key='salvar-user')    
    #editar informações via api

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