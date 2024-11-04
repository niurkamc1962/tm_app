frappe.listview_settings['Archivos PDF'] = {
    add_fields: ['estado_archivo'],
    hide_name_column: true,
    
    
    button: {
        show(doc) {
            // console.log('Estado Archivo:', doc.estado_archivo); // mostrando por consola el estado
            return doc.estado_archivo === 'Pendiente';  // Muestra el boton solo si el estado es Pendiente
        },
        get_label() {
            return __('Procesar');
        },
        get_description(doc) {
            return true;
        },
        action(doc) {
            frappe.msgprint(__('Procesando'));
        }
    },

    on_page_load: function(listview) {
        frappe.db.get_doc('Archivos PDF', null, { estado_archivo: 'Pendiente' })
            .then(doc => {
                console.log(doc)
            })

        // Agregando evento al hacer clic en la ruta del archivo para mostrar el contenido
        listview.on("click", ".file-name", function() {
            var ruta_archivo = $(this).data("ruta");
            if (ruta_archivo) {
                window.open(ruta_archivo, "_blank");
            } else {
                frappe.msgprint(__("La ruta del archivo no existe"));
            }
        });

    }
};

// Funcion para refrescar el listview y obtener solo los archivos pendientes
function refresh_listview(listview){
    frappe.call({
        method: 'frappe.db.get_list',
        args: {
            doctype: 'Archivos PDF',
            filters: { 'estado_archivo': 'Pendiente' }
        },
        callback: function(data) {
            console.log('Datos de la API:', data)
            if (data.message) {
                listview.update(data.message)
                console.log('Filtrados: ', data.message);
            } else {
                console.error('No se recibieron datos validos')
            }
            
        }
    });
}