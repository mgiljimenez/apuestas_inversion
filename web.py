#Importación de librerías
import streamlit as st
from streamlit_option_menu import option_menu
import hashlib
from utils.variables import contrasena_crip, url_grafica_desmos
from utils.functions import busqueda_inversion, comprobar_inversion
from utils.mysql import importar_datos, apuestas,mover_dinero, metricas, tablas, graficas
import time
import webbrowser

#Definimos variables del sistema
st.set_page_config(
    page_title="Inversiones",
    page_icon="chart_with_upwards_trend")
nombres_deportes=importar_datos.deportes(type="nombres")
nombre_inversores=importar_datos.inversores(type="nombres")
nombre_casas_apuesta=importar_datos.casas_apuestas(type="nombres")

#Codigo página web
with st.sidebar:
    selected = option_menu("Menu", ["Home", 'Inversiones',"Mover dinero"], 
        icons=['graph-up-arrow', 'plus-circle',"coin"], menu_icon="grid", default_index=0)

##################
####PÁGINA HOME###
##################
if selected=="Home":
    #Selección lateral de la subpágina
    sidebar=st.sidebar.radio("Seleccione la información a mostrar", 
                             ("Dashboard","Casas de apuesta","Inversores","Apuestas"))
    if sidebar=="Dashboard":
        col1, col2, col3= st.columns(3)
        with col1:
            col1.metric("Total en cartera", str(round(metricas.cartera_total_actual(),2))+"€","100%")
            col1.metric("Invertido histórico", str(round(metricas.invertido_historico_total(),2))+"€","100%")
            col1.metric("Beneficio histórico", str(round(metricas.beneficio_historico_total(),2))+"€","100%")
            col1.metric("Rentabilidad media histórica", str(round(metricas.rentabilidad_media_inversionesindividuales_historico(),4))+"%","100%")
        with col2:
            col2.metric("Dinero invertido", str(round(metricas.invertido_actual(),2))+"€","100%")
            col2.metric("Invertido este mes", str(round(metricas.invertido_este_mes_total(),2))+"€","100%")
            col2.metric("Beneficio este mes", str(round(metricas.beneficio_este_mes_total(),2))+"€","100%")
            col2.metric("Rentabilidad media este mes", str(round(metricas.rentabilidad_media_inversionesindividuales_este_mes(),4))+"%","100%")
        with col3:
            col3.metric("Dinero estancado", str(round(metricas.estancado_actual(),2))+"€","100%")
            col3.metric("Invertido hoy", str(round(metricas.invertido_hoy_total(),2))+"€","100%")
            col3.metric("Beneficio hoy", str(round(metricas.benecifio_hoy_total(),2))+"€","100%")
            col3.metric("Rentabilidad media hoy", str(round(metricas.rentabilidad_media_inversionesindividuales_hoy(),4))+"%","100%")
        st.write("---")
        st.plotly_chart(graficas.comparacion_inversion_estancado(),use_container_width=True)
    elif sidebar=="Casas de apuesta":
        st.metric("Dinero en Cuenta general central",str(metricas.cuenta_general())+"€")
        st.plotly_chart(graficas.dinero_en_cuentas_casas_apuesta(),use_container_width=True)
    elif sidebar=="Inversores":
        st.plotly_chart(graficas.aportaciones_inversores())
    elif sidebar=="Apuestas":
        st.dataframe(tablas.apuestas_individuales_todas())
#########################
####PÁGINA INVERSIONES###
#########################
elif selected=="Inversiones":
    #Selección lateral de la subpágina
    sidebar=st.sidebar.radio("Seleccione la acción a realizar", 
                             ("Buscar nuevas inversiones","Ayuda a la inversión","Registrar nueva inversión","Cerrar inversión"))
    #Subpágina para buscar las nuevas inversiones
    if sidebar=="Buscar nuevas inversiones":
        input_contrasena = st.text_input("Contraseña:", value="", type="password")
        if hashlib.sha256(input_contrasena.encode()).digest()==contrasena_crip:
            valor_inversion = st.number_input('Dinero total a invertir')
            st.write('Inversión:', valor_inversion)
            if valor_inversion>0:
                datos_tenis=busqueda_inversion.sporty_trader_streamlit(valor_inversion,"https://www.sportytrader.es/cuotas/tenis/")
                for i in datos_tenis:
                    st.info(datos_tenis[i][1] +"-------"+ datos_tenis[i][0]+"-------Tenis"+"---"+f"[link]({datos_tenis[i][2]})")
                    col1, col2= st.columns(2)
                    with col1:
                        st.header(datos_tenis[i][5]+" : "+datos_tenis[i][3])
                        st.write("Inversión:",datos_tenis[i][8])
                        st.write("Rentabilidad:",datos_tenis[i][10])
                    with col2:
                        st.header(datos_tenis[i][6]+" : "+datos_tenis[i][4])
                        st.write("Inversión:",datos_tenis[i][9])
                        st.write("Rentabilidad:",datos_tenis[i][11])
                datos_baloncesto=busqueda_inversion.sporty_trader_streamlit(valor_inversion,"https://www.sportytrader.es/cuotas/baloncesto/")
                for i in datos_baloncesto:
                    st.info(datos_baloncesto[i][1] +"-------"+ datos_baloncesto[i][0]+"-------Baloncesto"+"---"+f"[link]({datos_baloncesto[i][2]})")
                    col1, col2= st.columns(2)
                    with col1:
                        st.header(datos_baloncesto[i][5]+" : "+datos_baloncesto[i][3])
                        st.write("Inversión:", datos_baloncesto[i][8])
                        st.write("Rentabilidad:",datos_baloncesto[i][10])

                    with col2:
                        st.header(datos_baloncesto[i][6]+" : "+datos_baloncesto[i][4])
                        st.write("Inversión:", datos_baloncesto[i][9])
                        st.write("Rentabilidad:", datos_baloncesto[i][11])
            else:
                st.write("Introduzca un valor mayor a 0")
        else:
            st.write("Contraseña incorrecta")
    #Subpágina de útiles para la inversión
    elif sidebar=="Ayuda a la inversión":
        with st.form("rentabilidad_beneficio_final"):
            st.info("Comprobación de rentabiilidad y beneficio")
            col1, col2=st.columns(2)
            with col1:
                st.header("Primera casa")
                mul1=st.number_input("Multiplicador 1")
                inv1=st.number_input("Inversión 1")
            with col2:
                st.header("Segunda casa")
                mul2=st.number_input("Multiplicador 2")
                inv2=st.number_input("Inversión 2")
            submit_but=st.form_submit_button("Comprobar")
            if submit_but:
                datos=comprobar_inversion.comprobar(mul1, mul2, inv1, inv2)
                col3, col4=st.columns(2)
                with col3:
                    st.header("Primera casa")
                    st.write(f"Beneficio: {datos[0]} €")
                    st.write(f"Rentabilidad: {datos[1]} %")
                with col4:
                    st.header("Segunda casa")
                    st.write(f"Beneficio: {datos[2]} €")
                    st.write(f"Rentabilidad: {datos[3]} %")
        with st.form("Buscar_cuanto_invertir"):
            st.info("Buscar cuánto invertir en una casa sabiendo la inversión en la otra")
            col1, col2=st.columns(2)
            with col1:
                st.header("Primera casa")
                mul1=st.number_input("Multiplicador 1")
                inv1=st.number_input("Inversión 1")
            with col2:
                st.header("Segunda casa")
                mul2=st.number_input("Multiplicador 2")
            sub_button=st.form_submit_button("Comprobar")
            if sub_button:
                datos=comprobar_inversion.relacion_inversion(mul1,inv1,mul2)
                st.warning(f"Hay que invertir en la segunda casa: {datos[1]}")
                col3, col4=st.columns(2)
                with col3:
                    st.header("Primera casa")
                    st.write(f"Beneficio: {datos[0][0]} €")
                    st.write(f"Rentabilidad: {datos[0][1]} %")
                with col4:
                    st.header("Segunda casa")
                    st.write(f"Beneficio: {datos[0][2]} €")
                    st.write(f"Rentabilidad: {datos[0][3]} %") 
        boton_desmos=st.button("Abrir gráfica de área de rentabilidad", use_container_width=True)
        if boton_desmos:
            webbrowser.open_new_tab(url_grafica_desmos)
    #Subpágina para registrar nuevas inversiones realizadas
    elif sidebar=="Registrar nueva inversión":
        with st.form("registrar_nueva_inversion"):
            st.info("Rellena un nuevo registro tras haber realizado una inversión")
            fecha_inversion = st.date_input(
                "¿Qué día se ha realizado la apuesta?")
            fecha_partido = st.date_input(
                "¿Qué día se juega el partido?")
            hora_partido=st.time_input("¿A qué hora se juega el partido?")
            deporte= st.selectbox(
                'Deporte',importar_datos.deportes(type="nombres"))
            col1, col2 = st.columns(2)
            with col1:
                st.write("Inversión 1")
                equipo1=st.text_input('Nombre del primer equipo')
                casa1= st.selectbox(
                'Casa de apuesta 1',importar_datos.casas_apuestas(type="nombres"))
                multiplicador1=st.number_input('Multiplicador 1',min_value=0.000) 
                inversion1=st.number_input('Inversion 1',min_value=0.000,step=0.001) 
            with col2:
                st.write("Inversión 2")
                equipo2=st.text_input('Nombre del segundo equipo')
                casa2= st.selectbox(
                'Casa de apuesta 2',importar_datos.casas_apuestas(type="nombres"))
                multiplicador2=st.number_input('Multiplicador 2',min_value=0.000) 
                inversion2=st.number_input('Inversion 2',min_value=0.000) 
            submitted_but=st.form_submit_button("Registrar nueva apuesta", use_container_width=True)
            if submitted_but:
                fecha_partido_format=fecha_partido.strftime("%Y-%m-%d")
                hora_partido_format=hora_partido.strftime("%H:%M:%S")
                fecha_hora_partido=fecha_partido_format +" "+hora_partido_format
                if multiplicador1>0 and multiplicador2>0 and inversion1>0 and inversion2>0:
                    apuestas.nueva_apuesta(fecha_inversion,fecha_hora_partido,deporte,equipo1,equipo2,casa1,multiplicador1,inversion1,casa2,multiplicador2,inversion2)
                    st.success("Nuevo evento registrado correctamente")
                    time.sleep(3)
                else:
                    st.error("Rellene todos los campos correctamente")
                    time.sleep(3)
                st.experimental_rerun()
    #Subpágina para cerrar una inversión que está abierta
    elif sidebar=="Cerrar inversión":
        id_confirmado=False
        st.info("Apuestas actualmente abiertas:")
        st.dataframe(tablas.apuestas_individuales_abiertas())
        st.info("Tras finalizar un evento, indique su ID y el ganador")
        indice_seleccionado=st.selectbox("Indique el ID",importar_datos.apuestas_individuales(type="abiertas_id"))
        casa_ganadora=st.selectbox("Indique la casa de apuesta ganadora", importar_datos.casas_apuesta_de_una_inversion(indice_seleccionado))
        confirmar_id = st.button("Cerrar la apuesta", use_container_width=True)
        if confirmar_id:
            apuestas.cerrar_apuesta(indice_seleccionado,casa_ganadora)
            st.success("Inversión cerrada correctamente")
            time.sleep(3)
            st.experimental_rerun()
##########################
####PÁGINA MOVER DINERO###
##########################
elif selected=="Mover dinero":
    #Selección lateral de la subpágina
    sidebar=st.sidebar.radio("Seleccione la acción a realizar", 
                             ("INGRESO en casa de apuesta","RETIRADA de casa de apuesta","INGRESO de un inversor","RETIRADA de un inversor"))
    #Se ingresa dinero de la cuenta central general a la casa de apuesta
    if sidebar=="INGRESO en casa de apuesta":
        with st.form("ingreso_casa"): 
            st.info("Ingresar dinero en una casa de apuestas")
            casa=st.selectbox('Seleccione la casa de apuestas',nombre_casas_apuesta)
            dinero=st.number_input('Dinero ingresado',min_value=0.00)
            submitted = st.form_submit_button("Ingresar dinero en la casa de apuesta", use_container_width=True)
            if submitted:
                try:
                    mover_dinero.ingreso_casa_apuesta(casa,dinero)
                    st.success("Ingreso realizado")
                    time.sleep(3)
                except:
                    st.error("Error, no se ha realizado el ingreso")
                    time.sleep(3)
                st.experimental_rerun()
    #Se retira dinero de la cuenta de una casa de apuestas a la cuenta central general
    elif sidebar=="RETIRADA de casa de apuesta":
        with st.form("retirada_casa"): 
            st.info("Retirar dinero de una casa de apuestas")
            casa=st.selectbox('Seleccione la casa de apuestas',nombre_casas_apuesta)
            dinero=st.number_input('Dinero retirado',min_value=0.00)
            submitted = st.form_submit_button("Retirar dinero de la casa de apuesta", use_container_width=True)
            if submitted:
                try:
                    mover_dinero.retirada_casa_apuesta(casa,dinero)
                    st.success("Retirada realizada")
                    time.sleep(3)
                except:
                    st.error("Error, no se ha realizado la retirada")
                    time.sleep(3)
                st.experimental_rerun()
    #Se ingresa dinero por parte de un inversor a la cuenta general central
    elif sidebar=="INGRESO de un inversor":
        with st.form("ingreso_inversor"): 
            st.info("Un inversor ha ingresado dinero")
            inversor=st.selectbox('Seleccione al inversor',nombre_inversores)
            dinero=st.number_input('Dinero ingresado',min_value=0.00)
            submitted = st.form_submit_button("Ingresar el dinero del inversor", use_container_width=True)
            if submitted:
                try:
                    mover_dinero.ingreso_inversor(inversor,dinero)
                    st.success("Ingreso realizado")
                    time.sleep(3)
                except:
                    st.error("Error, no se ha realizado el ingreso")
                    time.sleep(3)
                st.experimental_rerun()
    #Se retira dinero de la cuenta general central para un inversor
    elif sidebar=="RETIRADA de un inversor":
       with st.form("retirada_inversor"): 
            st.info("Un inversor ha retirado dinero")
            inversor=st.selectbox('Seleccione al inversor',nombre_inversores)
            dinero=st.number_input('Dinero retirado',min_value=0.00)
            submitted = st.form_submit_button("Retirar dinero del inversor", use_container_width=True)
            if submitted:
                try:
                    mover_dinero.retirada_inversor(inversor,dinero)
                    st.success("Retirada realizada")
                    time.sleep(3)
                except:
                    st.error("Error, no se ha realizado la retirada")
                    time.sleep(3)
                st.experimental_rerun()