frappe.listview_settings['Archivos PDF'] = {
    on_page_load: function(listview) {
        // Agregando evento al hacer clic en el nombre del archivo
        listview.on("click", ".file-name", function() {
            var ruta_archivo = $(this).data("ruta");
            if (ruta_archivo) {
                window.open(ruta_archivo, "_blank");
            } else {
                frappe.msgprint(__("La ruta del archivo no existe"));
            }
        });

        // Agregar evento al cambiar el estado de selección
        listview.on('check', function() {
            var selected = listview.get_checked_items();
            if (selected.length > 0) {
                // Confirmar eliminación
                frappe.confirm(
                    __('¿Está seguro de que desea eliminar los archivos seleccionados?'),
                    function() {
                        selected.forEach(function(item) {
                            frappe.call({
                                method: 'tm_app.tm_crm.archivos_pdf.eliminar_archivo_pdf',
                                args: { archivo_id: item.name },
                                callback: function(r) {
                                    if (r.message) {
                                        frappe.msgprint(__('Archivo eliminado con éxito'));
                                        listview.refresh(); // Refrescar la lista
                                    }
                                },
                            });
                        });
                    },
                    function() {
                        frappe.msgprint(__('Proceso cancelado'));
                    }
                );
            }
        });
    }
};