import ruamel.yaml
from collections import OrderedDict

from kamidana import (
    as_filter,
)


def represent_odict(dumper, instance):
    return dumper.represent_mapping('tag:yaml.org,2002:map', instance.items())

ruamel.yaml.add_representer(OrderedDict, represent_odict)


def construct_odict(loader, node):
    return OrderedDict(loader.construct_pairs(node))

ruamel.yaml.add_constructor('tag:yaml.org,2002:map', construct_odict)


@as_filter
def to_yaml(ctx, a, *args, **kw):
    yaml = ruamel.yaml.YAML(typ=['rt', 'string'])
    yaml.default_flow_style = kw.pop('default_flow_style', None)
    yaml.allow_unicode=True
    yaml.indent=kw.pop('indent', 2)
    transformed = yaml.dump_to_string(a)
    return transformed


@as_filter
@contextfilter
def to_nice_yaml(ctx, a, indent=2, *args, **kw):
    yaml = ruamel.yaml.YAML(typ=['rt', 'string'])
    yaml.default_flow_style=False
    yaml.allow_unicode=True
    yaml.indent=indent
    transformed = yaml.dump_to_string(a)
    return transformed
