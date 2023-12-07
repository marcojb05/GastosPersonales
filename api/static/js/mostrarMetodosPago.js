function mostrarSelect() {
    var radioSeleccionado = document.querySelector('input[name="metodoPago"]:checked');
    var selectEfectivo = document.getElementById('efectivoSel');
    var selectTarjeta = document.getElementById('tarjetaSel');

    if (radioSeleccionado && radioSeleccionado.value === 'MP-EFEC') {
        selectEfectivo.style.display = 'block';  // Mostrar el select
        selectTarjeta.style.display = 'none';  // Mostrar el select
    } else if (radioSeleccionado && radioSeleccionado.value === 'MP-TARJ') {
        selectEfectivo.style.display = 'none';  // Mostrar el select
        selectTarjeta.style.display = 'block';  // Mostrar el select
    }
}