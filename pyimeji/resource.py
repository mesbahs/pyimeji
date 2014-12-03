import json

from dateutil.parser import parse


class Resource(object):
    """
        "createdBy": {
            "fullname": "Saquet",
            "id": "zhcQKsMR0A9SiC6x"
        },
        "modifiedBy": {
            "fullname": "admin",
            "id": "w7ZfmmC5LQR8KJIN"
        },
        "createdDate": "2014-10-09T13:01:25 +0200",
        "modifiedDate": "2014-11-19T14:50:21 +0100",
    """
    __readonly__ = ['id', 'createdBy', 'modifiedBy', 'createdDate', 'modifiedDate']
    __subresources__ = []

    def __init__(self, d, api):
        self._api = api
        self._json = d

    def _path(self):
        id_ = ''
        if self._json.get('id'):
            id_ = '/' + self.id
        return '/%ss%s' % (self.__class__.__name__.lower(), id_)

    def __getattr__(self, attr):
        """Attribute lookup.

        Attributes provide easy access to the following things:

        - subresources,
        - top-level keys in the resource's JSON representation.
        """
        if attr in self.__subresources__:
            # we fetch subresources using an API call when the corresponding attribute
            # is accessed - every time.
            json = True if not isinstance(self.__subresources__, dict) \
                else self.__subresources__[attr]
            return self._api._req(self._path() + '/' + attr, json=json)
        try:
            res = self._json[attr]
        except KeyError:
            raise AttributeError(attr)

        if attr.endswith('Date'):
            res = parse(res)

        #
        # TODO: once this is available, resolve users to proper objects upon access!
        #

        return res

    def __setattr__(self, attr, value):
        if attr.startswith('_'):
            return object.__setattr__(self, attr, value)
        if attr in self.__readonly__:
            raise AttributeError('%s is readonly' % attr)
        self._json[attr] = value

    def dumps(self, **kw):
        return json.dumps(self._json, **kw)

    def __repr__(self):
        return self.dumps(sort_keys=True, indent=4, separators=(',', ': '))

    def save(self):
        method = 'put' if self._json.get('id') else 'post'
        return self._api._req(
            self._path(),
            method=method,
            data=self.dumps(),
            headers={'content-type': 'application/json'})


class Collection(Resource):
    __subresources__ = ['mdprofiles']


class Item(Resource):
    __subresources__ = {'content': False}

    def save(self):
        if self._json.get('id'):
            raise NotImplemented()  # pragme: no cover
            #return Resource.save(self)
        return self._api._req(
            self._path(),
            method='post',
            json=False,
            files=dict(file='', json=self.dumps()))
