# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime


class NomUniones(Document):
    pass


@frappe.whitelist()
def inserta_actualiza_uniones(dato_organcodigo, dato_unioncodigo, dato_descripcion, dato_unionui, dato_unionfechamodif, dato_unionactivo):

    try:
        # verificando si ya existe
        existe_union = frappe.db.exists(
            "NomUniones", {"unioncodigo": dato_unioncodigo, "organcodigo": dato_organcodigo})

        print(
            f"[Resultado] existe_union: {existe_union} | [Codigo Union]: {dato_unioncodigo} | [Codigo Organ]: {dato_organcodigo}")

        if existe_union:
            # actualizar el registro
            doc = frappe.get_doc("NomUniones", existe_union)
            # doc.organcodigo = dato_organcodigo
            doc.descripcion = dato_descripcion
            doc.unionui = dato_unionui
            # doc.unionfechamodif = datetime.strptime(
            #     dato_unionfechamodif, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S"),
            if isinstance(dato_unionfechamodif, str):
                doc.unionfechamodif = datetime.strptime(
                    dato_unionfechamodif, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
            else:
                raise ValueError(
                    f"dato_unionfechamodif {dato_unionfechamodif} - {dato_unioncodigo} - {dato_descripcion} debe ser una cadena")
            doc.unionactivo = dato_unionactivo
            doc.save()
            return {"success": True, "message": f"Union {dato_unioncodigo} OrganCodigo {dato_organcodigo} actualizado"}
        else:
            # insertar nuevo registro
            new_doc = frappe.get_doc({
                "doctype": "NomUniones",
                "organcodigo": dato_organcodigo,
                "unioncodigo": dato_unioncodigo,
                "descripcion": dato_descripcion,
                "unionui": dato_unionui,
                "unionfechamodif": datetime.strptime(
                    dato_unionfechamodif, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S"),
                'unionactivo': dato_unionactivo
            })
            new_doc.insert()
            return {"success": True, "message": f"insertado {dato_unioncodigo} - {dato_descripcion} "}
    except frappe.exceptions.ValidationError as e:
        return {"message": f"Error al insertar o actualizar: {dato_unioncodigo} con {dato_organcodigo}, {str(e)}"}
