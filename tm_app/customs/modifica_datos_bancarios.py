from frappe import _
import frappe
from frappe.model.document import Document
import json
import os


@frappe.whitelist()
def actualiza_datos_bancarios_de_siscont(doctype_a, doctype_b):
    
    dir_app = os.path.join(frappe.get_app_path("tm_app"), "archivos-json-a-importar")
    
    doctype_a_file_path = os.path.join(dir_app, f"{doctype_a}.json")
    doctype_b_file_path = os.path.join(dir_app, f"{doctype_b}.json")
    
    with open(doctype_a_file_path,"r") as file:
                dataA = json.load(file)
    bancos = dataA[doctype_a]    
    with open(doctype_b_file_path,"r") as file:
                dataB = json.load(file)
    cuentas_bancarias = dataB[doctype_b]
    
    procesa_informacion_bancaria(bancos, cuentas_bancarias)
    
 
@frappe.whitelist()
def procesa_informacion_bancaria(bancos, cuentas_bancarias):
    print("ENTRE En procesa_informacion _bancaria")
    # Obteniendo los datos de los bancos y despues procesar las cuentas del mismo
    for banco in bancos:
        entfinancodigo = banco["EntFinanCodigo"]
        # Obteniendo las cuentas bancarias correspondientes al banco
        cuentas_bancarias_del_banco = [cuenta for cuenta in cuentas_bancarias if cuenta.get("EntFinanCodigo") == entfinancodigo]
        
        # Chequeando si el banco ya esta insertado para obtener el id y sino se crea nuevo y se obtiene el id
        existe_banco = frappe.db.exists("Bank", {"bank_name": banco["EntFinanDescripcion"]})
        
        if existe_banco:
            banco_id = frappe.get_value("Bank", {"bank_name": banco["EntFinanDescripcion"]}, "name")
            resultado_banco = actualizar_banco(banco_id, banco)
            
        else:
            resultado_banco = crear_banco(banco)
            if resultado_banco is None:
                print("No se pudo insertar el banco")
            else:
                print(f"Se inserto el banco {resultado_banco.bank_name}")
                banco_id = resultado_banco
                
        # ya procesado el banco paso a procesar las cuentas bancarias de ese banco
        for cuenta_bancaria in cuentas_bancarias_del_banco:
            
            existe_cuenta_bancaria = frappe.db.exists("Bank Account", 
                                                      {
                                                          "custom_clidbcuenta": cuenta_bancaria["CliDBCuenta"],
                                                          "account_name": cuenta_bancaria["CliDBTitular"]
                                                       })
            if existe_cuenta_bancaria:
                # Actualizar los datos de la cuenta bancaria
                actualiza_cuenta_bancaria(banco_id, cuenta_bancaria)
            else:
                # Crear cuenta bancaria
                crear_cuenta_bancaria(banco_id, cuenta_bancaria)

    return {"success": True, "message": "Procesados los datos bancarios"}


# Funcion para actualizar los datos del banco
def actualizar_banco(banco_name, banco):
    banco_doc = frappe.get_doc("Bank", {"bank_name": banco_name})
    banco_doc.address_html = banco["EntFinanDireccion"]
    banco_doc.custom_entfinancodigo = banco["EntFinanCodigo"]
    banco_doc.save()
    return{ banco_doc}
    
    
# Funcion para crear el nuevo banco
def crear_banco(banco):
    print(f"Entre en crear banco {banco}")
    nuevo_banco = frappe.get_doc(
        {
            "doctype": "Bank",
            "bank_name": banco["EntFinanDescripcion"],
            "address_html": banco["EntFinanDireccion"],
            "custom_entfinancodigo": banco["EntFinanCodigo"]
        }
    )
    
    try:
        nuevo_banco.insert()
        frappe.db.commit()
        
        # Verificando si se inserto
        if frappe.db.exists("Bank", {"custom_entfinancodigo": banco["EntFinanCodigo"]}):
            print(f"Banco Insertado correctamente: {nuevo_banco.bank_name}")            
            return nuevo_banco
        else:
            print("Error al insertar banco")
            return None
            
    except Exception as e:
        print(f"Ocurrio un error al insertat el banco: {e}")
        return None

# Funcion para actualizar la cuenta bancaria
def actualiza_cuenta_bancaria(banco_id, cuenta_bancaria):
    moneda = busca_moneda(cuenta_bancaria["CliDBCodMon"])
    print(f"Moneda: {moneda} de la cuenta {cuenta_bancaria['CliDBTitular']}")
    cuenta_bancaria_doc = frappe.get_doc("Bank Account", {"custom_clidbcuenta": cuenta_bancaria["CliDBCuenta"], "account_name": cuenta_bancaria["CliDBTitular"]})
    cuenta_bancaria_doc.account_name = cuenta_bancaria["CliDBTitular"]
    cuenta_bancaria_doc.bank = banco_id
    cuenta_bancaria_doc.custom_clidbcuenta = cuenta_bancaria["CliDBCuenta"]
    cuenta_bancaria_doc.custom_clidbswift = cuenta_bancaria["CliDBSWIFT"]
    cuenta_bancaria_doc.custom_clidbcodmon = moneda if moneda else None
    cuenta_bancaria_doc.custom_clidbnrotransit = cuenta_bancaria["CliDBNroTransit"]
    cuenta_bancaria_doc.save()
    return {"success": True, "message":f"Actualizada la cuenta bancaria {cuenta_bancaria_doc.account_name}"}

# Funcion para crear la cuenta bancaria
def crear_cuenta_bancaria(banco_id, cuenta_bancaria):
    moneda = busca_moneda(cuenta_bancaria["CliDBCodMon"])
    nueva_cuenta_bancaria = frappe.get_doc(
        {
            "doctype": "Bank Account",
            "account_name": cuenta_bancaria["CliDBTitular"],
            "bank": banco_id,
            "custom_clidbcuenta": cuenta_bancaria["CliDBCuenta"],
            "custom_clidbswift": cuenta_bancaria["CliDBSWIFT"],
            "custom_entfinancodigo": cuenta_bancaria["EntFinanCodigo"],
            "custom_clicodigo": cuenta_bancaria["CliCodigo"],
            "custom_clidbid": cuenta_bancaria["CliDBId"],
            "custom_clidbcodmon": moneda if moneda else None,
            "custom_clidbnrotransit": cuenta_bancaria["CliDBNroTransit"]
        }
    )
    nueva_cuenta_bancaria.insert()
    return {"success": True, "message": f"Creado nueva cuenta bancaria { nueva_cuenta_bancaria.account_name}"}
    
    
# Funcion para buscar el id de la moneda de la cuenta bancaria
def busca_moneda(dato_moneda):
    moneda_id = frappe.get_value("NomMonedas", {"moncodigo": dato_moneda})
    return moneda_id