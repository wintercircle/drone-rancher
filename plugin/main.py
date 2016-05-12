#!/usr/bin/env python
"""
Deploy builds to a Rancher orchestrated stack using rancher-compose
"""
import os

import drone
import subprocess


def main():
    """The main entrypoint for the plugin."""
    payload = drone.plugin.get_input()
    vargs = payload["vargs"]

    # Required fields should raise an error
    os.environ["RANCHER_URL"] = vargs['url']
    os.environ["RANCHER_ACCESS_KEY"] = vargs['access_key']
    os.environ["RANCHER_SECRET_KEY"] = vargs['secret_key']

    # Optional fields
    compose_file = vargs.get('compose_file', 'docker-compose.yml')
    stack = vargs.get('stack', payload['repo']['name'])
    services = vargs.get('services', '')

    # Change directory
    deploy_path = payload["workspace"]["path"]
    os.chdir(deploy_path)

    rc_args = [
        "rancher-compose", "-f", compose_file, "-p", stack, "up", services,
    ]
    subprocess.call(rc_args)


if __name__ == "__main__":
    main()
