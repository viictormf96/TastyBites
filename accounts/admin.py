from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """
    Administrador personalizado para CustomUser.
    """
    # Campos a mostrar en la lista
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    
    # Campos de búsqueda
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Filtros laterales
    list_filter = ('is_staff', 'is_superuser', 'is_active')

    # Vista de EDICIÓN de usuario
    fieldsets = (
        ('Credenciales', {
            'fields': ('username', 'password')
        }),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'email', 'bio', 'profile_picture')
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Fechas Importantes', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    # Vista de CREACIÓN de usuario
    add_fieldsets = (
        ('Credenciales', {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')
        }),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'email', 'bio', 'profile_picture')
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
    )

    # Campos de solo lectura
    readonly_fields = ('last_login', 'date_joined')


# Registrar el modelo
admin.site.register(CustomUser, CustomUserAdmin)