import streamlit as st
from streamlit_option_menu import option_menu
from sdk.UserAPI import UserAPI

def main():
    st.set_page_config(page_title='ProfHub', page_icon=':material/person:')
    st.sidebar.image("app/images/profhub-logo.png")
    user = st.session_state['user'] if 'user' in st.session_state else st.switch_page("app.py")

    with st.sidebar:
        selected = option_menu(
            menu_title=None,
            options=["Visualizar currículo", "Busca avançada", "Sair"],
            icons=["file-earmark-text", "search", "escape"],
            default_index=1,
        )

        if selected == "Visualizar currículo":
            st.switch_page("pages/visualizar.py")
        elif selected == "Buscar avançada":
            st.switch_page("pages/busca.py")
        elif selected == "Sair":
            st.session_state['user'] = None
            st.switch_page("app.py")

    st.title("olá, " + user['name'], anchor=False)

    option = st.selectbox(
        "Selecione o tipo de busca", ("Usuário", "Experiências", "Certificações", "Cursos", "Idiomas"),
    )

    prompt = st.chat_input(placeholder="Faça sua busca")

    if prompt:
        if option == "Usuário":
            search_auth(prompt)
        else: 
            st.write("Em breve teremos essa busca.")

def search_auth(prompt):
    response = UserAPI.search_by_text(prompt)
    num = len(response)
    container_list = []

    for exp in range(num):
        container_list.append(st.container(border=True, key="container-avan" + str(exp)))
    
    for index, container in enumerate(container_list):
        with container:
            st.subheader(response[index]['name'])
            with st.expander("Informações pessoais"):
                st.write(f"E-mail: {response[index]['email']}")
                st.write(f"Github: {response[index]['github']}")
                st.write(f"Telefone: {response[index]['phone']}")
                st.write(f"Aniversário: {response[index]['birthdate'].split('T')[0]}")

if __name__ == "__main__":
    main()