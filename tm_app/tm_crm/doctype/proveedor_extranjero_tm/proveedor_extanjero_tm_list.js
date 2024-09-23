frappe.listview_settings['Proveedor Extranjero TM'] = {
    onload: function (listview) {
        listview.page.add_inner_button(__('Importar JSON'), function () {
            // frappe.show_alert({ message: __('Procesando la información'), indicator: 'green' });
            frappe.call({
                method: "tm_app.utils.importa_nomenclador.import_nomenclador",
                args: {
                    doctype: "PROVEEDOR_EXTRANJERO"
                },
                callback: function (response) {
                    // console.log('response.message: ', response.message)
                    if (response.message) {
                        // Procesando el JSON
                        var json = response.message;
                        var proveedor_extranjero = json.PROVEEDOR_EXTRANJERO;
                        var total = proveedor_extranjero.length;
                        console.log("Total a procesar: ", total)

                        // var processed = 0;
                        for (var i in proveedor_extranjero) {
                            var item = proveedor_extranjero[i];
                            console.log('Procesando Proveedor: ', item.CliDescripcion, 'Organismo', item.OrganCodigo, 'Pais', item.CliPaisCodIntern, 'CliPaisCodIntern')
                            frappe.call({
                                method: "tm_app.tm_crm.doctype.proveedor_extranjero_tm.proveedor_extranjero_tm.inserta_actualiza_proveedor_ext",
                                args: item,
                                callback: function (response) {
                                    console.log("Callback:", response.message);
                                },
                                error: function (err) {
                                    console.error("Error al insertar o actualizar: ", err)
                                }
                            });
                        }
                        frappe.show_alert({ message: __('Accion completada'), indicator: 'green' });
                    } else {
                        frappe.show_alert({ message: __('No se recibió respuesta del servidor'), indicator: 'red' });
                    }
                },
                error: function (err) {
                    frappe.show_alert({ message: __('Error al ejecutar la accion: ' + err.message), indicator: 'red' });
                }
            });
        });
    }
};