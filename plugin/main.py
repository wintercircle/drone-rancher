#!/usr/bin/env python
"""
Deploy builds to a Rancher orchestrated stack using rancher-compose
"""
import os

import drone
import subprocess


def create_arg_flag(flag, value):
    """Return an arg list if a value exists, otherwise return None."""
    return [flag, value] if value else None


def main():
    """The main entrypoint for the plugin."""
    payload = drone.plugin.get_input()
    vargs = payload["vargs"]

    # Change directory to deploy path
    deploy_path = payload["workspace"]["path"]
    os.chdir(deploy_path)

    # Optional fields
    compose_file = vargs.get('compose_file', 'docker-compose.yml')
    rancher_file = vargs.get('rancher_file')
    stack = vargs.get('stack', payload['repo']['name'])
    services = vargs.get('services', '')

    # Set Required fields for rancher-compose to work
    # Should raise an error if they are not declared
    os.environ["RANCHER_URL"] = vargs['url']
    os.environ["RANCHER_ACCESS_KEY"] = vargs['access_key']
    os.environ["RANCHER_SECRET_KEY"] = vargs['secret_key']

    try:

        base_command = ["rancher-compose"]
        rancher_file_args = create_arg_flag("-r", rancher_file)
        compose_file_args = create_arg_flag("-f", compose_file)
        stack_args = create_arg_flag("-p", stack)
        up_args = ["up", "-d", "--upgrade", "--pull"]
        services_args = services

        rancher_compose_args = [
            base_command,
            rancher_file_args,
            compose_file_args,
            stack_args,
            up_args,
            services_args
        ]
        rancher_compose_cmd = filter(None, rancher_compose_args)

        print(' '.join(rancher_compose_cmd))
        subprocess.check_call(rancher_compose_cmd)
    finally:
        # Unset environmental variables, no point in them hanging about
        del os.environ['RANCHER_URL']
        del os.environ['RANCHER_ACCESS_KEY']
        del os.environ['RANCHER_SECRET_KEY']


if __name__ == "__main__":
    main()
