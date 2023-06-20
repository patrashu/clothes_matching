from __future__ import absolute_import

from components.human_parse.networks import AugmentCE2P

__factory = {
    'resnet101': AugmentCE2P.resnet101,
}


def init_model(name, *args, **kwargs):
    if name not in __factory.keys():
        raise KeyError("Unknown model arch: {}".format(name))
    return __factory[name](*args, **kwargs)