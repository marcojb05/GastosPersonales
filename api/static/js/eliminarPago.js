$(document).ready(function () {
    $(".eliminar-btn").click(function () {
        var id = $(this).data("id");
        if (confirm("¿Estás seguro de que deseas eliminar este registro?")) {
            $.ajax({
                type: "POST",
                url: "/eliminarEvento/",  // Ajusta la URL de tu vista de eliminación
                data: { id: id, csrfmiddlewaretoken: '{{ csrf_token }}' },
                success: function (data) {
                    // Procesa la respuesta de Django si es necesario
                    console.log(data);
                    // Actualiza la interfaz de usuario si es necesario
                    $(this).closest('tr').remove(); // Elimina la fila de la tabla
                },
                error: function () {
                    // Maneja errores si es necesario
                    console.error("Error en la solicitud POST");
                },
            });
        }
    });
});