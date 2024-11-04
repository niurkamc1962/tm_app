frappe.listview_settings["NomReeup"] = {
  onload: function (listview) {
    if (frappe.user.has_role("Administrator")) {
      listview.page.add_inner_button(__("Importar JSON"), function () {
        frappe.call({
          method: "tm_app.utils.importa_nomenclador.import_nomenclador",
          args: {
            doctype: "TEREEUP",
          },
          callback: function (response) {
            if (response.message) {
              var json = response.message;
              var nom_reeup = json.TEREEUP_faltan;
              var total = nom_reeup.length;

              for (var i in nom_reeup) {
                (function (item) {
                  // Usar una función de cierre para capturar el valor de 'item'
                  frappe.call({
                    method:
                      "tm_app.tm_sgc.doctype.nomreeup.nomreeup.inserta_actualiza_reeup",
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
                        "REEUP: ",
                        item.ReeupCod
                      );
                      // console.log('Problema con el ', item.ReeupCod, ' - ', item.ReeupNom);
                    },
                  });
                })(nom_reeup[i]); // Llamar a la función inmediatamente con el valor actual
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
