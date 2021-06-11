# ShitpostStorageSystem

Allows you to store shitposts and recall them later. Very simple.

No configuration. Just visit the webserver.

Docker environment variables:

* `SSS_PORT`: Configures the webserver port. Default is `8082`.
* `SSS_HOST`: Configures the webserver host. Default is `0.0.0.0`.
* `SSS_STORAGE`: Relative (or absolute) path of the file cache. Default is `downloads/`

## Routes

### GET `/shitposts`
Download a random shitpost from the archive. `Content-Type` header will signal what type the media is.

Possibilities include:

* `video/mp4`
* `image/gif`
* `image/png`

### POST `/shitposts`
Upload a shitpost to the archive.

Form data:
* `Media`: The shitpost. Must have either a content-type header or a file extension.

### GET `/list`
Return a list of all shitposts currently stored.
