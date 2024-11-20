import streamlit as st

def main():
    st.set_page_config(page_title='ProfHub', page_icon=':material/person:')
    user = st.session_state['view_user'] if 'view_user' in st.session_state else st.switch_page("busca.py")

    col1, col2, col3 = st.columns(3)
    
    with col2:
        st.image("app/images/profhub-logo.png", width=300)

    c1, c2, c3 = st.columns(3, vertical_alignment="bottom")
    c1.subheader(f"{user['name']}", anchor=False)
    sair = c3.button("Fechar currículo", use_container_width=True)

    if sair:
        st.session_state['view_user'] = None
        st.switch_page("app.py")

    with st.expander("Informações pessoais"):
        container = st.container(border=True, key='container-infos')
        container.write(f"Nome: {user['name']}")
        container.write(f"E-mail: {user['email']}")
        container.write(f"Github: {user['github']}")
        container.write(f"Telefone: {user['phone']}")
        container.write(f"Aniversário: {user['birthdate'].split('T')[0]}")

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

if __name__ == "__main__":
    main()