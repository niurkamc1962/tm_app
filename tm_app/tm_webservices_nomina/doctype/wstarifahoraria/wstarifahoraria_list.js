frappe.listview_settings["WSTarifaHoraria"] = {
  onload: function (listview) {
    if (frappe.user.has_role("Administrator")) {
      listview.page.add_inner_button(__("Sincronizar WebService"), function () {
        // frappe.show_alert({ message: __('Procesando la información'), indicator: 'green' });
        frappe.call({
          method: "tm_app.utils.webservice_nomina.sync_webservice",
          args: {
            doctype: "WSTarifaHoraria",
          },
          callback: function (response) {
            // console.log('response.message: ', response.message)
            if (response.message) {
              // Procesando el JSON
              var json = response.message;
              var sdtwstarifahoraria = json.SdtWSTarifaHoraria;
              var total = sdtwstarifahoraria.length;
              console.log("Total a procesar: ", total);

              // var processed = 0;
              for (var i in sdtwstarifahoraria) {
                var item = sdtwstarifahoraria[i];
                console.log("Procesando: ", item);
                console.log("NomTariId: ", item.NomTariId);
                frappe.call({
                  method:
                    "tm_app.tm_webservices_nomina.doctype.wstarifahoraria.wstarifahoraria.inserta_actualiza_tarifahoraria",
                  args: {
                    nomtari_id: item.NomTariId,
                    nomtaricod_tarifa: item.nomtariCodTarifa,
                    nomtaritarif_horaria: item.nomtariTarifHoraria,
                    escsalnomtari_id: item.EscSalNomTariID,
                    res_id: item.ResId,
                    res_descripcion: item.ResDescripcion,
                    escs_descripcion: item.EscSDescripcion,
                    nomtari_formapago: item.nomtariFormaPago,
                    nomtari_salmaximo: item.NomtariSalMaximo,
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
