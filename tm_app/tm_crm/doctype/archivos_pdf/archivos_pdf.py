# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import os
# import pdfplumber

class ArchivosPDF(Document):
	pass


@frappe.whitelist()
def eliminar_archivo_pdf(archivo_id):
    # Obteniendo el archivo pdf
    archivo_doc = frappe.get_doc('Archivos PDF', archivo_id)
    
    # Preguntando si es privado o public para eliminar segun la ruta
    if archivo_doc.is_private:
        ruta_archivo = '/sites/tmtest.local/private/files/' + archivo_doc.archivo_pdf
    else:
        ruta_archivo = '/sites/tmtest.local/public/files/' + archivo_doc.archivo_pdf
    
    # Verificando si el archivo existe antes de intentar elimiinarlo
    if os.path.exists(ruta_archivo):
        os.remove(ruta_archivo)
    
    # Eliminar el documento del doctype
    archivo_doc.delete()
    
    return True


@frappe.whitelist()
def procesar_archivo_pdf(archivo_id):
    # Obtener el archivo específico por su ID
    archivo = frappe.get_doc('Archivos PDF', archivo_id)
    
    if archivo.estado != 'Pendiente':
        frappe.throw("El archivo ya ha sido procesado o no está en estado pendiente.")
    
    # Extraer datos del PDF
    datos = extraer_datos_pdf(archivo.ruta_archivo)
    print ('datos: ',datos)
    
    # Guardar datos en el DocType 'Clientes TM'
    cliente = frappe.get_doc({
        'doctype': 'Clientes TM',
        'fecha': datos['Fecha'],
        'nuevo_cliente': datos['Nuevo Cliente'],
        'codigo_registro_comercial': datos['Código Registro Comercial'],
        'reeup_o_ci': datos['REEUP o CI'],
        'empresa_estatal': datos['Empresa Estatal'],
        'organismo': datos['Organismo']
    })
    
    cliente.insert()
    
    # Actualizar estado del archivo a 'Procesado'
    frappe.db.set_value('Archivos PDF', archivo.name, 'estado', 'Procesado')


def extraer_datos_pdf(ruta_pdf):
    campos = {
        "Fecha": None,
        "Nuevo Cliente": None,
        "Código Registro Comercial": None,
        "REEUP o CI": None,
        "Empresa Estatal": None,
        "Organismo": None
    }
    
    with pdfplumber.open(ruta_pdf) as pdf:
        pagina = pdf.pages[0]
        texto = pagina.extract_text()
        lineas = texto.split('\n')
        
        for i in range(len(lineas)):
            if lineas[i] in campos:
                campos[lineas[i]] = lineas[i + 1].strip()

    return campos