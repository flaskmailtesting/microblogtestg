from flask import Blueprint

bp = Blueprint("errors", __name__)

from megatutApp.error import handlers