# Movie Recommendation

## Run within a docker:

```bash
docker build . -t movies-suggester-service
docker run -p 80:80 movies-suggester-service
```

## To run outside docker:

* Install `pip install -r requirements.txt`
* Run `fastapi run src/main.py --port 80`

## Using the API

You can connect to the API using http methods to pull data or you can go to `0.0.0.0:80/docs` to test it with Swagger