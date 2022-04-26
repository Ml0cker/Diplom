from django.contrib import admin

from .models import Executors, Customers, Contracts, Employees, Works, Estimates, Bills, Acts

admin.site.register(Executors)
admin.site.register(Customers)
admin.site.register(Contracts)
admin.site.register(Employees)
admin.site.register(Works)
admin.site.register(Estimates)
admin.site.register(Bills)
admin.site.register(Acts)


