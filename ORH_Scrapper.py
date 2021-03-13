import requests
import urllib.request
import time
from bs4 import BeautifulSoup
url = 'https://orh.ucr.ac.cr/ofertas-laborales/puestos-vacantes/concursos-externos/' #link de concursos externos UCR
response = requests.get(url) #Se obtiene el codigo HTML de la pagina
soup = BeautifulSoup(response.text, "html.parser") # se convierte en un objeto bs4 para facilidad de analisis

def buscar_ofertas_laborales_default():
    oferta_encontrada=False
    ofertas_totales=[]
    for one_a_tag in soup.findAll('a'):  #'a' = tags para links
        oferta_actual=[]
        if "https://orh.ucr.ac.cr/wp-content/plugins/ORH-UCR-Plugin/downloader.php?" in str(one_a_tag):#link usado en la ORH para descarga de PDF
            if "Informática".lower() in str(one_a_tag).lower() or "Computación".lower() in str(one_a_tag).lower():#Se filtran las palabras deseadas
                oferta_encontrada=True
                #se guarda la informacion necesaria siguiendo el orden del HTML analizado
                informacion_oferta="Se encontro oferta: "+one_a_tag.text
                informacion_area="Area: "+one_a_tag.findNext('td').text
                informacion_jornada="Jornada: "+one_a_tag.findNext('td').findNext('td').text
                informacion_fecha="Fecha Valida: "+one_a_tag.findNext('td').findNext('td').findNext('td').text
                informacion_link = one_a_tag['href']
                oferta_actual.append(informacion_oferta)
                oferta_actual.append(informacion_area)
                oferta_actual.append(informacion_jornada)
                oferta_actual.append(informacion_fecha)
                oferta_actual.append(informacion_link)
                ofertas_totales.append(oferta_actual)             
    if oferta_encontrada==False:
        return False
    return ofertas_totales

def buscar_ofertas_laborales(oferta_deseada):
    oferta_encontrada=False
    ofertas_totales=[]
    for one_a_tag in soup.findAll('a'):  #'a' = tags para links
        oferta_actual=[]
        if "https://orh.ucr.ac.cr/wp-content/plugins/ORH-UCR-Plugin/downloader.php?" in str(one_a_tag):#link usado en la ORH para descarga de PDF
            if oferta_deseada.lower() in str(one_a_tag).lower():#Se filtran las palabras deseadas
                oferta_encontrada=True
                #se guarda la informacion necesaria siguiendo el orden del HTML analizado
                informacion_oferta="Se encontro oferta: "+one_a_tag.text
                informacion_area="Area: "+one_a_tag.findNext('td').text
                informacion_jornada="Jornada: "+one_a_tag.findNext('td').findNext('td').text
                informacion_fecha="Fecha Valida: "+one_a_tag.findNext('td').findNext('td').findNext('td').text
                informacion_link = one_a_tag['href']
                oferta_actual.append(informacion_oferta)
                oferta_actual.append(informacion_area)
                oferta_actual.append(informacion_jornada)
                oferta_actual.append(informacion_fecha)
                oferta_actual.append(informacion_link)
                ofertas_totales.append(oferta_actual)             
    if oferta_encontrada==False:
        return False
    return ofertas_totales





import kivy
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView


class MainWindow(Screen):
    search_input=ObjectProperty(None)
    def set_text(self):
        texto_encontrado="[b]"
        if buscar_ofertas_laborales(self.search_input.text)!=False:
            for ofertas in buscar_ofertas_laborales(self.search_input.text):
                texto_encontrado+=ofertas[0]+"\n"+ofertas[1]+"\n"+ofertas[2]+"\n"+ofertas[3]+"\n"+'[color=0000A0][u][ref='+ofertas[4]+']Informacion PDF[/ref][/u][/color]'+"\n\n\n" 
            texto_encontrado+="[/b]"               
            self.manager.get_screen('second').change_text(texto_encontrado)
        else:
            texto_encontrado="[b]No se encontró ninguna oferta.[/b]"
            self.manager.get_screen('second').change_text(texto_encontrado)
            
    
class SecondWindow(Screen):
    text_found=ObjectProperty(None)
    def change_text(self,texto_encontrado):
        self.text_found.text=texto_encontrado
    

class WindowManager(ScreenManager):
    pass


kv= Builder.load_file("orhscrapper.kv")


class ORHScrapper(App):
    def build(self):
        return kv

if __name__=="__main__":
    ORHScrapper().run()







