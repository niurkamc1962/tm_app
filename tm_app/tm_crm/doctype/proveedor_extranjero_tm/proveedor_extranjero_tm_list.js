frappe.listview_settings["Proveedor Extranjero TM"] = {
  onload: function (listview) {b
    if (frappe.user.has_role("Administrator")) {
      listview.page.add_inner_button(__("Importar JSON"), function () {
        frappe.call({
          method: "tm_app.utils.importa_nomenclador.import_nomenclador",
          args: {
            doctype: "PROVEEDOR_EXTRANJERO",
          },
          callback: function (response) {
            if (response.message) {
              var json = response.message; 
              var proveedor_extranjero = json.PROVEEDOR_EXTRANJERO;
              var total = proveedor_extranjero.length;

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
                      console.log("Callback:", response.message);
                    },
                    error: function (err) {
                      console.error(
                        "Error al insertar o actualizar: ",
                        err,
                        "Proveedor: ",
                        item.CliCodigo
                      );
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
    }
  },
};