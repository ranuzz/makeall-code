import functools
import time

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flask import jsonify
from flask import current_app as app

bp = Blueprint('data', __name__, url_prefix='/data')

@bp.route('/', methods=(['GET']))
def home():
    return render_template('data/index.html')
