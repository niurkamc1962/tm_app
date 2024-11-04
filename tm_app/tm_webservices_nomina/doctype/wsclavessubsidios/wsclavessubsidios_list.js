frappe.listview_settings["WSClavesSubsidios"] = {
  onload: function (listview) {
    if (frappe.user.has_role("Administrator")) {
      listview.page.add_inner_button(__("Sincronizar WebService"), function () {
        // frappe.show_alert({ message: __('Procesando la información'), indicator: 'green' });
        frappe.call({
          method: "tm_app.utils.webservice_nomina.sync_webservice",
          args: {
            doctype: "WSClavesSubsidios",
          },
          callback: function (response) {
            // console.log('response.message: ', response.message)
            if (response.message) {
              // Procesando el JSON
              var json = response.message;
              var sdtwsclavessubsidios = json.SdtWSClavesSubsidios;
              var total = sdtwsclavessubsidios.length;
              console.log("Total a procesar: ", total);

              // var processed = 0;
              for (var i in sdtwsclavessubsidios) {
                var item = sdtwsclavessubsidios[i];
                console.log("Procesando: ", item);
                console.log("SubsidId: ", item.subsidId);
                frappe.call({
                  method:
                    "tm_app.tm_webservices_nomina.doctype.wsclavessubsidios.wsclavessubsidios.inserta_actualiza_clavessubsidios",
                  args: {
                    subsid_id: item.SubsidId,
                    subsid_codigo: item.SubsidCodigo,
                    subsid_descripcion: item.SubsidDescripcion,
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
