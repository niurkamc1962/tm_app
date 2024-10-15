# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json
from datetime import datetime


class ProveedorExtranjeroTM(Document):
    pass


@frappe.whitelist()
def inserta_actualiza_proveedor_extranjero(dato):
    # print(f"Data: {dato}")
    try:
        # Convertir a diccionario
        dato = json.loads(dato)
        # print("dato json: ", dato)
        # print(f"CliPaisCodIntern: ", dato['CliPaisCodIntern'])
    except ValueError:
        return {
            "Success": False,
            "message": "El parametro 'dato' no es un JSON valido.",
        }

    # print(f"Dato: {dato}")
    try:
        # buscanndo el pais segun el codigo del JSON
        pais = busca_code_pais(dato["CliPaisCodIntern"])
        
        # convirtiendo el campo CliFechaModif
        if isinstance(dato['CliFechaModif'], str):
            fecha_modif = datetime.strptime(
                dato['CliFechaModif'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
        else:
            fecha_modif = None
        

        # verificando si ya existe ese codigo mincex en el doctype
        existe_proveedor = frappe.db.exists(
            "Proveedor Extranjero TM", {"codigo_mincex": dato["CliCodigo"]}
        )
        print(
            f"existe_proveedor: ",
            existe_proveedor,
            " con codigo ",
            dato["CliCodigo"],
            "y CliPaisCodIntern ",
            dato["CliPaisCodIntern"],
        )

        if existe_proveedor:
            print(f"ACTUALIZANDO Proveedor ", dato["CliCodigo"])
            # Obtener el documento existente
            doc = frappe.get_doc("Proveedor Extranjero TM", existe_proveedor)
            print(f"Documento encontrado: {doc.CliCodigo}")

            doc.nombre_compania = dato["CliDescripcion"]            
            doc.fecha_actualizacion = fecha_modif
            doc.siglas = dato["CliCMNombre"]
            doc.domicilio_legal = dato["CliDireccion"]
            doc.pais = pais if pais else None,
            doc.email = dato["CliEmail"]
            doc.sitio_web = dato["CliCMWeb"]
            doc.fax = dato["CliFax"]
            doc.telefonos = dato["CliTelefono"]
            doc.save()
            return {
                "success": True,
                "message": f"Proveedor {dato['CliCodigo']} *** actualizado ***",
            }
        else:
            print(f"*** CREANDO nuevo ", dato["CliCodigo"], "***")

            # insertar nuevo registro
            new_doc = frappe.get_doc(
                {
                    "doctype": "Proveedor Extranjero TM",
                    "codigo_mincex": dato["CliCodigo"],
                    "nombre_compania": dato["CliDescripcion"],
                    "fecha_actualizacion": fecha_modif,
                    "siglas": dato["CliCMNombre"],
                    "domicilio_legal": dato["CliDireccion"],
                    "pais": pais if pais else None,
                    "email": dato["CliEmail"],
                    "sitio_web": dato["CliCMWeb"],
                    'fax': dato["CliFax"],
                    'telefonos': dato["CliTelefono"]
                }
            )
            new_doc.insert()
            return {
                "success": True,
                "message": f" Insertado proveedor {dato['CliCodigo']} | Compania {dato['CliDescripcion']} ",
            }
    except frappe.exceptions.ValidationError as e:
        return {"success": False, "message": f"Error de validación: {str(e)}"}
    except frappe.exceptions.DoesNotExistError:
        return {
            "success": False,
            "message": "No se encontró el documento para actualizar.",
        }
    except Exception as e:
        return {"success": False, "message": f"Error inesperado: {str(e)}"}


# Buscando si existe el pais para devolver el id
def busca_code_pais(codigo_pais):
    # existe_pais = frappe.db.exists("Country", {"custom_paiscodintern": codigo_pais})
    existe_pais = frappe.db.get_value("Country", {"custom_paiscodintern": codigo_pais}, "name")
    
    return existe_pais
