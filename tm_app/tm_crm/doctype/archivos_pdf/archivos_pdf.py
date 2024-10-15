# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import pdfplumber


class ArchivosPDF(Document):
    pass


@frappe.whitelist()
def procesar_archivos_pdf(archivo_id):
    # obteniendo el archivo especifico por su ID
    archivo = frappe.get_doc("Archivos PDF", archivo_id)
    if archivo.estado != "Pendiente":
        frappe.throw("El archivo ya fue procesado o su estado no es pendiente")

    # Estrayendo datos del archivo pdf
    datos = extraer_datos_pdf(archivo.ruta_archivo)

    # Guardando en el doctype Clientes TM
    cliente = frappe.get_doc({ 
        "doctype": "Clientes TM",
        "fecha": datos["Fecha"],
        "reeup_o_ci": datos["REEUP"],
        "codigo_nit": datos["Código NIT"],
        "cod_registro_comercial": datos["Codigo Registro Comercial"],
        "organismo": datos["Organismo"],
        "uniones": datos["OSDE"]
    })
    cliente.insert()
    
    # Cambiando esta a Procesado
    frappe.db.set_value('Archivos PDF', archivo.name, 'estado': 'Procesado')



def extraer_datos_pdf(ruta_archivo_pdf):
    # definiendo diccionario con los campos del doctype Clientes TM
    campos = {
        "Fecha": None,
        "Nuevo Cliente": None,
        "Codigo Registro Comercial": None,
        "REEUP": None,
        "Empresa Estatal": None,
        "Empresa No Estatal": None,
        "Organismo": None,
        "OSDE": None,
        "Código NIT": None,
        "Nombre": None,
        "Dirección": None,
        "Provincia": None,
        "Municipio": None,
        "Email": None,
    }

    with pdfplumber.open(ruta_pdf) as pdf:
        pagina = pdf.pages[0]
        texto = pagina.extract_text()
        lineas = texto.split("\n")
        for i in range(len(lineas)):
            if lineas[i] in campos:
                campos[lineas[i]] = lineas[i + 1].strip()
    return campos
