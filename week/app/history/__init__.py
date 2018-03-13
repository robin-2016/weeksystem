#!/usr/bin/env python
# -*-coding:utf-8 -*-
from flask import Blueprint

history = Blueprint('history',__name__)

from . import views
