# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WSRegimenTrabajo(Document):
    pass


@frappe.whitelist()
def inserta_actualiza_regimentrabajo(retra_id, retra_codigo, retra_descripcion, retra_horlab, retra_hormax, retra_horsemanas, retra_hormaxlab):

    try:
        # verificando si ya existe
        existe_regimentrabajo = frappe.db.exists(
            "WSRegimenTrabajo", {"RetraId": retra_id})

        if existe_regimentrabajo:
            # actualizar el registro
            doc = frappe.get_doc("WSRegimenTrabajo", existe_regimentrabajo)
            doc.retracodigo = retra_codigo
            doc.retradescripcion = retra_descripcion
            doc.retrahorlab = retra_horlab
            doc.retrahormax = retra_hormax
            doc.retrahorsemanas = retra_horsemanas
            doc.retrahormaxlab = retra_hormaxlab
            doc.save()
            return {"success": True, "message": f"Regimen Trabajo con RetraId {retra_id} actualizado"}
        else:
            # insertar nuevo registro
            new_doc = frappe.get_doc({
                "doctype": "WSRegimenTrabajo",
                "retraid": retra_id,
                "retracodigo": retra_codigo,
                "retradescripcion": retra_descripcion,
                "retrahorlab": retra_horlab,
                "retrahormax": retra_hormax,
                "retrahorsemanas": retra_horsemanas,
                "retrahormaxlab": retra_hormaxlab
            })
            new_doc.insert()
            return {"success": True, "message": f"Regimen Trabajo con RetraId {retra_id} - {retra_descripcion} insertado"}
    except frappe.exceptions.ValidationError as e:
        return {"message": f"Error al insertar o actualizar: {str(e)}"}
