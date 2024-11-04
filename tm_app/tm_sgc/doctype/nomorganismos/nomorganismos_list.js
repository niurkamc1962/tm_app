frappe.listview_settings["NomOrganismos"] = {
  onload: function (listview) {
    if (frappe.user.has_role("Administrator")) {
      listview.page.add_inner_button(__("Importar Organismos"), function () {
        // frappe.show_alert({ message: __('Procesando la información'), indicator: 'green' });
        frappe.call({
          method: "tm_app.utils.importa_nomenclador.import_nomenclador",
          args: {
            doctype: "TEORGANISMO",
          },
          callback: function (response) {
            // console.log('response.message: ', response.message)
            if (response.message) {
              // Procesando el JSON
              var json = response.message;
              var nom_organismos = json.TEORGANISMO;
              var total = nom_organismos.length;
              console.log("Total a procesar: ", total);

              // var processed = 0;
              for (var i in nom_organismos) {
                var item = nom_organismos[i];
                console.log("Procesando: ", item);
                console.log("organismo: ", item.OrganCodigo);
                frappe.call({
                  method:
                    "tm_app.tm_sgc.doctype.nomorganismos.nomorganismos.inserta_actualiza_organismos",
                  args: {
                    dato_organcodigo: item.OrganCodigo,
                    dato_organdescripcion: item.OrganDescripcion,
                    dato_organei: item.OrganEI,
                    dato_organui: item.OrganUI,
                    dato_organfechamodif: item.OrganFechaModif,
                    dato_organactivo: item.OrganActivo,
                  },
                  callback: function (response) {
                    console.log(response.message);
                  },
                  error: function (err) {
                    console.error(
                      "Error al insertar o actualizar: ",
                      err.message
                    );
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
