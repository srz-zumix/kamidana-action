from kamidana import (
    as_filter,
    as_global,
)
from jinja2 import pass_context
from colour import Color
import os


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


@as_global
def status_success_color():
  return Color(os.getenv('KAMIDANA_STATUS_SUCCESS', '#1f883d'))


@as_global
def status_failure_color():
  return Color(os.getenv('KAMIDANA_STATUS_FAILURE', '#cf222e'))


@as_global
def status_other_color():
  return Color(os.getenv('KAMIDANA_STATUS_OTHER', '#6e7781'))


@as_filter
@pass_context
def outcome_color(ctx, v):
  lower_v = v.lower()
  if lower_v == 'success':
    return status_success_color()
  if lower_v == 'failure':
    return status_failure_color()
  return status_other_color()


@as_filter
@pass_context
def status_color(ctx, v):
  if is_success(ctx, v):
    return status_success_color()
  if is_failure(ctx, v):
    return status_failure_color()
  return status_other_color()


@as_filter
@pass_context
def discord_color(ctx, v):
  html_color = Color(v).hex_l
  hex_color = html_color.lstrip('#')
  return int(hex_color, 16)
