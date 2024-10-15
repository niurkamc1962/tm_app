frappe.listview_settings["NomUniones"] = {
  onload: function (listview) {
    if (frappe.user.has_role("Administrator")) {
      listview.page.add_inner_button(__("Importar Uniones"), function () {
        // frappe.show_alert({ message: __('Procesando la información'), indicator: 'green' });
        frappe.call({
          method: "tm_app.utils.importa_nomenclador.import_nomenclador",
          args: {
            doctype: "SMGUNION",
          },
          callback: function (response) {
            // console.log('response.message: ', response.message)
            if (response.message) {
              // Procesando el JSON
              var json = response.message;
              var nom_uniones = json.SMGUNION;
              var total = nom_uniones.length;
              console.log("Total a procesar: ", total);

              // var processed = 0;
              for (var i in nom_uniones) {
                var item = nom_uniones[i];
                console.log(
                  "Procesando union: ",
                  item.UnionCodigo,
                  "organcodigo",
                  item.OrganCodigo
                );
                frappe.call({
                  method:
                    "tm_app.tm_sgc.doctype.nomuniones.nomuniones.inserta_actualiza_uniones",
                  args: {
                    dato_organcodigo: item.OrganCodigo,
                    dato_unioncodigo: item.UnionCodigo,
                    dato_descripcion: item.UnionDescripcion,
                    dato_unionui: item.UnionUI,
                    dato_unionfechamodif: item.UnionFechaModif,
                    dato_unionactivo: item.UnionActivo,
                  },
                  callback: function (response) {
                    console.log("Callback:", response.message);
                  },
                  error: function (err) {
                    console.error("Error al insertar o actualizar: ", err);
                  },
                });
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
