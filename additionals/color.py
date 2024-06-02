from kamidana import (
    as_filter,
    as_global,
)
from jinja2 import pass_context

@as_global
def status_success_color():
  return os.getenv('KAMIDANA_STATUS_SUCCESS', '#1f883d')


@as_global
def status_failure_color():
  return os.getenv('KAMIDANA_STATUS_FAILURE', '#cf222e')


@as_global
def status_other_color():
  return os.getenv('KAMIDANA_STATUS_OTHER', '#6e7781')


@as_filter
@pass_context
def outcome_color(ctx, v):
  lower_v = v.lower()
  if lower_v == 'success':
    return status_success_color()
  if lower_v == 'failure':
    return status_failure_color()
  return status_other_color()


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
def status_color(ctx, v):
  lower_v = v.lower()
  if lower_v in success_texts:
    return status_success_color()
  if lower_v in failure_texts:
    return status_failure_color()
  return status_other_color()
