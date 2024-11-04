import frappe
import requests
import json


@frappe.whitelist()
def sync_webservice(doctype):
    """ 
    Sincronizando los datos del webservice en los doctypes correspondientes 

    args:
        doctype (str): Nombre del doctype a sincronizar

    returns:
        dict: Datos del doctype en formato diccionario
    """

    # Configurando la url del webservice
    webservice_url = " http: // 172.18.204.41/WS_AF_TM/APINomina/{}"

    url = webservice_url.format(doctype)

    Hacer la solicitud HTTP al webservice
    response = frappe.request.get(url)

    verficar si la solicitud fue exitosa
    if response.status_code == 200:
        # obtener el JSON
        data = json.loads(response.text)
        return data
    else:
        # Manejando el error
        frappe.throw("Error, al obtener los datos del Doctype {}:{}".format(
            doctype, response.status_code))

    # webservice_url = "/home/niurka/Proyectos/frappe/webservice-json/{}.json"
    # url = webservice_url.format(doctype)

    # leer el archivo json localmente
    with open(url, 'r') as file:
        data = json.load(file)

    return data
