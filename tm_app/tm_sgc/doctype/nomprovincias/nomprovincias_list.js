frappe.listview_settings['NomProvincias'] = {
    onload: function (listview) {
        // Verificar si el usuario tiene el rol de Administrator
        if (frappe.user.has_role('Administrator')) { 
            // Botón para importar provincias
            listview.page.add_inner_button(__('Importar Provincias'), function () {
                frappe.call({
                    method: "tm_app.utils.importa_nomenclador.import_nomenclador",
                    args: {
                        doctype: "TEPROVINCIA"
                    },
                    callback: function (response) {
                        if (response.message) {
                            var json = response.message;
                            var nom_provincias = json.TEPROVINCIA;
                            console.log("Total a procesar: ", nom_provincias.length);

                            var promises = [];

                            for (let i in nom_provincias) {
                                let item = nom_provincias[i];
                                console.log("Procesando Provincia: ", item.ProvCod, "Nombre", item.ProvNombre);
                                
                                promises.push(new Promise((resolve, reject) => {
                                    frappe.call({
                                        method: "tm_app.tm_sgc.doctype.nomprovincias.nomprovincias.inserta_actualiza_provincias",
                                        args: {
                                            dato_provcod: item.ProvCod,
                                            dato_provnombre: item.ProvNombre
                                        },
                                        callback: function (response) {
                                            if (response.message) {
                                                resolve(response.message);
                                            } else {
                                                if (response.exc && response.exc.indexOf("duplicate") !== -1) {
                                                    console.warn("Registro ya existe, ignorado: ", item.ProvCod);
                                                    resolve("Registro ya existe, ignorado");
                                                } else {
                                                    reject("Error en la inserción: " + JSON.stringify(response));
                                                }
                                            }
                                        },
                                        error: function (err) {
                                            reject("Error de llamada: " + err.message);
                                        }
                                    });
                                }));
                            }

                            Promise.all(promises).then(() => {
                                frappe.show_alert({ message: __('Acción completada'), indicator: 'green' });
                            }).catch(err => {
                                console.error("Error al procesar provincias: ", err);
                                frappe.show_alert({ message: __('Error al procesar provincias: ' + err), indicator: 'red' });
                            });
                        } else {
                            frappe.show_alert({ message: __('No se recibió respuesta del servidor'), indicator: 'red' });
                        }
                    },
                    error: function (err) {
                        frappe.show_alert({ message: __('Error al ejecutar la acción: ' + err.message), indicator: 'red' });
                    }
                });
            });

            // Botón para importar municipios
            listview.page.add_inner_button(__('Importar Municipios'), function () {
                frappe.call({
                    method: "tm_app.utils.importa_nomenclador.import_nomenclador",
                    args: {
                        doctype: "TEMUNICIPIOS"
                    },
                    callback: function (response) {
                        if (response.message) {
                            var json = response.message;
                            var nom_municipios = json.TEMUNICIPIOS;
                            console.log("Total a procesar: ", nom_municipios.length);

                            var promises = [];

                            for (let i in nom_municipios) {
                                let item = nom_municipios[i];
                                console.log("Procesando Municipio: ", item.MunicCod, "Nombre", item.MunicNombre);
                                
                                promises.push(new Promise((resolve, reject) => {
                                    frappe.call({
                                        method: "tm_app.tm_sgc.doctype.nommunicipios.nommunicipios.inserta_actualiza_municipios",
                                        args: {
                                            dato_provcod: item.ProvCod,
                                            dato_municnombre: item.MunicNombre,
                                            dato_municcod: item.MunicCod
                                        },
                                        callback: function (response) {
                                            if (response.message) {
                                                resolve(response.message);
                                            } else {
                                                if (response.exc && response.exc.indexOf("duplicate") !== -1) {
                                                    console.warn("Registro ya existe, ignorado: ", item.MunicCod);
                                                    resolve("Registro ya existe, ignorado");
                                                } else {
                                                    reject("Error en la inserción: " + JSON.stringify(response));
                                                }
                                            }
                                        },
                                        error: function (err) {
                                            reject("Error de llamada: " + err.message);
                                        }
                                    });
                                }));
                            }

                            Promise.all(promises).then(() => {
                                frappe.show_alert({ message: __('Acción completada'), indicator: 'green' });
                            }).catch(err => {
                                console.error("Error al procesar municipios: ", err);
                                frappe.show_alert({ message: __('Error al procesar municipios: ' + err), indicator: 'red' });
                            });
                        } else {
                            frappe.show_alert({ message: __('No se recibió respuesta del servidor'), indicator: 'red' });
                        }
                    },
                    error: function (err) {
                        frappe.show_alert({ message: __('Error al ejecutar la acción: ' + err.message), indicator: 'red' });
                    }
                });
            });
        }
    }
};