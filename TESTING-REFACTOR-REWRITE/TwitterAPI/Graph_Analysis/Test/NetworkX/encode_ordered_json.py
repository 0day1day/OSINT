

import simplejson
from collections import OrderedDict


class OrderedJsonEncoder( simplejson.JSONEncoder ):
    """Encode ordered dict objects into JSON for write to mongodb"""
    def encode(self, o):
        if isinstance(o, OrderedDict):
            return "{" + ", ".join([self.encode(k) + ": " + self.encode(v) for (k,v) in o.iteritems()]) + "}"
        else:
            return simplejson.JSONEncoder.encode(self, o)


def encode_json(ordered_dict):
    e = OrderedJsonEncoder()
    return e.encode(ordered_dict)

ordered = OrderedDict([("id",123), ("name","a_name"), ("timezone","tz")])
print encode_json(ordered)