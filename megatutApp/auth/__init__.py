from flask import Blueprint

bp = Blueprint("auth", __name__)

from megatutApp.auth import views