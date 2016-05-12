Write your plugin documentation here.

The following parameters are used to configuration the plugin's behavior:

* **url** - The URL to POST the webhook to.

The following is a sample drone-rancher configuration in your 
.drone.yml file:

```yaml
notify:
  drone-rancher:
    image: dangerfarms/drone-rancher
    url: http://mockbin.org/
```
