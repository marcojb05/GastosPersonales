function toggleDeactivateButton() {
    var checkbox = document.getElementById("accountActivation");
    var button = document.getElementById("deactivateButton");

    button.disabled = !checkbox.checked;
}