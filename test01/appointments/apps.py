from django.apps import AppConfig


class AppointmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointments'

    def ready(self):
        import appointments.signals

        # from .tasks import send_mails
        # from .scheduler import appointment_scheduler
        # print('запущено')
        #
        # appointment_scheduler.add_job(
        #     id='send mails',
        #     func=lambda: print('123'),
        #     trigger='interval',
        #     seconds=10,
        #
        # )
        # appointment_scheduler.start()



