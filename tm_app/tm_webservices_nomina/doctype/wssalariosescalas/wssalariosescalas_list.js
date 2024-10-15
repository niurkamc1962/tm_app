frappe.listview_settings["WSSalariosEscalas"] = {
  onload: function (listview) {
    if (frappe.user.has_role("Administrator")) {
      listview.page.add_inner_button(__("Sincronizar WebService"), function () {
        // frappe.show_alert({ message: __('Procesando la información'), indicator: 'green' });
        frappe.call({
          method: "tm_app.utils.webservice_nomina.sync_webservice",
          args: {
            doctype: "WSSalariosEscalas",
          },
          callback: function (response) {
            // console.log('response.message: ', response.message)
            if (response.message) {
              // Procesando el JSON
              var json = response.message;
              var sdtwsalariosescalas = json.SdtWSSalariosEscalas;
              var total = sdtwsalariosescalas.length;
              console.log("Total a procesar: ", total);

              // var processed = 0;
              for (var i in sdtwsalariosescalas) {
                var item = sdtwsalariosescalas[i];
                console.log("Procesando: ", item);
                console.log("SalEscId: ", item.SalEscId);
                frappe.call({
                  method:
                    "tm_app.tm_webservices_nomina.doctype.wssalariosescalas.wssalariosescalas.inserta_actualiza_salariosescalas",
                  args: {
                    salesc_id: item.SalEscId,
                    salesc_codigo: item.SalEscCodigo,
                    salesc_salarioescala: item.SalEscSalarioEscala,
                    escs_id: item.EscSId,
                    ressalesc_id: item.ResSalEscId,
                    res_descripcion: item.ResDescripcion,
                    escs_descripcion: item.EscSDescripcion,
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
