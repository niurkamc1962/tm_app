# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document
import os


class NomProvincias(Document):
    # def get_display_value(self):
    #     return f"{self.provcod} - {self.provnombre}"
    pass


@frappe.whitelist()
def inserta_actualiza_provincias(dato_provcod, dato_provnombre):

    try:
        # verificando si ya existe
        existe_provincia = frappe.db.exists(
            "NomProvincias", {"provdoc": dato_provcod})

        print(
            f"[Resultado] existe_provincia: {existe_provincia} | [Codigo Provincia]: {dato_provcod} | [Nombre Provincia]: {dato_provnombre}")

        if existe_provincia:
            # actualizar el registro
            doc = frappe.get_doc("NomProvincias", existe_provincia)
            doc.provnombre = dato_provnombre
            doc.save()
            return {"success": True, "message": f"Provincia {dato_provnombre} Codigo {dato_provcod} actualizado"}
        else:
            # insertar nuevo registro
            new_doc = frappe.get_doc({
                "doctype": "NomProvincias",
                "provcod": dato_provcod,
                "provnombre": dato_provnombre
            })
            new_doc.insert()
            return {"success": True, "message": f"insertado {dato_provnombre} - {dato_provcod} "}
    except frappe.exceptions.ValidationError as e:
        return {"message": f"Error al insertar o actualizar: {dato_provnombre} con {dato_provcod}, {str(e)}"}
    
    

@frappe.whitelist()
def importar_municipios():
    # Ruta al archivo JSON
    #json_file_path = "/home/niurka/Proyectos/frappe/nomencladores-json/TEMUNICIPIOS.json"
    json_file_path = os.path.join(frappe.get_app_path('tm_app'),'archivos-json-a-importar','TEMUNICIPIOS.json')
    url = json_file_path.format('TEMUNICIPIOS')
    
    # Lista para almacenar resultados de la importacion
    resultados = []
    
    try:
        with open(url, 'r') as f:
            data = json.load(f)
            # print(f'Datos leídos del JSON: {data}')  # Verifica el contenido del JSON

        try:
            for item in data['TEMUNICIPIOS']:
                provcod = item['ProvCod']
                municnombre = item['MunicNombre']
                municcod = item['MunicCod']
                
                print(f'Provcod: {provcod} MunicCod: {municcod} MunicNombre: {municnombre}')

                # Verificar si la provincia existe
                if not frappe.db.exists('NomProvincias', provcod):
                    resultados.append(f'La provincia {provcod} no existe. Saltando municipio {municnombre}.')
                    continue

                # Obtener el documento de la provincia
                provincia_doc = frappe.get_doc('NomProvincias', provcod)
                print(f'provincia: {provincia_doc.provcod}')
                
                # Verificar si el municipio ya existe
                existe_municipio = frappe.db.exists('NomMunicipios', {'provcod': provcod, 'municcod': municcod})
                print(f'existe_municipio: {existe_municipio}')

                if existe_municipio:
                    # Actualizar el registro existente
                    municipio_doc = frappe.get_doc('NomMunicipios', existe_municipio)
                    if municipio_doc:  # Verifica que municipio_doc no sea None
                        municipio_doc.municnombre = municnombre
                        municipio_doc.save()
                        resultados.append(f'Municipio {municnombre} actualizado.')
                    else:
                        resultados.append(f'Error al encontrar el municipio con código {municcod}.')
                else:
                    # Insertar nuevo registro
                    try:
                        # agregar nuevo municipio a la tabla de municipios en la provincia
                        provincia_doc.append('municipios', {
                            'municnombre': municnombre,
                            'municcod': municcod,
                            'provcod': provcod
                        })
                        provincia_doc.save()
                        resultados.append(f'Municipio {municnombre} importado con éxito.')
                    except Exception as e:
                        resultados.append(f'Error al insertar el municipio {municnombre}: {str(e)}')
                        print(f'Error al insertar el municipio:  {str(e)}')
            return {'resultados': resultados}
        
        except Exception as e:
            print(f'Error al procesar los municipios: {str(e)}')
            return {'error': f'Error al procesar los municipios: {str(e)}'}

        # Devolver los resultados
        return {'resultados': resultados}
    
    except Exception as e:
        print(f'Error al importar los municipios: {str(e)}')
        return {'error': f'Error al importar los municipios: {str(e)}'}
