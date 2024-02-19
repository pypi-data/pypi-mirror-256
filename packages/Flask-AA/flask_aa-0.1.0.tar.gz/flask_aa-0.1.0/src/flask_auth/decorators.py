import functools

from flask import flash, g, redirect, request, url_for


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            flash("Please log in to access this page", "warning")
            return redirect(
                url_for(
                    "auth.login",
                    next=request.path,
                    cancel=request.args.get("next", "/"),
                )
            )

        return view(*args, **kwargs)

    return wrapped_view
