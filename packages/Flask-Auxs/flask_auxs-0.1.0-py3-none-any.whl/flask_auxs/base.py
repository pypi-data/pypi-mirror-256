from zoneinfo import ZoneInfo

from flask import request


class Auxs:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        @app.context_processor
        def inject_redir_path():
            query_string = request.query_string.decode()
            redir_path = (
                request.path if not query_string else request.path + "?" + query_string
            )

            return dict(redir_path=redir_path)

        @app.template_filter()
        def dtformat(dt):
            utc_dt = dt.replace(tzinfo=ZoneInfo("UTC"))
            local_dt = utc_dt.astimezone(ZoneInfo(app.config.get("TIME_ZONE")))

            format = "%d %b %Y, %H:%M"

            return local_dt.strftime(format)
