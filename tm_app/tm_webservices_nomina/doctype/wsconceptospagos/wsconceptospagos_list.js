frappe.listview_settings["WSConceptosPagos"] = {
  onload: function (listview) {
    if (frappe.user.has_role("Administrator")) {
      listview.page.add_inner_button(__("Sincronizar WebService"), function () {
        // frappe.show_alert({ message: __('Procesando la información'), indicator: 'green' });
        frappe.call({
          method: "tm_app.utils.webservice_nomina.sync_webservice",
          args: {
            doctype: "WSConceptosPagos",
          },
          callback: function (response) {
            // console.log('response.message: ', response.message)
            if (response.message) {
              // Procesando el JSON
              var json = response.message;
              var sdtwsconceptospagos = json.SdtWSConceptosPagos;
              var total = sdtwsconceptospagos.length;
              console.log("Total a procesar: ", total);

              // var processed = 0;
              for (var i in sdtwsconceptospagos) {
                var item = sdtwsconceptospagos[i];
                console.log("Procesando: ", item);
                console.log("ConCPId: ", item.ConCPId);
                frappe.call({
                  method:
                    "tm_app.tm_webservices_nomina.doctype.wsconceptospagos.wsconceptospagos.inserta_actualiza_conceptospagos",
                  args: {
                    concp_id: item.ConCPId,
                    concp_codigo: item.ConcPCodigo,
                    concp_descripcion: item.ConcPDescripcion,
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
