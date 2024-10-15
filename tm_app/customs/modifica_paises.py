from frappe import _
import frappe
from frappe.model.document import Document
import json


@frappe.whitelist()
def leer_pais_json():
    """ Cargar los archivos JSON y devuelve los datos de SCOPAIS y un diccionario de nombre de paises. """
    url_json_scopais = "/home/niurka/Proyectos/frappe/nomencladores-json/SCOPAIS.json"
    url_json_country = "/home/niurka/Proyectos/frappe/nomencladores-json/countries.json"

    try:
        # Leer el archivo SCOPAIS.json
        with open(url_json_scopais, 'r') as fichero:
            data_scopais = json.load(fichero)
            scopais_data = data_scopais['SCOPAIS']

        # Leer el archivo country.json
        with open(url_json_country, 'r') as fichero:
            data_country = json.load(fichero)
            country_data = data_country['countries']

        # Crear un diccionario para mapear nombre de paises en espanol a ingles
        country_name_map = {item['es_name']: item['name']
                            for item in country_data}

        return scopais_data, country_name_map

    except FileNotFoundError:
        print(f"Uno de los archivos JSON no existe",
              "Error al leer JSON")
        return [], {}  # Devuelve listas vacias en caso de error


@frappe.whitelist()
def procesa_pais_json(custom_paiscodintern, pais_descripcion, custom_pais_siglas, custom_pais_seleccionado):
    print(f"Pais {pais_descripcion} seleccionado:  {custom_pais_seleccionado} con codigo interno {custom_paiscodintern} y siglas {custom_pais_siglas}")

    """ Procesa un pais y verifica si ya existe en la BD """
    scopais_data, country_name_map = leer_pais_json()

    # Asegurarse que los datos se cargaron correctamente
    if not scopais_data or not country_name_map:
        return _('Error: no se pudieron cargar los datos de los paises.')

    # Buscar el nombre en ingles del pais segun pais_descripcion
    country_name = country_name_map.get(pais_descripcion)

    if country_name:
        # Verificar si el pais ya existe en la base de datos
        existe_pais = frappe.db.exists(
            "Country", {"country_name": country_name})
        print(f"Buscando {country_name} resultado busqueda {existe_pais}")

        # Convirtiendo PaisSeleccionado de 'N'/'S' a True/False
        # pais_seleccionado = True if custom_pais_seleccionado == 'S' else False

        if existe_pais:
            print(
                f"País encontrado: {pais_descripcion} coincide nombres Por lo que lo actualizo")
            doc = frappe.get_doc("Country", country_name)
            doc.custom_paiscodintern = custom_paiscodintern
            doc.custom_pais_seleccionado = 'Yes' if custom_pais_seleccionado == 'S' else 'No'
            doc.custom_pais_siglas = custom_pais_siglas
            doc.save()
            return {"success": True, "message": f"Pais {custom_pais_seleccionado} Siglas {custom_pais_siglas} actualizado"}
        else:
            print(
                f"País NO encontrado: {pais_descripcion} Se crea nuevo")
            new_doc = frappe.new_doc("Country")
            new_doc.country_name = country_name
            new_doc.custom_paiscodintern = custom_paiscodintern
            new_doc.custom_pais_seleccionado = 'Yes' if custom_pais_seleccionado == 'S' else 'No'
            new_doc.custom_pais_siglas = custom_pais_siglas
            new_doc.insert()
            return {"success": True, "message": f"Nuevo Pais {custom_pais_seleccionado} Siglas {custom_pais_siglas} creado"}
    else:
        # entro por aqui cuando el pais_descripcion esta en ingles y no espanol

        print(
            f"No se encontró el nombre en inglés para el país: {pais_descripcion} por lo que paso a crearlo")
        # Antes de insertarlo se puede dar el caso que en Siscont el nombre este en Ingles y lo trata de insertar
        # por hacer la busqueda del nombre en Espanol por lo que pregunto por el pais_descripcion
        existe_pais = frappe.db.exists(
            "Country", {"country_name": pais_descripcion})
        if existe_pais:
            print(
                f"País encontrado: {pais_descripcion} coincide nombres Por lo que lo actualizo")
            doc = frappe.get_doc("Country", pais_descripcion)
            doc.custom_paiscodintern = custom_paiscodintern
            doc.custom_pais_seleccionado = 'Yes' if custom_pais_seleccionado == 'S' else 'No'
            doc.custom_pais_siglas = custom_pais_siglas
            doc.save()
            return {"success": True, "message": f"Pais {custom_pais_seleccionado} Siglas {custom_pais_siglas} actualizado"}
        else:
            new_doc = frappe.new_doc("Country")
            new_doc.country_name = pais_descripcion
            new_doc.custom_paiscodintern = custom_paiscodintern
            # new_doc.custom_pais_seleccionado = 'custom_pais_seleccionado == 'S''
            new_doc.custom_pais_siglas = custom_pais_siglas
            new_doc.insert()
            return {"success": True, "message": f"Nuevo Pais {custom_pais_seleccionado} Siglas {custom_pais_siglas} creado"}

    return 'Countries updated successfully'


@frappe.whitelist()
def actualizar_paises_desde_json():
    scopais_data, country_name_map = leer_pais_json()

    if not scopais_data or not country_name_map:
        return _('Error: No se pudieron cargar los datos de los paises en actualizad_desde_json')

    total_paises = len(scopais_data)
    print(f"Se encontraron {total_paises} países a procesar")

    for pais in scopais_data:
        procesa_pais_json(
            pais['PaisCodIntern'],
            pais['PaisDescripcion'],
            pais['PaisSiglas'],
            pais['PaisSeleccionado']
        )

    print('Finalizada la actualización de los países')
    return 'Países actualizados'
