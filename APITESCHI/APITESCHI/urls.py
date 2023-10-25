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
from django.urls import include, path, re_path
from api.views import Home, Cuenta, Notificaciones, Conexiones, Movimientos, Ingresos, Gastos, Ahorros, DeudasPagos, Tarjetas, Metas, dashboard, AuthCompleteView
from api import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name='index'),
    path('signup/', views.Registrar, name="registro"),
    #login/: es lo que se verá en el navegador y sin extensión
    #Login.as_view(): Es la importación de la plantilla, es decir, la muestra, transforma y hace visible
    #name='login': Es el nombre que se utilizará para navegar entre situaciones
    path('login/', views.signin, name='login'),
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
    # path('demo/', views.interactuar_con_google_calendar, name='demo'),
    path('demo/', views.interactuar_con_google_calendar, name='demo'),
    path('auth/google/', AuthCompleteView.as_view(), name='auth_google'),
    path('drive', views.list_files, name='drive'),
    path('auth/', include('social_django.urls', namespace='social')),
    # path('conecta', views.conectar,  name='conecta'),
    # path('auth/google/callback/', AuthCompleteView.as_view(), name='auth_google_callback'),
    # path('auth/google/error/', AuthErrorView.as_view(), name='auth_google_error'),
]
