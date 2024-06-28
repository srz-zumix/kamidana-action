from kamidana import (
    as_filter,
)
from jinja2 import pass_context
import jmespath
import json


@as_filter
@pass_context
def json_query(ctx, v, query):
  return jmespath.search(query, v)


@as_filter
@pass_context
def json_dumps(ctx, v):
  return json.dumps(v)


@as_filter
@pass_context
def json_loads(ctx, v):
  return json.loads(v)
