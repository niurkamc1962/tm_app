import frappe

def redirecciona_workspace():
    user = frappe.session.user
    roles = frappe.get_roles(user)
    
    if "Tm CRM" in roles:
        frappe.set_route("workspace", "Tecnomatica")
    else:
        frappe.set_route("desk")
