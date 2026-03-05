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