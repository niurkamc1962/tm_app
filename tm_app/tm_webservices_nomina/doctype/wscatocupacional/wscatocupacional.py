# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WSCatOcupacional(Document):
    pass


@frappe.whitelist()
def inserta_actualiza_catocupacional(categ_id, categ_codigo, categ_descripcion):

    try:
        # verificando si ya existe
        existe_categocupacional = frappe.db.exists(
            "WSCatOcupacional", {"categid": categ_id})

        if existe_categocupacional:
            # actualizar el registro
            doc = frappe.get_doc("WSCatOcupacional", existe_categocupacional)
            doc.categocodigo = categ_codigo
            doc.categodescripcion = categ_descripcion
            doc.save()
            return {"success": True, "message": f"Categoria con CategId {categ_id} actualizado"}
        else:
            # insertar nuevo registro
            new_doc = frappe.get_doc({
                "doctype": "WSCatOcupacional",
                "categid": categ_id,
                "categocodigo": categ_codigo,
                "categodescripcion": categ_descripcion
            })
            new_doc.insert()
            return {"success": True, "message": f"Categoria Ocupacional con CategId {categ_id} - {categ_descripcion} insertado"}
    except frappe.exceptions.ValidationError as e:
        return {"message": f"Error al insertar o actualizar: {str(e)}"}
