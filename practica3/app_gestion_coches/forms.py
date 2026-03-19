from django import forms
from .models import Cliente, Coche, Servicio


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'


class CocheForm(forms.ModelForm):
    class Meta:
        model = Coche
        fields = '__all__'


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = '__all__'


class ServicioConClienteForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        label='Usuario',
        required=True,
    )
    coche = forms.ModelChoiceField(
        queryset=Coche.objects.none(),
        label='Vehiculo',
        required=True,
    )

    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cliente_id = self.data.get('cliente')
        if cliente_id:
            self.fields['coche'].queryset = Coche.objects.filter(cliente_id=cliente_id)
        else:
            self.fields['coche'].queryset = Coche.objects.none()
