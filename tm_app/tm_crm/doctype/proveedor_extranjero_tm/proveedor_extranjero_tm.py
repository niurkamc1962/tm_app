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
            "Proveedor Extranjero TM", {"clicodigo": dato["CliCodigo"]}
        )
        

        if existe_proveedor:
            # Obtener el documento existente
            doc = frappe.get_doc("Proveedor Extranjero TM", existe_proveedor)
            clicodigo = doc.clicodigo
            
            doc.clicategoria = dato["CliCategoria"]
            doc.clicodigoimpresion = dato["CliCodImpresion"]
            doc.nombre_compania = dato["CliDescripcionLarga"]
            doc.codigo_mincex = dato["CliCodigoComercial"]
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
            # Buscar las cuentas bancarias para asociarlas al proveedor extranjero
            inserta_actualiza_cuentas_bancarias(dato["CliCodigo"])
            
            return {
                "success": True,
                "message": f"Proveedor {clicodigo} *** actualizado ***",
            }
        else:
           
            # insertar nuevo registro de Proveedor
            proveedor_doc = frappe.get_doc(
                {
                    "doctype": "Proveedor Extranjero TM",
                    "codigo_mincex": dato["CliCodigoComercial"],
                    "clicodigo": dato["CliCodigo"],
                    "clicategoria": dato["CliCategoria"],
                    "clicodigoimpresion": dato["CliCodImpresion"],
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
            
            # Buscar las cuentas bancarias para asociarlas al proveedor extranjero
            inserta_actualiza_cuentas_bancarias(dato["CliCodigo"])
            
            return {
                "success": True,
                "message": f" Insertado proveedor {dato['CliCodigo']} | Nombre {dato['CliDescripcionLarga']} ",
            }
        
    except frappe.exceptions.ValidationError as e:
        return {"success": False, "message": f"Error de validación: {str(e)}"}
    except frappe.exceptions.DoesNotExistError:
        return {
            "success": False,
            "message": "No se encontró el documento para actualizar.",
        }
    except Exception as e:
        print(f"Error inesperado en el proveedor {dato['CliCodigo']}")
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
            "Proveedor Extranjero TM", {"clicodigo": contacto_codigo}
        )
        if existe_proveedor:
            doc = frappe.get_doc("Proveedor Extranjero TM", existe_proveedor)
            proveedor_id = doc.clicodigo
            
            # concatenando nombre y apellidos
            nombre_completo = f"{contacto_nombre} {contacto_apellidos}"
                        
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
    
    
    
# Funcion para buscar las cuentas bancarias y asociarlas al proveedor en el doctype Datos Bancarios Proveedor Ext TM
def inserta_actualiza_cuentas_bancarias(clicodigo):
    existen_cuentas_bancarias = frappe.get_all("Bank Account", filters={"custom_clicodigo": clicodigo})
    if existen_cuentas_bancarias:
    # existen por lo que paso a insertarlas o actualizarlas en Datos Bancarios Proveedor Ext TM
        for cuenta in existen_cuentas_bancarias:
            # buscando los datos de la cuenta bancaria en BANK ACCOUNT
            doc_bank_account = frappe.get_doc("Bank Account", cuenta['name'])
            # asignando los valores a variables
            cuenta_bancaria_id = doc_bank_account.name
            cuenta_bancaria_no_cuenta = doc_bank_account.custom_clidbcuenta
            cuenta_bancaria_swift = doc_bank_account.custom_clidbswift
            cuenta_bancaria_tipo_moneda = doc_bank_account.custom_clidbcodmon
            cuenta_bancaria_clicodigo = doc_bank_account.custom_clicodigo
            cuenta_bancaria_entfinancodigo = doc_bank_account.custom_entfinancodigo
            cuenta_bancaria_clidbnrotransit = doc_bank_account.custom_clidbnrotransit
            
            # buscando la direccion del banco y el nombre
            print(f"Buscar datos del banco con entfinancodigo {cuenta_bancaria_entfinancodigo}")
            existe_banco = frappe.get_all("Bank", filters={"custom_entfinancodigo": cuenta_bancaria_entfinancodigo})
            print(f"Existe Banco: {existe_banco}")
            if existe_banco:
                datos_banco = frappe.get_doc("Bank", existe_banco[0]['name'])
                banco_nombre = datos_banco.name
                banco_direccion = datos_banco.custom_entfinandireccion
                print(f"DATOS del BANCO nombre {banco_nombre} con direccion {banco_direccion}")
            else:
                print(f"No se encontro banco con el codigo {cuenta_bancaria_entfinancodigo}")
                
            # buscando si ya esta en Datos Bancarios Proveedor Ext TM
            existe_cuenta_tm = frappe.db.exists("Datos Bancarios Proveedor Ext TM", {"cuenta_bancaria": cuenta_bancaria_id})
            if existe_cuenta_tm:
                doc_cuenta_tm = frappe.get_doc("Datos Bancarios Proveedor Ext TM", existe_cuenta_tm)
                # actualizo Cuenta Bancaria TM
                doc_cuenta_tm.no_cuenta = cuenta_bancaria_no_cuenta
                doc_cuenta_tm.swift = cuenta_bancaria_swift
                doc_cuenta_tm.tipo_moneda = cuenta_bancaria_tipo_moneda
                doc_cuenta_tm.no_transit = cuenta_bancaria_clidbnrotransit
                doc_cuenta_tm.banco = banco_nombre if banco_nombre else None
                doc_cuenta_tm.direccion = banco_direccion if banco_direccion else None
                doc_cuenta_tm.save()                
            else:
                # Creando cuenta bancaria en TM
                doc_cuenta_tm = frappe.get_doc({
                    "doctype": "Datos Bancarios Proveedor Ext TM",
                    "cuenta_bancaria": cuenta_bancaria_id,
                    "clicodigo": cuenta_bancaria_clicodigo,
                    "no_cuenta": cuenta_bancaria_no_cuenta,
                    "swift": cuenta_bancaria_swift,
                    "tipo_moneda": cuenta_bancaria_tipo_moneda,
                    'no_transit': cuenta_bancaria_clidbnrotransit,
                    'banco': banco_nombre if banco_nombre else None,
                    'direccion': banco_direccion if banco_direccion else None,
                    "parent": clicodigo,
                    "parenttype": "Proveedor Extranjero TM",
                    "parentfield": "datos_bancarios_proveedor_ext_tm"
                })
                doc_cuenta_tm.insert()
                
                print(f"Creada la cuenta bancaria en TM {cuenta_bancaria_no_cuenta} con clicodigo {cuenta_bancaria_clicodigo}")
        return {"susccess": True, "message": "Insertadas las cuentas bancarias"}
    else:
        print(f"No existen cuentas bancarias de {clicodigo}")
        return {"success": False, "message": f"Error inesperado cuenta bancaria con Clicodigo: {clicodigo}"}