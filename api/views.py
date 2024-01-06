from datetime import datetime, date, timedelta, timezone
from sqlite3 import IntegrityError
from django.core.mail import send_mail
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
import requests
from rest_framework.views import APIView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User  # Permite el registro
# Permite crear la cookie con el registro del login
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
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
from django.contrib.auth import login
from django.conf import settings
from django.http import JsonResponse
from rest_framework.response import Response
# Calendario
from .calendar_setup import get_calendar_service
from django.views.decorators.csrf import csrf_exempt
import pytz
# from oauthlib.oauth2.rfc6749.errors import AccessDeniedError
# from google.auth.exceptions import RefreshError
# from google.auth.exceptions import AccessDeniedError

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
class signin(APIView, LoginRequiredMixin):
    def get(self, request):
        return render(request, 'login.html', {
            'form': AuthenticationForm
        })
        
    def post(self, request):
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
        context = self.get_context_data('none', '', 'none', '')
        return render(request, self.template_name, context)

    def post(self, request):
        usuario = self.request.user
        usuarioId = usuario.id
        
        try:
            user = User.objects.get(id=usuarioId)
            user.first_name = request.POST['nombre']
            user.last_name = request.POST['apellidos']
            user.email = request.POST['email']
            user.save()
            
            context = self.get_context_data('none', '', 'block', 'Los datos se actualizaron correctamente.')
            return render(request, self.template_name, context)
        except IntegrityError as e:
            context = self.get_context_data('block', 'Este correo ya ha sido usado por otro usuario', 'none', '')
            return render(request, self.template_name, context)
        except:
            context = self.get_context_data('block', 'No es posible actualizar los campos', 'none', '')
            return render(request, self.template_name, context)
            
    def get_context_data(self, mensajeError, error, mostrarMensaje, mensaje):
         # Obtiene el usuairo y su ID
        usuario = self.request.user
        usuario_id = usuario.id
        user=usuario.get_username
        email=usuario.email
        nombre = usuario.first_name
        apellidos = usuario.last_name
        
        # Consulta las monedas registradas en la BD
        monedas = Moneda.objects.all()
        
        return {
            'monedas': monedas,
            'user': user,
            'nombre': nombre,
            'apellidos': apellidos,
            'email': email,
            'mostrarError': mensajeError,
            'error': error,
            'mostrarMensaje': mostrarMensaje,
            'mensaje': mensaje,
        }


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
        fecha_actual = date.today()
        primerDia = fecha_actual.replace(day=1)
        
        # Calcula el primer día del próximo mes restando un día al primer día del mes actual
        primer_dia_del_proximo_mes = fecha_actual.replace(day=1) + timedelta(days=31)
        # Resta un día al primer día del próximo mes para obtener el último día del mes actual
        ultimoDia = primer_dia_del_proximo_mes - timedelta(days=1)
        
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
        
        # Para las tablas
        # Consulta las transacciones según las fechas y el usuario
        ingresos = Transaccion.objects.filter(
            Q(id_transaccion__startswith='I') &
            Q(fk_usuario=usuario_id)
        )
        
        return {
            'monedas': monedas,
            'categorias': categorias,
            'carteras': carteras,
            'tarjetas': tarjetas,
            'ingresos': ingresos,
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
        
        # Para las tablas
        # Consulta las transacciones según las fechas y el usuario
        gastos = Transaccion.objects.filter(
            Q(id_transaccion__startswith='G') &
            Q(fk_usuario=usuario_id)
        )
        return {
            'monedas': monedas,
            'categorias': categorias,
            'carteras': carteras,
            'tarjetas': tarjetas,
            'gastos': gastos,
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
        # OBTTENER LOS DATOS POR POST
        if self.verifica() == True:
            tituloF = request.POST['titulo']
            descripcionF = request.POST['descripcion']
            montoF = request.POST['monto']
            fechaInicioF = request.POST['fechaInicio']
            fechaTerminoF = request.POST['fechaTermino']
            frecuenciaF = request.POST['frecuencia']
            monedaF = request.POST['moneda']
            # fechaInicio, fechaTermino, tituloEvento, descripcion, frecuencia
            insercionCalendario = self.create_event(fechaInicioF, fechaTerminoF, tituloF, descripcionF)
            if insercionCalendario is False:
                context = self.get_context_data('block', 'Ha ocurrido un error al conectar con Google Calendar.', 'none', '')
                return render(request, self.template_name, context)
            else:
                # GENERACIÓN DE ID DE TRANSACCIÓN (INGRESO)
                usuario = request.user
                usuario_id = usuario.id
                transaction_id = insercionCalendario
                metodoPagoF = request.POST['metodoPago']
                user = get_object_or_404(User, id=usuario_id)  # usuario_id es el valor que deseas asignar como clave foránea
                if metodoPagoF == 'MP-EFEC':
                    metodo = request.POST['efectivoSel']
                elif metodoPagoF == 'MP-TARJ':
                    metodo = request.POST['tarjetaSel']
                else:
                    context = self.get_context_data('block', 'El método de pago no es válido', 'none', '')
                    return render(request, self.template_name, context)
                try:
                    print("INSERTANDO DATOS EN PAGO")
                    nuevoPago = Pago(id_pago=transaction_id,
                                     titulo=tituloF,
                                     descripcion=descripcionF,
                                     monto=montoF,
                                     fechaInicio=fechaInicioF,
                                     fechaTermino=fechaTerminoF,
                                     frecuencia=frecuenciaF,
                                     fk_cuenta=Tarjeta.objects.get(id_cuenta=metodo),
                                     fk_usuario=User.objects.get(id = usuario_id),
                                    )
                    nuevoPago.save()
                    print("EL DATO SE HA INSERTADO")
                    context = self.get_context_data('none', '', 'block', 'Los datos se han registrado correctamente.')
                    return render(request, self.template_name, context)
                except IntegrityError:
                    context = self.get_context_data('block', 'Error, duplicación de datos', 'none', '')
                    return render(request, self.template_name, context)
                # except errors.AccessDeniedError as e:
                #     # Manejar el error de acceso denegado aquí
                #     context = self.get_context_data('block', 'AccessDeniedError. Asegúrate de otorgar los permisos necesarios.', 'none', '')
                #     return render(request, self.template_name, context)
                # except RefreshError as e:
                #     context = self.get_context_data('block', 'RefreshError. Asegúrate de otorgar los permisos necesarios.', 'none', '')
                #     return render(request, self.template_name, context)
                except Exception as e:
                    context = self.get_context_data('block', f"Los datos ingresados no son válidos: {str(e)}", 'none', '')
                    return render(request, self.template_name, context)
        else:
            context = self.get_context_data('block', "Todos los campos son obligatorios", 'none', '')
            return render(self.request, self.template_name, context)
    
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
        
        # Consulta las eventos para las tablas
        pagos = Pago.objects.filter(
            fk_usuario=usuario_id
        )
        
        return {
            'monedas': monedas,
            'categorias': categorias,
            'carteras': carteras,
            'tarjetas': tarjetas,
            'pagos': pagos,
            'mostrarError': mensajeError,
            'error': error,
            'mostrarMensaje': mostrarMensaje,
            'mensaje': mensaje,
        }

    # Verifica que existan los campos del HTML
    def verifica(self):
        if ('titulo' not in self.request.POST or
            'descripcion' not in self.request.POST or
            'fechaInicio' not in self.request.POST or
            'fechaTermino' not in self.request.POST or
            'frecuencia' not in self.request.POST or
            'monto' not in self.request.POST or
            'moneda' not in self.request.POST or
            'categoria' not in self.request.POST or
            'metodoPago' not in self.request.POST or
            ('efectivoSel' not in self.request.POST or
            'tarjetaSel' not in self.request.POST)
           ):
            return False
        else:
            return True
        
    # Crea el evento en Google Calendar
    def create_event(self, fechaInicios, fechaTerminos, tituloEvento, descripcion):
        # (aaaa, mm, dd, h, m)
        fechaInicio = datetime.fromisoformat(fechaInicios)
        fechaTermino = datetime.fromisoformat(fechaTerminos)
        self.tituloEvento = tituloEvento
        fechaInicioISO = fechaInicio.isoformat()
        fechaTerminoISO = fechaTermino.isoformat()
        calendar_service = get_calendar_service() 
        try:
            print("INTENTANDO CONECTAR CON GOOGLE CALENDAR")
            event_result = calendar_service.events().insert(calendarId='primary',
                body={
                    "summary": tituloEvento,
                    "description": descripcion,
                    "start": {"dateTime": fechaInicioISO, "timeZone": 'America/Mexico_City'},
                    "end": {"dateTime": fechaTerminoISO, "timeZone": 'America/Mexico_City'},
                }
            ).execute()
            print("Evento creado con éxito!")
            print("ID: ", event_result['id'])
            return event_result['id']
        except Exception:
            return False

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
            monedaF = request.POST['moneda']
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
                                     fk_moneda=Moneda.objects.get(id_moneda=monedaF),
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
        # Obtiene el usuairo y su ID
        usuario = self.request.user
        usuario_id = usuario.id
        
        # Consulta las monedas registradas en la BD
        monedas = Moneda.objects.all()
        
        # Consulta las eventos para las tablas
        metas = MetaFinanciera.objects.filter(
            fk_usuario=usuario_id
        )
        return {
            'monedas': monedas,
            'metas': metas,
            'mostrarError': mensajeError,
            'error': error,
            'mostrarMensaje': mostrarMensaje,
            'mensaje': mensaje,
        }
    
    # Verifica que se envíen los datos requeridos por POST
    def verifica(self):
        if ('objetivo' not in self.request.POST or
            'moneda' not in self.request.POST or
            'fechaInicio' not in self.request.POST or
            'fechaTermino' not in self.request.POST or
            'nota' not in self.request.POST
            ):
            return False
        else:
            return True

class actualizarMeta(APIView):
    def get(self, request):
        if request.method == "GET" and 'id_meta' in request.GET:
            # Obtiene el usuario y su ID
            usuario = request.user
            usuario_id = usuario.id
            
            # Obtiene id_meta de la solicitud GET
            id_meta = request.GET.get('id_meta')

            # Consulta para obtener la instancia de MetaFinanciera del usuario
            try:
                meta = MetaFinanciera.objects.get(id_meta=id_meta, fk_usuario=usuario_id)
                
                # Serializa los datos de la instancia de MetaFinanciera
                meta_data = serializers.serialize('json', [meta])

                return JsonResponse({'meta': meta_data})
            except MetaFinanciera.DoesNotExist:
                return JsonResponse({"error": f"No se encontró ninguna MetaFinanciera con id_meta='{id_meta}' para el usuario actual"})
            
    def post(self, request):
        if self.comprobarCampos():
            
            try:
                idEditar = request.POST.get('idEditar')
                objetivoEditar = request.POST.get('objetivoEditar')
                monedaEditar = request.POST.get('monedaEditar')
                fechaInicioEditar = request.POST.get('fechaInicioEditar')
                fechaTerminoEditar = request.POST.get('fechaTerminoEditar')
                notaEditar = request.POST.get('notaEditar')
                
                meta = get_object_or_404(MetaFinanciera, id_meta=idEditar)
                meta.objetivo = objetivoEditar
                meta.fk_moneda = Moneda.objects.get(id_moneda = monedaEditar)
                meta.fechaInicio =fechaInicioEditar
                meta.fechaTermino = fechaTerminoEditar
                meta.descripcion = notaEditar
                
                meta.save()
                
                return Response({"message": "La edición se realizó con éxito"})
            except IntegrityError as e:
                return JsonResponse({"error": "Se encontró un registro dulicado"}, status=400)
            except Exception as e:
                return JsonResponse({"error": "No se pudo realizar la edición"}, status=400)
            
        else:
            print("Todos los campos de edición son obligatorios")
            return JsonResponse({'error': "Todos los campos de edición son obligatorios"}, status=400)
        
    def comprobarCampos(self):
        if ('idEditar' not in self.request.POST or 'objetivoEditar' not in self.request.POST or
            'monedaEditar' not in self.request.POST or 'fechaInicioEditar' not in self.request.POST or
            'fechaTerminoEditar' not in self.request.POST or 'notaEditar' not in self.request.POST):
            return False
        else:
            return True

class eliminarMeta(APIView):
    def post(self, request):
        if 'id_meta' not in self.request.POST:
            return JsonResponse({'error': "Ocurrió un error al reaizar esta operación"}, status=400)
            
        else:
            try:
                id_meta = request.POST.get('id_meta')
                
                meta = get_object_or_404(MetaFinanciera, id_meta=id_meta)
                
                meta.delete()
                
                return Response({"message": "La meta se eliminó con éxito."})
            except Exception as e:
                return JsonResponse({"error": "No fue posible eliminar eñ registro"}, status=400)
        
    def comprobarCampos(self):
        if ('id_meta' not in self.request.POST):
            return False
        else:
            return True

class actualizarTransaccion(APIView):
    def get(self, request):
        if request.method == "GET" and 'id_transaccion' in request.GET:
            # Obtiene el usuario y su ID
            usuario = request.user
            usuario_id = usuario.id
            
            # Obtiene id_meta de la solicitud GET
            id_transaccion = request.GET.get('id_transaccion')

            # Consulta para obtener la instancia de MetaFinanciera del usuario
            try:
                transaccion = Transaccion.objects.get(id_transaccion=id_transaccion, fk_usuario=usuario_id)
                
                # Serializa los datos de la instancia de MetaFinanciera
                # transaccion_data = serializers.serialize('json', [transaccion])
                transaccion_data = {
                    'id_transaccion': transaccion.id_transaccion,
                    'fecha': transaccion.fecha,
                    'monto': transaccion.monto,
                    'moneda': transaccion.fk_moneda.id_moneda,
                    'categoria': transaccion.fkcategoria.id_categoria,
                    'metodoPago': transaccion.fk_cuenta.fk_metodo_pago.id_metodotipo,
                    'cuenta': transaccion.fk_cuenta.id_cuenta,
                    'descripcion': transaccion.descripcion,
                }

                return JsonResponse({'transaccion': transaccion_data})
            except Transaccion.DoesNotExist:
                return JsonResponse({"error": f"No se encontró ninguna transaccion con id_transaccion='{id_transaccion}' para el usuario actual"}, status=400)
            
    def post(self, request):
        if self.comprobarCampos():
            
            try:
                idEditar = request.POST.get('idEditar')
                fechaEditar = request.POST.get('fechaEditar')
                montoEditar = request.POST.get('montoEditar')
                monedaEditar = request.POST.get('monedaEditar')
                categoriaEditar = request.POST.get('categoriaEditar')
                tarjetaSelEditar = request.POST['cuenta']
                notaEditar = request.POST.get('notaEditar')
                
                transaccion = get_object_or_404(Transaccion, id_transaccion=idEditar)
                transaccion.fecha = fechaEditar
                transaccion.fk_moneda = Moneda.objects.get(id_moneda = monedaEditar)
                transaccion.monto = montoEditar
                transaccion.fkcategoria = Categoria.objects.get(id_categoria = categoriaEditar)
                transaccion.fk_cuenta = Tarjeta.objects.get(id_cuenta = tarjetaSelEditar)
                transaccion.descripcion = notaEditar
                
                transaccion.save()
                
                return Response({"message": "La edición se realizó con éxito"})
            except IntegrityError as e:
                return JsonResponse({"error": "Se encontró un registro dulicado"}, status=400)
            except Exception as e:
                print("ERROR: ", e)
                return JsonResponse({"error": "No se pudo realizar la edición"}, status=400)
            
        else:
            print("Todos los campos de edición son obligatorios")
            return JsonResponse({'error': "Todos los campos de edición son obligatorios"}, status=400)
        
    def comprobarCampos(self):
        if ('idEditar' not in self.request.POST or 'fechaEditar' not in self.request.POST or
            'montoEditar' not in self.request.POST or 'monedaEditar' not in self.request.POST or
            'categoriaEditar' not in self.request.POST or 'cuenta' not in self.request.POST or
            'notaEditar' not in self.request.POST):
            return False
        else:
            return True

class eliminarTransaccion(APIView):
    def post(self, request):
        print("POST")
        if 'id_transaccion' not in self.request.POST:
            return JsonResponse({'error': "Ocurrió un error al reaizar esta operación"}, status=400)
            
        else:
            try:
                id_transaccion = request.POST.get('id_transaccion')
                
                transaccion = get_object_or_404(Transaccion, id_transaccion=id_transaccion)
                
                transaccion.delete()
                
                return Response({"message": "La meta se eliminó con éxito."})
            except Exception as e:
                return JsonResponse({"error": "No fue posible eliminar eñ registro"}, status=400)

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

# CONEXIÓN CON API OPEN EXCHANGE RATE (CONVERSIÓN DE DIVISAS)
def exchange_rate():
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
    
    return data

    #return render(request, 'exchange_rate.html', {'data': data})

class Conversor(APIView):
    template_name = "conversor.html"

    def get(self, request):
        if 'monedaDe' in request.GET:
            if self.verifica() == False:
                return JsonResponse({'resultado': 'Todos los campos son obligatorios.'})
            else:
                monedaDe = request.GET['monedaDe']
                monedaA = request.GET['monedaA']
                divisas = exchange_rate()
                if monedaDe in divisas['rates'] and monedaA in divisas['rates']:
                    try:
                        if request.GET['convertir'].isdigit():
                            convertir = float(request.GET['convertir'])
                            divisaDe = divisas['rates'][monedaDe]
                            divisaA = divisas['rates'][monedaA]
                            
                            monto_en_dolares = convertir / divisaDe
                            conversion = monto_en_dolares * divisaA
                            
                            return JsonResponse({'resultado': conversion})
                        else:
                            return JsonResponse({'resultado': 'Solo valores numéricos.'})
                    except ValueError:
                        return JsonResponse({'resultado': 'Error de validación.'})
                else:
                    return JsonResponse({'resultado': 'Divisa no válida.'})
        else:
            context = self.get_context_data('none', '')
            return render(request, self.template_name, context)
                
    # Realiza las consultas y renderiza en los campos
    def get_context_data(self, mensajeError, error):
        # Consulta las monedas registradas en la BD
        monedas = Moneda.objects.all()
        return {
            'monedas': monedas,
            'mostrarError': mensajeError,
            'error': error,
        }

    # Verifica que existan los campos del HTML
    def verifica(self):
        if ('monedaDe' not in self.request.GET or
            'monedaA' not in self.request.GET or
            'convertir' not in self.request.GET
            ):
            return False
        else:
            return True
    
def eliminarEvento(request):
    if request.method == "POST":
        idEvento = request.POST.get("id")
        # Configura las credenciales y la API
        calendar_service = get_calendar_service()

        # ID del evento que deseas eliminar
        event_id = idEvento

        # ID del calendario en el que se encuentra el evento
        calendar_id = 'primary'  # 'primary' representa el calendario principal del usuario

        try:
            calendar_service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
            print(f'Evento con ID {event_id} eliminado con éxito.')
            eliminar_registro(idEvento)
        except Exception as e:
            print(f'Ocurrió un error al eliminar el evento: {str(e)}')
        
def eliminar_registro(registro_id):
    try:
        mi_registro = Pago.objects.get(id_pago=registro_id)
        mi_registro.delete()
        return HttpResponse("Registro eliminado con éxito")
    except Pago.DoesNotExist:
        return HttpResponse("El registro no existe")
    except IntegrityError:
        return HttpResponse("El registro no puede ser eiminado porque se encuentra referenciado en otra parte.")
    
@csrf_exempt
def actualizarEvento(request):
    if request.method == "POST":
        print("ACTUALIZANDO EVENTO...")
        print("EL ID ES: ",request.POST.get('idEditar'))
        id_pago = request.POST.get('idEditar')
        # Recuperar el objeto Pago
        evento = get_object_or_404(Pago, id_pago=id_pago)
        print("EVENTO: ", evento)

        try:
            # Actualizar los campos según los datos recibidos
        
            print("ACTUALIZANDO")
            evento.titulo = request.POST['tituloEditar']
            evento.monto = request.POST['montoEditar']
            evento.fechaInicio = request.POST['fechaInicioEditar']
            evento.fechaTermino = request.POST['fechaTerminoEditar']
            evento.frecuencia = request.POST['frecuenciaEditar']
            evento.descripcion = request.POST['descripcionEditar']
            # Guardar los cambios
            evento.save()
            print("SE ACTUALIZÓ")
            # Actualiza el evento en G-Calendar
            calendar_service = get_calendar_service()
            # Cree el evento
            """ FORMATO DE FECHA EN ISO """
            fechaInicio = datetime.fromisoformat(request.POST['fechaInicioEditar'])
            fechaTermino = datetime.fromisoformat(request.POST['fechaTerminoEditar'])
            # Define la zona horaria objetivo (UTC-6)
            zona_horaria_objetivo = pytz.timezone('America/Mexico_City')

            # Agrega la zona horaria a la fecha proporcionada
            fechaInicio_utc6 = fechaInicio.replace(tzinfo=zona_horaria_objetivo)
            fechaTermino_utc6 = fechaTermino.replace(tzinfo=zona_horaria_objetivo)
            # Convierte la fecha a UTC (si es necesario)
            fechaInicioF = fechaInicio_utc6.astimezone(pytz.utc)
            fechaTerminoF = fechaTermino_utc6.astimezone(pytz.utc)
            ############################
            fechaInicio = datetime.fromisoformat(request.POST['fechaInicioEditar'])
            fechaTermino = datetime.fromisoformat(request.POST['fechaTerminoEditar'])
            fechaInicioISO = fechaInicio.isoformat()
            fechaTerminoISO = fechaTermino.isoformat()
            """ FORMATO DE FECHA EN ISO """
            
            print("FECHA INICIO DE EDICIÓN: ", fechaInicioISO)
            print("FECHA TÉRMINO DE EDICIÓN: ", fechaTerminoISO)
            
            event = {
                "summary": request.POST['tituloEditar'],
                "description": request.POST['descripcionEditar'],
                "start": {"dateTime": fechaInicioISO, "timeZone": 'America/Mexico_City'},
                "end": {"dateTime": fechaTerminoISO, "timeZone": 'America/Mexico_City'},
            }
            calendar_service.events().update(calendarId="primary", eventId=id_pago, body=event).execute()
            print("EL EVENTO HA SIDO ACTUALIZADO")
        except Exception as e:
            print(f'OCURRIÓ UN ERROR AL ACTUALIZAR EL EVENTO: {str(e)}')
        
        return JsonResponse({'status': 'success', 'message': 'Datos guardados correctamente'})
    
    elif request.method == "GET" and 'id_pago' in request.GET:
        # Obtiene el usuario y su ID
        usuario = request.user
        usuario_id = usuario.id
        
        # Consulta para retornar el evento del usuario.
        eventos = Pago.objects.filter(
            id_pago=request.GET.get('id_pago'),
            fk_usuario=usuario_id
        )
        print(eventos)
        evento_list = [{'id_pago': evento.id_pago,
                        'titulo': evento.titulo,
                        'descripcion': evento.descripcion,
                        'monto': evento.monto,
                        'fechaInicio': evento.fechaInicio,
                        'fechaTermino': evento.fechaTermino,
                        'frecuencia': evento.frecuencia,
                        'fk_cuenta': {'id_cuenta': evento.fk_cuenta.id_cuenta},
                        } for evento in eventos]
        
        data = {
            'fechaInicio': '2023-11-11 20:54:00:00',
            'fechaTermino': '2023-11-11 21:54:00:00',
            'fk_moneda': 'USD',
            'evento': evento_list,
        }
        # Devuelve los datos como respuesta JSON
        return JsonResponse(data)

class dashboard_powerbi(APIView):
    def get(self, request):
        return render(request, 'Dashboard-PowerBI.html')
    def post(self, request):
        return render(request, 'Dashboard-PowerBI.html')