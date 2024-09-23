# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json


class NomReeup(Document):
    pass


@frappe.whitelist()
def inserta_actualiza_reeup(dato):
    # print(f"Data: {dato}")
    try:
        # Convertir a diccionario
        dato = json.loads(dato)
    except ValueError:
        return {"Success": False, "message": "El parametro 'dato' no es un JSON valido."}

    # print(f"Dato: {dato}")
    try:
        # verificando si ya existe ese codigo reeup en el doctype
        existe_reeup = frappe.db.exists(
            "NomReeup", {"reeupcod": dato['ReeupCod']})

        # print(f"Existe_reeup", existe_reeup, 'para ', dato['ReeupCod'])
        # print(
        #     f"[Resultado] ReeupCod: {dato['ReeupCod']} | [Descripcion]: {dato['ReeupNom']} | [ReeupDPA]: {dato['ReeupDPA']}")

        if existe_reeup:
            print(f"ACTUALIZANDO reeupcod ", dato['ReeupCod'])
            # Obtener el documento existente
            doc = frappe.get_doc("NomReeup", existe_reeup)
            print(f"Documento encontrado: {doc.reeupcod}")
            # actualizando los campos
            doc.reeupnom = dato['ReeupNom']
            doc.reeupdir = dato['ReeupDir']
            doc.reeuptelef = dato['ReeupTelef']
            doc.reeupcae = dato['ReeupCAE']
            doc.reeupdpa = dato['ReeupDPA']
            doc.reeuporg = dato['ReeupOrg']
            doc.reeupsub = dato['ReeupSub']
            doc.reeupnae = dato['ReeupNAE']
            doc.reeupsiglas = dato['ReeupSiglas']
            doc.reeupactivo = dato['ReeupActivo']
            doc.save()
            return {"success": True, "message": f"Reeup {dato['ReeupCod']} *** actualizado ***"}
        else:
            print(f"*** CREANDO nuevo ", dato['ReeupCod'], "***")
            # insertar nuevo registro
            new_doc = frappe.get_doc({
                "doctype": "NomReeup",
                'reeupcod': dato['ReeupCod'],
                "reeupnom": dato['ReeupNom'],
                "reeupdir": dato['ReeupDir'],
                "reeuptelef": dato['ReeupTelef'],
                "reeupcae": dato['ReeupCAE'],
                "reeupdpa": dato['ReeupDPA'],
                "reeuporg": dato['ReeupOrg'],
                "reeupsub": dato['ReeupSub'],
                "reeupnae": dato['ReeupNAE'],
                "reeupsiglas": dato['ReeupSiglas'],
                "reeupactivo": dato['ReeupActivo']
            })
            new_doc.insert()
            return {"success": True, "message": f" Insertado Reeup {dato['ReeupCod']} | Descripcion {dato['ReeupNom']} "}
    # except frappe.exceptions.ValidationError as e:
    #     return {"message": f"Error al insertar o actualizar: {dato['ReeupCod']} con {dato['ReeupNom']}, {str(e)}"}
    except frappe.exceptions.ValidationError as e:
        return {"success": False, "message": f"Error de validación: {str(e)}"}
    except frappe.exceptions.DoesNotExistError:
        return {"success": False, "message": "No se encontró el documento para actualizar."}
    except Exception as e:
        return {"success": False, "message": f"Error inesperado: {str(e)}"}
