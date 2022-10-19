from django.urls import path
from django.contrib import admin
from . import views
from myapp import views as myapp_views

urlpatterns = [
  path('', views.index, name='index'),
  path('add/', views.add, name='add'),
  path('add/addrecord/', views.addrecord, name='addrecord'),
  path('delete/<int:id>', views.delete, name='delete'),
  path('update/<int:id>', views.update, name='update'),
  path('update/updaterecord/<int:id>', views.updaterecord, name='updaterecord'),
  path('admin/', admin.site.urls),
  path('newtemplate/', views.vue_test),
]