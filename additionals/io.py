from kamidana import (
    as_filter,
)
from jinja2 import pass_context
import os


@as_filter
@pass_context
def basename(ctx, v):
    return os.path.basename(str(v))

@as_filter
@pass_context
def dirname(ctx, v):
    return os.path.dirname(str(v))
