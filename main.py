from random import randint, choice
import os
from json import load
from string import ascii_letters

from aiohttp import web, hdrs


routes: web.RouteTableDef = web.RouteTableDef()


CONTENT_TYPES: dict = load(open("resources/types.json"))


@routes.get("/list")
async def shitpost_list(request: web.Request):
    return web.json_response(os.listdir(request.app["download_dir"]))


@routes.post("/shitposts")
async def post(request: web.Request):
    if request.headers.get(hdrs.CONTENT_LENGTH) is None:
        raise web.HTTPBadRequest(reason="Missing Content-Length header.")
    elif int(request.headers.get(hdrs.CONTENT_LENGTH)) > 5000000:
        raise web.HTTPRequestEntityTooLarge(reason="I don't want my hard drive to explode. Size limit is 5 megabytes.")
    elif len(request.app["download_dir"]) >= 2000:
        raise web.HTTPInsufficientStorage(reason="2000 shitposts are present. You know the rules.")

    request_field = await request.multipart()

    shitpost = await request_field.next()
    assert shitpost.name == "shitpost"

    extension: str = os.path.splitext(shitpost.filename)[1].strip(".").lower()

    if CONTENT_TYPES.get(extension) is None:
        raise web.HTTPUnsupportedMediaType

    with open(
            f"{request.app['download_dir']}{''.join(choice(ascii_letters) for _ in range(15))}.{extension}", "wb"
    ) as writeable:
        while True:
            chunk: bytes = await shitpost.read_chunk()
            if not chunk:
                break
            writeable.write(chunk)

    raise web.HTTPCreated()


@routes.get("/shitposts")
async def get(request: web.Request):
    files: list = os.listdir(request.app["download_dir"])

    if len(files) == 0:
        raise web.HTTPInternalServerError(reason="No shitposts have been uploaded yet. Be the first!")

    random_index: int = randint(0, len(files) - 1)
    with open(f"{request.app['download_dir']}{files[random_index]}", "rb") as file:
        try:
            content_type: str = CONTENT_TYPES[os.path.splitext(file.name)[1].strip(".")]
        except KeyError:
            raise web.HTTPInternalServerError(reason="File selected was invalid.")

        stream_response = web.StreamResponse()
        stream_response.content_type = content_type
        await stream_response.prepare(request)
        await stream_response.write(file.read())
        await stream_response.write_eof()
        return stream_response


async def create_app():
    """Create an app and configure it."""

    # Create the app
    app = web.Application()

    # Configure the app
    app["download_dir"] = os.environ.get("SSS_STORAGE", "downloads/")

    if not os.path.exists(app["download_dir"]):
        os.mkdir(app["download_dir"])

    # Routes
    app.add_routes(routes)

    # Off we go!
    return app


if __name__ == "__main__":
    port = int(os.environ.get("SSS_PORT", "8082"))
    host = os.environ.get("SSS_HOST", "0.0.0.0")

    web.run_app(create_app(), host=host, port=port)
