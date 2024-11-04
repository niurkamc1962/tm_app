frappe.listview_settings["NomTiposEmpresas"] = {
  onload: function (listview) {
    if (frappe.user.has_role("Administrator")) {
      listview.page.add_inner_button(__("Importar Tipos Empresas"), function () {
        // frappe.show_alert({ message: __('Procesando la información'), indicator: 'green' });
        frappe.call({
          method: "tm_app.utils.importa_nomenclador.import_nomenclador",
          args: {
            doctype: "SCOTIPIFEMPRESA",
          },
          callback: function (response) {
            // console.log('response.message: ', response.message)
            if (response.message) {
              // Procesando el JSON
              var json = response.message;
              var nom_tiposempresas = json.SCOTIPIFEMPRESA;
              var total = nom_tiposempresas.length;
              console.log("Total a procesar: ", total);

              // var processed = 0;
              for (var i in nom_tiposempresas) {
                var item = nom_tiposempresas[i];
                console.log("Procesando: ", item);
                console.log("tipoempresa: ", item.TipifiCodigo);
                frappe.call({
                  method:
                    "tm_app.tm_sgc.doctype.nomtiposempresas.nomtiposempresas.inserta_actualiza_tiposempresas",
                  args: {
                    dato_tipoempresa: item.TipifiCodigo,
                    dato_descripcion: item.TipifiDescripcion,
                    dato_estado: item.TipifiEstado,
                    dato_ventacontabiliza: item.VentaContabiliza,
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
