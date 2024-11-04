# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class NomTiposEmpresas(Document):
    pass


@frappe.whitelist()
def inserta_actualiza_tiposempresas(dato_tipoempresa, dato_descripcion, dato_estado, dato_ventacontabiliza):
    # Validar que los valores no estén vacíos
    if not dato_tipoempresa:
        return {"message": "El Tipo Empresa no puede estar vacío."}
    if not dato_descripcion:
        return {"message": "La descripcion no puede estar vacía."}
    if not dato_estado:
        return {"message": "El Estado no puede estar vacio."}

    try:
        # verificando si ya existe
        existe_tipoempresa = frappe.db.exists(
            "NomTiposEmpresas", {"tipoempresa": dato_tipoempresa})

        if existe_tipoempresa:
            # actualizar el registro
            doc = frappe.get_doc("NomTiposEmpresas", existe_tipoempresa)
            doc.descripcion = dato_descripcion
            doc.estado = dato_estado
            doc.save()
            return {"success": True, "message": f"Tipo Empresa  con tipoempresa {dato_tipoempresa} actualizado"}
        else:
            # insertar nuevo registro
            new_doc = frappe.get_doc({
                "doctype": "NomTiposEmpresas",
                "tipoempresa": dato_tipoempresa,
                "descripcion": dato_descripcion,
                "estado": dato_estado,
                "ventacontabiliza": dato_ventacontabiliza
            })
            new_doc.insert()
            return {"success": True, "message": f"Tipo Empresa con tipoempresa {dato_tipoempresa} - {dato_descripcion} insertado"}
    except frappe.exceptions.ValidationError as e:
        return {"message": f"Error al insertar o actualizar: {str(e)}"}
