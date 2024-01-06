function mostrarSelect() {
    // Formulario de inserción
    var radioSeleccionado = document.querySelector('input[name="metodoPago"]:checked');
    var selectEfectivo = document.getElementById('efectivoSel');
    var selectTarjeta = document.getElementById('tarjetaSel');
    // Formulario de edición
    var metodoEditar = document.querySelector('input[name="metodoPagoEditar"]:checked');
    var efectivoSelEditar = document.getElementById('efectivoSelEditar');
    var tarjetaSelEditar = document.getElementById('tarjetaSelEditar');

    // Formulario de inserción
    if (radioSeleccionado && radioSeleccionado.value === 'MP-EFEC') {
        selectEfectivo.style.display = 'block';
        selectTarjeta.style.display = 'none';
    } else if (radioSeleccionado && radioSeleccionado.value === 'MP-TARJ') {
        selectEfectivo.style.display = 'none';
        selectTarjeta.style.display = 'block';
    }

    // Formulario de edición
    if (metodoEditar && metodoEditar.value === 'MP-EFEC') {
        efectivoSelEditar.style.display = 'block';
        tarjetaSelEditar.style.display = 'none';
    } else if (metodoEditar && metodoEditar.value === 'MP-TARJ') {
        efectivoSelEditar.style.display = 'none';
        tarjetaSelEditar.style.display = 'block';
    }
}