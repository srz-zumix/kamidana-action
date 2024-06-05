from kamidana import (
    as_filter,
)
from jinja2 import pass_context


success_texts = [
  "success",
  "succeeded",
  "pass",  
  "passed",
  "ok",
]

failure_texts = [
  "failure",
  "failed",
  "fail",
  "error",
  "errored",
  "ng",
]


@as_filter
@pass_context
def is_success(ctx, v):
  if isinstance(v, str):
    return v.lower() in success_texts
  if v:
    return True
  return False


@as_filter
@pass_context
def is_failure(ctx, v):
  if isinstance(v, str):
    return v.lower() in failure_texts
  if v:
    return True
  return False
