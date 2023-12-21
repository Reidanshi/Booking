from django.db import models

class HotelManager(models.Manager):
    def get_for_admin(self, admin):
        return self.get(admin=admin)