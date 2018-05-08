"""lti_launch views."""

import logging
import os


from flask import Blueprint
from flask import current_app
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required

from hxlti import __version__ as hxlti_version


blueprint = Blueprint(
    'lti_launch', __name__, url_prefix='/lti_launch', static_folder='../static')


@blueprint.route('/', methods=['GET', 'POST'])
def launch_lti():
    if method == 'GET':
        # not lti request, redirect to landing page


    # it's a post, assuming lti-launch request
    else:
        if current_user.is_authenticated:
            # display landing page
        else:
            # login process for lti user


