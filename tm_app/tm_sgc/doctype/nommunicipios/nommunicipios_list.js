frappe.listview_settings['NomMunicipios'] = {
    onload: function (listview) {
        listview.page.add_inner_button(__('Importar JSON'), function () {
            // frappe.show_alert({ message: __('Procesando la información'), indicator: 'green' });
            frappe.call({
                method: "tm_app.utils.importa_nomenclador.import_nomenclador",
                args: {
                    doctype: "TEMUNICIPIOS"
                },
                callback: function (response) {
                    // console.log('response.message: ', response.message)
                    if (response.message) {
                        // Procesando el JSON
                        var json = response.message;
                        var nom_municipios = json.TEMUNICIPIOS;
                        var total = nom_municipios.length;
                        console.log("Total a procesar: ", total)

                        // var processed = 0;
                        for (var i in nom_municipios) {
                            var item = nom_municipios[i];
                            console.log('Procesando Municipios: ', item.MunicCod, 'Nombre', item.MunicNombre)
                            frappe.call({
                                method: "tm_app.tm_sgc.doctype.nommunicipios.nommunicipios.inserta_actualiza_municipios",
                                args: {
                                    dato_provcod: item.ProvCod,
                                    dato_municnombre: item.MunicNombre,
                                    dato_municcod: item.MunicCod
                                },
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