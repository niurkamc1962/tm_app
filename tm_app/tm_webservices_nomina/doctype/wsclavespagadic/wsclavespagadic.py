# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WSClavesPagAdic(Document):
    pass


@frappe.whitelist()
def inserta_actualiza_clavespagadic(pagadic_id, pagadic_codigo, pagadic_descripcion):

    # Validar que los valores no estén vacíos
    if not pagadic_id:
        return {"message": "El PagAdicId no puede estar vacío."}
    if not pagadic_codigo:
        return {"message": "El PagAdicCodigo no puede estar vacío."}
    if not pagadic_descripcion:
        return {"message": "La PagAdicDescripcion no puede estar vacía."}

    try:
        # verificando si ya existe
        existe_pagadic = frappe.db.exists(
            "WSClavesPagAdic", {"PagAdicId": pagadic_id})

        if existe_pagadic:
            # actualizar el registro
            doc = frappe.get_doc("WSClavesPagAdic", existe_pagadic)
            doc.pagadiccodigo = pagadic_codigo
            doc.pagadicdescripcion = pagadic_descripcion
            doc.save()
            return {"success": True, "message": f"PagaAdic con PagAdicId {pagadic_id} actualizado"}
        else:
            # insertar nuevo registro
            new_doc = frappe.get_doc({
                "doctype": "WSClavesPagAdic",
                "pagadicid": pagadic_id,
                "pagadiccodigo": pagadic_codigo,
                "pagadicdescripcion": pagadic_descripcion
            })
            new_doc.insert()
            return {"success": True, "message": f"PagAdic con PagAdicId {pagadic_id} - {pagadic_descripcion} insertado"}
    except frappe.exceptions.ValidationError as e:
        return {"message": f"Error al insertar o actualizar: {str(e)}"}
