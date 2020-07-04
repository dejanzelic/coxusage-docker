# coxusage-docker

## Build

```
docker build -t dejandayoff/coxusage .
```

## Usage

```
docker container run --rm --env-file secret/cox.env -v ${PWD}/output/:/data/ dejandayoff/coxusage
```

Contents of secret/cox.env

```
COX_USER=username
COX_PASSWORD=password
JSON_LOCATION=/data/coxusage.json
```