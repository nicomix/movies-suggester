# Movie Recommendation

## Run within a docker:

```bash
docker build . -t movies-suggester-service
docker run -p 80:80 movies-suggester-service
```

## To run outside docker:

* Install `pip install "fastapi[standard]"`
* Install `pip install -r requirements.txt`
* Run `fastapi run src/main.py --port 80`