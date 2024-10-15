# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WSClavesSubsidios(Document):
    pass


@frappe.whitelist()
def inserta_actualiza_clavessubsidios(subsid_id, subsid_codigo, subsid_descripcion):

    # Validar que los valores no estén vacíos
    if not subsid_id:
        return {"message": "El SubsidId no puede estar vacío."}
    if not subsid_codigo:
        return {"message": "El SubsidCodigo no puede estar vacío."}
    if not subsid_descripcion:
        return {"message": "La SubsidDescripcion no puede estar vacía."}

    try:
        # verificando si ya existe
        existe_subsid = frappe.db.exists(
            "WSClavesSubsidios", {"SubsidId": subsid_id})

        if existe_subsid:
            # actualizar el registro
            doc = frappe.get_doc("WSClavesSubsidios", existe_subsid)
            doc.subsidcodigo = subsid_codigo
            doc.subsiddescripcion = subsid_descripcion
            doc.save()
            return {"success": True, "message": f"ClaveSubsid con SubsidId {subsid_id} actualizado"}
        else:
            # insertar nuevo registro
            new_doc = frappe.get_doc({
                "doctype": "WSClavesSubsidios",
                "subsidid": subsid_id,
                "subsidcodigo": subsid_codigo,
                "subsiddescripcion": subsid_descripcion
            })
            new_doc.insert()
            return {"success": True, "message": f"ClaveSubsid con SubsidId {subsid_id} - {subsid_descripcion} insertado"}
    except frappe.exceptions.ValidationError as e:
        return {"message": f"Error al insertar o actualizar: {str(e)}"}
