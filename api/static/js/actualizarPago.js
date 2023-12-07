$(document).ready(function () {
    $('.editar-btn').click(function () {
        // Obtén el ID del pago seleccionado
        var id_pago = $(this).data('id');

        // Realiza una solicitud GET AJAX para obtener los datos del servidor
        $.ajax({
            url: '/actualizarEvento/',  // Reemplaza con la ruta correcta
            method: 'GET',
            data: { id_pago: id_pago },
            success: function (data) {
                var evento = data.evento;
                // Fecha en formato ISO8601
                var fechaISO8601I = evento[0].fechaInicio;
                var fechaISO8601T = evento[0].fechaTermino;
                console.log("FECHA INICIAL DE LA BD: " + fechaISO8601I)
                // Convertir a un formato aceptado por datetime-local
                var fechaFormateadaI = fechaISO8601I.replace(" ", "T").slice(0, 16); // Recortar la cadena para eliminar la parte de los segundos
                var fechaFormateadaT = fechaISO8601T.replace(" ", "T").slice(0, 16); // Recortar la cadena para eliminar la parte de los segundos

                // Llena el formulario de edición con los datos obtenidos
                $('#idEditar').val(evento[0].id_pago);
                $('#tituloEditar').val(evento[0].titulo);
                // Asignar el valor al input datetime-local
                document.getElementById("fechaInicioEditar").value = fechaFormateadaI;
                document.getElementById("fechaTerminoEditar").value = fechaFormateadaT;
                $('input[name=frecuenciaEditar][value=' + evento[0].frecuencia + ']').prop('checked', true);
                $('#montoEditar').val(evento[0].monto);
                $('#monedaEditar').val(evento[0].fk_moneda);
                /* AQUÍ VA LA CATEGORIA SELECCIONADA */
                $('#descripcionEditar').val(evento[0].descripcion);

                $('#editarModal').modal('handleUpdate');  // Forzar la actualización del modal
                // Abre el modal
                $('#editarModal').modal('show');
            },
            error: function (error) {
                console.log('Error al obtener los datos del servidor:', error);
            }
        });

        // Agrega aquí el código para guardar los cambios cuando se haga clic en "Guardar cambios"
        $('#guardarCambios').click(function () {
            // Obtén los valores del formulario
            console.log($('#idEditar').val());
            var formData = {
                idEditar: $('#idEditar').val(),
                tituloEditar: $('#tituloEditar').val(),
                fechaInicioEditar: $('#fechaInicioEditar').val(),
                fechaTerminoEditar: $('#fechaTerminoEditar').val(),
                frecuenciaEditar: $('input[name=frecuenciaEditar]:checked').val(),
                montoEditar: $('#montoEditar').val(),
                monedaEditar: $('#monedaEditar').val(),
                //categoriaEditar: $('#categoriaEditar').val(),
                descripcionEditar: $('#descripcionEditar').val()
            };

            // Realiza una solicitud AJAX para enviar los datos al servidor
            $.ajax({
                url: '/actualizarEvento/',
                method: 'POST',
                //data: { formData, csrfmiddlewaretoken: '{{ csrf_token }}' },
                data: formData,
                success: function (response) {
                    // Maneja la respuesta del servidor si es necesario
                    console.log('Datos guardados exitosamente:', response);
                    // Cerrar el modal o hacer otras acciones necesarias
                    $('#editarModal').modal('hide');
                },
                error: function (error) {
                    console.log('Error al guardar los datos:', error);
                }
            });
        });

    });

    // Agrega aquí el código para guardar los cambios cuando se haga clic en "Guardar cambios"
    $('#guardarCambios').click(function () {
        // Obtén los valores del formulario de edición
        var nuevoTitulo = $('#titulo').val();
        // Obtén más valores según tus necesidades

        // Realiza la lógica para guardar los cambios (puedes usar AJAX para enviar los datos a Django)
        // ...

        // Cierra el modal
        $('#editarModal').modal('hide');
    });
});