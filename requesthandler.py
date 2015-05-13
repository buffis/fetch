import requests

class RequestHandler(object):
    def get(self, url, params={}, headers={}, cookies={}): pass
    def post(self, url, params={}, headers={}, cookies={}): pass

class HttpRequestHandler(RequestHandler):
    def get(self, url, params={}, headers={}, cookies={}):
        self._timeout_seconds = 5 # Maybe allow setting this?
        return self._do_request(requests.get, url, params=params, headers=headers, cookies=cookies)

    def post(self, url, params={}, headers={}, cookies={}):
        return self._do_request(requests.post, url, params=params, headers=headers, cookies=cookies)

    def _do_request(self, method, url, params={}, headers={}, cookies={}):
        try:
            req = method(url, params=params, headers=headers, cookies=cookies, timeout=self._timeout_seconds)
        except Exception:
            raise RequestException("Error when fetching from url: %s" % url)
        if req.status_code != 200:
            raise RequestException("Status code: %d for %s" % (req.status_code, url))
        try:
            return req.text
        except AttributeError:  # Older version of requests library use content instead of text
            return req.content

class TestRequestHandler(RequestHandler):
    def __init__(self, return_data):
        self.requests_sent = []
        self.return_data = return_data

    def get(self, url, params={}, headers={}, cookies={}):
        self.requests_sent.append({"url":url, "params":params,
                                   "headers":headers, "cookies":cookies, "method":"get"})
        return self.return_data

    def post(self, url, params={}, headers={}, cookies={}):
        self.requests_sent.append({"url":url, "params":params,
                                   "headers":headers, "cookies":cookies, "method":"post"})
        return self.return_data

class RequestException(Exception):
    def __init__(self, msg):
        self.msg = msg