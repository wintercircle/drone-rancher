drone-rancher
=============

Deploy builds to a Rancher orchestrated stack using rancher-compose

Build
-----

docker build -t wintercircle/drone-rancher .
docker push wintercircle/drone-rancher

Overview
--------

Execute from the working directory:

```
docker run --rm \
  -e PLUGIN_COMPOSE_FILE=docker-compose.yml \
  -e PLUGIN_RANCHER_FILE=rancher-compose.yml \
  -e PLUGIN_SERVICES=web \
  -e PLUGIN_FORCE=true \
  -e PLUGIN_CONFIRM=true \
  -e PLUGIN_ALWAYS_PULL=true \
  -e PLUGIN_URL=https://rancher.url/ \
  -e DRONE_REPO_NAME=my/repo \
  -e RANCHER_ACCESS_KEY=key \
  -e RANCHER_SECRET_KEY=secret \
  wintercircle/drone-rancher
```


License
-------

drone-rancher is licensed under the Apache License. A copy is included
in this repository.
