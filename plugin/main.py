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

    # Change directory to deploy path
    deploy_path = payload["workspace"]["path"]
    os.chdir(deploy_path)

    # Optional fields
    compose_file = vargs.get('compose_file', 'docker-compose.yml')
    stack = vargs.get('stack', payload['repo']['name'])
    services = vargs.get('services', '')

    # Set Required fields for rancher-compose to work
    # Should raise an error if they are not declared
    os.environ["RANCHER_URL"] = vargs['url']
    os.environ["RANCHER_ACCESS_KEY"] = vargs['access_key']
    os.environ["RANCHER_SECRET_KEY"] = vargs['secret_key']

    rc_args = [
        "rancher-compose", "-f", compose_file, "-p", stack, "up", services,
    ]
    subprocess.call(rc_args)

    # Unset environmental variables, no point in them hanging about
    del os.environ['RANCHER_URL']
    del os.environ['RANCHER_ACCESS_KEY']
    del os.environ['RANCHER_SECRET_KEY']


if __name__ == "__main__":
    main()
