import frappe
from frappe import _

def get_context(context):
    # Verifica si esta autenticado
    if frappe.session.user != "Guest":
        # redirige al portal
        context.redirect_to = "/tmweb/index"
    else:
        context.message = _("Por favor inicia session para acceder al Portal")
        
    return context