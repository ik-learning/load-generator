# Load Generator

- [Load Generator](#load-generator)
  * [Local Development and Testing](#local-development-and-testing)
    + [Wiremock](#wiremock)
  * [Setup local Development environment](#setup-local-development-environment)
  * [Usage](#usage)
  * [RUN Localy](#run-localy)
  * [Run Against Exercise endpoint](#run-against-exercise-endpoint)
  * [Think about it](#think-about-it)
  * [Output](#output)
  * [Features](#features)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

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
./cli.py --config-file ddos.config.json
```

## Think about it

- Request wait time????
- warm up
- Testing
- Controll CPU/Memory usage for a cannon
- Test different strategies e.g. speed up, slow down, check
- why chosed threading/async/multiprocessing
- Create controller/worker setup as future improvement as there is probably request limit per IP

## Output

```bash
$ ./cli.py --config-file config.json
09:13:53:INFO:cli run simulation... against https://c1i55mxsd6.execute-api.us-west-2.amazonaws.com/Live
09:13:54:ERROR:client_interface Expecting value: line 1 column 1 (char 0)
09:13:55:ERROR:client_interface Expecting value: line 1 column 1 (char 0)
09:13:56:ERROR:client_interface Expecting value: line 1 column 1 (char 0)
09:13:58:INFO:statistics processing. Number of requests:150.
	average RPS:27.3 and target RPS:30
	execution time:5.5
	percentiles:50%:0.18683818540999994. 75%:0.1870355990000001. 90%:0.1870355990000001. 95%:0.1870355990000001. 100%:0.1870355990000001.
	codes:{200: 144, 429: 2, 500: 2, 502: 1, 301: 1}
	errors:3
```

## Features

- [X] Calculate RPS
- [X] Mutli threading
- [X] Output to console every second statistics
- [X] Dynamic json payload
- [X] Add authentication token support
- [X] Read configuration from a file
- [X] Validate json input/output
- [X] Output RPS and desired RPS
- [X] Output statistics per endpoint
- [X] Async requests
- [ ] Global logging
- [X] Make explicit number of requests
- [ ] Run for explicit number of seconds
- [X] Json schema validator in configuration file
