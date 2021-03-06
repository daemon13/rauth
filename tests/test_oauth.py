'''
    rauth.test_oauth
    ------------------

    Test suite for rauth.oauth.
'''

from base import RauthTestCase
from rauth.oauth import (HmacSha1Signature, RsaSha1Signature,
        PlaintextSignature)

from urllib import urlencode


class OAuthTestHmacSha1Case(RauthTestCase):
    def test_hamcsha1_signature(self):
        self.request.params = {'foo': 'bar'}
        HmacSha1Signature().sign(self.request, self.consumer, self.token)
        oauth_signature = self.request.params_and_data['oauth_signature']
        self.assertTrue(oauth_signature is not None)
        self.assertTrue(isinstance(oauth_signature, str))

    def test_normalize_request_parameters_params(self):
        # params as a dict
        self.request.params = {'foo': 'bar'}
        normalized = \
                HmacSha1Signature()._normalize_request_parameters(self.request)
        self.assertEqual('foo=bar',  normalized)

        # params as a dict with URL encodable chars
        self.request.params_and_data = {}
        self.request.params = {'foo+bar': 'baz'}
        normalized = \
                HmacSha1Signature()._normalize_request_parameters(self.request)
        self.assertEqual('foo%2Bbar=baz',  normalized)
        self.assertTrue('+' not in normalized)

        # params as a string
        self.request.params_and_data = {}
        self.request.params = urlencode({'foo': 'bar'})
        normalized = \
                HmacSha1Signature()._normalize_request_parameters(self.request)
        self.assertEqual('foo=bar',  normalized)

        # params as a string with URL encodable chars
        self.request.params_and_data = {}
        self.request.params = urlencode({'foo+bar': 'baz'})
        normalized = \
                HmacSha1Signature()._normalize_request_parameters(self.request)
        self.assertEqual('foo%2Bbar=baz',  normalized)
        self.assertTrue('+' not in normalized)

        # params and dict as dicts
        self.request.params_and_data = {}
        self.request.params = {'a': 'b'}
        self.request.data = {'foo': 'bar'}
        normalized = \
                HmacSha1Signature()._normalize_request_parameters(self.request)
        self.assertEqual('a=b&foo=bar',  normalized)

    def test_normalize_request_parameters_data(self):
        # data as a dict
        self.request.data = {'foo': 'bar'}
        normalized = \
                HmacSha1Signature()._normalize_request_parameters(self.request)
        self.assertEqual('foo=bar',  normalized)

        # data as a dict with URL encodable chars
        self.request.params_and_data = {}
        self.request.data = {'foo+bar': 'baz'}
        normalized = \
                HmacSha1Signature()._normalize_request_parameters(self.request)
        self.assertEqual('foo%2Bbar=baz',  normalized)
        self.assertTrue('+' not in normalized)

        # data as a string with URL encodable chars
        self.request.data = urlencode({'foo+bar': 'baz'})
        normalized = \
                HmacSha1Signature()._normalize_request_parameters(self.request)
        self.assertEqual('foo%2Bbar=baz',  normalized)
        self.assertTrue('+' not in normalized)

    def test_normalize_request_parameters_both_string(self):
        # params and data both as a string
        self.request.params = urlencode({'a': 'b'})
        self.request.data = urlencode({'foo': 'bar'})
        normalized = \
                HmacSha1Signature()._normalize_request_parameters(self.request)
        # this also demonstrates sorting
        self.assertEqual('a=b&foo=bar',  normalized)

    def test_normalize_request_parameters_params_string(self):
        # params is a string but data is a dict
        self.request.params = urlencode({'a': 'b'})
        self.request.data = {'foo': 'bar'}
        normalized = \
                HmacSha1Signature()._normalize_request_parameters(self.request)
        self.assertEqual('a=b&foo=bar',  normalized)

    def test_normalize_request_parameters_data_string(self):
        # params is a dict but data is a string
        self.request.params = {'a': 'b'}
        self.request.data = urlencode({'foo': 'bar'})
        normalized = \
                HmacSha1Signature()._normalize_request_parameters(self.request)
        self.assertEqual('a=b&foo=bar',  normalized)

    def test_utf8_encoded_string(self):
        # in the event a string is already UTF-8
        self.request.params = {u'foo': u'bar'}
        self.request.url = u'http://example.com/'
        HmacSha1Signature().sign(self.request, self.consumer)
        self.assertEqual({'foo': 'bar'},  self.request.params)

    def test_remove_query_string(self):
        # can't sign the URL with the query string so
        url = 'http://example.com/?foo=bar'
        signable_url = HmacSha1Signature()._remove_qs(url)
        self.assertEqual('http://example.com/', signable_url)


class OAuthTestRsaSha1Case(RauthTestCase):
    def test_rsasha1_notimplemented(self):
        self.assertRaises(NotImplementedError, RsaSha1Signature)


class OAuthTestPlaintextCase(RauthTestCase):
    def test_plaintext_notimplemented(self):
        self.assertRaises(NotImplementedError, PlaintextSignature)
