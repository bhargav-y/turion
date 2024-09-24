## Setup

First, create an `.env` file within project root with the following environment variables:

```
POSTGRES_HOST=postgres
POSTGRES_USER="username"
POSTGRES_PASSWORD="password"
POSTGRES_DB="telemetry"
```
The database name is a suggestion, you can name it whatever you like. However, the `POSTGRES_HOST` must be `postgres` since that is the name of the container in the `docker-compose.yaml` file.

Next, (within project root) run the following commands:

```
docker-compose up -d --build
```

Run `python3 send_telemetry.py` to start sending telemetry data to the server. 

Example cURL request to see the telemetry data:

```
curl 'http://localhost:8000/api/v1/telemetry
```

Example cURL request to get the telemetry data with pagination:

```
 curl 'http://localhost:8000/api/v1/telemetry?page=1&page_size=20'
```

The default is page 1 with a page size of 10.