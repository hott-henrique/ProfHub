import streamlit as st
from streamlit_option_menu import option_menu
from sdk.UserAPI import UserAPI
from sdk.AcademicBackgroundAPI import AcademicBackgroundAPI
from model.AcademicBackground import EducationLevel
from sdk.WorkingExperienceAPI import WorkingExperienceAPI

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
        "Selecione o tipo de busca", ("Usuário", "Formação acadêmica", "Experiências", "Certificações", "Cursos", "Idiomas"),
    )
    
    if option == "Formação acadêmica":
        levels = ['Técnico', 'Graduação', 'Pós-graduação', 'Mestrado', 'Doutorado', 'Pós-doutorado']
        mapa = {'Técnico' : 'technical', 'Graduação' : 'undergraduate', 'Pós-graduação' : 'postgraduate', 
        'Mestrado': 'master', 'Doutorado': 'doctorate', 'Pós-doutorado': 'postdoctorate'}
        level = st.selectbox(label = "Nível", options=levels)
        level_o = mapa[level]

    prompt = st.chat_input(placeholder="Faça sua busca")

    if prompt:
        if option == "Usuário":
            search_user(prompt)
        elif option == "Formação acadêmica":
            search_form(prompt, level_o)
        elif option == "Experiências":
            search_xp(prompt)

def search_user(prompt):
    user = UserAPI.search_by_text(prompt)
    
    for u in user:
        st.button(label=u['name'], use_container_width=True, key="preview-" + str(u['id']), on_click=view, args=(u,))
            
def search_form(prompt, level):
    response = AcademicBackgroundAPI.search_by_text(prompt, EducationLevel(level))
    
    for form in response:
        u = UserAPI.search_by_id(form['uid'])
        st.button(label=u['name'], use_container_width=True, key="preview-" + str(u['id']), on_click=view, args=(u,))

def search_xp(prompt):
    response = WorkingExperienceAPI.search_by_text(prompt)
    
    for form in response:
        u = UserAPI.search_by_id(form['uid'])
        st.button(label=u['name'], use_container_width=True, key="preview-" + str(u['id']), on_click=view, args=(u,))

@st.dialog("Currículo")
def view(user):
    st.write(f"Nome: {user['name']}")
    with st.expander("Informações pessoais"):
        container = st.container(border=True, key='container-infos')
        container.write(f"E-mail: {user['email']}")
        container.write(f"Github: {user['github']}")
        container.write(f"Telefone: {user['phone']}")
        container.write(f"Aniversário: {user['birthdate'].split('T')[0]}")

    with st.expander("Formação acadêmica"):
        formations = AcademicBackgroundAPI.get_all_from_uid(user['id'])
        num_formations = len(formations)
        container_list_formations = []
        
        for x in range(num_formations):
            container_list_formations.append(st.container(border=True, key="container-form" + str(x)))
        
        for index_formation, container_formation in enumerate(container_list_formations):    
            with container_formation:
                st.write(f"Nome: {formations[index_formation]['name']}")
                st.write(f"Instituição: {formations[index_formation]['institution']}")
                st.write(f"Início: {formations[index_formation]['starting_date'].split('T')[0]}")
                st.write(f"Fim ou Previsão: {formations[index_formation]['ending_date'].split('T')[0]}")
                st.write(f"Carga horária: {formations[index_formation]['workload']}")
                st.write(f"Descrição: {formations[index_formation]['description']}")
                st.write(f"Nível: {formations[index_formation]['level']}")
    
    with st.expander("Experiências profissionais"):
        xp = WorkingExperienceAPI.get_all_from_uid(user['id'])
        num = len(xp)
        container_list = []

        for exp in range(num):
            container_list.append(st.container(border=True, key="container-xp" + str(exp)))

        for index, container in enumerate(container_list):
            with container:
                st.write(f"Cargo: {xp[index]['job']}")
                st.write(f"Empresa: {xp[index]['company'].split('T')[0]}")
                st.write(f"Início: {xp[index]['starting_date'].split('T')[0]}")
                st.write(f"Fim: {xp[index]['ending_date'].split('T')[0]}")
                st.write(f"Descrição: {xp[index]['description']}")


    with st.expander("Cursos"):
        st.write("Em breve...")

    with st.expander("Certificações"):
        st.write("Em breve...")

    with st.expander("Idiomas"):
        st.write("Em breve...")

if __name__ == "__main__":
    main()