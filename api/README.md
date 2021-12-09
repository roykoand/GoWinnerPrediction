# Go Winner Prediction API

Specify URL to your png image in the format (for example, use ```curl```):
```
$ curl -X GET http://127.0.0.1:5000/?url=<URL_TO_IMAGE>
{
    "<URL_TO_IMAGE>": "<COLOR_OF_WINNER>"
}
```