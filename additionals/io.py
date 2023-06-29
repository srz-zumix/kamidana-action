from kamidana import (
    as_filter,
)
from jinja2.filters import contextfilter
import os


@as_filter
@contextfilter
def basename(ctx, v):
    return os.path.basename(str(v))

@as_filter
@contextfilter
def dirname(ctx, v):
    return os.path.dirname(str(v))
