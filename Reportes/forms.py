#----------------------------------------------------------------------------------------------------------------#
# Importaciones necesarias
#----------------------------------------------------------------------------------------------------------------#

from django import forms
from .models import *

#----------------------------------------------------------------------------------------------------------------#
# Formularios
#----------------------------------------------------------------------------------------------------------------#

# Login por rut
class Login1Form(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'rut_usuario'
        ]
        widgets = {
            'rut_usuario'     : forms.TextInput(attrs={
                'class'       : 'text',
                'id'          : "idRut",
                'placeholder' : 'Rut sin puntos y con guión',
                'required'    : 'true',
                'oninput'     :"formatRut('idRut')",
            }),
        }

# Login por nombre de usuario y contraseña
class Login2Form(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'nombre_usuario',
            'contraseña_usuario'
        ]
        widgets = {
            'nombre_usuario'  : forms.TextInput(attrs={
                'class'       : 'text',
                'placeholder' : 'Nombre de usuario',
                'required'    : 'true',
            }),
            'contraseña_usuario' : forms.PasswordInput(attrs={
                'class'          : 'text',
                'placeholder'    : 'Contraseña',
                'required'       : 'true',
            }),
        }

# Formulario de reportes
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
                'min' : '00:01',
                'id' : 'time1',
                'onchange' : 'CalculoHorasArriendo();',
                'required' : 'true',
            }),
            'hora_termino' : forms.TimeInput(format=('%H:%M'), attrs={
                'class' : 'fechahora',
                'type': 'time',
                'value' : '00:00',
                'min' : '00:01',
                'id' : 'time2',
                'onchange' : 'CalculoHorasArriendo();',
                'required' : 'true',
            }),
            'horometro_inicial' : forms.NumberInput(attrs={
                'class' : 'form-reporte',
                'placeholder' : 'Horómetro Inicial',
                'value' : 0,
                'id' : 'horometer1',
                'oninput' : 'CalculoHorometroTotal();',
                'required' : 'true',
            }),
            'horometro_final' : forms.NumberInput(attrs={
                'class' : 'form-reporte',
                'placeholder' : 'Horómetro Final',
                'value' : 0,
                'id' : 'horometer2',
                'oninput' : 'CalculoHorometroTotal();',
                'required' : 'true',
            }),
            'horometro_total' : forms.NumberInput(attrs={
                'class' : 'form-reporte',
                'placeholder' : 'Horómetro Total',
                'value': 0,
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

# Formulario de persona
class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields= [
            'nombres',
            'apellido_paterno',
            'apellido_materno',
            'celular',
            'correo',
        ]
        widgets ={
            'nombres': forms.TextInput(attrs={
                'class' : 'text',
                'placeholder' : 'Primer y segundo nombre',
                'required' : 'true',
            }),
            'apellido_paterno': forms.TextInput(attrs={
                'class' : 'text',
                'placeholder' : 'Apellido paterno',
                'required' : 'true',
            }),
            'apellido_materno': forms.TextInput(attrs={
                'class' : 'text',
                'placeholder' : 'Apellido materno',
                'required' : 'true',
            }),
            'celular': forms.NumberInput(attrs={
                'class' : 'number',
                'placeholder' : '9 9999 9999',
                'min' : "100000000",
                'max' : "999999999",
            }),
            'correo': forms.EmailInput(attrs={
                'class' : 'email',
                'placeholder' : 'Correo@email.com',
            }),
        }

# Formulario de contactos
class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields= {
            'nombre',
            'correo',
            'empresa',
            'cargo',
            'celular',
        }
        widgets ={
            'nombre': forms.TextInput(attrs={
                'class': 'text',
                'placeholder': 'Nombre completo del contacto',
                'required': 'true',
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'email',
                'placeholder': 'Correo del contacto',
                'required':'true',
            }),
            'empresa': forms.TextInput(attrs={
                'class': 'text',
                'placeholder': 'Empresa del contacto',
                'required': 'true',
            }),
            'cargo': forms.TextInput(attrs={
                'class': 'text',
                'placeholder': 'Cargo del contacto',
                'required': 'true',
            }),
            'celular': forms.NumberInput(attrs={
                'class': 'text',
                'placeholder': 'Celular del contacto',
                'required': 'true',
            }),
        }

# Formulario de correos
class CorreoForm(forms.ModelForm):
    class Meta:
        model = Correo
        fields= {
            'asunto',
            'cuerpo',

        }
        widgets ={
            'asunto': forms.TextInput(attrs={
                'class': 'text',
                'placeholder': 'Asunto del correo.',
                'required': 'true',
            }),
            'cuerpo': forms.Textarea(attrs={
                'class': 'email',
                'placeholder': 'Cuerpo del correo.',
                'cols'      : '30',
                'rows'      : '10',
                'style'     : 'resize: none; font-family: monospace;',
                'required':'true',
            }),
        }

# Formulario de mantencion
class MantencionForm(forms.ModelForm):
    class Meta:
        model = Mantencion
        fields= {
            'fecha',
            'numero_maquina',
            'horometro_maq',
            'descripcion',
            'observacion',
            'insumos',
            'prox_mantencion',
            'prox_horometro',

        }
        widgets ={
            'fecha' : forms.DateInput(format=('%d-%m-%Y'), attrs={
                'class' : 'fechahora',
                'type' : 'date',
                'required' : 'true',
            }),
            'numero_maquina': forms.TextInput(attrs={
                'class': 'text',
                'placeholder': 'N° Máquina',
                'required': 'true',
            }),
            'horometro_maq' : forms.NumberInput(attrs={
                'class' : 'number',
                'placeholder' : 'Horómetro de la máquina',
                'value' : 0,
                'required' : 'true',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'txtarea',
                'placeholder': 'Descripción',
                'cols'      : '30',
                'rows'      : '10',
                'style'     : 'resize: none; font-family: monospace;',
                'required':'true',
            }),
            'observacion': forms.Textarea(attrs={
                'class': 'txtarea',
                'placeholder': 'Observaciones',
                'cols'      : '30',
                'rows'      : '10',
                'style'     : 'resize: none; font-family: monospace;',
                'required':'true',
            }),
            'insumos': forms.Textarea(attrs={
                'class': 'txtarea',
                'placeholder': 'Insumos',
                'cols'      : '30',
                'rows'      : '10',
                'style'     : 'resize: none; font-family: monospace;',
                'required':'true',
            }),
            'prox_mantencion': forms.TextInput(attrs={
                'class': 'text',
                'placeholder': 'Fecha apróximada',
                'required': 'true',
            }),
            'prox_horometro' : forms.NumberInput(attrs={
                'class' : 'number',
                'placeholder' : 'Horómetro próxima mantención',
                'value' : 0,
                'required' : 'true',
            }),
        }