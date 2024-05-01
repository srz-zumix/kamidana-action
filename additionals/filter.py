from kamidana import (
    as_filter,
)
from jinja2 import pass_context
import base64
import jmespath
import re


@as_filter
@pass_context
def regex_replace(ctx, v, pattern, repl, count=0, flags=0):
  return re.sub(pattern, repl, v, count, flags)


@as_filter
@pass_context
def ternary(ctx, v, true_val, false_val, null_val=None):
  if v:
    return true_val
  if null_val is not None and v is None:
    return null_val
  return false_val


@as_filter
@pass_context
def b64encode(ctx, v, *, encoding='utf-8'):
  return base64.b64encode(v.encode(encoding))


@as_filter
@pass_context
def b64decode(ctx, v, *, encoding='utf-8'):
  return base64.b64decode(v).decode(encoding)


@as_filter
@pass_context
def json_query(ctx, v, query):
  return jmespath.search(query, v)


@as_filter
@pass_context
def typeof(ctx, v):
  return type(v)
