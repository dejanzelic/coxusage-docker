# coxusage-docker

## Build

```
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t dejandayoff/coxusage:dev --push .
```

## Usage

```
docker container run --rm --env-file secret/cox.env -v ${PWD}/output/:/data/ dejandayoff/coxusage
```
The script outputs to /data/ so the mapped destination must stay /data/. Adjust the source mapping to your needs (ie. ~/.homeassistant/config/:/data/)

Contents of secret/cox.env

```
COX_USER=username
COX_PASSWORD=password
JSON_FILENAME=coxusage.json
```

## Pro Tips
Run the container daily in your crontab!

Check out: https://github.com/ntalekt/coxusage-docker For examples of integrating into Home Assistant