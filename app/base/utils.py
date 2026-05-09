import datetime
from django.conf import settings


def set_cookie(response, key, value, days_expire=365):
    """Crea una cookie.
    Arguments:
        response -- La respuesta HTTP a la que se asigna la cookie
        key -- Nombre de la cookie
        value -- Datos de la cookie
        days_expire -- Días de persistencia de la cookie (por defecto 365)
    """
    max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(
        datetime.datetime.now() + datetime.timedelta(seconds=max_age),
        "%a, %d-%b-%Y %H:%M:%S GMT",
    )
    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires,
        secure=settings.SESSION_COOKIE_SECURE or None,
    )

    return response
