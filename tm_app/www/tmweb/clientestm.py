import frappe

def get_context(context):
    context.clientes = frappe.get_all('Clientes', fields=['nombre'])
        
    return context