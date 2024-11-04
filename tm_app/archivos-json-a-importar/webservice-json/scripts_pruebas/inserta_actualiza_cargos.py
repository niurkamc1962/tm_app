# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WSCargos(Document):
    pass


@frappe.whitelist()
def inserta_actualiza_cargos(carg_id, carg_codigo, carg_descripcion):
    try:
        # Mostrar los valores de las variables
        frappe.msgprint(
            title="Valores Recibidos",
            msg=f"""
                CargId: {carg_id},
                CargCodigo: {carg_codigo},
                CargDescripcion: {carg_descripcion}
            """,
            indicator="blue"
        )
        # verificando si ya existe
        existe_cargo = frappe.db.exists("WSCargos", {"CargId": carg_id})

        if existe_cargo:
            # actualizar el registro
            doc = frappe.get_doc("WSCargos", existe_cargo)
            doc.CargCodigo = carg_codigo
            doc.CargDescripcion = carg_descripcion
            doc.save()
            return {"message": f"Cargo con CargId {carg_id} actualizado"}
        else:
            # insertar nuevo registro
            new_doc = frappe.new_doc("WSCargos")
            new_doc.CargId = carg_id
            new_doc.CargCodigo = carg_codigo
            new_doc.CargDescripcion = carg_descripcion
            new_doc.insert()
            return {"message": f"Cargo con CargId {carg_id} insertado"}
    except frappe.exceptions.ValidationError as e:
        return {"message": f"Error al insertar o actualizar: {str(e)}"}

