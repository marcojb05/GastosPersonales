from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User  # Permite el registro
from django.contrib.auth import login, logout, authenticate # Permite crear la cookie con el registro del login
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
            try:
                # Registro del usuario
                # Devuelve un objeto user y es un usuario que se puede guardar en la bd
                user = User.objects.create_user(first_name=request.POST['first_name'],
                                                last_name=request.POST['last_name'],
                                                username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                #Se envía el request y el usuario
                login(request, user)
                return redirect('login')
            except:
                return render(request, 'signup.html',{
                    'form': UserCreationForm,
                    "error": 'El usuario ya existe'
                })
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
        

class Home (APIView):
    template_name = "index.html"
    # self es el equivalente del this en Java, hace referencia a sí mismo
    # request se consume

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)


class Login (LoginView):
    template_name = "login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)


class Registro (APIView):
    template_name = "register.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)


class Reestablecer (APIView):
    template_name = "forgot-password.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)


class Botones (APIView):
    template_name = "buttons.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)


class Tarjetas (APIView):
    template_name = "cards.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)


class Graficas (APIView):
    template_name = "charts.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)


class Tablas (APIView):
    template_name = "tables.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)


class Animacion (APIView):
    template_name = "utilities-animation.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)


class Border (APIView):
    template_name = "utilities-border.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)


class Color (APIView):
    template_name = "utilities-color.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)


class Otro (APIView):
    template_name = "utilities-other.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)


class Error404 (APIView):
    template_name = "404.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)


class Blank (APIView):
    template_name = "blank.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_name)
