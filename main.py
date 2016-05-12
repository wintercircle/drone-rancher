#!/usr/bin/env python
"""
Deploy builds to a Rancher orchestrated stack using rancher-compose
"""
import os

import drone
import subprocess


def create_arg_flag(flag, value):
    """Return an arg list if a value exists, otherwise return None."""
    return "{} {}".format(flag, value) if value else ''


def str_to_bool(value):
    return value in ['true', 'True', True]


def main():
    """The main entrypoint for the plugin."""
    payload = drone.plugin.get_input()
    vargs = payload["vargs"]

    # Change directory to deploy path
    deploy_path = payload["workspace"]["path"]
    os.chdir(deploy_path)

    # Optional fields
    compose_file = vargs.get('compose_file')
    rancher_file = vargs.get('rancher_file')
    stack = vargs.get('stack', payload['repo']['name'])
    services = vargs.get('services', '')
    force_upgrade = str_to_bool(vargs.get('force', 'false'))
    confirm_upgrade = str_to_bool(vargs.get('confirm', 'false'))
    pull = str_to_bool(vargs.get('pull', 'false'))

    # Set Required fields for rancher-compose to work
    # Should raise an error if they are not declared
    os.environ["RANCHER_URL"] = vargs['url']
    os.environ["RANCHER_ACCESS_KEY"] = vargs['access_key']
    os.environ["RANCHER_SECRET_KEY"] = vargs['secret_key']

    try:
        base_rancher_compose_cmd = \
            "rancher-compose {rancher_file} {compose_file} {stack} up -d {{upgrade}} {{pull}} {{confirm}} {services}".format(
                rancher_file=create_arg_flag("-r", rancher_file),
                compose_file=create_arg_flag("-f", compose_file),
                stack=create_arg_flag("-p", stack),
                services=services
            )
        rancher_compose_upgrade_cmd = base_rancher_compose_cmd.format(
            upgrade='--force-upgrade' if force_upgrade else '--upgrade',
            pull='--pull' if pull else '',
            confirm='',
        )
        print(rancher_compose_upgrade_cmd)
        subprocess.check_call(rancher_compose_upgrade_cmd.split())

        if confirm_upgrade:
            rancher_compose_confirm_cmd = base_rancher_compose_cmd.format(
                upgrade='--upgrade',
                pull='',
                confirm='--confirm-upgrade',
            )
            print(rancher_compose_confirm_cmd)
            subprocess.check_call(rancher_compose_confirm_cmd.split())
    finally:
        # Unset environmental variables, no point in them hanging about
        del os.environ['RANCHER_URL']
        del os.environ['RANCHER_ACCESS_KEY']
        del os.environ['RANCHER_SECRET_KEY']


if __name__ == "__main__":
    main()
