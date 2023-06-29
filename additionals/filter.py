from kamidana import (
    as_filter,
)
from jinja2.filters import contextfilter
import base64


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
    return base64.encode(v.encode(encoding))


@as_filter
@contextfilter
def b64decode(ctx, v, *, encoding='utf-8'):
    return base64.decode(v.encode(encoding))
