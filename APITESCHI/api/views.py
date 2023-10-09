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
import tablib
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from api import models
from django.db import models
#Para la generación de contraseña Aleatoria
import secrets
import string

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
                recipient_list = [request.POST['email']]

                # Crea el contenido HTML
                html_message = render_to_string('correo/Bienvenida.html',
                                                {'nombre':request.POST['first_name'],
                                                 'username':request.POST['username'],
                                                 'password':request.POST['password1']})
                plain_message = strip_tags(html_message)

                enviarCorreo(subject, plain_message, recipient_list, html_message=html_message)
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

# @method_decorator(login_required, name='dispatch')
def Reestablecer (request):
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
                    #Contiene la cadena de la contraseña
                    contra_aleatoria = ''.join(secrets.choice(caracteres) for _ in range(longitud)) # Generacion de la contraseña
                    
                    usuario.set_password(contra_aleatoria)
                    usuario.save()
                    
                    # Se prepara el correo a enviar
                    subject = 'Restablecimiento de Contraseña'
                    recipient_list = [request.POST['email']]
                    

                    # Crea el contenido HTML
                    html_message = render_to_string('correo/Restablecimiento.html',
                                                    {'nombre':nombre,
                                                    'password':contra_aleatoria})
                    plain_message = strip_tags(html_message)
                    # Envía el correo
                    enviarCorreo(subject, plain_message, recipient_list, html_message)
                    # Redirecciona al Login
                    return redirect('login')
            except usuario.DoesNotExist:
                print("No se encontró")
    return render(request, template_name, {
        'mensaje': 'Si el correo proporcionado coincide con el registrado te enviaremos un mensaje con tus nuevas credenciales'
    })

def enviarCorreo(subject, plain_message, recipient_list, html_message):
    send_mail(subject, plain_message, 'antonio2552001@gmail.com', recipient_list, html_message=html_message)                

class tabla_html(APIView):
    template_name = "mi_tabla.html"
    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        return render(request, self.template_name)
    
""" def exportar_a_excel(request):
    # Renderiza el contenido del archivo HTML desde el directorio de plantillas
    rendered_html = render_to_string('mi_tabla.html', {})  # Reemplaza 'mi_tabla.html' con el nombre de tu archivo HTML

    # Parsea el HTML renderizado
    soup = BeautifulSoup(rendered_html, 'html.parser')

    # Crea un objeto de respuesta Excel
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="tabla_excel.xlsx"'

    # Crea un libro de trabajo de Excel y una hoja de trabajo
    workbook = Workbook()
    sheet = workbook.active

    # Encuentra la tabla en el HTML por su id
    tabla_html = soup.find('table', {'id': 'dataTable'})

    # Itera a través de las filas y celdas de la tabla HTML y copia los datos a Excel
    for row in tabla_html.find_all('tr'):
        fila_excel = []
        for cell in row.find_all(['th', 'td']):
            fila_excel.append(cell.get_text())
        sheet.append(fila_excel)

    # Guarda el libro de trabajo en la respuesta
    workbook.save(response)

    return response """
    
def exportar_excel(request):
    # Obtén los datos de la tabla HTML
    data = tablib.Dataset()
    table = request.POST['data']  # Asegúrate de que este sea el nombre correcto del campo POST

    # Aquí debes parsear los datos de la tabla HTML y agregarlos al objeto Dataset
    # Por ejemplo, puedes usar BeautifulSoup o cualquier otra forma que prefieras.

    # Luego, convierte los datos en un archivo Excel
    excel_data = data.export('xls')

    # Prepara la respuesta HTTP para descargar el archivo
    response = HttpResponse(excel_data, content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="tabla_excel.xls"'

    return response