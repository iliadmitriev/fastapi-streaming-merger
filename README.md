# Fastapi streaming service

Fastapi streaming service simple example

## Install

```sh
pip3 install -r requirements.txt
```

## Usage

Run streams
```sh
hypercorn -b localhost:8001 stream1:app
hypercorn -b localhost:8002 stream2:app
```

Check streams

```sh
curl -N http://127.0.0.1:8001/stream1
curl -N http://127.0.0.1:8002/stream2
```

Run main service
```sh
hypercorn -b localhost:8000 main:app
```

Get stream
```sh
curl -N http://127.0.0.1:8000/main
```