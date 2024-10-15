import frappe
from frappe import _

def get_context(context):
    context.redirect_url = frappe.utils.get_url('/tmweb/index')