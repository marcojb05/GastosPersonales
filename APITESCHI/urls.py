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
from django.shortcuts import render
from django.urls import path
from api.views import (Home, signin, Cuenta, Notificaciones, Conexiones, Movimientos, Ingresos, Gastos, Ahorros, DeudasPagos, Tarjetas, Metas, 
                       dashboard, Conversor, dashboard_powerbi, actualizarMeta, eliminarMeta)
from api import views
from django.views.generic.base import RedirectView
from django.conf.urls import handler404, handler500

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)

handler404 = custom_404
handler500 = custom_500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name='index'),
    path('signup/', views.Registrar, name="registro"),
    #login/: es lo que se verá en el navegador y sin extensión
    #Login.as_view(): Es la importación de la plantilla, es decir, la muestra, transforma y hace visible
    #name='login': Es el nombre que se utilizará para navegar entre situaciones
    path('login/', signin.as_view(), name='login'),
    path('logout/', views.signout, name='logout'),
    path('reestablecer/', views.Reestablecer, name="reestablecer"),
    path('cuenta/', Cuenta.as_view(), name="cuenta"),
    path('notificaciones/', Notificaciones.as_view(), name="notificaciones"),
    path('conexiones/', Conexiones.as_view(), name="conexiones"),
    path('movimientos/', Movimientos.as_view(), name="movimientos"),
    path('ingresos/', Ingresos.as_view(), name="ingresos"),
    path('gastos/', Gastos.as_view(), name="gastos"),
    path('pagos/', Gastos.as_view(), name="pagos"),
    path('ahorros/', Ahorros.as_view(), name="ahorros"),
    path('deudasypagos/', DeudasPagos.as_view(), name="deudasypagos"),
    path('tarjetas/', Tarjetas.as_view(), name="tarjetas"),
    path('metas/', Metas.as_view(), name="metas"),
    path('dashboard/', dashboard.as_view(), name="dashboard"),
    path('conversor/', Conversor.as_view(), name='conversor'),
    path('dashboard_powerbi/', dashboard_powerbi.as_view(), name='dashboard_powerbi'),
    path('eliminarEvento/', views.eliminarEvento, name='eliminarEvento'),
    path('actualizarEvento/', views.actualizarEvento, name='actualizarEvento'),
    path('eliminarTransaccion/', views.eliminarTransaccion, name='eliminarTransaccion'),
    path('actualizarMeta/', actualizarMeta.as_view(), name='actualizarMeta'),
    path('eliminarMeta/', eliminarMeta.as_view(), name='eliminarMeta'),
]