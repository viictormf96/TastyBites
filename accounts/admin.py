from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.apps import apps # <-- Importación necesaria
from .models import CustomUser 

# 1. Definimos la clase de administración personalizada
class CustomUserAdmin(UserAdmin):
    # Campos a mostrar en la lista del panel de administración
    list_display = UserAdmin.list_display + ('bio', 'profile_picture')

    # Campos a mostrar en el formulario de edición de usuario
    fieldsets = UserAdmin.fieldsets + (
        ('Información Personal Adicional', {
            'fields': ('bio', 'profile_picture'),
        }),
    )

    # Campos a mostrar en el formulario de creación de un nuevo usuario
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Personal Adicional', {
            'fields': ('bio', 'profile_picture'),
        }),
    )

# 2. Desregistrar el modelo User predeterminado
# Usamos apps.get_model() en lugar de admin.site.get_model()
try:
    admin.site.unregister(apps.get_model('auth', 'User')) 
except admin.sites.NotRegistered:
    # Esto maneja el caso donde 'auth.User' ya no estaba registrado,
    # lo cual puede ocurrir si AUTH_USER_MODEL ya apunta a tu CustomUser.
    pass

# 3. Registrar el modelo CustomUser con nuestra clase de administración personalizada
admin.site.register(CustomUser, CustomUserAdmin)