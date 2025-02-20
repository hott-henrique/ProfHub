import streamlit as st
from sdk.AcademicBackgroundAPI import AcademicBackgroundAPI
from sdk.WorkingExperienceAPI import WorkingExperienceAPI
from sdk.CourseAPI import CourseAPI
from sdk.CertificateAPI import CertificateAPI
from sdk.LanguageKnowledgeAPI import LanguageKnowledgeAPI

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
        cou = CourseAPI.get_all_from_uid(user['id'])
        num = len(xp)
        container_list = []

        for cu in range(num):
            container_list.append(st.container(border=True, key="container-cu" + str(cu)))

        for index, container in enumerate(container_list):
            with container:
                st.write(f"Nome: {cou[index]['name']}")
                st.write(f"Workload: {cou[index]['workload']}")
                st.write(f"Data: {cou[index]['date'].split('T')[0]}")
                st.write(f"Descrição: {cou[index]['description']}")

    with st.expander("Certificações"):
        cert = CertificateAPI.get_all_from_uid(user['id'])
        cert = sorted(cert, key=lambda x: x['id'])
        num = len(cert)
        container_list = []

        for c in range(num):
            container_list.append(st.container(border=True, key="container-cert" + str(c)))

        for index, container in enumerate(container_list):
            with container:
                st.write(f"Nome: {cert[index]['name']}")
                st.write(f"Chave para validação: {cert[index]['validation_key']}")
                st.write(f"Data da obtenção: {cert[index]['date'].split('T')[0]}")
                st.write(f"Expira em: {cert[index]['date'].split('T')[0]}")

    with st.expander("Idiomas"):
        idiomas = LanguageKnowledgeAPI.get_all_from_uid(user['id'])
        idiomas = sorted(idiomas, key=lambda x: x['id']) #ordenando por id
        num = len(idiomas)
        container_list = []

        for c in range(num):
            container_list.append(st.container(border=True, key="idiomas-cert" + str(c)))

        for index, container in enumerate(container_list):
            with container:
                st.write(f"Idioma: {idiomas[index]['language']}")
                st.write(f"Proeficiência: {idiomas[index]['proficiency_level']}")

if __name__ == "__main__":
    main()