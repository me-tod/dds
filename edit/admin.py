# -*- coding: utf-8 -8-
from django.contrib import admin
import edit.dynsh as dynsh

'''
from edit.models import users
from edit.models import rooms

admin.site.register(users)
admin.site.register(rooms)

'''

sh = dynsh.getSchema()
for name in sh:
  admin.site.register(dynsh.getModel(name))



