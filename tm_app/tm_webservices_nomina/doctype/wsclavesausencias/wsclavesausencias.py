# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WSClavesAusencias(Document):
    pass


@frappe.whitelist()
def inserta_actualiza_clavesausencias(cause_id, cause_codigo, cause_descripcion):

    # Validar que los valores no estén vacíos
    if not cause_id:
        return {"message": "El CAuseId no puede estar vacío."}
    if not cause_codigo:
        return {"message": "El CAuseCodigo no puede estar vacío."}
    if not cause_descripcion:
        return {"message": "La CAuseDescripcion no puede estar vacío."}

    try:
        # verificando si ya existe
        existe_cause = frappe.db.exists(
            "WSClavesAusencias", {"CAuseId": cause_id})

        if existe_cause:
            # actualizar el registro
            doc = frappe.get_doc("WSClavesAusencias", existe_cause)
            doc.causecodigo = cause_codigo
            doc.causedescripcion = cause_descripcion
            doc.save()
            return {"success": True, "message": f"CAuse con CAuseId {cause_id} actualizado"}
        else:
            # insertar nuevo registro
            new_doc = frappe.get_doc({
                "doctype": "WSClavesAusencias",
                "causeid": cause_id,
                "causecodigo": cause_codigo,
                "causedescripcion": cause_descripcion
            })
            new_doc.insert()
            return {"success": True, "message": f"CAuse con CAuseId {cause_id} - {cause_descripcion} insertado"}
    except frappe.exceptions.ValidationError as e:
        return {"message": f"Error al insertar o actualizar: {str(e)}"}
