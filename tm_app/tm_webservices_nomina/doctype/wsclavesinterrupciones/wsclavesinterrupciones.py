# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WSClavesInterrupciones(Document):
    pass


@frappe.whitelist()
def inserta_actualiza_clavesinterrupciones(inter_id, inter_codigo, inter_descripcion):

    try:
        # verificando si ya existe
        existe_claveinterrupcion = frappe.db.exists(
            "WSClavesInterrupciones", {"InterId": inter_id})

        if existe_claveinterrupcion:
            # actualizar el registro
            doc = frappe.get_doc("WSClavesInterrupciones",
                                 existe_claveinterrupcion)
            doc.intercoodigo = inter_codigo
            doc.interdescripcion = inter_descripcion
            doc.save()
            return {"success": True, "message": f"Clave Interrupcion con InterId {inter_id} actualizado"}
        else:
            # insertar nuevo registro
            new_doc = frappe.get_doc({
                "doctype": "WSClavesInterrupciones",
                "interid": inter_id,
                "intercodigo": inter_codigo,
                "interdescripcion": inter_descripcion
            })
            new_doc.insert()
            return {"success": True, "message": f"Clave Interrupcion con InterId {inter_id} - {inter_descripcion} insertado"}
    except frappe.exceptions.ValidationError as e:
        return {"message": f"Error al insertar o actualizar: {str(e)}"}
