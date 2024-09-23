frappe.listview_settings['NomMonedas'] = {
    onload: function (listview) {
        if (frappe.user.has_role('Administrator')) { 
            listview.page.add_inner_button(__('Importar Monedas'), function () {
                // frappe.show_alert({ message: __('Procesando la información'), indicator: 'green' });
                frappe.call({
                    method: "tm_app.utils.importa_nomenclador.import_nomenclador",
                    args: {
                        doctype: "SMGNOMMONEDAS"
                    },
                    callback: function (response) {
                        // console.log('response.message: ', response.message)
                        if (response.message) {
                            // Procesando el JSON
                            var json = response.message;
                            var nom_monedas = json.SMGNOMMONEDAS;
                            var total = nom_monedas.length;
                            console.log("Total a procesar: ", total)

                            // var processed = 0;
                            for (var i in nom_monedas) {
                                var item = nom_monedas[i];
                                console.log('Procesando Moneda: ', item.MonCodigo, 'Descripcion', item.MonDescrip, 'MonPais', item.MonPais, 'PaisCodIntern')
                                frappe.call({
                                    method: "tm_app.tm_sgc.doctype.nommonedas.nommonedas.inserta_actualiza_monedas",
                                    args: {
                                        dato_moncodigo: item.MonCodigo,
                                        dato_monsiglas: item.MonSiglas,
                                        dato_mondescrip: item.MonDescrip,
                                        dato_monflag: item.MonFlag,
                                        dato_monfechamodif: item.MonFechaModif,
                                        dato_monui: item.MonUI,
                                        dato_monpais: item.MonPais,
                                        dato_paiscodintern: item.PaisCodIntern
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
    }
};