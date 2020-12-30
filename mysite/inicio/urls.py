"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

from inicio.views import Home,Index,Admin,Empre,soli,pagoAutomatico, pagoAdelantado, estadoCuenta

urlpatterns = [

    path ('individual', Home.decirHola, name = 'individual'),
    path('menuAd', Admin.enviar, name='menuAd'),
    path ('index/', Index.indexView, name = 'index'),
    path('empresarial', Empre.enviar, name='empresarial'),
    path('solicitud/', soli.solicitud, name='solicitud'),
    path('pagoA/', pagoAutomatico.pagar, name='pagoA'),
    path('pagoAde/', pagoAdelantado.adelantar, name='pagoAde'),
    path('estadoC/', estadoCuenta.enviar, name='estadoC')

]
