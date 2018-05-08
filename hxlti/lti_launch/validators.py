"""oauth validators for lti."""

import logging
from oauthlib.oauth1 import RequestValidator
from oauthlib.common import to_unicode

from hxlti.extensions import cache
from hxlti.consumer.models import Consumer

log = logging.getLogger(__name__)

NONCE_TTL = 3600 * 6

class LTIRequestValidator(RequestValidator):

    enforce_ssl = False

    dummy_secret = u'secret'
    dummy_client = (
        u'dummy_'
        '42237E2AB9614C4EAB0C089A96B40686B1C97DE114EC40659E64F1CE3C195AAC')


    def check_client_key(self, key):
        # any non-empty string is OK as a client key
        return len(key) > 0

    def check_nonce(self, nonce):
        # any non-empty string is OK as a nonce
        return len(nonce) > 0

    def validate_client_key(self, client_key, request):
        c = Consumer.query.filter(Consumer.client_key == client_key)
        return True if c else False

    def validate_timestamp_and_nonce(
        self, client_key, timestamp, nonce,
        request, request_token=None, access_token=None):

        exists = cache.get('nonce:' + nonce)
        if exists:
            log.debug("nonce already exists: %s", nonce)
            return False
        else:
            log.debug("unused nonce, storing: %s", nonce)
            cache.set('nonce:' + nonce, timestamp, timeout=NONCE_TTL)
            return True

    def get_client_secret(self, client_key, request):
        secret = Consumer.query(Consumer.secrek_key).filter(
            Consumer.client_key == client_key)

        if secret:
            # make sure secret val is unicode
            return to_unicode(secret)
        else:
            return self.dummy_secret

