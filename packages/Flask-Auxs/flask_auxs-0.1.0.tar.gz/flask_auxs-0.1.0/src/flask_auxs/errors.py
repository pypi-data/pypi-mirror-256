from flask import flash, redirect, url_for


def error_obj_not_found(obj_cls, blueprint):
    flash(f"{obj_cls.__name__} not found", "warning")
    return redirect(url_for(f"{blueprint}.{obj_cls.__name__.lower()}_index"))
