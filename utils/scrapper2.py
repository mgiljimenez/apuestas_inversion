#Importacion de librerias
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime

class busqueda_inversion():
    """Clase con la que se realiza el webscrapping y se encuentran las posibles inversiones, su inversion y rentabilidad"""
    def __init__(self):
        pass
    # Importamos todo el código DOM de la web de EEUU
    def descargar_datos_partidos(url):
        """Abrimos la web por la región de EEUU y descargamos el html
        return: código con las 2 "div" donde se encuentran todos los datos"""
        configuration_driver = webdriver.ChromeOptions()
        configuration_driver.add_argument('--headless')
        driver = webdriver.Chrome(options=configuration_driver)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        driver.close()
        #Extraemos los dos bloques div que contienen las dos tablas a explorar y las guardamos en tabla1 y tabla2
        return(soup)