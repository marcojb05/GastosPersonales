"""
URL configuration for APITESCHI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from api.views import Home, Login, Registro, Reestablecer, Botones, Tarjetas, Graficas, Tablas, Animacion, Border, Color, Otro, Blank, Error404, Cuenta, Notificaciones, Conexiones
from api import views
from django.views.generic.base import RedirectView


favicon_view = RedirectView.as_view(url='/static/img/favicon.ico', permanent=True)

urlpatterns = [
    re_path(r'^favicon\.ico$', favicon_view),
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name='index'),
    path('signup/', views.Registrar, name="registro"),
    #login/: es lo que se verá en el navegador y sin extensión
    #Login.as_view(): Es la importación de la plantilla, es decir, la muestra, transforma y hace visible
    #name='login': Es el nombre que se utilizará para navegar entre situaciones
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    #path('registro/', Registro.as_view(), name="registro"),
    path('reestablecer/', Reestablecer.as_view(), name="reestablecer"),
    path('botones/', Botones.as_view(), name="botones"),
    path('tarjetas/', Tarjetas.as_view(), name="tarjetas"),
    path('graficas/', Graficas.as_view(), name="graficas"),
    path('tablas/', Tablas.as_view(), name="tablas"),
    path('animacion/', Animacion.as_view(), name="animacion"),
    path('border/', Border.as_view(), name="border"),
    path('color/', Color.as_view(), name="color"),
    path('otro/', Otro.as_view(), name="otro"),
    path('error404/', Error404.as_view(), name="error404"),
    path('blank/', Blank.as_view(), name="blank"),
    path('cuenta/', Cuenta.as_view(), name="cuenta"),
    path('notificaciones/', Notificaciones.as_view(), name="notificaciones"),
    path('conexiones/', Conexiones.as_view(), name="conexiones"),
]
