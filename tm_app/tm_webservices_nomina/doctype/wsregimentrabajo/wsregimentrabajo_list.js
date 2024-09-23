frappe.listview_settings["WSRegimenTrabajo"] = {
  onload: function (listview) {
    if (frappe.user.has_role("Administrator")) {
      listview.page.add_inner_button(__("Sincronizar WebService"), function () {
        // frappe.show_alert({ message: __('Procesando la información'), indicator: 'green' });
        frappe.call({
          method: "tm_app.utils.webservice_nomina.sync_webservice",
          args: {
            doctype: "WSRegimenTrabajo",
          },
          callback: function (response) {
            // console.log('response.message: ', response.message)
            if (response.message) {
              // Procesando el JSON
              var json = response.message;
              var sdtwsregimentrabajo = json.SdtWSRegimenTrabajo;
              var total = sdtwsregimentrabajo.length;
              console.log("Total a procesar: ", total);

              // var processed = 0;
              for (var i in sdtwsregimentrabajo) {
                var item = sdtwsregimentrabajo[i];
                console.log("Procesando: ", item);
                console.log("RetraId: ", item.RetraId);
                frappe.call({
                  method:
                    "tm_app.tm_webservices_nomina.doctype.wsregimentrabajo.wsregimentrabajo.inserta_actualiza_regimentrabajo",
                  args: {
                    retra_id: item.RetraId,
                    retra_codigo: item.ReTraCodigo,
                    retra_descripcion: item.ReTraDescripcion,
                    retra_horlab: item.ReTraHorLab,
                    retra_hormax: item.ReTraHorMax,
                    retra_horsemanas: item.RetraHorSemanas,
                    retra_hormaxlab: item.RetraHorMaxLab,
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
