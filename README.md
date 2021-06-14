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

- [X] Calculate RPS
- [X] Mutli threading
- [X] Output to console every second statistics
- [ ] Dynamic json payload
- [ ] Add authentication token
- [ ] Read from file
- [X] Validate json input/output
- [ ] Output RPS and desired RPS
- [ ] Output statistics per endpoint
- [ ] Global logging
- [X] Make explicit number of requests
- [ ] Run for explicit number of seconds
- [X] Json schema validator in configuration file
