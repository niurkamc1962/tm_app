frappe.listview_settings['Archivos PDF'] = {
    onload: function (listview) {
        if (frappe.user.has_role('Administrator')) { 
            listview.page.add_inner_button(__('Procesar Archivo'), function () {
                // Abrir modal para seleccionar el archivo
                frappe.prompt({
                    label: __('Selecciona un archivo')
                })
                
        }
    }
};