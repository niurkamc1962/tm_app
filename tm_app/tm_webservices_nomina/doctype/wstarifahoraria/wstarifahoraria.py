# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WSTarifaHoraria(Document):
    pass


@frappe.whitelist()
def inserta_actualiza_tarifahoraria(nomtari_id, nomtaricod_tarifa, nomtaritarif_horaria, escsalnomtari_id, res_id, res_descripcion, escs_descripcion, nomtari_formapago, nomtari_salmaximo):

    try:
        # verificando si ya existe
        existe_tarifahoraria = frappe.db.exists(
            "WSTarifaHoraria", {"NomTariId": nomtari_id})

        if existe_tarifahoraria:
            # actualizar el registro
            doc = frappe.get_doc("WSTarifaHoraria", existe_tarifahoraria)
            doc.nomtaricodtarifa = nomtaricod_tarifa
            doc.nomtaritarifhoraria = nomtaritarif_horaria
            doc.escsalnomtariid = escsalnomtari_id
            doc.resid = res_id
            doc.resdescripcion = res_descripcion
            doc.escsdescripcion = escs_descripcion
            doc.nomtariformapago = nomtari_formapago
            doc.nomtarisalmaximo = nomtari_salmaximo
            doc.save()
            return {"success": True, "message": f"Tarifa Horaria con NomTariId {nomtari_id} actualizado"}
        else:
            # insertar nuevo registro
            new_doc = frappe.get_doc({
                "doctype": "WSTarifaHoraria",
                "nomtariid": nomtari_id,
                "nomtaricodtarifa": nomtaricod_tarifa,
                "nomtaritarifhoraria": nomtaritarif_horaria,
                "escsalnomtariid": escsalnomtari_id,
                "resid": res_id,
                "resdescripcion": res_descripcion,
                "escsdescripcion": escs_descripcion,
                "nomtariformapago": nomtari_formapago,
                "nomtarisalmaximo": nomtari_salmaximo
            })
            new_doc.insert()
            return {"success": True, "message": f"Tarifa Horaria con NomTariId {nomtari_id} - {nomtaricod_tarifa} insertado"}
    except frappe.exceptions.ValidationError as e:
        return {"message": f"Error al insertar o actualizar: {str(e)}"}
