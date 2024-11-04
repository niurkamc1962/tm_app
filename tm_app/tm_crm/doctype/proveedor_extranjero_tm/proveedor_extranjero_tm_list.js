frappe.listview_settings["Proveedor Extranjero TM"] = {
  onload: function (listview) {
    if (frappe.user.has_role("Administrator")) {
      listview.page.add_inner_button(__("Importar Proveedores"), function () {
        frappe.call({
          method: "tm_app.utils.importa_nomenclador.import_nomenclador",
          args: {
            doctype: "PROVEEDOR_EXTRANJERO",
          },
          callback: function (response) {
            if (response.message) {
              var json = response.message;
              var proveedor_extranjero = json.PROVEEDOR_EXTRANJERO;

              for (var i in proveedor_extranjero) {
                (function (item) {
                  // Usar una función de cierre para capturar el valor de 'item'
                  frappe.call({
                    method:
                      "tm_app.tm_crm.doctype.proveedor_extranjero_tm.proveedor_extranjero_tm.inserta_actualiza_proveedor_extranjero",
                    args: {
                      dato: item,
                    },
                    callback: function (response) {
                      if (response.message) {
                        console.log("Callback:", response.message);
                        frappe.show_alert({
                          message:  __("Proveedor ") + item.CliDescripcion + __(" insertado o actualizado correctamente."),
                          indicator: "green",
                        });
                      }
                    },
                    error: function (err) {
                      console.error("Error al insertar o actualizar: ", err);
                      frappe.show_alert({
                        message:
                          __("Error al insertar o actualizar") + item.CliDescripcion + err.message,
                        indicator: "red",
                      });
                    },
                  });
                })(proveedor_extranjero[i]); // Llamar a la función inmediatamente con el valor actual
              }
              frappe.show_alert({
                message: __("Accion completada"),
                indicator: "green",
              });
            } else {
              frappe.show_alert({
                message: __("No se recibió respuesta del servidor"),
                indicator: "red",
              });
            }
          },
          error: function (err) {
            frappe.show_alert({
              message: __("Error al ejecutar la accion: " + err.message),
              indicator: "red",
            });
          },
        });
      });

      // Creando el boton para importar los contactos
      const importContactButton = listview.page.add_inner_button(
        __("Importar Contactos"),
        function () {
          // Verificando si hay proveedores en el doctype para importar los contactos
          frappe.call({
            method: "frappe.client.get_list",
            args: {
              doctype: "Proveedor Extranjero TM",
              fields: ["name"], // Solo se necesita el nombre o ID para verificar si hay datos en el doctype
            },
            callback: function (response) {
              if (response.message && response.message.length > 0) {
                // Existe al menos un proveedor por lo que paso a procesar los contactos
                frappe.call({
                  method: "tm_app.utils.importa_nomenclador.import_nomenclador",
                  args: {
                    doctype: "SCOCLIENTECONTACTOS_EXT",
                  },
                  callback: function (response) {
                    if (response.message) {
                      var json = response.message;
                      var clientes_contactos_ext = json.SCOCLIENTECONTACTOS_EXT;

                      for (var i in clientes_contactos_ext) {
                        (function (dato) {
                          frappe.call({
                            method:
                              "tm_app.tm_crm.doctype.proveedor_extranjero_tm.proveedor_extranjero_tm.inserta_actualiza_contactos_proveedor_ext",
                            args: {
                              contacto: dato,
                            },
                            callback: function (response) {
                              if (response.message) {
                                console.log("Callback:", response.message);
                                frappe.show_alert({
                                  message:  __("Contacto ") + dato.CliContacNombre + __(" insertado o actualizado correctamente."),
                                  indicator: "green",
                                });
                              }
                            },
                            error: function (err) {
                              console.error(
                                "Error al insertar o actualizar: ",
                                err
                              );
                              frappe.show_alert({
                                 message:  __("Contacto ") + dato.CliContacNombre + __(" ERROR al insertar o actualizar"),
                                indicator: "red",
                              });
                            },
                          });
                        })(clientes_contactos_ext[i]);
                      }

                      frappe.show_alert({
                        message: __("Contactos importados correctamente"),
                        indicator: "green",
                      });
                    } else {
                      frappe.show_alert({
                        message: __("No se obtuvo respuesta del servidor"),
                        indicator: "red",
                      });
                    }
                  },
                  error: function (err) {
                    frappe.show_alert({
                      message: __(
                        "Error al ejecutar la accion: " + err.message
                      ),
                      indicator: "red",
                    });
                  },
                });
              } else {
                // No hay proveedores por lo que se muestra advertencia
                frappe.show_alert({
                  message: __(
                    "No hay proveedores insertados, No se pueden importar los contactos"
                  ),
                  indicator: "orange",
                });
              }
            },
          });
        }
      );

      // Inicialmente, deshabilitar el botón de importar contactos
      importContactButton.prop("disabled", true);

      // Verificar si hay proveedores al cargar la lista
      frappe.call({
        method: "frappe.client.get_list",
        args: {
          doctype: "Proveedor Extranjero TM",
          fields: ["name"],
        },
        callback: function (response) {
          if (response.message && response.message.length > 0) {
            // Habilitar el botón si hay proveedores
            importContactButton.prop("disabled", false);
          }
        },
      });
    }
  },
};
