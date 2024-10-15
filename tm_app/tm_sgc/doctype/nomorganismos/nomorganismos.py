# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime


class NomOrganismos(Document):
    pass


@frappe.whitelist()
def inserta_actualiza_organismos(dato_organcodigo, dato_organdescripcion, dato_organei, dato_organui, dato_organfechamodif, dato_organactivo):

    try:
        # verificando si ya existe
        existe_organismo = frappe.db.exists(
            "NomOrganismos", {"organcodigo": dato_organcodigo})

        if existe_organismo:
            # actualizar el registro
            doc = frappe.get_doc("NomOrganismos", existe_organismo)
            doc.organdescripcion = dato_organdescripcion
            doc.organei = dato_organei
            doc.organui = dato_organui
            doc.organactivo = dato_organactivo
            if isinstance(dato_organfechamodif, str):
                doc.organfechamodif = datetime.strptime(
                    dato_organfechamodif, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
            else:
                raise ValueError(
                    f"dato_organfechamodif {dato_organfechamodif} - {dato_organcodigo} - {dato_organdescripcion} debe ser una cadena")

            doc.save()
            return {"success": True, "message": f"OrganCodigo {dato_organcodigo} con {dato_organdescripcion} actualizado"}
        else:
            # insertar nuevo registro
            new_doc = frappe.get_doc({
                "doctype": "NomOrganismos",
                "organcodigo": dato_organcodigo,
                "organdescripcion": dato_organdescripcion,
                "organei": dato_organei,
                "organui": dato_organui,
                "organfechamodif": datetime.strptime(
                    dato_organfechamodif, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S"),
                'organactivo': dato_organactivo
            })
            new_doc.insert()
            return {"success": True, "message": f"insertado {dato_organcodigo} - {dato_organdescripcion} "}
    except frappe.exceptions.ValidationError as e:
        return {"message": f"Error al insertar o actualizar: {dato_organcodigo} con {dato_organdescripcion}, {str(e)}"}
