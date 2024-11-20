import streamlit as st
from streamlit_option_menu import option_menu

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

        if selected == "Visualizar currículo":
            st.switch_page("pages/visualizar.py")
        elif selected == "Sair":
            st.session_state['user'] = None
            st.switch_page("app.py")
    
    st.title("olá, " + user['name'], anchor=False)

if __name__ == "__main__":
    main()