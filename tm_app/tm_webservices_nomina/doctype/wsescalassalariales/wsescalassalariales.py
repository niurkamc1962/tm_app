# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WSEscalasSalariales(Document):
    pass


@frappe.whitelist()
def inserta_actualiza_escalassalariales(escs_id, escs_codigo, escs_descripcion):

    # Validar que los valores no estén vacíos
    if not escs_id:
        return {"message": "El EscSId no puede estar vacío."}
    if not escs_codigo:
        return {"message": "El EscSCodigo no puede estar vacío."}
    if not escs_descripcion:
        return {"message": "La EscSDescripcion no puede estar vacía."}

    try:
        # verificando si ya existe
        existe_escalasalarial = frappe.db.exists(
            "WSEscalasSalariales", {"EscSId": escs_id})

        if existe_escalasalarial:
            # actualizar el registro
            doc = frappe.get_doc("WSEscalasSalariales", existe_escalasalarial)
            doc.escscodigo = escs_codigo
            doc.escsdescripcion = escs_descripcion
            doc.save()
            return {"success": True, "message": f"Escala Salarial con EscSId {escs_id} actualizado"}
        else:
            # insertar nuevo registro
            new_doc = frappe.get_doc({
                "doctype": "WSEscalasSalariales",
                "escsid": escs_id,
                "escscodigo": escs_codigo,
                "escsdescripcion": escs_descripcion
            })
            new_doc.insert()
            return {"success": True, "message": f"Escala Salarial con EscSId {escs_id} - {escs_descripcion} insertado"}
    except frappe.exceptions.ValidationError as e:
        return {"message": f"Error al insertar o actualizar: {str(e)}"}
