from api.models import *


def get_available_driver():
    drivers = Motorista.objects.all()

    # FIXME really bad idea, but could not manage to use filter(is_busy=False)
    for driver in drivers:
        if not driver.is_busy:
            return driver

    return drivers
