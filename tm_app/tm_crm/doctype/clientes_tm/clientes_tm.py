# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json
from datetime import datetime


class ClientesTM(Document):
    pass


@frappe.whitelist()
def inserta_actualiza_cliente_tm(dato, contactos_json):
    try:
        # Convertir a diccionario
        dato = json.loads(dato)
        # print(f"JSON.load: {dato}")

        # Tratamiento para filtrar los contactos
        contactos_a_procesar = []

        if contactos_json:
            try:
                # convertir el json de Contactos
                contactos = json.loads(contactos_json)
                # Filtrar los contactos del cliente (clicodigo campo por el que se busca)
                contactos_a_procesar = [
                    c for c in contactos if c.get("CliCodigo") == dato["CliCodigo"]
                ]
            except json.JSONDecodeError:
                frappe.throw(_("Error al procesar los contactos: JSON no valido"))

        fecha_modif = procesar_fecha(dato["CliFechaModif"])
        provincia_id, provincia_nombre = busca_provincia(dato["ProvCod"])
        municipio_id, municipio_nombre = busca_municipio(provincia_id, dato["MunicCod"])
        organismo_id, organismo_nombre = busca_organismo(dato["OrganCodigo"])
        categoria_id, categoria_nombre = busca_categoria_cliente_proveedor(
            dato["CliCategoria"]
        )
        
        print(f"Municipio ID: {municipio_id}, Municipio Nombre: {municipio_nombre}")
        
        # verificando si ya existe ese codigo reeup en el doctype Clientes
        existe_cliente_tm = frappe.db.exists(
            "Clientes TM", {"clicodigo": dato["CliCodigo"]}
        )

        # Preparando cliente_data para poder pasarlo como parametro segun el caso
        cliente_data = {
            "clicodigo": dato["CliCodigo"],
            "clicategoria": categoria_id if categoria_id else None,
            "fecha": fecha_modif,
            "codigo_nit": dato["CliNit"],
            "cod_registro_comercial": dato["CliCodigoComercial"],
            "nombre_empresa": dato["CliDescripcionLarga"],
            "direccion_empresa": dato["CliDireccion"],
            "provincia_empresa": provincia_id if provincia_id else None,
            "municipio_empresa": municipio_id if municipio_id else None,
            "organismo": organismo_id if organismo_id else None,
            "fax": dato["CliFax"],
            "telefono": dato["CliTelefono"],
            "email": dato["CliEmail"],
        }

        if existe_cliente_tm:
            result_actualizar = actualizar_cliente(cliente_data)
            mensaje_cliente = result_actualizar.get("message")
        else:
            result_crear = crear_cliente(cliente_data)
            mensaje_cliente = result_crear.get("message")

        # print(f"contactos a procesar: {contactos_a_procesar}")
        # procesar los contactos
        for contacto in contactos_a_procesar:
            print(f"Contacto a procesar: {contacto}")
            result_contacto = procesar_contacto(contacto)
            if result_contacto is None or not isinstance(result_contacto, dict):
                mensaje_cliente += f"Error desconocido al procesar el contacto {contacto['CliContacNombre']}"
                continue
            
            if not result_contacto.get("success"):
                mensaje_cliente += f"{result_contacto.get('message')}"
            else:
                mensaje_cliente += f"Contacto {contacto['CliContacNombre']} procesado con exito"

        return {"success": True, "message": mensaje_cliente}

    except frappe.exceptions.ValidationError as e:
        return {"success": False, "message": f"Error de validación: {str(e)}"}
    except frappe.exceptions.DoesNotExistError:
        return {
            "success": False,
            "message": "No se encontró el documento para actualizar.",
        }
    except Exception as e:
        return {"success": False, "message": f"Error inesperado: {str(e)}"}



def actualizar_cliente(cliente_data):
    try:
        # buscando segun el clicodigo para actualizar el cliente
        cliente_doc = frappe.get_doc("Clientes TM", cliente_data["clicodigo"])

        cliente_doc.clicategoria = cliente_data["clicategoria"]
        cliente_doc.fecha = cliente_data["fecha"]
        cliente_doc.codigo_nit = cliente_data["codigo_nit"]
        cliente_doc.cod_registro_comercial = cliente_data["cod_registro_comercial"]
        cliente_doc.organismo = cliente_data["organismo"]
        cliente_doc.nombre_empresa = cliente_data["nombre_empresa"]
        cliente_doc.direccion_empresa = cliente_data["direccion_empresa"]
        cliente_doc.provincia_empresa = cliente_data["provincia_empresa"]
        cliente_doc.municipio_empresa = cliente_data["municipio_empresa"]
        # cliente_doc.nombre_ueb = cliente_data["nombre_ueb"]
        # cliente_doc.direccion_ueb = cliente_data["direccion_ueb"]
        # cliente_doc.provincia_ueb = cliente_data["provincia_ueb"]
        # cliente_doc.municipio_ueb = cliente_data["municipio_ueb"]
        cliente_doc.fax = cliente_data["fax"]
        cliente_doc.telefono = cliente_data["telefono"]
        cliente_doc.email = cliente_data["email"]
        cliente_doc.save()
        return {
            "success": True,
            "message": f"Cliente {cliente_data['clicodigo']} - {cliente_data['nombre_empresa']} ACTUALIZADO.",
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error al actualizar el cliente {cliente_data['clicodigo']} : {str(e)}",
        }


def crear_cliente(cliente_data):
    try:
        nuevo_cliente = frappe.get_doc(
            {
                "doctype": "Clientes TM",
                "clicodigo": cliente_data["clicodigo"],
                "clicategoria": cliente_data["clicategoria"],
                "fecha": cliente_data["fecha"],
                "codigo_nit": cliente_data["codigo_nit"],
                "cod_registro_comercial": cliente_data["cod_registro_comercial"],
                "organismo": cliente_data["organismo"],
                "nombre_empresa": cliente_data["nombre_empresa"],
                "direccion_empresa": cliente_data["direccion_empresa"],
                "provincia_empresa": cliente_data["provincia_empresa"],
                "municipio_empresa": cliente_data["municipio_empresa"],
                # "nombre_ueb": cliente_data["nombre_empresa"],
                # "direccion_ueb": cliente_data["direccion_ueb"],
                # "provincia_ueb": cliente_data["provincia_ueb"],
                # "municipio_ueb": cliente_data["municipio_ueb"],
                "fax": cliente_data["fax"],
                "telefono": cliente_data["telefono"],
                "email": cliente_data["email"],
            }
        )
        nuevo_cliente.insert()
        return {
            "success": True,
            "message": f"Cliente {cliente_data['clicodigo']} - {cliente_data['nombre_empresa']} CREADO.",
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error al CREAR el cliente {cliente_data['clicodigo']} : {str(e)}",
        }


# Procesando los contactos del cliente
def procesar_contacto(contacto):
    try:
        # buscando si ya esta el contacto para pasar a actualizarlo de lo contrario se crea nuevo
        existe_contacto = frappe.db.exists(
            "Contactos Clientes TM",
            {"clicodigo": contacto["CliCodigo"], "ci_contacto": contacto["CliContacCI"]},
        )
        print(f"Existe contacto: {existe_contacto} | Cargo: {contacto['CliContacCargo']} | CliContacId: {contacto['CliContacId']} | Nombre: {contacto['CliContacNombre']}")
        cargo = contacto["CliContacCargo"]
        nombre_apellidos = f"{contacto['CliContacNombre']} {contacto['CliContacApellidos']}"
        # obteniendo el cliente para el caso del Dir. Gral y Dir. Econ que van em el doctype del cliente
        cliente_id = frappe.get_value("Clientes TM", {"clicodigo": contacto["CliCodigo"]})
        
        # preguntando si es director gral o economico
        if cargo in [
            "Director",
            "Directora",
            "Director General",
            "Dir.General",
            "Dir.Gral",
            "Director Económico",
            "Dir. Económico",
            "Director Económica",
            "Dir. Económica",
        ]:
            procesa_dir_gral_econ(contacto, cargo, cliente_id)
            
        else:
            # preguntando si ya esta insertado el contacto si no lo creo nuevo
            if existe_contacto:
                # Actualiza en el doctype de los contactos
                doc_contacto = frappe.get_doc("Contactos Clientes TM", existe_contacto)
                doc_contacto.clicodigo = contacto["CliCodigo"]
                doc_contacto.ci_contacto = contacto["CliContacCI"]
                doc_contacto.telefono_contacto = contacto["CliContacTlfno"]
                doc_contacto.nombre_y_apellidos_contacto = nombre_apellidos
                doc_contacto.email_contacto = contacto["CliContacEmail"]
                doc_contacto.cargo_contacto = cargo
                doc_contacto.save()
            else:
                doc_contacto = frappe.get_doc(
                    {
                        "doctype": "Contactos Clientes TM",
                        "clicodigo": contacto["CliCodigo"],
                        "ci_contacto": contacto["CliContacCI"],
                        "cargo_contacto": contacto["CliContacCargo"],
                        "nombre_y_apellidos_contacto": nombre_apellidos,
                        "telefono_contacto": contacto["CliContacTlfno"],
                        "email_contacto": contacto["CliContacEmail"],
                        "parent": cliente_id,
                        "parenttype": "Clientes TM",
                        "parentfield": "contactos_clientes_tm"
                    }
                )
                doc_contacto.autoname()
                doc_contacto.insert()
            return { "success": True, "message": "Contacto procesado correctamente"}
        
    except Exception as e:
        return {"success": False, "message": f"Error al procesar el contacto: {str(e)}"}


# funcion para procesar los datos del Dir. Gral y/o Dir. Econ.
def procesa_dir_gral_econ(contacto, cargo, cliente_id):
    # buscando el id del cliente para insertar los datos del dir. gral y/o el econ.
    doc_cliente = frappe.get_doc("Clientes TM", cliente_id)
    # mostrar las propiedades del objeto doc_cliente
    # print(dir(doc_cliente))
    
    if not doc_cliente:
        return { "success":False, "message":f"No se encontro el cliente {cliente_id}"}

    nombre_apellidos = f"{contacto['CliContacNombre']} {contacto['CliContacApellidos']}"
    print(f"cargo: {cargo}")
    if cargo in [
        "Director",
        "Directora",
        "Director General",
        "Dir.General",
        "Dir.Gral",
    ]:
        # Los datos del Director General
        doc_cliente.ci_dir_general = contacto["CliContacCI"]
        doc_cliente.telefono_dir_general = contacto["CliContacTlfno"]
        doc_cliente.email_dir_general = contacto["CliContacEmail"]
        doc_cliente.nombre_dir_general = nombre_apellidos
    else:
        # Los datos del Director Economico
        doc_cliente.ci_dir_economico = contacto["CliContacCI"]
        doc_cliente.telefono_dir_economico = contacto["CliContacTlfno"]
        doc_cliente.email_dir_economico = contacto["CliContacEmail"]
        doc_cliente.nombre_dir_economico = nombre_apellidos
        
    doc_cliente.save()
    frappe.db.commit()
    print(f"Insertado el contacto dir con cargo {cargo} y nombre {nombre_apellidos}")
   

# buscando el id del organisno
def busca_organismo(organismo):
    organismo_doc = frappe.db.get_value(
        "NomOrganismos",
        {"organcodigo": organismo},
        ["name", "descripcion"],
        as_dict=True,
    )
    organismo_id = organismo_doc.name
    organismo_nombre = organismo_doc.descripcion

    # print(f"Organismo: {organismo_id}, con nombre {organismo_nombre}")
    return organismo_id, organismo_nombre


# función para buscar el id de la provincia
def busca_provincia(codigo_provincia):
    provincia_doc = frappe.db.get_value(
        "NomProvincias",
        {"provcod": codigo_provincia},
        ["name", "provnombre"],
        as_dict=True,
    )
    provincia_id = provincia_doc.name
    provincia_nombre = provincia_doc.provnombre

    # print(f"Provincia: {provincia_id} con nombre {provincia_nombre}")
    return provincia_id, provincia_nombre


# buscando el codigo del municipio segun la provincia
def busca_municipio(provincia_id, municipio):
    # print("Entre en busca municipio")
    municipio_doc = frappe.get_value(
        "NomMunicipios",
        {"provcod": provincia_id, "municcod": municipio},
        ["name", "municnombre"],
        as_dict=True,
    )

    if municipio_doc:
        municipio_id = municipio_doc.name
        municipio_nombre = municipio_doc.municnombre
        # print(
        #     f"Municipio encontrado: {municipio_nombre} (ID: {municipio_id}) para la provincia {provincia_id}"
        # )
        return municipio_id, municipio_nombre
    else:
        # print(
        #     f"No se encontró municipio para provcod: {provincia_id} y municcod: {municipio}"
        # )
        return None, None


# Buscando el id del codigo reeup
def busca_reeup(codigo_reeup):
    reeup_id = frappe.db.get_value("NomReeup", {"reeupcod", codigo_reeup}, "name")
    print(f"reeup_id: {codigo_reeup}")
    return reeup_id


# Buscando la categoria del Cliente segun los datos de Siscont
def busca_categoria_cliente_proveedor(categoria):
    categoria_doc = frappe.db.get_value(
        "NomCategClienteProveedor",
        {"categoria": categoria},
        ["name", "descripcion"],
        as_dict=True,
    )
    categoria_id = categoria_doc.name
    categoria_descripcion = categoria_doc.descripcion
    # print(f"Categoria: {categoria_id} con descripcion {categoria_descripcion}")
    return categoria_id, categoria_descripcion


# funcion para procesar la fecha
def procesar_fecha(dato):
    if "CliFechaModif" in dato and isinstance(dato["CliFechaModif"], str):
        fecha_modif = datetime.strptime(
            dato["CliFechaModif"], "%Y-%m-%dT%H:%M:%S.%fZ"
        ).strftime("%Y-%m-%d %H:%M:%S")
    else:
        fecha_modif = None
    return fecha_modif


# Funcion para obtener el listado de los municipios de la provincia
@frappe.whitelist()
def obtener_municipios(provincia):
    print(f"provincia: {provincia}")
    if not provincia:
        return []
   
    
    # obteniendo el listado de los municipios asociados
    municipios = frappe.get_all('NomMunicipios', filters={'provcod': provincia}, fields=['municcod', 'municnombre', 'provcod'])
    print(f"Municipios: {municipios}")
    
    # Preparando el formato del naming de los municipios
    result_municipios = []
    for municipio in municipios:
        naming_value = f"{municipio['provcod']}-{municipio['municcod']}" # preparando el naming rule igual que en el doctype
        print(f"naming_value: {naming_value} | municipio: {municipio['municnombre']}")
        result_municipios.append({
            'value': naming_value,
            'label': municipio['municnombre']
        })
    
    return result_municipios


# Funcion que se ejecuta cuando se carga el formulario del cliente por si tiene importado datos muestre 
# el municipio y la lista de los que son de la provincia seleccionada
@frappe.whitelist()
def obtener_datos_cliente(cliente_codigo):
    try:
        cliente = frappe.get_doc("Clientes TM", cliente_codigo)
        
        provincia_id = cliente.provincia_empresa
        municipio_id = cliente.municipio_empresa
        
        print(f"Cliente codigo Provincia: {provincia_id} - municipio_id: {municipio_id}")
        
        # Obtener los municipios de la provincia para enviar al campo select Municipios
        municipios_provincia = buscar_municipios_provincia(provincia_id)
        print(f"Municipios_provincia: {municipios_provincia}")
        # Creando la lista de las opciones para el campo select
        opciones_municipios = []
        # for municipio_id, municipio_nombre in municipios_provincia:
        #     opciones_municipios.append({
        #         'value': municipio_id,
        #         'label': municipio_nombre
        #     })
        opciones_municipios = [{'value': municipio['name'], 'label': municipio['municnombre']} for municipio in municipios_provincia]
        return {
            "success": True,
            "provincia": provincia_id,
            "opciones_municipios": opciones_municipios,
            "municipio_seleccionado": municipio_id
        }
    except Exception as e:
        return {"success": False, "message": str(e)}
    
def buscar_municipios_provincia(provincia_id):
    # consultando doctype para seleccionar todos los municipios de la provincia_id
    municipios = frappe.db.get_all('NomMunicipios', filters={'provcod': provincia_id}, fields=['name', 'municnombre'])
    return municipios