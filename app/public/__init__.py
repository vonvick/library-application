# app/public/__init__.py

from flask import Blueprint

public = Blueprint(

  'public',
  __name__,
  template_folder = 'templates',
  static_folder   = 'static'
)

from . import views
