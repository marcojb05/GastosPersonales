# forms.py
from django import forms
from .models import Cuenta

class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ['id_cuenta', 'fk_usuario', 'nombre_cuenta', 'fk_metodo_pago']