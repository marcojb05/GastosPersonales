from datetime import datetime
import datetime
from sqlite3 import IntegrityError
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
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
from .models import Moneda, Categoria, Tarjeta, MetodoPago, Transaccion, TipoTransaccion, Ahorro, MetaFinanciera, Pago, encuesta

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
        print(calificaciones)
        etiquetasPregunta1 = [calificacion['pregunta1'] for calificacion in calificaciones]
        print("Etiquetas: ",etiquetasPregunta1)
        valoresPregunta1 = [calificacion['total'] for calificacion in calificaciones]
        print("Datos: ",valoresPregunta1)
        return render(request, self.template_name,{'etiquetasPregunta1': etiquetasPregunta1,
                                                   'valoresPregunta1': valoresPregunta1})
    
    def post(self, request):
        return render(request, self.template_name)