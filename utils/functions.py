#Importacion de librerias
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime

"""Importante: Además de este código se hizo webscrapping de https://es.surebet.com/surebets
Aquí se encontraban oportunidades con una mucha mayor rentabilidad. No se publica aquí el código por política de privacidad de la web.
Para más detalles puede contactar el desarrollador"""


class busqueda_inversion():
    """Clase con la que se realiza el webscrapping y se encuentran las posibles inversiones, su inversion y rentabilidad"""
    def __init__(self):
        pass
    def apuesta(X1, X2):
        try:
            if 1/(X2-1)<=X1-1:
                print(f"Combinacion encontrada: {X1},{X2}")
                return(True)
            else:
                return(False)
        except:
            return(False)
    # Importamos todo el código DOM de la web
    def descargar_datos_partidos(url):
        configuration_driver = webdriver.ChromeOptions()
        configuration_driver.add_argument('--headless')
        driver = webdriver.Chrome(options=configuration_driver)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        driver.close()
        return(soup)
    def optimizacion_streamlit(inversion, mul1, mul2):
        pendiente_media=(mul1-1+(1/(mul2-1)))/2
        x=inversion/(pendiente_media+1)
        y=(inversion*pendiente_media)/(pendiente_media+1)
        rentabilidad1=((mul1*x*100)/inversion)-100
        rentabilidad2=((mul2*y*100)/inversion)-100
        return(x,y,rentabilidad1, rentabilidad2)
    def sporty_trader_streamlit(inversion, url):
        soup=busqueda_inversion.descargar_datos_partidos(url)
        eventos=soup.find_all("div", class_="cursor-pointer border rounded-md mb-4 px-1 py-2 flex flex-col lg:flex-row relative")
        fecha = datetime.datetime.now()
        fecha_formateada = fecha.strftime("%d/%m/%Y %H:%M")
        print(f"Nueva actualizacion {fecha_formateada}")
        print("------------------------------------")
        eventos_total={}
        num=0
        for evento in eventos:
            multiplicadores=evento.find_all("span", class_="px-1 h-booklogosm font-bold bg-primary-yellow text-white leading-8 rounded-r-md w-14 md:w-18 flex justify-center items-center text-base")
            multiplicadores[0].text
            multiplicadores[1].text
            valores_encontrados=busqueda_inversion.apuesta(float(multiplicadores[0].text),float(multiplicadores[1].text))
            if valores_encontrados==True:
                fecha=eventos[eventos.index(evento)].find("span", class_="text-sm text-gray-600 w-full lg:w-1/2 text-center dark:text-white").text
                evento_name=eventos[eventos.index(evento)].find("span", class_="font-medium w-full lg:w-1/2 text-center dark:text-white").text.replace("\n","")
                enlace=eventos[eventos.index(evento)].find("span", class_="font-medium w-full lg:w-1/2 text-center dark:text-white").find("a")["href"]
                enlace = enlace.split('/')[-2:]
                enlace = "https://www.sportytrader.es/cuotas/"+'/'.join(enlace)
                casas_apuestas=eventos[eventos.index(evento)].find_all("img", class_="booklogo")
                casa1=casas_apuestas[0]["alt"]
                casa2=casas_apuestas[1]["alt"]
                optimizado=busqueda_inversion.optimizacion_streamlit(inversion, float(multiplicadores[0].text), float(multiplicadores[1].text))
                eventos_total[num]=[fecha, evento_name, enlace, casa1, casa2, multiplicadores[0].text,multiplicadores[1].text,inversion,optimizado[0],optimizado[1],optimizado[2], optimizado[3]]
                num+=1
        return(eventos_total)
    

class comprobar_inversion:
    """Esta clase servirá para facilitar la comprobación de una inverión (ayuda a la inversión)"""
    def __init__(self):
        pass
    def rentabilidad(mul1,mul2,inversion=100):
        #Comprobar la rentabilidad de una inversión sin saber una de sus inversiones
        if busqueda_inversion.apuesta(mul1,mul2)==True:
            resultado=busqueda_inversion.optimizacion_streamlit(inversion,mul1,mul2)
            return resultado
        else:
            return False
    def comprobar(mul1, mul2, inversion1, inversion2):
        #Comprobar la rentabilidad final aportando datos de multiplicadores e inversiones
        inversion_total=inversion1+inversion2
        if mul1*inversion1>= inversion_total and mul2*inversion2>=inversion_total:
            beneficio1=(mul1*inversion1)-inversion_total
            beneficio2=(mul2*inversion2)-inversion_total
            rentabilidad1=beneficio1*100/inversion_total
            rentabilidad2=beneficio2*100/inversion_total
            return (beneficio1,rentabilidad1,beneficio2,rentabilidad2)            
        else:
            return False
    def relacion_inversion(mul1, inv1, mul2):
        #Dando los multiplicadores y una de las inversiones, encontrar la segunda inversion optima
        relacion_inversion_100=comprobar_inversion.rentabilidad(mul1,mul2)
        inv2=(relacion_inversion_100[1]*inv1)/relacion_inversion_100[0]
        comprobacion=comprobar_inversion.comprobar(mul1,mul2,inv1,inv2)
        return(comprobacion,inv2)
