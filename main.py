from os import environ

from aiohttp import web


routes = web.RouteTableDef()


@routes.post("/shitposts")
async def post(request: web.Request):
    pass


@routes.get("/shitposts")
async def get(request: web.Request):
    pass


async def create_app():
    """Create an app and configure it."""

    # Create the app
    app = web.Application()

    # Routes
    app.add_routes(routes)

    # Off we go!
    return app


if __name__ == "__main__":
    port = int(environ.setdefault("SSS_PORT", "8082"))
    host = environ.setdefault("SSS_HOST", "0.0.0.0")

    web.run_app(create_app(), host=host, port=port)
