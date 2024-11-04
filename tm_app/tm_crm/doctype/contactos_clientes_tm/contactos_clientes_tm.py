# Copyright (c) 2024, Niurka and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ContactosClientesTM(Document):
    def autoname(self):
        # Obtener el clicodigo
        base_name = self.clicodigo
        # Generar un sufijo único
        suffix = self.get_next_suffix(base_name)
        self.name = f"{base_name}-{suffix.zfill(4)}"  # Asegurando que el sufijo tenga 4 dígitos

    def get_next_suffix(self, clicodigo):
        # Obtener los contactos existentes con el mismo clicodigo
        existing_contacts = frappe.get_all("Contactos Clientes TM", filters={"clicodigo": clicodigo}, fields=["name"])
        suffixes = [int(contact.name.split('-')[-1]) for contact in existing_contacts]  # Corregido para usar corchetes []
        return str(max(suffixes) + 1) if suffixes else '1'  # Comienza con '1' si no hay contactos existentes