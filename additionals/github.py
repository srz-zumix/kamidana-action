from kamidana import (
    as_filter,
)
from jinja2 import pass_context

from github import Github
from github import Auth

import os

token =os.getenv('GITHUB_TOKEN', os.getenv('INPUTS_GITHUB_TOKEN'. ''))
auth = Auth.Token(token) if token else None
g = Github(base_url=os.getenv('GITHUB_API_URL', 'https://api.github.com'), auth=auth)


@as_filter
@pass_context
def github_user(ctx, v):
    return g.get_user(v)


@as_filter
@pass_context
def github_user_email(ctx, v):
    user = g.get_user(v)
    return user.email
