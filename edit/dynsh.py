# -*- coding: utf-8 -*-

from django.db import models
import json
from django.conf import settings
import yaml
from yaml import Loader, SafeLoader


def getSchema():
  def construct_yaml_str(self, node):
      return self.construct_scalar(node)

  Loader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)
  SafeLoader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)


  SCHEMA_DIR = getattr(settings, "STATIC_ROOT", None)
  SCHEMA_FILE = SCHEMA_DIR + 'schema.yaml'

  stream = open(SCHEMA_FILE, 'r')
  schema = yaml.load(stream)
  return schema


def getModel(name):
  schema = getSchema()
  if name not in schema:
    return None

  class Base(models.Model):
    pass

  flist = {'__module__': 'edit.dynsh'}
  for fdata in schema[name]['fields']:
    field = fdata
    # print(field)
    if field['type'] == 'char':
      finfo = models.CharField(field['title'], max_length = 50)
    elif field['type'] == 'int':
      finfo = models.IntegerField(field['title'], default = 0)
    elif field['type'] == 'date':
      finfo = models.DateField(field['title'], default = '2014-01-01')

    if finfo:
      flist[str(field['id'])] = finfo
  print(flist)
  return type(str(name), (models.Model,), flist)
