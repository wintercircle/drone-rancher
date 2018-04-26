#!/usr/bin/env python
"""
Deploy builds to a Rancher orchestrated stack using rancher-compose
"""
import os

import subprocess


def create_arg_flag(flag, value):
    """Return an arg list if a value exists, otherwise return None."""
    return "{} {}".format(flag, value) if value else ''


def str_to_bool(value):
    return value in ['true', 'True', True]


def main():
    """The main entrypoint for the plugin."""
    # Optional fields
    compose_file = os.environ["PLUGIN_COMPOSE_FILE"]
    rancher_file = os.environ["PLUGIN_RANCHER_FILE"]
    use_tag_in_stack = str_to_bool(os.environ.get('PLUGIN_USE_TAG_IN_STACK', 'false'))
    stack = os.environ["PLUGIN_STACK"] or os.environ["DRONE_REPO_NAME"]
    if use_tag_in_stack and os.environ["DRONE_TAG"]:
        stack = '{}-{}'.format(stack, os.environ["DRONE_TAG"])

    services = os.environ.get("PLUGIN_SERVICES", '')
    force_upgrade = str_to_bool(os.environ.get('PLUGIN_FORCE', 'false'))
    confirm_upgrade = str_to_bool(os.environ.get('PLUGIN_CONFIRM', 'false'))
    pull = str_to_bool(os.environ.get('PLUGIN_ALWAYS_PULL', 'false'))

    # Set Required fields for rancher-compose to work
    # Should raise an error if they are not declared
    
    os.environ["RANCHER_URL"] = os.environ.get('PLUGIN_URL')

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


if __name__ == "__main__":
    main()
