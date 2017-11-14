from flask import Blueprint

muser = Blueprint('muser',__name__)

from . import views
