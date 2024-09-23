# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ClientesTM(Document):
	pass


# Definiendo la busqueda de los municipios de la provincia
@frappe.whitelist()
def obtener_municipios(provincia):
    return frappe.get_all(
        'NomMunicipios',
        filters={'provcod': provincia},
        fields=['municcod', 'municnombre']
    )