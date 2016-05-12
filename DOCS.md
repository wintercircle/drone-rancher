

The following parameters are used to configuration the plugin's behavior:

**Required**
* **url** - The URL of the rancher API server
* **access_key** - A rancher API access key
* **secret_key** - The associated secret key with the given API access key

**Optional**
* **compose_file** - The compose file to use to deploy services to rancher
  * If not provided leaves defaults to docker-compose.yml
* **stack** - The stack to deploy
  * If not provided defaults to name of repository
* **services** - A space-separated list of services declared in the docker-compose file to upgrade
  * If not provided deploys/upgrades all services defined in compose_file


The following is a sample drone-rancher configuration in your 
.drone.yml file:

```yaml
deploy:
  rancher:
    image: dangerfarms/drone-rancher
    url: $$RANCHER_URL
    access_key: $$RANCHER_ACCESS_KEY
    secret_key: $$RANCHER_SECRET_KEY
    compose_file: config/prod/docker-compose.yml
    services: web worker
    stack: api-{{TAG}}
```
