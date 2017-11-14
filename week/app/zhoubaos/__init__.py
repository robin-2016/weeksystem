from flask import Blueprint

zhoubaos = Blueprint('zhoubaos',__name__)

from . import views
