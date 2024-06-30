from django.apps import AppConfig


class AppointmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointments'



import redis

red = redis.Redis(
    host='redis-12591.c277.us-east-1-3.ec2.cloud.redislabs.com',
    port=12591,
    password='CuBwcZCYtioddwHkZn4XhlMDO4rg3rsE'
)
