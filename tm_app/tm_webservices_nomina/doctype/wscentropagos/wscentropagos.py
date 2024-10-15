# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WSCentroPagos(Document):
    pass


@frappe.whitelist()
def inserta_actualiza_centropagos(cpago_id, cpago_codigo, cpago_descripcion):

    try:
        # verificando si ya existe
        existe_cpago = frappe.db.exists("WSCentroPagos", {"CPagoId": cpago_id})

        if existe_cpago:
            # actualizar el registro
            doc = frappe.get_doc("WSCentroPagos", existe_cpago)
            doc.cpagocodigo = cpago_codigo
            doc.cpagodescripcion = cpago_descripcion
            doc.save()
            return {"success": True, "message": f"CentroPago con CPagoId {cpago_id} actualizado"}
        else:
            # insertar nuevo registro
            new_doc = frappe.get_doc({
                "doctype": "WSCentroPagos",
                "cpagoid": cpago_id,
                "cpagocodigo": cpago_codigo,
                "cpagodescripcion": cpago_descripcion
            })
            new_doc.insert()
            return {"success": True, "message": f"CentroPago con CPagoId {cpago_id} - {cpago_descripcion} insertado"}
    except frappe.exceptions.ValidationError as e:
        return {"message": f"Error al insertar o actualizar: {str(e)}"}
