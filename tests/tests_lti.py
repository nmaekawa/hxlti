"""testing lti."""

from flask import current_app
from flask import url_for
import time
import pytest

from lti import ToolConsumer

from hxlti.consumer.models import Consumer
from hxlti.user.models import User

from .factories import ConsumerFactory
from .factories import UserFactory


@pytest.mark.usefixtures('db')
class TestLtiLaunch:
    """lti launch: auth and login."""

    def test_can_login(self, app, db):
        app.config['SERVER_NAME'] = 'localhost:5000'
        app.config['SERVER_PORT'] = 5000
        app.config['PREFERRED_URL_SCHEME'] = 'http'

        consumer = ConsumerFactory()
        consumer.save()
        params = {
            'lti_message_type': 'basic-lti-launch-request',
            'lti_version': 'LTI-1p0',
            'resource_link_id' : 'same.site.org-9fcae62972a240e488ca1de83dc4a6d9',
        }
        tool_consumer = ToolConsumer(
            consumer_key=consumer.client_key,
            consumer_secret=consumer.secret_key,
            launch_url=url_for('lti_launch.lti_launch', _external=True),
            params=params
        )

        lti_params = tool_consumer.generate_launch_data()

        res = app.post(url_for('lti_launch.lti_launch'), lti_params)

        assert res.status_code == 200



