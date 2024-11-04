frappe.listview_settings["WSColectivos"] = {
  onload: function (listview) {
    if (frappe.user.has_role("Administrator")) {
      listview.page.add_inner_button(__("Sincronizar WebService"), function () {
        // frappe.show_alert({ message: __('Procesando la información'), indicator: 'green' });
        frappe.call({
          method: "tm_app.utils.webservice_nomina.sync_webservice",
          args: {
            doctype: "WSColectivos",
          },
          callback: function (response) {
            // console.log('response.message: ', response.message)
            if (response.message) {
              // Procesando el JSON
              var json = response.message;
              var sdtwscolectivos = json.SdtWSColectivos;
              var total = sdtwscolectivos.length;
              console.log("Total a procesar: ", total);

              // var processed = 0;
              for (var i in sdtwscolectivos) {
                var item = sdtwscolectivos[i];
                console.log("Procesando: ", item);
                console.log("ColecId: ", item.ColecId);
                frappe.call({
                  method:
                    "tm_app.tm_webservices_nomina.doctype.wscolectivos.wscolectivos.inserta_actualiza_colectivos",
                  args: {
                    colec_id: item.ColecId,
                    colec_codigo: item.ColecCodigo,
                    colec_descripcion: item.ColecDescripcion,
                  },
                  callback: function (response) {
                    console.log(response.message);
                  },
                  error: function (err) {
                    console.error("Error al insertar o actualizar: ", err);
                  },
                });
              }
              frappe.show_alert({
                message: __("Sincronización completada"),
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
              message: __("Error al sincronizar: " + err.message),
              indicator: "red",
            });
          },
        });
      });
    }
  },
};
