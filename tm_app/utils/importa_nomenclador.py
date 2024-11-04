import frappe
import requests
import json
import os


@frappe.whitelist()
def import_nomenclador(doctype):
    """ 
    Importa datos Json segun fichero especificado

    args:
        doctype (str): Nombre del doctype a importar

    returns:
        dict: Datos del doctype en formato diccionario
    """

    # webservice_url = "/home/niurka/Proyectos/frappe/nomencladores-json/{}.json"
    # url = webservice_url.format(doctype)

    # # leer el archivo json localmente
    # with open(url, 'r') as file:
    #     data = json.load(file)
    
    # Obtener el directorio de la aplicación tm_app
    app_dir = os.path.join(frappe.get_app_path('tm_app'), 'archivos-json-a-importar')
    json_file_path = os.path.join(app_dir, f"{doctype}.json")

    # leer el archivo json 
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    return data
