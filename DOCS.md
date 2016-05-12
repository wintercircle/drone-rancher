

The following parameters are used to configuration the plugin's behavior:

**Required**
* **url** - The URL of the rancher API server
* **access_key** - A rancher API access key
* **secret_key** - The associated secret key with the given API access key

**Optional**
* **compose_file** - The compose file with which to use to deploy services to rancher
  * If not provided leaves out of the call, rancher-compose will use docker-compose.yml in that case
* **services** - A comma separated list of services declared in the docker-compose file to upgrade
  * If not provided defaults to all
* **stack** - The stack to deploy
  * If not provided defaults to name of repository


The following is a sample drone-rancher configuration in your 
.drone.yml file:

```yaml
notify:
  drone-rancher:
    image: dangerfarms/drone-rancher
    url: $$RANCHER_URL
    access_key: $$RANCHER_ACCESS_KEY
    secret_key: $$RANCHER_SECRET_KEY
    compose_file: config/prod/docker-compose.yml
    services: web
    stack: api-{{TAG}}
```
