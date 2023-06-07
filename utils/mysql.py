#Importamos la librerías y variables necesarias
import mysql.connector
from datetime import date
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.variables import sql_user,sql_password,sql_database
#################################################################################
#################################################################################
"""Definimos las variables generales para atacar la base de datos"""
#Definimos la fecha actual
fecha_actual = date.today().strftime("%Y-%m-%d")
#Definimos un cursor con el que atacar a la DB
cnx = mysql.connector.connect(
    user=sql_user,
    password=sql_password,
    database=sql_database
)
cursor = cnx.cursor()
#Definimos una función mediante la que ejecutar las querys
def make_query(code):
    cursor.execute(code)
    results = cursor.fetchall()
    return(results)
#Definimos una función mediante la que ejecutar las querys devolviendo un dataframe
def make_query_dataframe(code):
    cursor.execute(code)
    results = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]  # Obtener los nombres de las columnas
    df = pd.DataFrame(results, columns=column_names)  # Crear el DataFrame
    return df
#################################################################################
#################################################################################

class importar_datos:
    """Importación de tablas solo para lectura"""
    def __init__(self):
        pass
    def deportes(type="all"):
        if type=="all":
            deportes=make_query("SELECT * FROM deportes;")
            return deportes
        elif type =="nombres":
            deportes = make_query("SELECT deporte FROM deportes;")
            nombre_deportes = [deporte[0] for deporte in deportes]
            return nombre_deportes
    def casas_apuestas(type="all"):
        if type=="all":
            casas_apuestas=make_query("SELECT * FROM casas_apuesta;")
            return casas_apuestas
        elif type=="nombres":
            casas_apuestas=make_query("SELECT nombre FROM casas_apuesta;")
            nombre_casas = [casa[0] for casa in casas_apuestas]
            return nombre_casas
    def inversores(type="all"):
        if type=="all":
            inversores=make_query("SELECT * FROM inversores;")
            return inversores
        elif type=="nombres":
            inversores=make_query("SELECT nombre FROM inversores;")
            nombre_inversores = [inversor[0] for inversor in inversores]
            return nombre_inversores
    def apuestas_individuales(type="all"):
        if type=="all":
            apuestas=make_query("SELECT * FROM apuestas_individuales;")
            return apuestas
        elif type=="abiertas":
            apuestas=make_query("SELECT * FROM apuestas_individuales\
                                WHERE ganador IS NULL;")
            return apuestas
        elif type=="abiertas_id":
            lista_tuplas=make_query("SELECT id_apuesta FROM apuestas_individuales\
                                WHERE ganador IS NULL;")
            numeros_simples = [tupla[0] for tupla in lista_tuplas]
            return numeros_simples
    def casas_apuesta_de_una_inversion(id_abierto):
        #Devuelve las dos casas de apuestas a partir de un id de una apuesta individual abierta
        casas=make_query(f"SELECT c1.nombre as casa_apuesta_1, c2.nombre as casa_apuesta_2\
                                FROM apuestas_individuales a\
                                LEFT JOIN deportes d ON a.id_deporte=d.id_deporte\
                                LEFT JOIN casas_apuesta AS c1 ON a.id_casa_apuesta_1 = c1.id_casa_apuesta\
                                LEFT JOIN casas_apuesta AS c2 ON a.id_casa_apuesta_2 = c2.id_casa_apuesta\
                                WHERE a.id_apuesta={id_abierto};")[0]
        return casas

class extraer_id:
    """Clase que facilita acceder al id rápidamente de un valor en una tabla"""
    def __init__(self):
        pass
    def casa_apuesta(nombre_casa):
        #Devuelve el ID de una casa de apuestas a partir de su nombre
        id_casa_apuesta=make_query(f"SELECT id_casa_apuesta FROM casas_apuesta\
                    WHERE nombre='{nombre_casa}';")
        return id_casa_apuesta[0][0]
    def inversor(nombre_inversor):
        #Devuelve el ID de un inversor a partir de su nombre
        id_inversor=make_query(f"SELECT id_inversor FROM inversores\
                    WHERE nombre='{nombre_inversor}';")
        return id_inversor[0][0]
    def deporte(nombre_deporte):
        #Devuelve el ID de un deporte a partir de su nombre
        id_deporte=make_query(f"SELECT id_deporte FROM deportes \
                   WHERE deporte='{nombre_deporte}';")
        return id_deporte[0][0]
    def cuenta_inversor(nombre_inversor):
        #Devuelve el ID de la cuenta de un inversor a partir de su nombre
        id_cuenta_inversor=make_query(f"SELECT id_cuenta from inversores \
                           WHERE nombre='{nombre_inversor}'")[0][0]
        return id_cuenta_inversor
    def cuenta_casa_no_apostado(nombre_casa):
        #Devuelve el ID de la cuenta general de una casa a partir del nombre de la casa
        id_cuenta_casa=make_query(f"SELECT id_cuenta_casa from casas_apuesta \
                           WHERE nombre='{nombre_casa}'")[0][0]
        return id_cuenta_casa
    def cuenta_casa_apostado(nombre_casa):
        #Devuelve el ID de la cuenta de apuestas de una casa a partir del nombre de la casa
        id_cuenta_casa_apostado=make_query(f"SELECT id_cuenta_apostado from casas_apuesta \
                           WHERE nombre='{nombre_casa}'")[0][0]
        return id_cuenta_casa_apostado
    def cuenta_banco_central():
        #Devuelve el ID de la cuenta general central
        id_cuenta_general=make_query(f"SELECT id_cuenta from cuentas \
                           WHERE descripcion='Cuenta_Banco_Central'")[0][0]
        return id_cuenta_general
    def cuenta_banco_beneficios():
        #Devuelve el ID de la cuenta de beneficios
        id_cuenta_general=make_query(f"SELECT id_cuenta from cuentas \
                           WHERE descripcion='Cuenta_Beneficios'")[0][0]
        return id_cuenta_general
    def id_cuenta_casa_apartir_de_idcuenta(id_cuenta):
        #Devuelve el id de la cuenta general de una casa de apuestas a partir del id de la casa
        id_cuenta_casa=make_query(f"SELECT id_cuenta_casa FROM casas_apuesta \
            WHERE id_casa_apuesta={id_cuenta}")[0][0]
        return id_cuenta_casa
    def id_cuenta_casa_apostado_apartir_de_idcuenta(id_cuenta):
        #Devuelve el id de la cuenta de apuestas de una casa de apuestas a partir del id de la casa
        id_cuenta_apostado=make_query(f"SELECT id_cuenta_apostado FROM casas_apuesta \
            WHERE id_casa_apuesta={id_cuenta}")[0][0]
        return id_cuenta_apostado
    

class apuestas:
    """Esta clase se dedica a imputar en la base de datos las apuestas nuevas y las apuestas finalizadas"""
    def __init__(self):
        pass
    def nueva_apuesta(fecha_inversion,fecha_hora_evento,deporte,equipo1,equipo2,casa_apuesta_1,multiplicador_1,inversion_1,casa_apuesta_2,multiplicador_2,inversion_2):
        #Imputación de una nueva apuesta
        id_deporte=extraer_id.deporte(deporte)
        id_casa_apuesta_1=extraer_id.casa_apuesta(casa_apuesta_1)
        id_cuenta_casa1_general=extraer_id.cuenta_casa_no_apostado(casa_apuesta_1)
        id_cuenta_casa1_apostado=extraer_id.cuenta_casa_apostado(casa_apuesta_1)
        id_casa_apuesta_2=extraer_id.casa_apuesta(casa_apuesta_2)
        id_cuenta_casa2_general=extraer_id.cuenta_casa_no_apostado(casa_apuesta_2)
        id_cuenta_casa2_apostado=extraer_id.cuenta_casa_apostado(casa_apuesta_2)
        #Creamos la nueva fila en diario
        make_query(f"INSERT INTO diario (descripcion, fecha) \
                   VALUES ('Nueva_apuesta','{fecha_actual}')")
        id_diario=make_query("SELECT LAST_INSERT_ID() FROM diario AS id_generado LIMIT 1;")[0][0]
        #Creamos las nuevas filas en movimientos
        make_query(f"INSERT INTO movimientos (id_diario, id_cuenta, salida) \
                   VALUES ({id_diario},'{id_cuenta_casa1_general}',{inversion_1})")
        make_query(f"INSERT INTO movimientos (id_diario, id_cuenta, entrada) \
                   VALUES ({id_diario},'{id_cuenta_casa1_apostado}',{inversion_1})")
        make_query(f"INSERT INTO movimientos (id_diario, id_cuenta, salida) \
                    VALUES ({id_diario},'{id_cuenta_casa2_general}',{inversion_2})")
        make_query(f"INSERT INTO movimientos (id_diario, id_cuenta, entrada) \
                   VALUES ({id_diario},'{id_cuenta_casa2_apostado}',{inversion_2})")
        #Insertamos en la tabla de apuestas_individuales la nueva apuesta
        make_query(f"INSERT INTO apuestas_individuales (fecha_inversion, fecha_hora_evento, id_deporte, equipo1, equipo2, id_casa_apuesta_1,multiplicador_1,inversion_1,id_casa_apuesta_2,multiplicador_2,inversion_2)\
        VALUES ('{fecha_inversion}','{fecha_hora_evento}',{id_deporte},'{equipo1}','{equipo2}',{id_casa_apuesta_1},{multiplicador_1},{inversion_1},{id_casa_apuesta_2},{multiplicador_2},{inversion_2});")
        cnx.commit()
        
    def cerrar_apuesta(id_apuesta, casa_ganadora):
        #Cerrar una apuesta que todavía se encuentra abierta
        #Importamos los datos necesarios de la apuesta que queremos cerrar
        datos_apuesta=make_query(f"SELECT id_casa_apuesta_1,multiplicador_1,inversion_1,id_casa_apuesta_2,multiplicador_2,inversion_2 FROM apuestas_individuales \
                                WHERE id_apuesta={id_apuesta}")[0]
        #Sacamos cuales son las cuentas entre las que se va a mover el dinero
        id_cuenta1_general=extraer_id.id_cuenta_casa_apartir_de_idcuenta(datos_apuesta[0])
        id_cuenta1_apostado=extraer_id.id_cuenta_casa_apostado_apartir_de_idcuenta(datos_apuesta[0])
        id_cuenta2_general=extraer_id.id_cuenta_casa_apartir_de_idcuenta(datos_apuesta[3])
        id_cuenta2_apostado=extraer_id.id_cuenta_casa_apostado_apartir_de_idcuenta(datos_apuesta[3])
        id_cuenta_beneficios=extraer_id.cuenta_banco_beneficios()
        #Sacamos el ID de la casa ganadora
        id_casa_ganadora=extraer_id.casa_apuesta(casa_ganadora)
        make_query(f"INSERT INTO diario (descripcion, fecha) \
                   VALUES ('Cierre_apuesta','{fecha_actual}')")
        id_diario=make_query("SELECT LAST_INSERT_ID() FROM diario AS id_generado LIMIT 1;")[0][0]
        #Caso en el que gane la primera casa
        if id_casa_ganadora==datos_apuesta[0]:
            beneficio_obtenido=datos_apuesta[1]*datos_apuesta[2]-(datos_apuesta[2]+datos_apuesta[5])
            make_query(f"INSERT INTO movimientos (id_diario, id_cuenta, salida) \
                    VALUES ({id_diario},'{id_cuenta1_apostado}',{datos_apuesta[2]})")
            make_query(f"INSERT INTO movimientos (id_diario, id_cuenta, salida) \
                    VALUES ({id_diario},'{id_cuenta2_apostado}',{datos_apuesta[5]})")
            make_query(f"INSERT INTO movimientos (id_diario, id_cuenta, salida) \
                        VALUES ({id_diario},'{id_cuenta_beneficios}',{beneficio_obtenido})")
            make_query(f"INSERT INTO movimientos (id_diario, id_cuenta, entrada) \
                    VALUES ({id_diario},'{id_cuenta1_general}',{datos_apuesta[1]*datos_apuesta[2]})")
            make_query(f"UPDATE apuestas_individuales \
                        SET ganador = {id_casa_ganadora}, rentabilidad = {(beneficio_obtenido*100)/(datos_apuesta[2]+datos_apuesta[5])}, beneficio={beneficio_obtenido}\
                        WHERE id_apuesta={id_apuesta};")
        #Caso en el que gane la segunda casa
        elif id_casa_ganadora==datos_apuesta[3]:  
            beneficio_obtenido=datos_apuesta[4]*datos_apuesta[5]-(datos_apuesta[2]+datos_apuesta[5])
            make_query(f"INSERT INTO movimientos (id_diario, id_cuenta, salida) \
                    VALUES ({id_diario},'{id_cuenta1_apostado}',{datos_apuesta[2]})")
            make_query(f"INSERT INTO movimientos (id_diario, id_cuenta, salida) \
                    VALUES ({id_diario},'{id_cuenta2_apostado}',{datos_apuesta[5]})")
            make_query(f"INSERT INTO movimientos (id_diario, id_cuenta, salida) \
                        VALUES ({id_diario},'{id_cuenta_beneficios}',{beneficio_obtenido})")
            make_query(f"INSERT INTO movimientos (id_diario, id_cuenta, entrada) \
                    VALUES ({id_diario},'{id_cuenta2_general}',{datos_apuesta[4]*datos_apuesta[5]})")
            make_query(f"UPDATE apuestas_individuales \
                        SET ganador = {id_casa_ganadora}, rentabilidad = {(beneficio_obtenido*100)/(datos_apuesta[2]+datos_apuesta[5])}, beneficio={beneficio_obtenido}\
                        WHERE id_apuesta={id_apuesta};")
        cnx.commit()


class mover_dinero:
    """Sirve para ejecutar ingresos y retiradas tanto de inversores como de las cuentas de las casas de apuestas"""
    def __init__(self):
        pass
    def ingreso_inversor(inversor, cantidad):
        #Función para ejecutar el ingreso de dinero por parte del inversor
        id_cuenta_inversor=extraer_id.cuenta_inversor(inversor)
        id_cuenta_general=extraer_id.cuenta_banco_central()
        make_query(f"INSERT INTO diario (descripcion, fecha) \
                   VALUES ('Ingreso_inversor','{fecha_actual}')")
        id_diario=make_query("SELECT LAST_INSERT_ID() FROM diario AS id_generado LIMIT 1;")[0][0]
        make_query(f"INSERT INTO movimientos (id_diario, id_cuenta, salida) \
                   VALUES ({id_diario},'{id_cuenta_inversor}',{cantidad})")
        make_query(f"INSERT INTO movimientos (id_diario, id_cuenta, entrada) \
                   VALUES ({id_diario},'{id_cuenta_general}',{cantidad})")
        cnx.commit()
    def retirada_inversor(inversor, cantidad):
        #Función para ejecutar la retirada de dinero por parte del inversor
        id_cuenta_inversor=extraer_id.cuenta_inversor(inversor)
        id_cuenta_general=extraer_id.cuenta_banco_central()
        make_query(f"INSERT INTO diario (descripcion, fecha) \
                   VALUES ('Retirada_inversor','{fecha_actual}')")
        id_diario=make_query("SELECT LAST_INSERT_ID() FROM diario AS id_generado LIMIT 1;")[0][0]
        make_query(f"INSERT INTO movimientos (id_diario, id_cuenta, salida) \
                   VALUES ({id_diario},'{id_cuenta_general}',{cantidad})")
        make_query(f"INSERT INTO movimientos (id_diario, id_cuenta, entrada) \
                   VALUES ({id_diario},'{id_cuenta_inversor}',{cantidad})")
        cnx.commit()
    def ingreso_casa_apuesta(casa_apuesta, cantidad):
        #Función para ejecutar el traspaso de dinero de la cuenta general a una casa de apuestas
        id_cuenta_casa=extraer_id.cuenta_casa_no_apostado(casa_apuesta)
        id_cuenta_general=extraer_id.cuenta_banco_central()
        make_query(f"INSERT INTO diario (descripcion, fecha) \
                   VALUES ('Ingreso_en_casa_apuesta','{fecha_actual}')")
        id_diario=make_query("SELECT LAST_INSERT_ID() FROM diario AS id_generado LIMIT 1;")[0][0]
        make_query(f"INSERT INTO movimientos (id_diario, id_cuenta, salida) \
                   VALUES ({id_diario},'{id_cuenta_general}',{cantidad})")
        make_query(f"INSERT INTO movimientos (id_diario, id_cuenta, entrada) \
                   VALUES ({id_diario},'{id_cuenta_casa}',{cantidad})")
        cnx.commit()
    def retirada_casa_apuesta(casa_apuesta,cantidad):
        #Función para ejecutar el traspaso de dinero de una casa de apuestas a la cuenta general
        id_cuenta_casa=extraer_id.cuenta_casa_no_apostado(casa_apuesta)
        id_cuenta_general=extraer_id.cuenta_banco_central()
        make_query(f"INSERT INTO diario (descripcion, fecha) \
                   VALUES ('Retirada_de_casa_apuesta','{fecha_actual}')")
        id_diario=make_query("SELECT LAST_INSERT_ID() FROM diario AS id_generado LIMIT 1;")[0][0]
        make_query(f"INSERT INTO movimientos (id_diario, id_cuenta, salida) \
                   VALUES ({id_diario},'{id_cuenta_casa}',{cantidad})")
        make_query(f"INSERT INTO movimientos (id_diario, id_cuenta, entrada) \
                   VALUES ({id_diario},'{id_cuenta_general}',{cantidad})")
        cnx.commit()

class metricas:
    """Devuelve métricas concretas de consulta recurrente"""
    def cartera_total_actual():
        #Dinero total en la cartera tanto en casas de puesta como invertido como en general
        cartera=make_query("SELECT ifnull((ifnull(total_entradas,0) - ifnull(total_salidas,0)),0) AS resultado\
                            FROM (\
                            SELECT SUM(ifnull(m.entrada,0)) AS total_entradas, SUM(ifnull(m.salida,0)) AS total_salidas\
                            FROM movimientos AS m\
                            LEFT JOIN cuentas AS c ON m.id_cuenta = c.id_cuenta\
                            LEFT JOIN inversores AS i ON m.id_cuenta = i.id_cuenta\
                            WHERE i.id_inversor IS NULL\
                                AND c.descripcion != 'Cuenta_Beneficios'\
                            ) AS subconsulta;")
        return cartera[0][0]
    def invertido_actual():
        #Dinero que está en las cuentas de inversión ahora mismo
        invertido=make_query("SELECT ifnull(SUM(ifnull(inversion_1,0) + ifnull(inversion_2,0)),0) AS suma_total\
                            FROM apuestas_individuales\
                            WHERE ganador IS NULL;")
        return invertido[0][0]
    def estancado_actual():
        #Dinero actual que no está en inversión (Total de cartera-Invertido)
        estancado=metricas.cartera_total_actual()-metricas.invertido_actual()
        return estancado
    def invertido_hoy_total():
        #Total del dinero que se ha invertido hoy en apuestas
        invertido=make_query("SELECT ifnull(SUM(ifnull(inversion_1,0) + ifnull(inversion_2,0)),0) AS suma_total\
                            FROM apuestas_individuales\
                            WHERE DATE(fecha_hora_evento) = CURDATE();")
        return invertido[0][0]
    def invertido_este_mes_total():
        #Total del dinero que se ha invertido este mes en apuestas
        invertido=make_query("SELECT ifnull(SUM(ifnull(inversion_1,0) + ifnull(inversion_2,0)),0) AS suma_total\
                            FROM apuestas_individuales\
                            WHERE YEAR(fecha_hora_evento) = YEAR(CURDATE()) AND MONTH(fecha_hora_evento) = MONTH(CURDATE());")
        return invertido[0][0]
    def invertido_historico_total():
        #Total del dinero que se ha invertido hoy en apuestas
        invertido=make_query("SELECT ifnull(SUM(ifnull(inversion_1,0) + ifnull(inversion_2,0)),0) AS suma_total\
                            FROM apuestas_individuales;")
        return invertido[0][0]
    def rentabilidad_media_inversionesindividuales_historico():
        #Rentabilidad media de las inversiones individuales históricamente (Rentabilidad de una inversión resprecto a su propia inversión)
        rentabiliad=make_query("SELECT ifnull(AVG(rentabilidad),0) AS rentabiliad_media\
                                FROM apuestas_individuales;")
        return rentabiliad[0][0]
    def rentabilidad_media_inversionesindividuales_este_mes():
        #Rentabilidad media de las inversiones individuales este mes (Rentabilidad de una inversión resprecto a su propia inversión)
        rentabiliad=make_query("SELECT ifnull(AVG(rentabilidad),0) AS rentabiliad_media\
                                FROM apuestas_individuales\
                                WHERE YEAR(fecha_hora_evento) = YEAR(CURDATE()) AND MONTH(fecha_hora_evento) = MONTH(CURDATE());")
        return rentabiliad[0][0]
    def rentabilidad_media_inversionesindividuales_hoy():
        #Rentabilidad media de las inversiones individuales hoy (Rentabilidad de una inversión resprecto a su propia inversión)
        rentabiliad=make_query("SELECT ifnull(AVG(rentabilidad),0) AS rentabiliad_media\
                                FROM apuestas_individuales\
                                WHERE DATE(fecha_hora_evento) = CURDATE();")
        return rentabiliad[0][0]

    def benecifio_hoy_total():
        #Beneficio obtenido hoy en inversiones
        beneficio=make_query("SELECT ifnull(SUM(beneficio),0) AS beneficio_total\
                            FROM apuestas_individuales\
                            WHERE DATE(fecha_hora_evento) = CURDATE();")
        return beneficio[0][0]
    def beneficio_este_mes_total():
        #Beneficio obtenido este mes en inversiones
        beneficio=make_query("SELECT ifnull(SUM(beneficio),0) AS suma_total\
                            FROM apuestas_individuales\
                            WHERE YEAR(fecha_hora_evento) = YEAR(CURDATE()) AND MONTH(fecha_hora_evento) = MONTH(CURDATE());")
        return beneficio[0][0]
    def beneficio_historico_total():
        #Beneficio obtenido históricamente en inversiones
        beneficio=make_query("SELECT ifnull(SUM(beneficio),0) AS suma_total\
                                FROM apuestas_individuales;")
        return beneficio[0][0]
    def cuenta_general():
        cuenta=make_query("SELECT SUM(ifnull(entrada,0))-SUM(ifnull(SALIDA,0)) as cuenta_general FROM movimientos\
                            WHERE id_cuenta=1;")
        return(cuenta)[0][0]

class tablas:
    """Devuelve consultas en mysql en forma de Dataframe"""
    def __init__(self):
        pass
    def apuestas_individuales_todas():
        #Todas las apuestas individuales
        df=make_query_dataframe("SELECT a.id_apuesta, a.fecha_inversion,a.fecha_hora_evento, d.deporte,a.equipo1, a.equipo2,c1.nombre as casa_apuesta_1, a.multiplicador_1, a.inversion_1, c2.nombre as casa_apuesta_2, a.multiplicador_2,a.inversion_2\
                                FROM apuestas_individuales a\
                                LEFT JOIN deportes d ON a.id_deporte=d.id_deporte\
                                LEFT JOIN casas_apuesta AS c1 ON a.id_casa_apuesta_1 = c1.id_casa_apuesta\
                                LEFT JOIN casas_apuesta AS c2 ON a.id_casa_apuesta_2 = c2.id_casa_apuesta;").set_index("id_apuesta")
        return df
    def apuestas_individuales_30():
        #Últimas 30 apuestas individuales
        df=make_query_dataframe("SELECT a.id_apuesta, a.fecha_inversion, a.fecha_hora_evento, d.deporte, a.equipo1, a.equipo2, c1.nombre AS casa_apuesta_1, a.multiplicador_1, a.inversion_1, c2.nombre AS casa_apuesta_2, a.multiplicador_2, a.inversion_2\
                                FROM apuestas_individuales AS a\
                                LEFT JOIN deportes AS d ON a.id_deporte = d.id_deporte\
                                LEFT JOIN casas_apuesta AS c1 ON a.id_casa_apuesta_1 = c1.id_casa_apuesta\
                                LEFT JOIN casas_apuesta AS c2 ON a.id_casa_apuesta_2 = c2.id_casa_apuesta\
                                ORDER BY a.id_apuesta DESC\
                                LIMIT 30;").set_index("id_apuesta")
        return df
    def apuestas_individuales_abiertas():
        #Todas las apuestas individuales que están abiertas
        df=make_query_dataframe("SELECT a.id_apuesta, a.fecha_inversion,a.fecha_hora_evento, d.deporte,a.equipo1, a.equipo2,c1.nombre as casa_apuesta_1, a.multiplicador_1, a.inversion_1, c2.nombre as casa_apuesta_2,a.multiplicador_2,a.inversion_2\
                                FROM apuestas_individuales a\
                                LEFT JOIN deportes d ON a.id_deporte=d.id_deporte\
                                LEFT JOIN casas_apuesta AS c1 ON a.id_casa_apuesta_1 = c1.id_casa_apuesta\
                                LEFT JOIN casas_apuesta AS c2 ON a.id_casa_apuesta_2 = c2.id_casa_apuesta\
                                WHERE ganador IS NULL;").set_index("id_apuesta")
        return df
    def dinero_cuentas_casas_generales():
        #Dinero que hay en cada casa de apuesta sin apostar
        df_generales=make_query_dataframe("SELECT c.nombre, SUM(ifnull(m.entrada,0))-SUM(ifnull(m.salida,0)) AS cuentas_generales\
                    FROM casas_apuesta c\
                    LEFT JOIN movimientos m ON c.id_cuenta_casa = m.id_cuenta\
                    GROUP BY c.id_casa_apuesta, c.nombre, c.id_cuenta_casa;")
        return df_generales
    def dinero_cuentas_casas_apostado():
        #Dinero que hay en cada casa de apuesta apostado
        df_apostado=make_query_dataframe("SELECT c.nombre, SUM(ifnull(m.entrada,0))-SUM(ifnull(m.salida,0)) AS cuentas_apostado\
                        FROM casas_apuesta c\
                        LEFT JOIN movimientos m ON c.id_cuenta_apostado = m.id_cuenta\
                        GROUP BY c.id_casa_apuesta, c.nombre, c.id_cuenta_apostado;")
        return df_apostado
    
class graficas:
    """Devuelve gráficas de plotly con 'return fig'"""
    def __init__(self):
        pass
    def comparacion_inversion_estancado():
        #Gráfico circular comparativo del dinero estancado respecto al invertido
        valores = [metricas.invertido_actual(), metricas.estancado_actual()]  # Valores numéricos
        etiquetas = ['Dinero invertido', 'Dinero estancado']  # Etiquetas correspondientes a los valores
        colores = ['#77dd77', '#FF6961']  # Colores de las etiquetas
        # Crear el gráfico circular
        fig = go.Figure(data=[go.Pie(labels=etiquetas, values=valores, textinfo='label+percent', marker=dict(colors=colores))])
        # Ajustar el diseño del título
        fig.update_layout(
            title={
                'text': 'Estado del dinero en cartera',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'})
        return fig
    def aportaciones_inversores():
        #Aportaciones realizadas por cada inversor (dinero de cada inversor que tenemos en cartera)
        datos=make_query_dataframe("SELECT i.nombre, SUM(ifnull(m.salida,0))-SUM(ifnull(m.entrada,0)) AS aportacion_en_caja\
                FROM inversores i\
                LEFT JOIN movimientos m ON i.id_cuenta = m.id_cuenta\
                GROUP BY i.id_inversor, i.nombre, i.fecha_registro, i.id_cuenta;")
        # Crear el gráfico de barras verticales con Plotly
        fig = px.bar(datos, x='nombre', y='aportacion_en_caja', 
                    labels={'aportacion_en_caja': 'Aportaciones €',"nombre":"Inversores"},
                    title='Aportaciones €')
        # Configurar el estilo del gráfico
        fig.update_layout(
            title={'text': 'Aportaciones actuales de inversores', 'x': 0.5, 'xanchor': 'center'},
            barmode='group',
            uniformtext_minsize=8,
            uniformtext_mode='hide'
        )
        # Asignar un color diferente a cada barra
        fig.update_traces(marker_color=px.colors.qualitative.Set1)
        return fig
    def dinero_en_cuentas_casas_apuesta():
        #Distribución del dinero a lo largo de las casas de apuesta
        df_generales=tablas.dinero_cuentas_casas_generales()
        df_apostado=tablas.dinero_cuentas_casas_apostado()
        # Fusionar los dataframes en uno solo
        df_merged = pd.merge(df_generales, df_apostado, on='nombre')
        # Crear la figura del gráfico de barras
        fig = go.Figure()
        # Agregar las barras de cuentas generales
        fig.add_trace(go.Bar(
            x=df_merged['nombre'],
            y=df_merged['cuentas_generales'],
            name='Dinero sin apostar',
            offsetgroup=0))
        # Agregar las barras de cuentas apostado
        fig.add_trace(go.Bar(
            x=df_merged['nombre'],
            y=df_merged['cuentas_apostado'],
            name='Dinero apostado',
            offsetgroup=1))
        # Configurar el diseño del gráfico
        fig.update_layout(
            barmode='group',
            title={
                'text': 'Distribución del dinero en las casas de apuesta',
                'x': 0.5,
                'xanchor': 'center'
            },
            xaxis_title='Casa de apuesta',
            yaxis_title='Dinero €',)
        return fig

        