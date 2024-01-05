$(document).ready(function () {
    // Configura jQuery AJAX para incluir automáticamente el token CSRF en todas las solicitudes POST
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Busca el token CSRF en las cookies
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    // Configura el token CSRF en el encabezado de todas las solicitudes AJAX
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Solo envía el token CSRF a URLs relativas
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('.editar-btn').click(function () {
        // Obtén el ID de la meta seleccionada
        var id_meta = $(this).data('id');

        // Realiza una solicitud GET AJAX para obtener los datos del servidor
        $.ajax({
            url: '/actualizarMeta/',
            method: 'GET',
            data: { id_meta: id_meta },
            success: function (data) {
                // Rellena los campos de la modal con los datos recibidos
                var meta = JSON.parse(data.meta)[0].fields; // Parsea los datos JSON
                console.log("ID: "+id_meta+" de la meta")
                $('#idEditar').val(id_meta);
                $('#objetivoEditar').val(meta.objetivo);
                $('#monedaEditar').val(meta.fk_moneda);
                $('#fechaInicioEditar').val(meta.fechaInicio);
                $('#fechaTerminoEditar').val(meta.fechaTermino);
                $('#notaEditar').val(meta.descripcion);

                // Muestra la modal
                $('#editarModal').modal('show');
            },
            error: function (error) {
                console.log('Error al obtener los datos del servidor:', error);
            }
        });
    });

    // Agrega aquí el código para guardar los cambios cuando se haga clic en "Guardar cambios"
    $('#guardarCambios').click(function () {
        // Obtén los valores del formulario
        var formData = {
            idEditar: $('#idEditar').val(),
            objetivoEditar: $('#objetivoEditar').val(),
            monedaEditar: $('#monedaEditar').val(),
            fechaInicioEditar: $('#fechaInicioEditar').val(),
            fechaTerminoEditar: $('#fechaTerminoEditar').val(),
            notaEditar: $('#notaEditar').val(),
            csrfmiddlewaretoken: csrftoken  // Agrega el token CSRF a los datos de la solicitud
        };
        console.log(formData)

        // Realiza una solicitud AJAX para enviar los datos al servidor
        $.ajax({
            url: '/actualizarMeta/',
            method: 'POST',
            data: formData,
            success: function (response) {
                // Muestra un modal de éxito con SweetAlert2 y el mensaje de la respuesta JSON
                if (response.message) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Éxito',
                        text: response.message,
                        showConfirmButton: false,
                        timer: 2000
                    });
                    location.reload()
                    $('#editarModal').modal('hide');
                }
            },
            error: function (error) {
                $('#editarModal').modal('hide');
                // Muestra un modal de error con SweetAlert2 y el mensaje de la respuesta JSON
                if (error.responseJSON && error.responseJSON.error) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: error.responseJSON.error,
                        confirmButtonText: 'Entendido'
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'Hubo un problema al intentar actualizar los datos. Por favor, inténtalo de nuevo.',
                        confirmButtonText: 'Entendido'
                    });
                }
                console.log('Error al guardar los datos:', error);
            }
        });
    });

    $('.eliminar-btn').click(function () {
        // Obtiene el ID de la meta seleccionada
        var id_meta = $(this).data('id');

        // Muestra una ventana modal de confirmación con SweetAlert2
        Swal.fire({
            title: '¿Estás seguro de que deseas eliminar este registro?',
            text: 'Esta acción no se puede deshacer',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, eliminar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                // Realiza una solicitud AJAX para enviar el ID de la meta a la vista eliminarMeta
                $.ajax({
                    url: '/eliminarMeta/',
                    method: 'POST',
                    data: { id_meta: id_meta },
                    success: function (response) {
                        // Muestra un modal de éxito con SweetAlert2 y el mensaje de la respuesta JSON
                        Swal.fire({
                            icon: 'success',
                            title: '¡Registro eliminado!',
                            text: response.message,
                            showConfirmButton: false,
                            timer: 2000
                        });
                        location.reload()
                    },
                    error: function (error) {
                        // Muestra un modal de error con SweetAlert2 y el mensaje de la respuesta JSON
                        Swal.fire({
                            icon: 'error',
                            title: '¡Error al eliminar el registro!',
                            text: error.responseJSON.error,
                            confirmButtonText: 'Entendido'
                        });
                        console.log('Error al eliminar el registro:', error);
                    }
                });
            }
        });
    });
});
