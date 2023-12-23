import streamlit as st
import jwt
import os
from dotenv import dotenv_values
valores = dotenv_values("secrets.env") 
codigo_privado=valores["codigo_privado"]
st.title("Hola")

encriptado='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyIxIjoiaG9sYSJ9.vfG89E4Cr-8d_gmq5Z6xL96qaK1CPDeCjDhB2cdjaDU'

input_contrasena=st.text_input("Introduce tu conseña:", type="password")

if input_contrasena==jwt.decode(encriptado, codigo_privado, algorithms="HS256")["1"]:
    st.info("Tienes en al banco 1000€")
else:
    st.error("Contrasñea incorrecta")
