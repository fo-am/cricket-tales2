from django.contrib import admin
from crickets.models import *

# Register your models here.
admin.site.register(Player)
admin.site.register(Cricket)
admin.site.register(Movie)

class EventAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('movie', 'timestamp')
        return self.readonly_fields

admin.site.register(Event, EventAdmin)
