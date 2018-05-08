from flask import Blueprint

bp = Blueprint("main", __name__)

from megatutApp.main import views