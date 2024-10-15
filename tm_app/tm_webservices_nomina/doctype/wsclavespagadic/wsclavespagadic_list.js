frappe.listview_settings["WSClavesPagAdic"] = {
  onload: function (listview) {
    if (frappe.user.has_role("Administrator")) {
      listview.page.add_inner_button(__("Sincronizar WebService"), function () {
        // frappe.show_alert({ message: __('Procesando la información'), indicator: 'green' });
        frappe.call({
          method: "tm_app.utils.webservice_nomina.sync_webservice",
          args: {
            doctype: "WSClavesPagAdic",
          },
          callback: function (response) {
            // console.log('response.message: ', response.message)
            if (response.message) {
              // Procesando el JSON
              var json = response.message;
              var sdtwsclavespagadic = json.SdtWSClavesPagAdic;
              var total = sdtwsclavespagadic.length;
              console.log("Total a procesar: ", total);

              // var processed = 0;
              for (var i in sdtwsclavespagadic) {
                var item = sdtwsclavespagadic[i];
                console.log("Procesando: ", item);
                console.log("PagAdicId: ", item.PagAdicId);
                frappe.call({
                  method:
                    "tm_app.tm_webservices_nomina.doctype.wsclavespagadic.wsclavespagadic.inserta_actualiza_clavespagadic",
                  args: {
                    pagadic_id: item.PagAdicId,
                    pagadic_codigo: item.PagAdicCodigo,
                    pagadic_descripcion: item.PagAdicDescripcion,
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
