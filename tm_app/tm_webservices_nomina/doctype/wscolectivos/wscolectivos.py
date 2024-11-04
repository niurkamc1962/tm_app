# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WSColectivos(Document):
    pass


@frappe.whitelist()
def inserta_actualiza_colectivos(colec_id, colec_codigo, colec_descripcion):

    # Validar que los valores no estén vacíos
    if not colec_id:
        return {"message": "El ColecId no puede estar vacío."}
    if not colec_codigo:
        return {"message": "El ColecCodigo no puede estar vacío."}
    if not colec_descripcion:
        return {"message": "La ColecDescripcion no puede estar vacía."}

    try:
        # verificando si ya existe
        existe_colectivo = frappe.db.exists("WSCargos", {"ColecId": colec_id})

        if existe_colectivo:
            # actualizar el registro
            doc = frappe.get_doc("WSColectivos", existe_colectivo)
            doc.coleccodigo = colec_codigo
            doc.colecdescripcion = colec_descripcion
            doc.save()
            return {"success": True, "message": f"Colectivo con ColecId {colec_id} actualizado"}
        else:
            # insertar nuevo registro
            new_doc = frappe.get_doc({
                "doctype": "WSColectivos",
                "colecid": colec_id,
                "coleccodigo": colec_codigo,
                "colecdescripcion": colec_descripcion
            })
            new_doc.insert()
            return {"success": True, "message": f"Colectivo con ColecId {colec_id} - {colec_descripcion} insertado"}
    except frappe.exceptions.ValidationError as e:
        return {"message": f"Error al insertar o actualizar: {str(e)}"}
