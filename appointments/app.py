from django.apps import AppConfig


class AppointmentConfig(AppConfig):
    name = 'appointments'

    # нам надо переопределить метод ready, чтобы при готовности нашего приложения импортировался модуль со
    # всеми функциями обработчиками
    def ready(self):
        import appointment.signals


import redis

red = redis.Redis(
    host='redis-12591.c277.us-east-1-3.ec2.cloud.redislabs.com',
    port=12591,
    password='CuBwcZCYtioddwHkZn4XhlMDO4rg3rsE'
)