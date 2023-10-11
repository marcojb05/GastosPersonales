from sqlite3 import IntegrityError
from django.core.mail import send_mail
from django.shortcuts import render, redirect
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
from .models import Moneda, Categoria, Tarjeta, MetodoPago, Transaccion, TipoTransaccion

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
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)

# Ingresos del usuario
@method_decorator(login_required, name='dispatch')
class Ingresos (APIView):
    template_name = "ingresos.html"

    def get(self, request):
        # Consulta las monedas registradas en la BD
        monedas = Moneda.objects.all()
        # Consultas para ingresos
        categorias = Categoria.objects.filter(fk_tipo='TP-ING')
        return render(request, self.template_name, {'monedas': monedas,
                                                    'categorias': categorias})

    def post(self, request):
        cantidad = request.POST['cantidad']
        if cantidad is None:
            return render(request, self.template_name, {'error': 'Todos los campos son obligatorios'})
        else:
            try:
                #cuenta = Cuenta.objects.get(id_cuenta='12358432547554')
                nuevaTransaccion = Transaccion(id_transaccion='123123',
                                       fk_usuario=User.objects.get(id='2'),
                                       fk_cuenta=Cuenta.objects.get(id_cuenta='12358432547554'),
                                       fkcategoria=Categoria.objects.get(id_categoria='CAT-01'),
                                       fk_tipo=TipoTransaccion.objects.get(id_tipo='TP-ING'),
                                       descripcion='Ejemplo de ingreso',
                                       monto='350',
                                       fecha='2023-10-10',
                                       fk_moneda=Moneda.objects.get(id_moneda='MXN')
                )
                nuevaTransaccion.save()
                return render(request, self.template_name)
            except IntegrityError:
                return render(request, self.template_name, {'error': 'Hubo un problema al agregar la cuenta'})
        

@method_decorator(login_required, name='dispatch')
class Gastos (APIView):
    template_name = "gastos.html"

    def get(self, request):
        # Consulta las monedas registradas en la BD
        monedas = Moneda.objects.all()
        # Consultas para ingresos
        categorias = Categoria.objects.filter(fk_tipo=1)

        return render(request, self.template_name, {'monedas': monedas,
                                                    'categorias': categorias})

    def post(self, request):
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class Ahorros (APIView):
    template_name = "ahorros.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class DeudasPagos (APIView):
    template_name = "deudasypagos.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class Tarjetas(APIView):
    template_name = "Tarjetas.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        numero = request.POST.get('numero')
        nombre = request.POST.get('nombre')
        tipo = request.POST.get('tipo')
        usuario = User.objects.get(id=2)

        # Comprobar que no vengan datos vacíos
        if not numero or not nombre or not tipo:
            return render(request, self.template_name, {'error': 'Todos los campos son obligatorios'})
        else:
            try:
                tipo_pago = MetodoPago.objects.get(id_metodotipo=tipo)
                nuevaCuenta = Tarjeta(id_cuenta=numero,
                                    nombre_cuenta=nombre,
                                    fk_metodo_pago=tipo_pago,
                                    fk_usuario=usuario)
                nuevaCuenta.save()  # Save the new Cuenta object to the database
                return render(request, self.template_name)  # Página de éxito
            except IntegrityError:
                return render(request, self.template_name, {'error': 'Hubo un problema al agregar la cuenta'})


@method_decorator(login_required, name='dispatch')
class Metas (APIView):
    template_name = "metas.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)


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
