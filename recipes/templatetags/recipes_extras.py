from django import template

register = template.Library()

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