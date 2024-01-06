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
        var id_transaccion = $(this).data('id');

        // Realiza una solicitud GET AJAX para obtener los datos del servidor
        $.ajax({
            url: '/actualizarTransaccion/',
            method: 'GET',
            data: { id_transaccion: id_transaccion },
            success: function (data) {
                // Rellena los campos de la modal con los datos recibidos
                var transaccion = data.transaccion;
                console.log("ID: " + transaccion.id_transaccion + " de la transaccion");
                $('#idEditar').val(transaccion.id_transaccion);
                $('#fechaEditar').val(transaccion.fecha);
                $('#montoEditar').val(transaccion.monto);
                $('#monedaEditar').val(transaccion.moneda);
                $('#categoriaEditar').val(transaccion.categoria);
                var metodoPago = transaccion.metodoPago;
                // Seleccionar el botón de radio basado en el valor de metodoPago
                if (metodoPago === 'MP-EFEC') {
                    $('input[name="metodoPagoEditar"][value="MP-EFEC"]').prop('checked', true);
                    $('#efectivoSelEditar').show();
                    $('#efectivoSelEditar').val(transaccion.cuenta);
                    $('#tarjetaSelEditar').hide();
                } else if (metodoPago === 'MP-TARJ') {
                    $('input[name="metodoPagoEditar"][value="MP-TARJ"]').prop('checked', true);
                    $('#efectivoSelEditar').hide();
                    $('#tarjetaSelEditar').show();
                    $('#tarjetaSelEditar').val(transaccion.cuenta);
                }
                console.log("DESCRIPCIÓN: "+transaccion.descripcion)
                $('#notaEditar').val(transaccion.descripcion);

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
        var cuenta
        var metodoSeleccionado = document.querySelector('input[name="metodoPagoEditar"]:checked');
        // Comprobar qué botón de radio está seleccionado
        if (metodoSeleccionado && metodoSeleccionado.value === 'MP-EFEC') {
            cuenta = $('#efectivoSelEditar').val();
        } else if (metodoSeleccionado && metodoSeleccionado.value === 'MP-TARJ') {
            cuenta = $('#tarjetaSelEditar').val();
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: "Debe seleccionar una cuenta válida",
                confirmButtonText: 'Entendido'
            });
            return; // Salir de la función si no se seleccionó ningún botón de radio
        }
        // Obtén los valores del formulario
        var formData = {
            idEditar: $('#idEditar').val(),
            fechaEditar: $('#fechaEditar').val(),
            montoEditar: $('#montoEditar').val(),
            monedaEditar: $('#monedaEditar').val(),
            categoriaEditar: $('#categoriaEditar').val(),
            cuenta: cuenta,

            notaEditar: $('#notaEditar').val(),
            csrfmiddlewaretoken: csrftoken  // Agrega el token CSRF a los datos de la solicitud
        };
        console.log(formData)

        // Realiza una solicitud AJAX para enviar los datos al servidor
        $.ajax({
            url: '/actualizarTransaccion/',
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
        var id_transaccion = $(this).data('id');

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
                // Realiza una solicitud AJAX para enviar el ID de la meta a la vista eliminarTransaccion
                $.ajax({
                    url: '/eliminarTransaccion/',
                    method: 'POST',
                    data: { id_transaccion: id_transaccion },
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
