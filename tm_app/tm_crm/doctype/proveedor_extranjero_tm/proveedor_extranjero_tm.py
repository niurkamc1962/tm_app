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
        if isinstance(dato["CliFechaModif"], str):
            fecha_modif = datetime.strptime(
                dato["CliFechaModif"], "%Y-%m-%dT%H:%M:%S.%fZ"
            ).strftime("%Y-%m-%d %H:%M:%S")
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
            # Obtener el documento existente
            doc = frappe.get_doc("Proveedor Extranjero TM", existe_proveedor)
            codigo_mincex = doc.codigo_mincex
            
            print(f"Actualizando Proveedor con codigo: {codigo_mincex}")
            
            doc.nombre_compania = dato["CliDescripcionLarga"]
            doc.fecha_actualizacion = fecha_modif
            doc.siglas = dato["CliDescripcion"]
            doc.domicilio_legal = dato["CliDireccion"]
            doc.pais = (pais if pais else None,)
            doc.email = dato["CliEmail"]
            doc.sitio_web = dato["CliCMWeb"]
            doc.fax = dato["CliFax"]
            doc.telefonos = dato["CliTelefono"]
            doc.save()

            # chequeando si ya tiene junta directiva insertada
            inserta_actualiza_junta_directiva(
                doc.name, dato["CliCMNombre"], dato['CliCMCargo'], dato["CliCMTlfno"]
            )

            return {
                "success": True,
                "message": f"Proveedor {codigo_mincex} *** actualizado ***",
            }
        else:
            print(f"*** CREANDO nuevo Proveedor ", dato["CliCodigo"], "***")

            # insertar nuevo registro de Proveedor
            proveedor_doc = frappe.get_doc(
                {
                    "doctype": "Proveedor Extranjero TM",
                    "codigo_mincex": dato["CliCodigo"],
                    "nombre_compania": dato["CliDescripcionLarga"],
                    "fecha_actualizacion": fecha_modif,
                    "siglas": dato["CliDescripcion"],
                    "domicilio_legal": dato["CliDireccion"],
                    "pais": pais if pais else None,
                    "email": dato["CliEmail"],
                    "sitio_web": dato["CliCMWeb"],
                    "fax": dato["CliFax"],
                    "telefonos": dato["CliTelefono"],
                }
            )
            proveedor_doc.insert()

            # Obteniendo el id del proveedor al que pertenece la junta directiva
            proveedor_id = proveedor_doc.name

            inserta_actualiza_junta_directiva(
                proveedor_id,
                dato["CliCMNombre"],
                dato["CliCMCargo"],
                dato["CliCMTlfno"]    
            )

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
    existe_pais = frappe.db.get_value(
        "Country", {"custom_paiscodintern": codigo_pais}, "name"
    )

    return existe_pais



# Insertando o actualizando junta directiva del proveedor extranjero
def inserta_actualiza_junta_directiva(proveedor_id, nombre, cargo, telefono):
    print (f"Junta directiva con nombre {nombre} y cargo {cargo} y PROVEEDOR {proveedor_id}")
    # primero busco si ya se inserto para que no este repetido
    existe_junta_directiva = frappe.db.exists(
        "Junta Directiva Proveedor Extranjero", {"nombre": nombre, "cargo": cargo}
    )
    if existe_junta_directiva:
        # indica que ya esta insertada por lo que actualizo
        junta_directiva_doc = frappe.get_doc(
            "Junta Directiva Proveedor Extranjero", existe_junta_directiva
        )
        if junta_directiva_doc:
            junta_directiva_doc.cargo = cargo
            junta_directiva_doc.nombre = nombre
            junta_directiva_doc.telefono = telefono
            junta_directiva_doc.save()
    else:
        # creando nueva junta directiva
        junta_doc = frappe.get_doc(
            {
                "doctype": "Junta Directiva Proveedor Extranjero",
                "parent": proveedor_id,
                "parenttype": "Proveedor Extranjero TM",
                "parentfield": "junta_directiva_proveedor_ext",
                "nombre": nombre,
                "telefono": telefono,
                "cargo": cargo,
            }
        )
        junta_doc.insert()
        return {"message": f"Insertada datos Junta Directiva: {nombre} con cargo {cargo}."}



# Insertando o actualizando los contactos del proveedor extranjero
@frappe.whitelist()
def inserta_actualiza_contactos_proveedor_ext(contacto):
    
    try:
        # Verificando si contacto es un dict
        if isinstance(contacto, str):
            # convirtiendola en un dict
            dato = json.loads(contacto)
            
        # Accediendo a los campos
        contacto_nombre = dato['CliContacNombre']
        contacto_apellidos = dato['CliContacApellidos']
        contacto_cargo = dato['CliContacCargo']
        contacto_telefono = dato['CliContacTlfno']
        contacto_email = dato['CliContacEmail']
        contacto_codigo = dato['CliCodigo']
        
        # Buscando el id del Proveedor para asignarlo en la insercion 
        existe_proveedor = frappe.db.exists(
            "Proveedor Extranjero TM", {"codigo_mincex": contacto_codigo}
        )
        if existe_proveedor:
            doc = frappe.get_doc("Proveedor Extranjero TM", existe_proveedor)
            proveedor_id = doc.codigo_mincex
            
            # concatenando nombre y apellidos
            nombre_completo = f"{contacto_nombre} {contacto_apellidos}"
            print(f"Nombre Completo: {nombre_completo}")
            
            # preguntando si ya se inserto este contacto del proveedor para no tenerlo repetido
            
            existe_contacto_proveedor_ext = frappe.db.exists(
                "Contactos Proveedor Extranjeros", 
                {
                    'nombre': nombre_completo, 
                    'email': contacto_email, 
                    'parent': proveedor_id
                }
            )
            
            if existe_contacto_proveedor_ext:
                print(f"Existe el contacto {nombre_completo}")
                # indica que ya esta insertada por lo que lo obtengo para actualizar 
                contacto_proveedor_doc = frappe.get_doc(
                    "Contactos Proveedor Extranjero", existe_contacto_proveedor_ext
                )        
                contacto_proveedor_doc.cargo = contacto_cargo
                contacto_proveedor_doc.telefono = contacto_telefono
                contacto_proveedor_doc.save()
            else:
                # Insertando el nuevo contacto del proveedor extranjero
                nuevo_contacto = frappe.get_doc({
                    "doctype": "Contactos Proveedor Extranjeros",
                    "nombre": nombre_completo,
                    "email": contacto_email,
                    "cargo": contacto_cargo,
                    "telefono": contacto_telefono,
                    "parent": proveedor_id,
                    "parenttype": "Proveedor Extranjero TM",
                    "parentfield": "contactos_proveedor_ext",
                })
                nuevo_contacto.insert()
                return {"message": f"Insertado contacto : {nombre} con email {email}."}
            
        
        
    except Exception as e:
        return {"Success": False, "message": str(e)}
    
    