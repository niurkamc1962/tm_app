frappe.listview_settings['Archivos PDF'] = {
    on_page_load: function(listview) {
        //Agregando evento al hacer click en el nombre del archivo
        listview.on('click','.file-name', function() {
            //Obteniendo la ruta del archivo desde el atributo data-ruta
            var ruta_archivo = $(this).data('ruta');
            //Verificar ruta no este vacia
            if(ruta_archivo) {
                //Abrir pdf en una ventana
                window.open(ruta_archivo, '_blank');
            }else{
                frappe.msgprint(__('La ruta del archivo no existe'));
            }
        });
    }
}