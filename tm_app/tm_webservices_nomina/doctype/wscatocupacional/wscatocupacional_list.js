frappe.listview_settings["WSCatOcupacional"] = {
  onload: function (listview) {
    if (frappe.user.has_role("Administrator")) {
      listview.page.add_inner_button(__("Sincronizar WebService"), function () {
        // frappe.show_alert({ message: __('Procesando la información'), indicator: 'green' });
        frappe.call({
          method: "tm_app.utils.webservice_nomina.sync_webservice",
          args: {
            doctype: "WSCatOcupacional",
          },
          callback: function (response) {
            if (response.message) {
              // Procesando el JSON
              var json = response.message;
              var sdtwscatocupacional = json.SdtWSCatOcupacional;
              var total = sdtwscatocupacional.length;
              console.log("Total a procesar: ", total);

              // var processed = 0;
              for (var i in sdtwscatocupacional) {
                var item = sdtwscatocupacional[i];
                // console.log("Procesando: ", item);
                // console.log('CargId: ', item.CargId)
                frappe.call({
                  method:
                    "tm_app.tm_webservices_nomina.doctype.wscatocupacional.wscatocupacional.inserta_actualiza_catocupacional",
                  args: {
                    categ_id: item.CategId,
                    categ_codigo: item.CategOCodigo,
                    categ_descripcion: item.CategODescripcion,
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
