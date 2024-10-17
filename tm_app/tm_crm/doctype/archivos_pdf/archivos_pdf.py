# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import os


class ArchivosPDF(Document):
	pass


@frappe.whitelist()
def eliminar_archivo_pdf(archivo_id):
    # Obteniendo el archivo pdf
    archivo_doc = frappe.get_doc('Archivos PDF', archivo_id)
    
    # Preguntando si es privado o public para eliminar segun la ruta
    if archivo_doc.is_private:
        ruta_artivo = '/sites/tecnomatica.local/private/files/' + archivo_doc.archivo_pdf
    else:
        ruta_artivo = '/sites/tecnomatica.local/public/files/' + archivo_doc.archivo_pdf
    
    # Verificando si el archivo existe antes de intentar elimiinarlo
    if os.path.exists(ruta_artivo):
        os.remove(ruta_artivo)
    
    # Eliminar el documento del doctype
    archivo_doc.delete()
    
    return True