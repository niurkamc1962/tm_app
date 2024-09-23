# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WSCargos(Document):
    pass


@frappe.whitelist()
def inserta_actualiza_cargos(carg_id, carg_codigo, carg_descripcion):

    # Validar que los valores no estén vacíos
    if not carg_id:
        return {"message": "El CargId no puede estar vacío."}
    if not carg_codigo:
        return {"message": "El CargCodigo no puede estar vacío."}
    if not carg_descripcion:
        return {"message": "La CargDescripcion no puede estar vacía."}

    try:
        # verificando si ya existe
        existe_cargo = frappe.db.exists("WSCargos", {"CargId": carg_id})

        if existe_cargo:
            # actualizar el registro
            doc = frappe.get_doc("WSCargos", existe_cargo)
            doc.cargcodigo = carg_codigo
            doc.cargdescripcion = carg_descripcion
            doc.save()
            return {"success": True, "message": f"Cargo con CargId {carg_id} actualizado"}
        else:
            # insertar nuevo registro
            new_doc = frappe.get_doc({
                "doctype": "WSCargos",
                "cargid": carg_id,
                "cargcodigo": carg_codigo,
                "cargdescripcion": carg_descripcion
            })
            new_doc.insert()
            return {"success": True, "message": f"Cargo con CargId {carg_id} - {carg_descripcion} insertado"}
    except frappe.exceptions.ValidationError as e:
        return {"message": f"Error al insertar o actualizar: {str(e)}"}
