# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core import serializers
import edit.dynsh as dynsh
import json



def index(request):
  return render_to_response('index.html')


def list(request):
  response_data = dynsh.getSchema()
  return HttpResponse(json.dumps(response_data), content_type = "application/json")


def rows(request):
  res_path = str(request.path).split('/')
  res_name = res_path[3]

  if request.method == 'GET':
    try:
      # className = getattr(models, res_name)
      className = dynsh.getModel(res_name)
    except:
      className = None
    if className:
      data = className.objects.all()
      data = serializers.serialize("json", data)

  elif request.method == 'POST':
    if '.' in res_name:
      res_name = res_name.split('.')[1]
      row_id = res_path[4]
    else:
      row_id = None

    try:
      # className = getattr(models, res_name)
      className = dynsh.getModel(res_name)
    except:
      className = None

    data = eval(request.read())
    if className:
      if row_id:
        row = className.objects.get(pk = row_id)
      else:
        row = className.objects.create()
      if 'fields' in data:
        for key in data['fields']:
          setattr(row, key, data['fields'][key])
      row.save()
      data = {}
    else:
      data = {}

  return HttpResponse(data, content_type = "application/json")


def api(request):
  response_data = {}
  return HttpResponse(json.dumps(response_data), content_type = "application/json")




