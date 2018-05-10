"""lti_launch views."""

import logging
import os

from oauthlib.oauth1 import SignatureOnlyEndpoint
from lti.contrib.flask import FlaskToolProvider


from flask import Blueprint
from flask import current_app
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user

from hxlti import __version__ as hxlti_version
from hxlti.lti_launch.validators import LTIRequestValidator

dummy_pwd = 'dummy'

logger = logging.getLogger(__name__)
blueprint = Blueprint(
    'lti_launch', __name__, url_prefix='/lti_launch', static_folder='../static')


@blueprint.route('/', methods=['POST'])
def lti_launch():
    if current_user.is_authenticated:
        # redirect to landing page
        return redirect(url_for('lti_launch.landing_page'))
    else:
        # login process for lti user
        tool_provider = FlaskToolProvider.from_flask_request(
            request=request)

        valid = tool_provider.is_valid_request(LTIRequestValidator)



        if valid:
            # login user, lti request authenticated
            username = tool_provider.launch_params.get('lis_person_sourceid', None)
            user_email = tool_provider.launch_params.get(
                'lis_person_contact_email_primary', None)

            logger.debug('FROM LTI POST USERNAME:EMAIL is {}:{}'.format(
                username, user_email))

            if username is None:
                # lti is missing info!
                return render_template(
                    '400.html',
                    message='Missing required param "lis_person_sourceid"',
                ), 400

            # pull user from db
            user = User.query.filter(User.username == username)
            if user is None:

                logger.debug("HAVE TO CREATE A USER")

                # create user in local db
                user = User(username=username, email=user_email)
                # TODO: what needs to be saved? roles?
                user.save()

                logger.debug("CREATEd A USER")

            login_user(user)

            # redirect to landing page
            return redirect(url_for('lti_launch.landing_page'))
        else:
            # return 401
            return render_template('401.html'), 401


@blueprint.route('/index.html', methods=['GET'])
@login_required
def landing_page():
    return render_template('lti_launch/landing_page.html')

