# Go Winner Prediction API

Specify URL to your png image in the format (for example, use ```curl```):
```
$ curl -X GET http://127.0.0.1:5000/?url=<URL_TO_THE_IMAGE>
{
    "prediction": "<COLOR_OF_THE_WINNER>",
    "url": "<URL_TO_THE_IMAGE>"
}
```