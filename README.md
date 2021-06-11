# ShitpostStorageSystem

Allows you to store shitposts and recall them later. Very simple.

No configuration. Just visit the webserver.

Docker environment variables:

* `SSS_PORT`: Configures the webserver port. Default is `8082`.
* `SSS_HOST`: Configures the webserver host. Default is `0.0.0.0`.
* `SSS_STORAGE`: Relative (or absolute) path of the file cache. Default is `downloads/`
