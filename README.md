# Load Generator

## Local Development and Testing

To simplify development added [Wiremock](http://wiremock.org/docs)

```sh
make wiremock-up
make wiremock-restart
make wiremock-down
```

Example usage
```sh
make wiremock-up
curl --location --request POST 'http://localhost:8080/Live' --header 'Content-Type: application/json' --data-raw '{ "name": "test", "date": "09:01:52", "requests_sent": 1 }'
```

### Wiremock

Should be awaialble `http://localhost:8080/__admin`

## Setup local Development environment

```sh
pipenv shell
pipenv install --dev
```


## Think about it

- Request wait time????
- warm up
- Testing
- Create controller/worker setup as future improvement
- Controll CPU/Memory usage for a cannon
- Test different strategies e.g. speed up, slow down, check
- why chosed threading/async/multiprocessing

## TODO

- [ ] Calculate RPS
- [ ] Mutli threading
- [ ] Output to console every second statistics
- [ ] Add authentication token
- [ ] Read from file
- [ ] Validate json input/output
