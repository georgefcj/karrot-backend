from json import loads as load_json_string


class Parameter(object):
    def __init__(self, name, validator=None):
        self.name = name
        self.validator = validator or (lambda _: True)


class JsonRequest(object):
    def __init__(self, http_request, json_body):
        self._http_request = http_request
        self._json_body = json_body

    @classmethod
    def from_http_request(cls, http_request, parameters):
        """
        :type http_request: HttpRequest
        :type parameters: list
        :rtype: JsonRequest
        :raises ValueError: if the request body is not valid JSON or one of the expected keys is missing

        """
        try:
            json_data = load_json_string(http_request.body.decode("utf-8"))
        except ValueError:
            raise ValueError('incorrect json request')

        for paramter in parameters:
            paramter.validator(json_data)

        return cls(http_request, json_data)

    def __getattr__(self, item):
        if item == 'body':
            return self._json_body
        return getattr(self._http_request, item)