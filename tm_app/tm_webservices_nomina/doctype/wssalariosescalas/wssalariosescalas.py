# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WSSalariosEscalas(Document):
    pass


@frappe.whitelist()
def inserta_actualiza_salariosescalas(salesc_id, salesc_codigo, salesc_salarioescala, escs_id, ressalesc_id, res_descripcion, escs_descripcion):

    try:
        # verificando si ya existe
        existe_salarioescala = frappe.db.exists(
            "WSSalariosEscalas", {"SalEscId": salesc_id})

        if existe_salarioescala:
            # actualizar el registro
            doc = frappe.get_doc("WSSalariosEscalas", existe_salarioescala)
            doc.salesccodigo = salesc_codigo
            doc.salescsalarioescala = salesc_salarioescala
            doc.escsid = escs_id
            doc.ressalescid = ressalesc_id
            doc.resdescripcion = res_descripcion
            doc.escsdescripcion = escs_descripcion
            doc.save()
            return {"success": True, "message": f"Salarios Escala con SalEscId {salesc_id} actualizado"}
        else:
            # insertar nuevo registro
            new_doc = frappe.get_doc({
                "doctype": "WSSalariosEscalas",
                "salescid": salesc_id,
                "salesccodigo": salesc_codigo,
                "salescsalarioescala": salesc_salarioescala,
                "escsid": escs_id,
                "essalescid": ressalesc_id,
                "resdescripcion": res_descripcion,
                "escsdescripcion": escs_descripcion
            })
            new_doc.insert()
            return {"success": True, "message": f"Salarios Escala con SalescIc {salesc_id} - {salesc_salarioescala} insertado"}
    except frappe.exceptions.ValidationError as e:
        return {"message": f"Error al insertar o actualizar: {str(e)}"}
