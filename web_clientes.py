#Importación de librerías
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth
import hashlib
from utils.variables import contrasena_crip, url_grafica_desmos
from utils.functions import busqueda_inversion, comprobar_inversion
from utils.mysql import importar_datos, apuestas,mover_dinero, metricas, tablas, graficas
import time
import webbrowser

import yaml
from yaml.loader import SafeLoader
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

#Definimos variables del sistema
st.set_page_config(
    page_title="Inversiones",
    page_icon="chart_with_upwards_trend")

sesion_iniciada=False
#Página actual

if sesion_iniciada==False:
    #Definimos la página de inicio
    with st.form("my_form"):
        st.write("Log In")
        user = st.text_input("Correo")
        password = st.text_input("Contraseña", value="", type="password")
        if st.form_submit_button("Iniciar"):
            if user=="mgiljimenez@gmail.com" and password=="developer321":
                sesion_iniciada=True
if sesion_iniciada==True:
    #Codigo página web
    with st.sidebar:
        selected = option_menu("Menu", ["Home", 'Inversiones',"Mover dinero"], 
            icons=['graph-up-arrow', 'plus-circle',"coin"], menu_icon="grid", default_index=0)

    if selected=="Home":
        st.title("Hola")
    if selected=="Inversiones":
        st.title("Adios")


    