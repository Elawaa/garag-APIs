# -*- coding: utf-8 -*-
"""
    flask_jwt
    ~~~~~~~~~

    Flask-JWT module
"""

import logging
import warnings

from collections import OrderedDict
from datetime import datetime, timedelta
from functools import wraps

import jwt

from flask import current_app, request, jsonify, _request_ctx_stack
from werkzeug.local import LocalProxy

__version__ = '0.3.2'

logger = logging.getLogger(__name__)

current_identity = LocalProxy(lambda: getattr(_request_ctx_stack.top, 'current_identity', None))

_jwt = LocalProxy(lambda: current_app.extensions['jwt'])

CONFIG_DEFAULTS = {
    'JWT_DEFAULT_REALM': 'Login Required',
    'JWT_AUTH_URL_RULE': '/auth',
    'JWT_AUTH_ENDPOINT': 'jwt',
    'JWT_AUTH_USERNAME_KEY': 'username',
    'JWT_AUTH_PASSWORD_KEY': 'password',
    'JWT_ALGORITHM': 'HS256',
    'JWT_LEEWAY': timedelta(seconds=10),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_EXPIRATION_DELTA': timedelta(seconds=300),
    'JWT_NOT_BEFORE_DELTA': timedelta(seconds=0),
    'JWT_VERIFY_CLAIMS': ['signature', 'exp', 'nbf', 'iat'],
    'JWT_REQUIRED_CLAIMS': ['exp', 'iat', 'nbf']
}


def _default_jwt_headers_handler(identity):
    return None


def _default_jwt_payload_handler(identity):
    iat = datetime.utcnow()
    exp = iat + current_app.config.get('JWT_EXPIRATION_DELTA')
    nbf = iat + current_app.config.get('JWT_NOT_BEFORE_DELTA')


    identity = getattr(identity, 'id', None) or identity['id']
    return {'exp': exp, 'iat': iat, 'nbf': nbf, 'identity': identity}