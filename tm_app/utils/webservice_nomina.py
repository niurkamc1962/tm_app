import frappe
import requests
import json
import os

@frappe.whitelist()
def sync_webservice(doctype):
    """ 
    Sincronizando los datos del webservice en los doctypes correspondientes 

    args:
        doctype (str): Nombre del doctype a sincronizar

    returns:
        dict: Datos del doctype en formato diccionario
    """

    # #Configurando la url del webservice
    # webservice_url = "http://172.18.204.41/WS_AF_TM/APINomina/{}"
    # url = webservice_url.format(doctype)

    # try:
    #     # Hacer la solicitud HTTP al webservice
    #     response = frappe.request.get(url)

    #     # Verficar si la solicitud fue exitosa
    #     if response.status_code == 200:
    #         # obtener el JSON directamente desde la respuesta
    #         data = json.loads(response.text)
    #         # Imprimir el Json En la consola
    #         print(json.dumps(data, indent=4))
            
    #         return data
    #     else:
    #         # Manejando el error
    #         frappe.throw("Error, al obtener los datos del Doctype {}:{}".format(
    #             doctype, response.status_code))
            
    # except requests.exception.ResquestException as e:
    #     # Manejo de excepciones en caso de fallo en la solicitud
    #     frappe.throw("Error al realizar la solicitud: {}".format(str(e)))
        

    # webservice_url = "/home/niurka/Proyectos/frappe/nomencladores-json/webservice-json/{}.json"
    # url = webservice_url.format(doctype)
    app_dir = os.path.join(frappe.get_app_path('tm_app'), 'archivos-json-a-importar/webservice-json/')
    json_file_path = os.path.join(app_dir, f"{doctype}.json")


    # leer el archivo json localmente
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    return data
