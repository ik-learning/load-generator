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

## Usage

```
▶️  ./cli.py --help
usage: cli.py [-h] [--config-file CONFIG_FILE] [--auth-token AUTH_TOKEN]

optional arguments:
  -h, --help            show this help message and exit
  --config-file CONFIG_FILE
                        configuration file
  --auth-token AUTH_TOKEN
                        authentication token
```

## RUN Localy

```
make wiremock-up
./cli.py
```

## Run Against Exercise endpoint

```
export AUTH_TOKEN=<token>
./cli.py --config-file config.json
```

## Think about it

- Request wait time????
- warm up
- Testing
- Controll CPU/Memory usage for a cannon
- Test different strategies e.g. speed up, slow down, check
- why chosed threading/async/multiprocessing
- Create controller/worker setup as future improvement

## Features

- [X] Calculate RPS
- [X] Mutli threading
- [X] Output to console every second statistics
- [X] Dynamic json payload
- [X] Add authentication token support
- [X] Read configuration from a file
- [X] Validate json input/output
- [ ] Output RPS and desired RPS
- [ ] Output statistics per endpoint
- [ ] Global logging
- [X] Make explicit number of requests
- [ ] Run for explicit number of seconds
- [X] Json schema validator in configuration file
