from kamidana import (
    as_filter,
)
from jinja2 import pass_context
import os
import io


# no univeral newlines
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, newline='')


@as_filter
@pass_context
def relativepath(ctx, v):
  dirname = os.path.dirname(os.path.abspath(ctx.name))
  return os.path.normpath(os.path.join(dirname, v))


@as_filter
@pass_context
def abspath(ctx, v):
  return os.path.abspath(str(v))


@as_filter
@pass_context
def basename(ctx, v):
  return os.path.basename(str(v))


@as_filter
@pass_context
def dirname(ctx, v):
  return os.path.dirname(str(v))


@as_filter
@pass_context
def path_exists(ctx, v):
  return os.path.exists(str(v))


@as_filter
@pass_context
def listdir(ctx, v):
  return os.listdir(str(v))


@as_filter
@pass_context
def listdir_files(ctx, v):
  return [f for f in os.listdir(str(v)) if os.path.isfile(os.path.join(str(v), f))]


@as_filter
@pass_context
def listdir_dirs(ctx, v):
  return [f for f in os.listdir(str(v)) if os.path.isdir(os.path.join(str(v), f))]
