# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WSConceptosPagos(Document):
    pass


@frappe.whitelist()
def inserta_actualiza_conceptospagos(concp_id, concp_codigo, concp_descripcion):

    # Validar que los valores no estén vacíos
    if not concp_id:
        return {"message": "El ConCPId no puede estar vacío."}
    if not concp_codigo:
        return {"message": "El ConcPCodigo no puede estar vacío."}
    if not concp_descripcion:
        return {"message": "La ConcPDescripcion no puede estar vacía."}

    try:
        # verificando si ya existe
        existe_concp = frappe.db.exists("WSCargos", {"ConCPId": concp_id})

        if existe_concp:
            # actualizar el registro
            doc = frappe.get_doc("WSConceptosPagos", existe_concp)
            doc.concpcodigo = concp_codigo
            doc.concpdescripcion = concp_descripcion
            doc.save()
            return {"success": True, "message": f"Concepto Pago con ConCPId {concp_id} actualizado"}
        else:
            # insertar nuevo registro
            new_doc = frappe.get_doc({
                "doctype": "WSConceptosPagos",
                "concpid": concp_id,
                "concpcodigo": concp_codigo,
                "concpdescripcion": concp_descripcion
            })
            new_doc.insert()
            return {"success": True, "message": f"Concepto Pago con ConCPId {concp_id} - {concp_descripcion} insertado"}
    except frappe.exceptions.ValidationError as e:
        return {"message": f"Error al insertar o actualizar: {str(e)}"}
