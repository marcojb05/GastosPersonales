window.addEventListener('DOMContentLoaded', event => {
    // Simple-DataTables
    // https://github.com/fiduswriter/Simple-DataTables/wiki

    const datatablesSimple = document.getElementById('datatablesSimple');
    if (datatablesSimple) {
        new simpleDatatables.DataTable(datatablesSimple);
    }

    // TABLA DE METAS
    const tablaMetas = document.getElementById('tablaMetas');
    if (tablaMetas) {
        new simpleDatatables.DataTable(tablaMetas);
    }
    // TABLA DE METAS
});
