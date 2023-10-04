from django.core.mail import send_mail
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User  # Permite el registro
from django.contrib.auth import login, logout, authenticate # Permite crear la cookie con el registro del login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# Create your views here.

# Crea una vista para el registro

def Registrar(request):
    if request.method == "GET":
        return render(request, "signup.html", {
            'form': UserCreationForm
        })
    else:
        print(request.POST)
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
                message = 'Este es el mensaje de texto.'
                from_email = 'antonio2552001@gmail.com'
                recipient_list = [request.POST['email']]

                # Crea el contenido HTML
                html_message = render_to_string('correo/Bienvenida.html',
                                                {'nombre':request.POST['first_name'],
                                                 'username':request.POST['username'],
                                                 'password':request.POST['password1']})
                plain_message = strip_tags(html_message)

                send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
                
                # html_message = render_to_string('correo/Bienvenida.html',
                #                                 {'username':request.POST['username'],
                #                                  'password':request.POST['password']})
                # plain_message = strip_tags(html_message)
                # subject = 'Te damos la bienvenida'
                # #message = 'Hola '+request.POST['first_name']+", tu cuenta ha sido activada."
                # from_email = 'antonio2552001@gmail.com'
                # recipient_list = [request.POST['email']]

                # send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
                #Se envía el request y el usuario
                login(request, user)
                return redirect('login')
            
        return render(request, 'signup.html',{
            'form': UserCreationForm,
            "error": 'Las contraseñas no coinciden'
        })

#Cierra la sesión
def signout (request):
    logout(request)
    return redirect('login')

#Iniciar sesión
def signin(request):
    if request.method == "GET":
        return render(request, 'login.html',{
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password']
        )
        if user is None:
            return render(request, 'login.html',{
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

class Movimientos (APIView):
    template_name = "movimientos.html"
    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        return render(request, self.template_name)

@method_decorator(login_required, name='dispatch')
class Ingresos (APIView):
    template_name = "ingresos.html"
    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        return render(request, self.template_name)

@method_decorator(login_required, name='dispatch')
class Gastos (APIView):
    template_name = "gastos.html"
    def get(self, request):
        return render(request, self.template_name)
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
class Tarjetas (APIView):
    template_name = "tarjetas.html"
    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        return render(request, self.template_name)

@method_decorator(login_required, name='dispatch')
class Metas (APIView):
    template_name = "metas.html"
    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        return render(request, self.template_name)

@method_decorator(login_required, name='dispatch')
class Reestablecer (APIView):
    template_name = "forgot-password.html"
    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        return render(request, self.template_name)