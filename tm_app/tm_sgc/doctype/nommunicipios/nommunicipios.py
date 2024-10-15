# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class NomMunicipios(Document):
    pass


@frappe.whitelist()
def inserta_actualiza_municipios(dato_provcod, dato_municnombre, dato_municcod):

    try:
        # verificando si ya existe
        existe_municipio = frappe.db.exists(
            "NomMunicipios", {"provdoc": dato_provcod, "municcod": dato_municcod})

        print(
            f"[Resultado] existe_municipio: {existe_municipio} | [Codigo Provincia]: {dato_provcod} | [Codigo Municipio]: {dato_municcod}")

        if existe_municipio:
            # actualizar el registro
            doc = frappe.get_doc("NomMunicipios", existe_municipio)
            doc.municnombre = dato_municnombre
            doc.save()
            return {"success": True, "message": f"Provincia {dato_provcod} Municipio {dato_municcod} - {dato_municnombre} actualizado"}
        else:
            # insertar nuevo registro
            new_doc = frappe.get_doc({
                "doctype": "NomMunicipios",
                "provcod": dato_provcod,
                "municnombre": dato_municnombre,
                "municcod": dato_municcod
            })
            new_doc.insert()
            return {"success": True, "message": f"insertado {dato_municnombre} - {dato_provcod} - {dato_municcod}"}
    except frappe.exceptions.ValidationError as e:
        return {"message": f"Error al insertar o actualizar: {dato_municnombre} con {dato_provcod} - {dato_municcod}, {str(e)}"}
