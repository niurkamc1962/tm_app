import os
import json
import frappe
from frappe import _

@frappe.whitelist()
def import_nomencladores(doctype_a, doctype_b):
    """
    Importa datos de múltiples archivos JSON según doctypes especificados.
    
    args:
        doctype_a (str): Nombre del primer doctype a importar.
        doctype_b (str): Nombre del segundo doctype a importar.

    returns:
        dict: Retorna diccionario con los datos de cada doctype.
    """
    
    print(f"Entré en import_nomencladores con doctype_a: {doctype_a} y doctype_b: {doctype_b}")
    
    data = {
        "doctype_a": [],
        "doctype_b": []
    }

    # Obtener el directorio de la aplicación tm_app
    app_dir = os.path.join(frappe.get_app_path("tm_app"), "archivos-json-a-importar")

    doctype_a_json_file_path = os.path.join(app_dir, f"{doctype_a}.json")
    doctype_b_json_file_path = os.path.join(app_dir, f"{doctype_b}.json")

    try:
        # Leer el archivo doctype_a JSON
        if os.path.exists(doctype_a_json_file_path):
            with open(doctype_a_json_file_path, "r") as file:
                dataA = json.load(file)
            if doctype_a in dataA and isinstance(dataA[doctype_a], list):
                data["doctype_a"] = dataA[doctype_a]
            else:
                raise ValueError(f"El contenido de {doctype_a}.json no es una lista")
        else:
            raise FileNotFoundError(f"El archivo {doctype_a}.json no existe en {app_dir}")

        # Leer el archivo doctype_b JSON
        if os.path.exists(doctype_b_json_file_path):
            with open(doctype_b_json_file_path, "r") as file:
                dataB = json.load(file)
            if doctype_b in dataB and isinstance(dataB[doctype_b], list):
                data["doctype_b"] = dataB[doctype_b]
            else:
                raise ValueError(f"El contenido de {doctype_b}.json no es una lista")
        else:
            raise FileNotFoundError(f"El archivo {doctype_b}.json no existe en {app_dir}")

        return data

    except Exception as e:
        print(f"Error al importar nomencladores: {str(e)}")
        frappe.throw(_("Error al importar nomencladores: {0}").format(str(e)))