import datetime
import os
from sqlite3 import IntegrityError
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
import requests
# import google_auñth_oauthlib
from rest_framework.views import APIView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User  # Permite el registro
# Permite crear la cookie con el registro del login
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render
from django.contrib.auth.models import User
# Para la generación de contraseña Aleatoria
import secrets
import string
# Importación de los modelos
from django.db.models import Q, Count

from APITESCHI.settings import BASE_DIR
from .models import Moneda, Categoria, Tarjeta, MetodoPago, Transaccion, TipoTransaccion, Ahorro, MetaFinanciera, Pago, encuesta
# CONEXIÓN CON API DE GOOGLE CALENDAR
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
from django.contrib.auth import login
# from social_django.utils import load_strategy
# from social_django.strategy import DjangoStrategy
# from social_core.backends.google import GoogleOAuth2
# from social_core.exceptions import AuthException
# from google.oauth2.service_account import Credentials
from django.conf import settings
from django.http import JsonResponse
from openexchangerate import OpenExchangeRates
# from django_googledrive_api import GoogleDriveClient

# Create your views here.

# Crea una vista para el registro
def Registrar(request):
    if request.method == "GET":
        return render(request, "signup.html", {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:

            # Registro del usuario
            # Devuelve un objeto user y es un usuario que se puede guardar en la bd
            user = User.objects.create_user(first_name=request.POST['first_name'],
                                            last_name=request.POST['last_name'],
                                            username=request.POST['username'],
                                            email=request.POST['email'],
                                            password=request.POST['password1'])
            user.save()

            subject = 'Te damos la bienvenida'
            recipient_list = [request.POST['email']]

            # Crea el contenido HTML
            html_message = render_to_string('correo/Bienvenida.html',
                                            {'nombre': request.POST['first_name'],
                                             'username': request.POST['username'],
                                             'password': request.POST['password1']})
            plain_message = strip_tags(html_message)

            enviarCorreo(subject, plain_message,
                                 recipient_list, html_message)
            login(request, user)
            return redirect('login')

        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'Las contraseñas no coinciden'
        })

# Cierra la sesión
def signout(request):
    logout(request)
    return redirect('login')

# Iniciar sesión
def signin(request):
    if request.method == "GET":
        return render(request, 'login.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password']
                            )
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': "El usuario o contraseña son incorrectos"
            })
        else:
            login(request, user)
            return redirect('index')


@method_decorator(login_required, name='dispatch')
class Home (APIView):
    template_name = "index.html"
    # self es el equivalente del this en Java, hace referencia a sí mismo
    # request se consume

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class Cuenta (APIView):
    template_name = "cuenta.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class Notificaciones (APIView):
    template_name = "notificaciones.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class Conexiones (APIView):
    template_name = "conexiones.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class Movimientos (APIView):
    template_name = "movimientos.html"

    def get(self, request):
        fecha_actual = datetime.date.today()
        primerDia = fecha_actual.replace(day=1)
        
        # Calcula el primer día del próximo mes restando un día al primer día del mes actual
        primer_dia_del_proximo_mes = fecha_actual.replace(day=1) + datetime.timedelta(days=31)
        # Resta un día al primer día del próximo mes para obtener el último día del mes actual
        ultimoDia = primer_dia_del_proximo_mes - datetime.timedelta(days=1)
        
        fechaInicio = primerDia
        fechaFin = ultimoDia
        
        if self.verifica:
            context = self.get_context_data(fechaInicio, fechaFin, 'none', '')
            return render(request, self.template_name, context)
        else:
            context = self.get_context_data('', '', 'block', 'Todos los campos son obligatorios.')
            return render(request, self.template_name, context)
            

    def post(self, request):
        if self.verifica:
            try:
                fechaInicioF = request.POST['fechaInicial']
                print("Fecha Inicio: ", fechaInicioF)
                fechaFinF = request.POST['fechaFinal']
                print("Fecha final: ", fechaFinF)
                context = self.get_context_data(fechaInicioF, fechaFinF, 'none', '')
                return render(request, self.template_name, context)
            except Exception as e:
                context = self.get_context_data('','','block', f"Los datos ingresados no son válidos: {str(e)}")
                return render(request, self.template_name, context)
                
        else:
            
            return render(request, self.template_name, context)
    
    def verifica(self):
        if ('fechaInicial' not in self.request.POST or 
            'fechaFinal' not in self.request.POST):
            return False
        else:
            return True
    
    def get_context_data(self, fechaInicio, fechaFin, mostrarError, error):
        # Obtiene el usuairo y su ID
        usuario = self.request.user
        usuario_id = usuario.id
        
        # Consulta las transacciones según las fechas y el usuario
        transacciones_entre_fechas = Transaccion.objects.filter(
            Q(fecha__gte=fechaInicio) & Q(fecha__lte=fechaFin),
            fk_usuario=usuario_id
        )
        return {
            'transacciones': transacciones_entre_fechas,
            'mostrarError': mostrarError,
            'error': error
        }

# Ingresos del usuario
@method_decorator(login_required, name='dispatch')
class Ingresos (APIView):
    template_name = "ingresos.html"
    # MÉTODO GET
    def get(self, request):
        # mensajeError, error, mostrarMensaje, mensaje
        context = self.get_context_data('none', '', 'none', '')
        return render(request, self.template_name, context)
        
   # MÉTODO POST
    def post(self, request):
        #Comprueba que estén los datos requeridos.
        
        if self.verifica() == False:
            context = self.get_context_data('block', 'Todos los campos son obligatorios.', 'none', '')
            return render(request, self.template_name, context)
        else:
            # OBTTENER LOS DATOS POR POST
            categoriaF = request.POST['categoria']
            montoF = request.POST['monto']
            fechaF = request.POST['fecha']
            monedaF = request.POST['moneda']
            metodoPagoF = request.POST['metodoPago']
            notaF = request.POST['nota']
            
            if metodoPagoF == 'MP-EFEC':
                metodo = request.POST['efectivoSel']
            elif metodoPagoF == 'MP-TARJ':
                metodo = request.POST['tarjetaSel']
            else:
                context = self.get_context_data('block', 'El método de pago no es válido', 'none', '')
                return render(request, self.template_name, context)
            
            # GENERACIÓN DE ID DE TRANSACCIÓN (INGRESO)
            current_time = datetime.now()
            usuario = request.user
            usuario_id = usuario.id
            fecha = f"I{usuario_id}-{current_time.strftime('%Y%m%d%H%M%S')}"
            transaction_id = str(fecha)
            try:
                nuevaTransaccion = Transaccion(id_transaccion=transaction_id,
                                               descripcion=notaF,
                                               monto=montoF,
                                               fecha=fechaF,
                                               fk_cuenta=Tarjeta.objects.get(id_cuenta=metodo),
                                               fk_moneda=Moneda.objects.get(id_moneda=monedaF),
                                               fk_tipo=TipoTransaccion.objects.get(id_tipo='TP-ING'),
                                               fk_usuario=usuario,
                                               fkcategoria=Categoria.objects.get(id_categoria=categoriaF)
                )
                nuevaTransaccion.save()
                context = self.get_context_data('none', '', 'block', 'Los datos se han registrado correctamente.')
                return render(request, self.template_name, context)
            except IntegrityError:
                context = self.get_context_data('block', 'Error, se presentó una duplicación de datos', 'none', '')
                return render(request, self.template_name, context)
            except Exception as e:
                context = self.get_context_data('block', f"Los datos ingresados no son válidos: {str(e)}", 'none', '')
                return render(request, self.template_name, context)
    
    # Realiza las consultas y renderiza en los campos
    def get_context_data(self, mensajeError, error, mostrarMensaje, mensaje):
         # Obtiene el usuairo y su ID
        usuario = self.request.user
        usuario_id = usuario.id
        
        # Consulta las monedas registradas en la BD
        monedas = Moneda.objects.all()
        # Consultas para ingresos
        categorias = Categoria.objects.filter(fk_tipo='TP-ING')
        
        # Consulta para retornar las carteras del usuario.
        carteras = Tarjeta.objects.filter(
            fk_metodo_pago__id_metodotipo='MP-EFEC',
            fk_usuario=usuario_id
        )
        
        # Consulta para retornar las tarjetas del usuario.
        tarjetas = Tarjeta.objects.filter(
            fk_metodo_pago__id_metodotipo='MP-TARJ',
            fk_usuario=usuario_id
        )
        return {
            'monedas': monedas,
            'categorias': categorias,
            'carteras': carteras,
            'tarjetas': tarjetas,
            'mostrarError': mensajeError,
            'error': error,
            'mostrarMensaje': mostrarMensaje,
            'mensaje': mensaje,
        }

    def verifica(self):
        if ('categoria' not in self.request.POST or 
            'monto' not in self.request.POST or
            'fecha' not in self.request.POST or
            'moneda' not in self.request.POST or
            'metodoPago' not in self.request.POST or
            'nota' not in self.request.POST or
            'efectivoSel' not in self.request.POST or
            'tarjetaSel' not in self.request.POST
            ):
            return False
        else:
            return True
        
    def get_context_data(self, mensajeError, error, mostrarMensaje, mensaje):
         # Obtiene el usuairo y su ID
        usuario = self.request.user
        usuario_id = usuario.id
        
        # Consulta las monedas registradas en la BD
        monedas = Moneda.objects.all()
        # Consultas para ingresos
        categorias = Categoria.objects.filter(fk_tipo='TP-ING')
        
        # Consulta para retornar las carteras del usuario.
        carteras = Tarjeta.objects.filter(
            fk_metodo_pago__id_metodotipo='MP-EFEC',
            fk_usuario=usuario_id
        )
        
        # Consulta para retornar las tarjetas del usuario.
        tarjetas = Tarjeta.objects.filter(
            fk_metodo_pago__id_metodotipo='MP-TARJ',
            fk_usuario=usuario_id
        )
        return {
            'monedas': monedas,
            'categorias': categorias,
            'carteras': carteras,
            'tarjetas': tarjetas,
            'mostrarError': mensajeError,
            'error': error,
            'mostrarMensaje': mostrarMensaje,
            'mensaje': mensaje,
        }
        
# Gastos del usuario
@method_decorator(login_required, name='dispatch')
class Gastos (APIView):
    template_name = "gastos.html"

    # MÉTODO GET
    def get(self, request):
        # mensajeError, error, mostrarMensaje, mensaje
        context = self.get_context_data('none', '', 'none', '')
        return render(request, self.template_name, context)
        
    # MÉTODO POST
    def post(self, request):
        #Comprueba que estén los datos requeridos.
        
        if self.verifica() == False:
            context = self.get_context_data('block', 'Todos los campos son obligatorios.', 'none', '')
            return render(request, self.template_name, context)
        else:
            # OBTTENER LOS DATOS POR POST
            categoriaF = request.POST['categoria']
            montoF = request.POST['monto']
            fechaF = request.POST['fecha']
            monedaF = request.POST['moneda']
            metodoPagoF = request.POST['metodoPago']
            notaF = request.POST['nota']
            
            if metodoPagoF == 'MP-EFEC':
                metodo = request.POST['efectivoSel']
            elif metodoPagoF == 'MP-TARJ':
                metodo = request.POST['tarjetaSel']
            else:
                context = self.get_context_data('block', 'El método de pago no es válido', 'none', '')
                return render(request, self.template_name, context)
            
            # GENERACIÓN DE ID DE TRANSACCIÓN (INGRESO)
            current_time = datetime.now()
            usuario = request.user
            usuario_id = usuario.id
            fecha = f"G{usuario_id}-{current_time.strftime('%Y%m%d%H%M%S')}"
            transaction_id = str(fecha)
            try:
                nuevaTransaccion = Transaccion(id_transaccion=transaction_id,
                                               descripcion=notaF,
                                               monto=montoF,
                                               fecha=fechaF,
                                               fk_cuenta=Tarjeta.objects.get(id_cuenta=metodo),
                                               fk_moneda=Moneda.objects.get(id_moneda=monedaF),
                                               fk_tipo=TipoTransaccion.objects.get(id_tipo='TP-GAS'),
                                               fk_usuario=usuario,
                                               fkcategoria=Categoria.objects.get(id_categoria=categoriaF)
                )
                nuevaTransaccion.save()
                context = self.get_context_data('none', '', 'block', 'Los datos se han registrado correctamente.')
                return render(request, self.template_name, context)
            except IntegrityError:
                context = self.get_context_data('block', 'Error, se presentó una duplicación de datos', 'none', '')
                return render(request, self.template_name, context)
            except Exception as e:
                context = self.get_context_data('block', f"Los datos ingresados no son válidos: {str(e)}", 'none', '')
                return render(request, self.template_name, context)
    
    # Realiza las consultas y renderiza en los campos
    def get_context_data(self, mensajeError, error, mostrarMensaje, mensaje):
        # Obtiene el usuairo y su ID
        usuario = self.request.user
        usuario_id = usuario.id
        
        # Consulta las monedas registradas en la BD
        monedas = Moneda.objects.all()
        # Consultas para ingresos
        categorias = Categoria.objects.filter(fk_tipo='TP-GAS')
        
        # Consulta para retornar las carteras del usuario.
        carteras = Tarjeta.objects.filter(
            fk_metodo_pago__id_metodotipo='MP-EFEC',
            fk_usuario=usuario_id
        )
        
        # Consulta para retornar las tarjetas del usuario.
        tarjetas = Tarjeta.objects.filter(
            fk_metodo_pago__id_metodotipo='MP-TARJ',
            fk_usuario=usuario_id
        )
        return {
            'monedas': monedas,
            'categorias': categorias,
            'carteras': carteras,
            'tarjetas': tarjetas,
            'mostrarError': mensajeError,
            'error': error,
            'mostrarMensaje': mostrarMensaje,
            'mensaje': mensaje,
        }

    def verifica(self):
        if ('categoria' not in self.request.POST or 
            'monto' not in self.request.POST or
            'fecha' not in self.request.POST or
            'moneda' not in self.request.POST or
            'metodoPago' not in self.request.POST or
            'nota' not in self.request.POST or
            'efectivoSel' not in self.request.POST or
            'tarjetaSel' not in self.request.POST
            ):
            return False
        else:
            return True

# Ahorros del usuario
@method_decorator(login_required, name='dispatch')
class Ahorros (APIView):
    template_name = "ahorros.html"

    # MÉTODO GET
    def get(self, request):
        # mensajeError, error, mostrarMensaje, mensaje
        context = self.get_context_data('none', '', 'none', '')
        return render(request, self.template_name, context)

    # MÉTODO POST
    def post(self, request):
        #Comprueba que estén los datos requeridos.
        if self.verifica() == False:
            context = self.get_context_data('block', 'Todos los campos son obligatorios.', 'none', '')
            return render(request, self.template_name, context)
        else:
            # OBTTENER LOS DATOS POR POST
            montoF = request.POST['monto']
            fechaF = request.POST['fecha']
            #monedaF = request.POST['moneda']
            notaF = request.POST['nota']
            
            # GENERACIÓN DE ID DE TRANSACCIÓN (INGRESO)
            current_time = datetime.now()
            usuario = request.user
            usuario_id = usuario.id
            fecha = f"A{usuario_id}-{current_time.strftime('%Y%m%d%H%M%S')}"
            transaction_id = str(fecha)
            metodoPagoF = request.POST['metodoPago']
            user = get_object_or_404(User, id=usuario_id)  # usuario_id es el valor que deseas asignar como clave foránea
            print("Estado del usuario ", user)
            if metodoPagoF == 'MP-EFEC':
                metodo = request.POST['efectivoSel']
            elif metodoPagoF == 'MP-TARJ':
                metodo = request.POST['tarjetaSel']
            else:
                context = self.get_context_data('block', 'El método de pago no es válido', 'none', '')
                return render(request, self.template_name, context)
            try:
                nuevoAhorro = Ahorro(id_ahorro=transaction_id,
                                     descripcion=notaF,
                                     monto=montoF,
                                     fecha=fechaF,
                                     fk_cuenta=Tarjeta.objects.get(id_cuenta=metodo),
                                     fk_usuario=User.objects.get(id = usuario_id),
                                    )
                nuevoAhorro.save()
                context = self.get_context_data('none', '', 'block', 'Los datos se han registrado correctamente.')
                return render(request, self.template_name, context)
            except IntegrityError:
                context = self.get_context_data('block', 'Error, se presentó una duplicación de datos', 'none', '')
                return render(request, self.template_name, context)
            except Exception as e:
                context = self.get_context_data('block', f"Los datos ingresados no son válidos: {str(e)}", 'none', '')
                return render(request, self.template_name, context)
    
    # Realiza las consultas y renderiza en los campos
    def get_context_data(self, mensajeError, error, mostrarMensaje, mensaje):        
        # Obtiene el usuairo y su ID
        usuario = self.request.user
        usuario_id = usuario.id
        
        # Consulta las monedas registradas en la BD
        monedas = Moneda.objects.all()
        # Consultas para ingresos
        categorias = Categoria.objects.filter(fk_tipo='TP-GAS')
        
        # Consulta para retornar las carteras del usuario.
        carteras = Tarjeta.objects.filter(
            fk_metodo_pago__id_metodotipo='MP-EFEC',
            fk_usuario=usuario_id
        )
        
        # Consulta para retornar las tarjetas del usuario.
        tarjetas = Tarjeta.objects.filter(
            fk_metodo_pago__id_metodotipo='MP-TARJ',
            fk_usuario=usuario_id
        )
        
        return {
            'monedas': monedas,
            'categorias': categorias,
            'carteras': carteras,
            'tarjetas': tarjetas,
            'mostrarError': mensajeError,
            'error': error,
            'mostrarMensaje': mostrarMensaje,
            'mensaje': mensaje,
        }

    # Verifica que existan los campos del HTML
    def verifica(self):
        if ('fecha' not in self.request.POST or
            'monto' not in self.request.POST or
            #'moneda' not in self.request.POST or
            'nota' not in self.request.POST or
            'metodoPago' not in self.request.POST or
            'nota' not in self.request.POST or
            'efectivoSel' not in self.request.POST or
            'tarjetaSel' not in self.request.POST
            ):
            return False
        else:
            return True


@method_decorator(login_required, name='dispatch')
class DeudasPagos (APIView):
    template_name = "deudasypagos.html"

    # MÉTODO GET
    def get(self, request):
        context = self.get_context_data('none', '', 'none', '')
        return render(request, self.template_name, context)

    # MÉTODO POST
    def post(self, request):
        #Comprueba que estén los datos requeridos.
        if self.verifica() == False:
            context = self.get_context_data('block', 'Todos los campos son obligatorios.', 'none', '')
            return render(request, self.template_name, context)
        else:
            # OBTTENER LOS DATOS POR POST
            montoF = request.POST['monto']
            fechaF = request.POST['fecha']
            #monedaF = request.POST['moneda']
            notaF = request.POST['nota']
            
            # GENERACIÓN DE ID DE TRANSACCIÓN (INGRESO)
            current_time = datetime.now()
            usuario = request.user
            usuario_id = usuario.id
            fecha = f"A{usuario_id}-{current_time.strftime('%Y%m%d%H%M%S')}"
            transaction_id = str(fecha)
            metodoPagoF = request.POST['metodoPago']
            user = get_object_or_404(User, id=usuario_id)  # usuario_id es el valor que deseas asignar como clave foránea
            print("Estado del usuario ", user)
            if metodoPagoF == 'MP-EFEC':
                metodo = request.POST['efectivoSel']
            elif metodoPagoF == 'MP-TARJ':
                metodo = request.POST['tarjetaSel']
            else:
                context = self.get_context_data('block', 'El método de pago no es válido', 'none', '')
                return render(request, self.template_name, context)
            try:
                nuevoPago = Pago(id_ahorro=transaction_id,
                                     descripcion=notaF,
                                     monto=montoF,
                                     fecha=fechaF,
                                     fk_cuenta=Tarjeta.objects.get(id_cuenta=metodo),
                                     fk_usuario=User.objects.get(id = usuario_id),
                                    )
                nuevoPago.save()
                context = self.get_context_data('none', '', 'block', 'Los datos se han registrado correctamente.')
                return render(request, self.template_name, context)
            except IntegrityError:
                context = self.get_context_data('block', 'Error, se presentó una duplicación de datos', 'none', '')
                return render(request, self.template_name, context)
            except Exception as e:
                context = self.get_context_data('block', f"Los datos ingresados no son válidos: {str(e)}", 'none', '')
                return render(request, self.template_name, context)
    
    # Realiza las consultas y renderiza en los campos
    def get_context_data(self, mensajeError, error, mostrarMensaje, mensaje):        
        # Obtiene el usuairo y su ID
        usuario = self.request.user
        usuario_id = usuario.id
        
        # Consulta las monedas registradas en la BD
        monedas = Moneda.objects.all()
        # Consultas para ingresos
        categorias = Categoria.objects.filter(fk_tipo='TP-GAS')
        
        # Consulta para retornar las carteras del usuario.
        carteras = Tarjeta.objects.filter(
            fk_metodo_pago__id_metodotipo='MP-EFEC',
            fk_usuario=usuario_id
        )
        
        # Consulta para retornar las tarjetas del usuario.
        tarjetas = Tarjeta.objects.filter(
            fk_metodo_pago__id_metodotipo='MP-TARJ',
            fk_usuario=usuario_id
        )
        
        return {
            'monedas': monedas,
            'categorias': categorias,
            'carteras': carteras,
            'tarjetas': tarjetas,
            'mostrarError': mensajeError,
            'error': error,
            'mostrarMensaje': mostrarMensaje,
            'mensaje': mensaje,
        }

    # Verifica que existan los campos del HTML
    def verifica(self):
        if ('fecha' not in self.request.POST or
            'monto' not in self.request.POST or
            'moneda' not in self.request.POST or
            'nota' not in self.request.POST or
            'metodoPago' not in self.request.POST or
            'nota' not in self.request.POST or
            'efectivoSel' not in self.request.POST or
            'tarjetaSel' not in self.request.POST
            ):
            return False
        else:
            return True

@method_decorator(login_required, name='dispatch')
class Tarjetas(APIView):
    template_name = "Tarjetas.html"
    def get(self, request):
        return render(request, self.template_name, {'mostrarError':'none',
                                                    'mostrarMensaje':'none',
                                                    'error':'Hola'})

    def post(self, request):
        usuario = request.user  # Obtiene al usuario loggeado
        numero = request.POST.get('numero')
        nombre = request.POST.get('nombre')
        tipo = request.POST.get('tipo')

        # Comprobar que no vengan datos vacíos
        if numero is None or nombre is None or request.POST.get('tipo') is None:
            return render(request, self.template_name, {'mostrarError':'block',
                                                        "error": 'Todos los campos son obligatorios.'
                                                        })
        else:
            try:
                tipo_pago = MetodoPago.objects.get(id_metodotipo=tipo)
                nuevaCuenta = Tarjeta(id_cuenta=numero,
                                      nombre_cuenta=nombre,
                                      fk_metodo_pago=tipo_pago,
                                      fk_usuario=usuario)
                nuevaCuenta.save()  # Guarda el nuevo objeto Tarjeta en la base de datos
                return render(request, self.template_name, {'mostrarMensaje':'block',
                                                            'mensaje':'Se ha completado el registro exitosamente.'
                    })  # Página de éxito
            except IntegrityError:
                mensaje_error = 'Esta cuenta ya ha sido registrada previamente'
                print(mensaje_error)  # Agrega esto para verificar que se alcanza esta sección
                return render(request, self.template_name, {'mostrar': 'block', 'error': mensaje_error})
            except Exception as e:
                mensaje_error = f"Los datos ingresados no son válidos: {str(e)}"
                return render(request, self.template_name, {'mostrar':'block',
                                                            'error': mensaje_error})


@method_decorator(login_required, name='dispatch')
class Metas (APIView):
    template_name = "metas.html"

    # MÉTODO GET
    def get(self, request):
        # mensajeError, error, mostrarMensaje, mensaje
        context = self.get_context_data('none', '', 'none', '')
        return render(request, self.template_name, context)

    # MÉTODO POST
    def post(self, request):
        #Comprueba que estén los datos requeridos.
        if self.verifica() == False:
            context = self.get_context_data('block', 'Todos los campos son obligatorios.', 'none', '')
            return render(request, self.template_name, context)
        else:
            # OBTTENER LOS DATOS POR POST
            objetivoF = request.POST['objetivo']
            fechaInicioF = request.POST['fechaInicio']
            fechaTerminoF = request.POST['fechaTermino']
            notaF = request.POST['nota']
            
            # GENERACIÓN DE ID DE TRANSACCIÓN (INGRESO)
            current_time = datetime.now()
            usuario = request.user
            usuario_id = usuario.id
            fecha = f"A{usuario_id}-{current_time.strftime('%Y%m%d%H%M%S')}"
            transaction_id = str(fecha)
            
            try:
                nuevaMeta = MetaFinanciera(id_meta=transaction_id,
                                     descripcion=notaF,
                                     objetivo=objetivoF,
                                     fechaInicio=fechaInicioF,
                                     fechaTermino=fechaTerminoF,
                                     fk_usuario=User.objects.get(id = usuario_id),
                                    )
                nuevaMeta.save()
                context = self.get_context_data('none', '', 'block', 'Los datos se han registrado correctamente.')
                return render(request, self.template_name, context)
            except IntegrityError:
                context = self.get_context_data('block', 'Error, se presentó una duplicación de datos', 'none', '')
                return render(request, self.template_name, context)
            except Exception as e:
                context = self.get_context_data('block', f"Los datos ingresados no son válidos: {str(e)}", 'none', '')
                return render(request, self.template_name, context)
    
    # Realiza las consultas y renderiza en los campos
    def get_context_data(self, mensajeError, error, mostrarMensaje, mensaje):
        return {
            'mostrarError': mensajeError,
            'error': error,
            'mostrarMensaje': mostrarMensaje,
            'mensaje': mensaje,
        }
    
    # Verifica que se envíen los datos requeridos por POST
    def verifica(self):
        if ('objetivo' not in self.request.POST or
            'fechaInicio' not in self.request.POST or
            'fechaTermino' not in self.request.POST or
            'nota' not in self.request.POST
            ):
            return False
        else:
            return True


def Reestablecer(request):
    template_name = "forgot-password.html"
    if request.method == 'GET':
        render(request, template_name)
    else:
        if request.POST['email']:
            try:
                usuario = User.objects.filter(email=request.POST['email'])
                if usuario.exists():
                    usuario = usuario[0]
                    nombre = usuario.first_name
                    # Creación de contraseña Aleatoria
                    longitud = 10  # Longitud de la contraseña
                    caracteres = string.ascii_letters + string.digits  # Caracteres permitidos
                    # Contiene la cadena de la contraseña
                    contra_aleatoria = ''.join(secrets.choice(caracteres) for _ in range(
                        longitud))  # Generacion de la contraseña

                    usuario.set_password(contra_aleatoria)
                    usuario.save()

                    # Se prepara el correo a enviar
                    subject = 'Restablecimiento de Contraseña'
                    recipient_list = [request.POST['email']]

                    # Crea el contenido HTML
                    html_message = render_to_string('correo/Restablecimiento.html',
                                                    {'nombre': nombre,
                                                     'password': contra_aleatoria})
                    plain_message = strip_tags(html_message)
                    # Envía el correo
                    enviarCorreo(subject, plain_message,
                                 recipient_list, html_message)
                    # Redirecciona al Login
                    return redirect('login')
            except usuario.DoesNotExist:
                print("No se encontró")
    return render(request, template_name, {
        'mensaje': 'Si el correo proporcionado coincide con el registrado te enviaremos un mensaje con tus nuevas credenciales'
    })


def enviarCorreo(subject, plain_message, recipient_list, html_message):
    send_mail(subject, plain_message, 'antonio2552001@gmail.com',
              recipient_list, html_message=html_message)


class tabla_html(APIView):
    template_name = "mi_tabla.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)

class dashboard(APIView):
    template_name = 'dashboard.html'
    
    def get(self, request):
        # Primera grafica -calificación- de barras
        calificaciones = encuesta.objects.values('pregunta1').annotate(total=Count('pregunta1')).order_by('pregunta1')
        etiquetasPregunta1 = [calificacion['pregunta1'] for calificacion in calificaciones]
        valoresPregunta1 = [calificacion['total'] for calificacion in calificaciones]
        
        # Pregunta 2 -facilidad de uso- de barras
        facilidades = encuesta.objects.values('pregunta2').annotate(total=Count('pregunta2')).order_by('pregunta2')
        etiquetasPregunta2 = [facilidad['pregunta2'] for facilidad in facilidades]
        valoresPregunta2 = [facilidad['total'] for facilidad in facilidades]
        
        # Pregunta 3 -interfaz amigable- circular
        usos = encuesta.objects.values('pregunta3').annotate(total=Count('pregunta3'))
        etiquetasPregunta3 = [uso['pregunta3'] for uso in usos]
        valoresPregunta3 = [uso['total'] for uso in usos]
        
        # Pregunta 4 -frecuencia de problemas- dona
        problemas = encuesta.objects.values('pregunta4').annotate(total=Count('pregunta4'))
        etiquetasPregunta4 = [problema['pregunta4'] for problema in problemas]
        valoresPregunta4 = [problema['total'] for problema in problemas]
        
        # Pregunta 5 -frecuencia de problemas- dona
        adaptables = encuesta.objects.values('pregunta5').annotate(total=Count('pregunta5'))
        etiquetasPregunta5 = [adaptable['pregunta5'] for adaptable in adaptables]
        valoresPregunta5 = [adaptable['total'] for adaptable in adaptables]
        
        # Pregunta 6 -mejoras- radar
        mejoras = encuesta.objects.values('pregunta6').annotate(total=Count('pregunta6')).order_by('pregunta6')
        etiquetasPregunta6 = [mejora['pregunta6'] for mejora in mejoras]
        valoresPregunta6 = [mejora['total'] for mejora in mejoras]
        
        # Pregunta 7 -informes - barras
        informes = encuesta.objects.values('pregunta7').annotate(total=Count('pregunta7'))
        etiquetasPregunta7 = [informe['pregunta7'] for informe in informes]
        valoresPregunta7 = [informe['total'] for informe in informes ]
        
        # Pregunta 8 -divisas- barras
        divisas = encuesta.objects.values('pregunta8').annotate(total=Count('pregunta8')).order_by('pregunta8')
        etiquetasPregunta8 = [divisa['pregunta8'] for divisa in divisas]
        valoresPregunta8 = [divisa['total'] for divisa in divisas]
        
        # Pregunta 9 -interrupciones- linea
        interrupciones = encuesta.objects.values('pregunta9').annotate(total=Count('pregunta9'))
        etiquetasPregunta9 = [interrupcion['pregunta9'] for interrupcion in interrupciones]
        valoresPregunta9 = [interrupcion['total'] for interrupcion in interrupciones]
        
        # Pregunta 10 -pérdidas- circular
        perdidas = encuesta.objects.values('pregunta10').annotate(total=Count('pregunta10'))
        etiquetasPregunta10 = [perdida['pregunta10'] for perdida in perdidas]
        valoresPregunta10 = [perdida['total'] for perdida in perdidas]
        
        return render(request, self.template_name,{'etiquetasPregunta1': etiquetasPregunta1,
                                                   'valoresPregunta1': valoresPregunta1,
                                                   'etiquetasPregunta2': etiquetasPregunta2,
                                                   'valoresPregunta2': valoresPregunta2,
                                                   'etiquetasPregunta3': etiquetasPregunta3,
                                                   'valoresPregunta3': valoresPregunta3,
                                                   'etiquetasPregunta4': etiquetasPregunta4,
                                                   'valoresPregunta4': valoresPregunta4,
                                                   'etiquetasPregunta5': etiquetasPregunta5,
                                                   'valoresPregunta5': valoresPregunta5,
                                                   'etiquetasPregunta6': etiquetasPregunta6,
                                                   'valoresPregunta6': valoresPregunta6,
                                                   'etiquetasPregunta7': etiquetasPregunta7,
                                                   'valoresPregunta7': valoresPregunta7,
                                                   'etiquetasPregunta8': etiquetasPregunta8,
                                                   'valoresPregunta8': valoresPregunta8,
                                                   'etiquetasPregunta9': etiquetasPregunta9,
                                                   'valoresPregunta9': valoresPregunta9,
                                                   'etiquetasPregunta10': etiquetasPregunta10,
                                                   'valoresPregunta10': valoresPregunta10})
    
    def post(self, request):
        return render(request, self.template_name)
   
""" # GOOGLE CALENDAR
# def interactuar_con_google_calendar(request):
#     # Ruta al archivo JSON de credenciales que descargaste
#     archivo_de_credenciales = os.path.join(BASE_DIR, 'finanzapp-402806-84e70ab4eb8a.json')

#     # Carga las credenciales desde el archivo JSON
#     credentials = service_account.Credentials.from_service_account_file(
#         archivo_de_credenciales,
#         scopes=['https://www.googleapis.com/auth/calendar']
#     )

#     # Construye el servicio de Google Calendar API
#     service = build('calendar', 'v3', credentials=credentials)

#     # Ahora puedes utilizar 'service' para interactuar con la API de Google Calendar

#     # Por ejemplo, obtener la lista de calendarios
#     calendarios = service.calendarList().list().execute()
#     print(calendarios)
#     return render(request, 'calendar.html', {'calendarios': calendarios})

# def test_calendar():
#     print("RUNNING TEST_CALENDAR()")
#     test_event1 = {"start": {"date": "2022-01-01"}, "end": {"date": "2022-01-07"}, "summary":"test event 1"}
#     test_event2 = {"start": {"date": "2022-02-01"}, "end": {"date": "2022-02-07"}, "summary":"test event 2"}
#     events = [test_event1, test_event2]

#     return events

# def demo(request):
#     results = test_calendar()
#     context = {"results": results}
#     return render(request, 'calendar.html', context)


# class AuthCompleteView(View):
#     def get(self, request, *args, **kwargs):
#         # Inicializa la estrategia de autenticación
#         strategy = load_strategy(request)
#         backend = google_auth_oauthlib(DjangoStrategy(request, strategy), redirect_uri=None)

#         # Intenta autenticar al usuario con Google
#         try:
#             user = backend.do_auth(request.GET.urlencode())
#             login(request, user)
#         except AuthException as e:
#             # Manejar errores de autenticación aquí si es necesario
#             # Puedes redirigir a una página de error o mostrar un mensaje
#             return HttpResponseRedirect('/auth/google/error')

#         # Si la autenticación fue exitosa, redirige a la página de inicio o a donde desees
#         return HttpResponseRedirect('/')

#     def post(self, request, *args, **kwargs):
#         return HttpResponse("Método POST no permitido", status=405)
    
# def list_files(request):
#     credentials = Credentials.from_service_account_file(
#         settings.GOOGLE_DRIVE_CREDENTIALS,
#         scopes=['https://www.googleapis.com/auth/drive.readonly']
#     )

#     service = build('drive', 'v3', credentials=credentials)

#     results = service.files().list().execute()
#     files = results.get('files', [])

#     # return JsonResponse(files, safe=False)
#     return render(request, 'list_files.html', {'files': files})

# def login_with_google(request):
#     return redirect('social:begin', 'google-oauth2')

# def conectar(request):
#     # Obtén el cliente de Google Drive.
#     client = GoogleDriveClient()

#     # Listado de todos los archivos en la raíz del almacenamiento de Google Drive.
#     files = client.list_files()

#     context = {
#         'files': files,
#     }

#     return render(request, 'conectar.html', context)

# CONEXIÓN CON API OPEN EXCHANGE RATE (CONVERSIÓN DE DIVISAS)
# def get_exchange_rates(request):
#     if request.GET:
#         api_key = '051f01d6b07d4ea5997f2a21d8c4c14f'  # Clave de API
#         base_currency = 'USD'
#         symbols = 'EUR,GBP'

#         url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}&base={base_currency}&symbols={symbols}"
#         response = requests.get(url)

#         if response.status_code == 200:
#             data = response.json()
#             return JsonResponse(data)
#         else:
#             return JsonResponse({'error': 'No se pudieron obtener las tasas de cambio.'}, status=500) """

def exchange_rate(request):
    try:
        api_key = settings.OPEN_EXCHANGE_RATES_API_KEY
        base_currency = 'USD'
        api_url = f'https://openexchangerates.org/api/latest.json?app_id={api_key}&base={base_currency}'
        # Se añade historical/2013-02-16.json para consultar en determinada fecha
        response = requests.get(api_url)
        response.raise_for_status()  # Manejo de errores de solicitud

        if response.status_code == 200:
            data = response.json()
        else:
            # Puedes manejar la respuesta en función del estado aquí
            data = {}
    except requests.RequestException as e:
        data = {}

    return render(request, 'exchange_rate.html', {'data': data})