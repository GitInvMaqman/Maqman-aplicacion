#----------------------------------------------------------------------------------------------------------------#
# Importaciones necesarias
#----------------------------------------------------------------------------------------------------------------#

from django import forms
from .models import *

#----------------------------------------------------------------------------------------------------------------#
# Formularios
#----------------------------------------------------------------------------------------------------------------#

class LoginForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'nombre_usuario',
            'contraseña_usuario'
        ]
        widgets = {
            'nombre_usuario'           : forms.TextInput(attrs={
                'class'       : 'text',
                'placeholder' : 'Nombre de usuario',
                'required'    : 'true',
            }),
            'contraseña_usuario'       : forms.PasswordInput(attrs={
                'class'       : 'text',
                'placeholder' : 'Contraseña',
                'required'    : 'true',
            }),
        }

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields= [
            'cliente',
            'obra',
            'fecha',
            'hora_ingreso',
            'hora_termino',
            'horometro_inicial',
            'horometro_final',
            'equipo_numero',
            'horas_arriendo',
            'observaciones',
            'horometro_total',
            'hora_minima',
        ]
        widgets ={
            'cliente' : forms.TextInput(attrs={
                'class' : 'text',
                'placeholder' : 'Cliente',
                'required' : 'true',
            }),
            'obra' : forms.TextInput(attrs={
                'class' : 'text',
                'placeholder' : 'Obra',
                'required' : 'true',
            }),
            'fecha' : forms.DateInput(format=('%d-%m-%Y'), attrs={
                'class' : 'fechahora',
                'type' : 'date',
                'required' : 'true',
            }),
            'hora_ingreso' : forms.TimeInput(format=('%H:%M'), attrs={
                'class' : 'fechahora',
                'type': 'time',
                'value' : '00:00',
                'id' : 'time1',
                'onchange' : 'CalculoHorasArriendo();',
                'required' : 'true',
            }),
            'hora_termino' : forms.TimeInput(format=('%H:%M'), attrs={
                'class' : 'fechahora',
                'type': 'time',
                'value' : '00:00',
                'id' : 'time2',
                'onchange' : 'CalculoHorasArriendo();',
                'required' : 'true',
            }),
            'horometro_inicial' : forms.NumberInput(attrs={
                'class' : 'form-reporte',
                'placeholder' : 'Horómetro Inicial',
                'value' : 0,
                'id' : 'horometer1',
                'onchange' : 'CalculoHorometroTotal();',
                'required' : 'true',
            }),
            'horometro_final' : forms.NumberInput(attrs={
                'class' : 'form-reporte',
                'placeholder' : 'Horómetro Final',
                'value' : 0,
                'id' : 'horometer2',
                'onchange' : 'CalculoHorometroTotal();',
                'required' : 'true',
            }),
            'horometro_total' : forms.NumberInput(attrs={
                'class' : 'form-reporte',
                'placeholder' : 'Horómetro Total',
                'required' : 'true',
            }),
            'equipo_numero' : forms.TextInput(attrs={
                'class' : 'text',
                'placeholder' : 'Equipo N°',
                'required' : 'true',
            }),
            'horas_arriendo' : forms.NumberInput(attrs={
                'class' : 'form-reporte',
                'placeholder' : 'Horas de Arriendo',
                'required' : 'true',
            }),
            'hora_minima' : forms.NumberInput(attrs={
                'class' : 'form-reporte',
                'placeholder' : 'Hora Mínima',
                'required' : 'true',
            }),
            'observaciones' : forms.Textarea(attrs={
                'class' : 'form-reporte',
                'placeholder' : 'Observaciones',
                'cols'      : '100',
                'rows'      : '10',
                'style'     : 'resize: none; font-family: monospace;',
                'required' : 'true',
            }),
        }