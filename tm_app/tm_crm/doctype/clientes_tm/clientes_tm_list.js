frappe.listview_settings["Clientes TM"] = {
  onload: function (listview) {
    if (frappe.user.has_role("Administrator")) {
      listview.page.add_inner_button(
        __("Importar Clientes TM con sus Contactos"),
        function () {
          frappe.call({
            method: "tm_app.utils.importa_nomencladores.import_nomencladores",
            args: {
              doctype_a: "CLIENTES_TM_C",
              doctype_b: "SCOCLIENTECONTACTOS_NAC",
            },
            callback: function (response) {
              if (response.message) {
                var json = response.message
                var clientes_tm = json.doctype_a;
                var contactos_nac = json.doctype_b;

                // Contador para verificar si todas las inserciones están completas
                let totalItems = clientes_tm.length;
                let processedItems = 0;

                // Procesar cada cliente
                for (var i in clientes_tm) {
                  (function (item) {
                    // console.log("Datos a enviar: ", item);
                    frappe.call({
                      method:
                        "tm_app.tm_crm.doctype.clientes_tm.clientes_tm.inserta_actualiza_cliente_tm",
                      args: {
                        dato: item,
                        contactos_json: JSON.stringify(contactos_nac)
                      },
                      callback: function (response) {
                        if (response.message) {
                          console.log("Cliente Insertado:", response.message);
                          frappe.show_alert({
                            message:
                              __("Cliente ") +
                              item.CliDescripcion +
                              __(" insertado o actualizado correctamente."),
                            indicator: "green",
                          });
                        } else {
                          console.error("Respuesta inesperada: ", response);
                          frappe.show_alert({
                            message: __("No se recibio cliente valido"),
                            indicator: 'red'
                          });
                        }
                        
                        processedItems++;
                        checkCompletion();
                      },
                      error: function (err) {
                        // console.error("Error al insertar o actualizar:", err);
                        frappe.show_alert({
                          message:
                            __("Error al insertar o actualizar") +
                            item.CliDescripcion +
                            err.message,
                          indicator: "red",
                        });
                        processedItems++;
                        checkCompletion();
                      },
                    });
                  })(clientes_tm[i]);
                }

                // Función para procesar contactos
                function processContactos(contactos) {
                  console.log("Entre en procesar contacto: ", contactos)
                  for (let j = 0; j < contactos.length; j++) {
                    // Cambiar var a let
                    let contacto = contactos[j]; // Captura el contacto actual

                    console.log("Contacto:", contacto); // Ahora contacto está definido
                    console.log(typeof contacto);

                    // Verificando que contacto sea un objeto
                    if (typeof contacto !== 'object' || contacto === null){
                      console.error('El contacto no es un objecto valido: ', contacto);
                      continue; //saltando el contacto que no es valido
                    }

                    (function (contacto) {                      
                      frappe.call({
                        method:
                          "tm_app.tm_crm.doctype.clientes_tm.clientes_tm.inserta_actualiza_contactos_clientes_tm",
                        args: {
                          contacto: contacto,
                        },
                        callback: function (response) {
                          if (response.message) {
                            console.log(
                              "Contacto insertado:",
                              response.message
                            );
                          }
                          processedItems++;
                          checkCompletion();
                        },
                        error: function (err) {
                          console.error("Error al insertar el contacto:", err);
                          frappe.show_alert({
                            message:
                              __("Error al insertar contacto") +
                              contacto.CliContacNombre +
                              err.message,
                            indicator: "red",
                          });
                          processedItems++;
                          checkCompletion();
                        },
                      });
                    })(contacto); // Aquí contacto tiene el valor correcto
                  }
                }

                // Función para verificar si todos los elementos han sido procesados
                function checkCompletion() {
                  if (processedItems === totalItems + contactos_nac.length) {
                    frappe.show_alert({
                      message: __("Acción completada"),
                      indicator: "green",
                    });
                  }
                }
              } else {
                frappe.show_alert({
                  message: __("No se recibió respuesta del servidor"),
                  indicator: "red",
                });
              }
            },
            error: function (err) {
              frappe.show_alert({
                message: __("Error al ejecutar la acción: ") + err.message,
                indicator: "red",
              });
            },
          });
        }
      );
    }
  },
};
