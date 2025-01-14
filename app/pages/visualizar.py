import streamlit as st
import time

from datetime import date
from streamlit_option_menu import option_menu
from sdk.UserAPI import UserAPI
from model.User import User
from sdk.AuthAPI import AuthAPI
from model.Login import Login
from model.UpdatePassword import UpdatePassword
from sdk.AcademicBackgroundAPI import AcademicBackgroundAPI
from model.AcademicBackground import AcademicBackground
from sdk.WorkingExperienceAPI import WorkingExperienceAPI
from model.WorkingExperience import WorkingExperience
from model.Course import Course
from sdk.CourseAPI import CourseAPI
from model.Certificate import Certificate
from sdk.CertificateAPI import CertificateAPI
from sdk.LanguageKnowledgeAPI import LanguageKnowledgeAPI
from model.LanguageKnowledge import Language, LanguageProciencyLevel, LanguageKnowledge

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
    
    with st.expander("Formação acadêmica"):
        formations = AcademicBackgroundAPI.get_all_from_uid(user['id'])
        formations = sorted(formations, key=lambda x: x['id']) #ordernar por id
        
        num = len(formations)
        container_list = []

        for form in range(num):
            container_list.append(st.container(border=True, key="container-avan" + str(form)))
        
        for index, container in enumerate(container_list):
            with container:
                st.write(formations[index]['name'])
                st.write(f"Instituição: {formations[index]['institution']}")
                st.write(f"Início: {formations[index]['starting_date'].split('T')[0]}")
                st.write(f"Até: {formations[index]['ending_date'].split('T')[0]}")
                st.write(f"Carga horária: {formations[index]['workload']}")
                st.write(f"Nível: {formations[index]['level']}")
                st.write(f"Descrição: {formations[index]['description']}")

                left, right = st.columns(2, vertical_alignment="bottom")

                left.button("Editar formação", key=f'editar-form-{index}', use_container_width=True, on_click=edit_formation, args=(formations[index]['id'], formations[index]))
                right.button("Apagar formação", key=f'apagar-form-{index}', use_container_width=True, on_click=delete_formation, args=(formations[index]['id'], formations[index]))
        
        st.button("Adicionar formação", key='adicionar-form', use_container_width=True, on_click=add_formation)
        
    with st.expander("Experiências profissionais"):
        xp = WorkingExperienceAPI.get_all_from_uid(user['id'])
        xp = sorted(xp, key=lambda x: x['id']) #ordenar por id

        num = len(xp)
        container_list = []

        for exp in range(num):
            container_list.append(st.container(border=True, key="container-xp" + str(exp)))

        for index, container in enumerate(container_list):
            with container:
                st.write(f"Cargo: {xp[index]['job']}")
                st.write(f"Empresa: {xp[index]['company']}")
                st.write(f"Início: {xp[index]['starting_date'].split('T')[0]}")
                st.write(f"Fim: {xp[index]['ending_date'].split('T')[0]}")
                st.write(f"Descrição: {xp[index]['description']}")

                left, right = st.columns(2, vertical_alignment="bottom")

                left.button("Editar experiência", key=f'editar-xp-{index}', use_container_width=True, on_click=edit_xp, args=(xp[index]['id'], xp[index]))
                right.button("Apagar experiência", key=f'apagar-xp-{index}', use_container_width=True, on_click=delete_xp, args=(xp[index]['id'], xp[index]))
        
        st.button("Adicionar experiência", key='adicionar-xp', use_container_width=True, on_click=add_xp, args=(user, ))
    
    with st.expander("Cursos"):
        cou = CourseAPI.get_all_from_uid(user['id'])
        cou = sorted(cou, key=lambda x: x['id']) #ordenando por id

        num = len(cou)
        container_list = []

        for caaa in range(num):
            container_list.append(st.container(border=True, key="container-course" + str(caaa)))

        for index, container in enumerate(container_list):
            with container:
                st.write(f"Nome: {cou[index]['name']}")
                st.write(f"Workload: {cou[index]['workload']}")
                st.write(f"Data: {cou[index]['date'].split('T')[0]}")
                st.write(f"Descrição: {cou[index]['description']}")

                left, right = st.columns(2, vertical_alignment="bottom")

                left.button("Editar curso", key=f'editar-c-{index}', use_container_width=True, on_click=edit_course, args=(cou[index], ))
                right.button("Apagar curso", key=f'apagar-c-{index}', use_container_width=True, on_click=delete_course, args=(cou[index], ))
    
        st.button("Adicionar curso", key='add-course', use_container_width=True, on_click=add_course, args=(user['id'], ))
    
    with st.expander("Certificações"):
        cert = CertificateAPI.get_all_from_uid(user['id'])
        cert = sorted(cert, key=lambda x: x['id']) #ordenando por id
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

                left, right = st.columns(2, vertical_alignment="bottom")

                left.button("Editar certificação", key=f'editar-cer-{index}', use_container_width=True, on_click=edit_cert, args=(cert[index], ))
                right.button("Apagar certificação", key=f'apagar-cer-{index}', use_container_width=True, on_click=delete_cert, args=(cert[index], ))
        
        st.button("Adicionar certificação", key='add-cert', use_container_width=True, on_click=add_cert, args=(user['id'], ))

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
                
                left, right = st.columns(2, vertical_alignment="bottom")

                left.button("Editar idioma", key=f'editar-idio-{index}', use_container_width=True, on_click=edit_idioma, args=(idiomas[index], ))
                right.button("Apagar idioma", key=f'apagar-idio-{index}', use_container_width=True, on_click=delete_idioma, args=(idiomas[index], ))
        
        st.button("Adicionar idioma", key='add-idio', use_container_width=True, on_click=add_idioma, args=(user['id'], ))
    
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

@st.dialog("Adicionar formação acadêmica")
def add_formation():
    name = st.text_input(label = "Nome")
    institution = st.text_input(label = "Instituição")
    s_date = st.date_input(label = "Início", format='DD/MM/YYYY', min_value=date(1900, 1, 1))
    e_date = st.date_input(label = "Fim ou Previsão", format='DD/MM/YYYY', min_value=date(1900, 1, 1))
    workload = st.number_input(label  = "Carga horária", step=100)
    description = st.text_area(label = "Descrição", max_chars=300)
    levels = ['Técnico', 'Graduação', 'Pós-graduação', 'Mestrado', 'Doutorado', 'Pós-doutorado']
    mapa = {'Técnico' : 'technical', 'Graduação' : 'undergraduate', 'Pós-graduação' : 'postgraduate', 
            'Mestrado': 'master', 'Doutorado': 'doctorate', 'Pós-doutorado': 'postdoctorate'}
    level = st.selectbox(label = "Nível", options=levels)
    level_o = mapa[level]

    data = {
        'uid': st.session_state['user']['id'],
        'name': name,
        'institution': institution,
        'starting_date': s_date,
        'ending_date': e_date,
        'workload': workload,
        'description': description,
        'level': level_o
    }

    add = st.button("Adicionar", use_container_width=True, key='add-form-button') 

    if add:
        try:
            AcademicBackgroundAPI.create(AcademicBackground(**data))
            st.success("Formação adicionada.")
            time.sleep(2)
            st.rerun()
        except Exception as e:
            st.error(f'Erro: {e}')
            
@st.dialog("Editar formação acadêmica")
def edit_formation(arg1, arg2):
    sta_data = arg2['starting_date'].split("T")[0].split("-")
    end_data = arg2['ending_date'].split("T")[0].split("-")

    name = st.text_input(label = "Nome", value=arg2['name'])
    institution = st.text_input(label = "Instituição", value=arg2['institution'])
    s_date = st.date_input(label = "Início", format='DD/MM/YYYY', min_value=date(1900, 1, 1), value=date(int(sta_data[0]), int(sta_data[1]), int(sta_data[2])))
    e_date = st.date_input(label = "Fim ou Previsão", format='DD/MM/YYYY', min_value=date(1900, 1, 1), value=date(int(end_data[0]), int(end_data[1]), int(end_data[2])))
    workload = st.number_input(label  = "Carga horária", step=100, value=arg2['workload'])
    description = st.text_area(label = "Descrição", max_chars=300, value=arg2['description'])
    
    levels = ['Técnico', 'Graduação', 'Pós-graduação', 'Mestrado', 'Doutorado', 'Pós-doutorado']
    mapa = {'Técnico' : 'technical', 'Graduação' : 'undergraduate', 'Pós-graduação' : 'postgraduate', 
            'Mestrado': 'master', 'Doutorado': 'doctorate', 'Pós-doutorado': 'postdoctorate'}
    chave = [key for key, value in mapa.items() if value == arg2['level']][0]
    indice = levels.index(chave)

    level = st.selectbox(label = "Nível", options=levels, index=indice)
    level_o = mapa[level]

    data = {
        'uid': st.session_state['user']['id'],
        'name': name,
        'institution': institution,
        'starting_date': s_date,
        'ending_date': e_date,
        'workload': workload,
        'description': description,
        'level': level_o
    }

    att = st.button("Atualizar", use_container_width=True, key='att-form-button') 

    if att:
        try:
            AcademicBackgroundAPI.update(arg1, AcademicBackground(**data))
            st.success("Formação atualizada.")
            time.sleep(2)
            st.rerun()
        except Exception as e:
            st.error(f'Erro: {e}')

@st.dialog("Remover formação acadêmica")
def delete_formation(arg1, arg2):
    confirm = st.button("Confirmar exclusão da formação acadêmica.", use_container_width=True)

    if confirm:
        AcademicBackgroundAPI.delete(arg1)
        st.success("Formação removida.")
        time.sleep(2)
        st.rerun()

@st.dialog("Adicionar experiência profissional")
def add_xp(user):
    job = st.text_input(label = "Cargo", max_chars=32)
    company = st.text_input(label = "Empresa", max_chars=128)
    s_date = st.date_input(label = "Início", format='DD/MM/YYYY', min_value=date(1900, 1, 1))
    e_date = st.date_input(label = "Fim", format='DD/MM/YYYY', min_value=date(1900, 1, 1))
    description = st.text_area(label = "Descrição", max_chars=300)
    
    data = {
        'uid': user['id'],
        'job': job,
        'company': company,
        'starting_date': s_date,
        'ending_date': e_date,
        'description': description,
    }

    add = st.button("Adicionar", use_container_width=True, key='add-xp-button') 

    if add:
        try:
            WorkingExperienceAPI.create(WorkingExperience(**data))
            st.success("Experiência profissional adicionada.")
            time.sleep(2)
            st.rerun()
        except Exception as e:
            st.error(f'Erro: {e}')

@st.dialog("Editar experiência profissional")
def edit_xp(id, xp):
    sta_data = xp['starting_date'].split("T")[0].split("-")
    end_data = xp['ending_date'].split("T")[0].split("-")

    job = st.text_input(label = "Cargo", value=xp['job'])
    company = st.text_input(label = "Empresa", value=xp['company'])
    s_date = st.date_input(label = "Início", format='DD/MM/YYYY', min_value=date(1900, 1, 1), value=date(int(sta_data[0]), int(sta_data[1]), int(sta_data[2])))
    e_date = st.date_input(label = "Fim", format='DD/MM/YYYY', min_value=date(1900, 1, 1), value=date(int(end_data[0]), int(end_data[1]), int(end_data[2])))
    description = st.text_area(label = "Descrição", max_chars=300, value=xp['description'])
    
    data = {
        'uid': st.session_state['user']['id'],
        'job': job,
        'company': company,
        'starting_date': s_date,
        'ending_date': e_date,
        'description': description,
    }

    att = st.button("Atualizar", use_container_width=True, key='att-xp-button') 

    if att:
        try:
            WorkingExperienceAPI.update(id, WorkingExperience(**data))
            st.success("Experiência profissional atualizada.")
            time.sleep(2)
            st.rerun()
        except Exception as e:
            st.error(f'Erro: {e}')

@st.dialog("Remover experiência profisisonal")
def delete_xp(arg1, arg2):
    confirm = st.button("Confirmar exclusão da experiência profissional.", use_container_width=True)

    if confirm:
        WorkingExperienceAPI.delete(arg1)
        st.success("Experiência removida.")
        time.sleep(2)
        st.rerun()

@st.dialog("Adicionar curso")
def add_course(id_user):
    name = st.text_input(label = "Nome", max_chars=32)
    carga = st.number_input(label = "Carga horária", step=100)
    s_date = st.date_input(label = "Data", format='DD/MM/YYYY', min_value=date(1900, 1, 1))
    description = st.text_area(label = "Descrição", max_chars=300)
    
    data = {
        'uid': id_user,
        'name': name,
        'workload': carga,
        'date': s_date,
        'description': description,
    }

    add = st.button("Adicionar", use_container_width=True, key='add-course-button') 

    if add:
        try:
            CourseAPI.create(Course(**data))
            st.success("Curso adicionado.")
            time.sleep(2)
            st.rerun()
        except Exception as e:
            st.error(f'Erro: {e}')

@st.dialog("Editar curso")
def edit_course(course):
    sta_data = course['date'].split("T")[0].split("-")
    
    name = st.text_input(label = "Nome", max_chars=32, value=course['name'])
    carga = st.number_input(label = "Carga horária", value=course['workload'], step=100)
    s_date = st.date_input(label = "Data", format='DD/MM/YYYY', min_value=date(1900, 1, 1), value=date(int(sta_data[0]), int(sta_data[1]), int(sta_data[2])))
    description = st.text_area(label = "Descrição", max_chars=300, value=course['description'])
    
    data = {
        'uid': course['uid'],
        'name': name,
        'workload': carga,
        'date': s_date,
        'description': description,
    }

    att = st.button("Atualizar", use_container_width=True, key='att-course-button') 

    if att:
        try:
            CourseAPI.update(course['id'], Course(**data))
            st.success("Curso atualizado.")
            time.sleep(2)
            st.rerun()
        except Exception as e:
            st.error(f'Erro: {e}')

@st.dialog("Excluir curso")
def delete_course(course):
    confirm = st.button("Confirmar exclusão do curso.", use_container_width=True)

    if confirm:
        CourseAPI.delete(course['id'])
        st.success("Curso removido.")
        time.sleep(2)
        st.rerun()

@st.dialog("Adicionar certificação")
def add_cert(id):
    name = st.text_input(label = "Nome", max_chars=32)
    key = st.text_input(label = "Chave de validação", max_chars=128)
    date_cert = st.date_input(label = "Data", format='DD/MM/YYYY', min_value=date(1900, 1, 1))
    expire_date = st.date_input(label = "Expira", format='DD/MM/YYYY', min_value=date(1900, 1, 1))
    
    data = {
        'uid': id,
        'name': name,
        'validation_key': key,
        'date': date_cert,
        'expire_date': expire_date,
    }

    add = st.button("Adicionar", use_container_width=True, key='add-cert-button') 

    if add:
        try:
            CertificateAPI.create(Certificate(**data))
            st.success("Certificação adicionada.")
            time.sleep(2)
            st.rerun()
        except Exception as e:
            st.error(f'Erro: {e}')

@st.dialog("Editar certificação")
def edit_cert(cert):
    sta_data = cert['date'].split("T")[0].split("-")
    sta_data2 = cert['expire_date'].split("T")[0].split("-")

    name = st.text_input(label = "Nome", max_chars=32, value=cert['name'])
    validation_key = st.text_input(label = "Chave de validação", max_chars=128,value=cert['validation_key'])
    s_date = st.date_input(label = "Data", format='DD/MM/YYYY', min_value=date(1900, 1, 1), value=date(int(sta_data[0]), int(sta_data[1]), int(sta_data[2])))
    expire_date = st.date_input(label = "Expira", format='DD/MM/YYYY', min_value=date(1900, 1, 1), value=date(int(sta_data2[0]), int(sta_data2[1]), int(sta_data2[2])))
    
    data = {
        'uid': cert['uid'],
        'name': name,
        'validation_key': validation_key,
        'date': s_date,
        'expire_date': expire_date,
    }

    att = st.button("Atualizar", use_container_width=True, key='att-cert-button') 

    if att:
        try:
            CertificateAPI.update(cert['id'], Certificate(**data))
            st.success("Certificação atualizada.")
            time.sleep(2)
            st.rerun()
        except Exception as e:
            st.error(f'Erro: {e}')

@st.dialog("Remover certificação")
def delete_cert(cert):
    confirm = st.button("Confirmar exclusão da certificação.", use_container_width=True)

    if confirm:
        CertificateAPI.delete(cert['id'])
        st.success("Certificação removida.")
        time.sleep(2)
        st.rerun()

@st.dialog("Adicionar idioma")
def add_idioma(id):
    idiomas = [language.value for language in Language]
    proficiencias = [level.value for level in LanguageProciencyLevel]

    idioma = st.selectbox(label = "Idioma", options=idiomas, index=0, placeholder="Selecione o idioma")
    proef = st.selectbox(label = "Proeficiência", options=proficiencias, index=0, placeholder="Selecione sua proeficiência.")
    
    data = {
        'uid': id,
        'language': Language(idioma),
        'proficiency_level': LanguageProciencyLevel(proef)
    }

    add = st.button("Adicionar", use_container_width=True, key='add-idioma-button') 

    if add:
        try:
            LanguageKnowledgeAPI.create(LanguageKnowledge(**data))
            st.success("Idioma adicionado.")
            time.sleep(2)
            st.rerun()
        except Exception as e:
            st.error(f'Erro: {e}')

@st.dialog("Editar idioma")
def edit_idioma(idioma_data):
    idiomas = [language.value for language in Language]
    proficiencias = [level.value for level in LanguageProciencyLevel]

    idi = st.selectbox(label = "Idioma", options=idiomas, index=idiomas.index(idioma_data['language']))
    proefici = st.selectbox(label = "Proeficiência", index=idiomas.index(idioma_data['language']), options=proficiencias)
    
    
    data = {
        'uid': idioma_data['uid'],
        'language': Language(idi),
        'proficiency_level': LanguageProciencyLevel(proefici)
    }

    att = st.button("Atualizar", use_container_width=True, key='att-idioma-button') 

    if att:
        try:
            LanguageKnowledgeAPI.update(idioma_data['id'], LanguageKnowledge(**data))
            st.success("Idioma atualizado.")
            time.sleep(2)
            st.rerun()
        except Exception as e:
            st.error(f'Erro: {e}')

@st.dialog("Remover idioma")
def delete_idioma(idio):
    confirm = st.button("Confirmar exclusão do idioma?", use_container_width=True)

    if confirm:
        LanguageKnowledgeAPI.delete(idio['id'])
        st.success("Idioma removido.")
        time.sleep(2)
        st.rerun()

if __name__ == "__main__":
    main()