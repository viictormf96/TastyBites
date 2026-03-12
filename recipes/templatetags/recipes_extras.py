from django import template
from django.utils.safestring import mark_safe
from django.utils import timezone
from datetime import datetime
from django.utils.translation import gettext as _
from typing import Union, Optional

register = template.Library()

@register.filter(name='smart_time')
def smart_time(value):
    """
    Calcula el tiempo relativo de forma profesional.
    - Soporta objetos 'aware' y 'naive'.
    - Utiliza internacionalización (i18n).
    - Basado en una arquitectura de umbrales para mayor legibilidad.
    """
    if not value or not isinstance(value, (datetime,)):
        return value

    try:
        now = timezone.now() if timezone.is_aware(value) else datetime.now()
        
        # Si la fecha es futura (margen de error por sincronización de servidor)
        if value > now:
            return _("ahora mismo")

        delta = now - value
        seconds = int(delta.total_seconds())

        # Estructura de umbrales: (Límite en segundos, Divisor, Singular, Plural)
        thresholds = [
            (60, 1, _("hace un momento"), None),
            (3600, 60, _("hace %(n)d minuto"), _("hace %(n)d minutos")),
            (86400, 3600, _("hace %(n)d hora"), _("hace %(n)d horas")),
            (604800, 86400, _("hace %(n)d día"), _("hace %(n)d días")),
            (2592000, 604800, _("hace %(n)d semana"), _("hace %(n)d semanas")),
            (31536000, 2592000, _("hace %(n)d mes"), _("hace %(n)d meses")),
            (float('inf'), 31536000, _("hace %(n)d año"), _("hace %(n)d años")),
        ]

        for limit, divisor, singular, plural in thresholds:
            if seconds < limit:
                count = seconds // divisor
                if count <= 1 or not plural:
                    return singular
                return plural % {'n': count}

    except Exception:
        return value
    
    return value

@register.filter
def highlight_last_word(value):
    words = value.split()
    if len(words) > 1:
        # Guardamos todas menos la última
        first_part = " ".join(words[:-1])
        # La última palabra
        last_word = words[-1]
        # Retornamos el HTML con la clase para el color naranja
        return mark_safe(f'{first_part} </br><span class="text-primary italic">{last_word}</span>')
    
    return value

@register.filter(name='format_k') # Forzamos el nombre por seguridad
def format_k(value):
    try:
        num = float(value)
        if num < 1000:
            return str(int(num))
        
        if num < 1000000:
            # Si es exacto (ej. 2000), devuelve 2k
            if num % 1000 == 0:
                return f"{int(num/1000)}k"
            # Si tiene decimales (ej. 1500), devuelve 1.5k
            return f"{num/1000:.1f}k".replace('.0', '')
            
        return f"{num/1000000:.1f}M".replace('.0', '')
    except (ValueError, TypeError):
        return value

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """
    Este tag permite actualizar o eliminar parámetros de la URL actual 
    manteniendo el resto de los filtros activos.
    
    Uso en HTML: <a href="?{% url_replace parametro='valor' %}">
    """
    # 1. Obtenemos el objeto request del contexto de la plantilla
    request = context.get('request')
    if not request:
        return ""
    
    # 2. Creamos una copia mutable de los parámetros GET actuales (QueryDict)
    # Es necesario usar .copy() porque los QueryDict de request son inmutables
    query_params = request.GET.copy()
    
    # 3. Iteramos sobre los argumentos pasados al tag (kwargs)
    for key, value in kwargs.items():
        if value is None or value == "":
            # Si el valor es una cadena vacía o None, eliminamos el parámetro
            # Esto es útil para botones de "Limpiar filtro"
            query_params.pop(key, None)
        else:
            # Si hay un valor, lo actualizamos o lo creamos
            query_params[key] = value
            
    # 4. Retornamos los parámetros codificados para URL (ej: 'q=busqueda&page=2')
    return query_params.urlencode()