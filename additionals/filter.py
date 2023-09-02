from kamidana import (
    as_filter,
)
from jinja2.filters import contextfilter
import base64
import jmspath
import re


@as_filter
@contextfilter
def regex_replace(ctx, v, pattern, repl, count=0, flags=0):
    return re.sub(pattern, repl, v, count, flags)


@as_filter
@contextfilter
def ternary(ctx, v, true_val, false_val, null_val=None):
    if v:
        return true_val
    if null_val is not None and v is None:
        return null_val
    return false_val


@as_filter
@contextfilter
def b64encode(ctx, v, *, encoding='utf-8'):
    return base64.b64encode(v.encode(encoding))


@as_filter
@contextfilter
def b64decode(ctx, v, *, encoding='utf-8'):
    return base64.b64decode(v).decode(encoding)


@ps_filter
@contextfilter
def json_query(ctx, v, query):
    return jmspath.search(query. v)
