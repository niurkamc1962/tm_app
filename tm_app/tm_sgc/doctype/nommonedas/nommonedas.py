# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime


class NomMonedas(Document):
    pass


@frappe.whitelist()
def inserta_actualiza_monedas(dato_moncodigo, dato_monsiglas, dato_mondescrip, dato_monflag, dato_monfechamodif, dato_monui, dato_monpais, dato_paiscodintern):

    try:
        # verificando si ya existe
        existe_moneda = frappe.db.exists(
            "NomMonedas", {"name": dato_moncodigo})

        print(
            f"[Resultado] existe_moneda: {existe_moneda} | [Sigla Moneda]: {dato_monsiglas} | [Codigo Moneda]: {dato_moncodigo}")

        if existe_moneda:
            # actualizar el registro
            doc = frappe.get_doc("NomMonedas", existe_moneda)
            doc.mondescrip = dato_mondescrip
            doc.monsiglas = dato_monsiglas
            doc.monflag = dato_monflag
            if isinstance(dato_monfechamodif, str):
                doc.monfechamodif = datetime.strptime(
                    dato_monfechamodif, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
            else:
                raise ValueError(
                    f"dato_monfechamodif {dato_monfechamodif} - {dato_monsiglas} - {dato_mondescrip} debe ser una cadena")
            doc.monui = dato_monui
            doc.monpais = dato_monpais
            doc.paiscodintern = dato_paiscodintern
            doc.save()
            return {"success": True, "message": f"Moneda {dato_mondescrip} MonCodigo {dato_moncodigo} actualizado"}
        else:
            # insertar nuevo registro
            new_doc = frappe.get_doc({
                "doctype": "NomMonedas",
                "moncodigo": dato_moncodigo,
                "monsiglas": dato_monsiglas,
                "mondescrip": dato_mondescrip,
                "monui": dato_monflag,
                "monfechamodif": datetime.strptime(
                    dato_monfechamodif, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S"),
                'monui': dato_monui,
                'monpais': dato_monpais,
                'paiscodintern': dato_paiscodintern
            })
            new_doc.insert()
            return {"success": True, "message": f"Insertado {dato_moncodigo} - {dato_mondescrip} "}
    except frappe.exceptions.ValidationError as e:
        return {"message": f"Error al insertar o actualizar: {dato_monsiglas} con {dato_moncodigo}, {str(e)}"}
