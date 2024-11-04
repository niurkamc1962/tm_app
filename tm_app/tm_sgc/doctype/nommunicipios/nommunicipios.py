# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class NomMunicipios(Document):
    pass


@frappe.whitelist()
def inserta_actualiza_municipios(dato_provcod, dato_municnombre, dato_municcod):

    try:
        # Obteniendo el id de la provincia en el documento padre NomProvincia
        parent_provincia = frappe.db.get_value("NomProvincias", {"provcod": dato_provcod}, "name")
        
        if not parent_provincia:
            return {"success": False, "message": f"No se encontro la provincia con el codigo {dato_provcod}"}
        
        # verificando si ya existe
        existe_municipio = frappe.db.exists(
            "NomMunicipios", {"provcod": dato_provcod, "municcod": dato_municcod})

        print(
            f"[Resultado] existe_municipio: {existe_municipio} | [Codigo Provincia]: {dato_provcod} | [Codigo Municipio]: {dato_municcod}")

        if existe_municipio:
            # actualizar el registro
            doc = frappe.get_doc("NomMunicipios", existe_municipio)
            doc.municnombre = dato_municnombre
            doc.save()
            return {"success": True, "message": f"Provincia {dato_provcod} Municipio {dato_municcod} - {dato_municnombre} actualizado"}
        else:
            # insertar nuevo registro en NomMunicpios teniendo en cuenta el doctype padre NomProvincias
            new_doc = frappe.get_doc({
                "doctype": "NomMunicipios",
                "provcod": dato_provcod,
                "municnombre": dato_municnombre,
                "municcod": dato_municcod,
                "parent": parent_provincia,     # id del documento padre al que esta asociado el municipio
                "parenttype": "NomProvincias",  # documento padre
                "parentfield": "municipios"     # nombre del campo en el doctype padre que referencia al child
            })
            new_doc.insert()
            return {"success": True, "message": f"Municipio Insertado {dato_municnombre} - {dato_provcod} - {dato_municcod}"}
        
    except frappe.exceptions.ValidationError as e:
        return {"message": f"Error al insertar o actualizar: {dato_municnombre} con {dato_provcod} - {dato_municcod}, {str(e)}"}
