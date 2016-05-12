#!/usr/bin/env python
"""
Deploy builds to a Rancher orchestrated stack using rancher-compose
"""
import drone
import requests


def main():
    """
    The main entrypoint for the plugin.
    """
    # Retrives plugin input from stdin/argv, parses the JSON, returns a dict.
    payload = drone.plugin.get_input()
    # vargs are where the values passed in the YaML reside.
    vargs = payload["vargs"]

    # Formulate the POST request.
    data = payload["build"]
    response = requests.get(vargs["url"], data=data)
    response.raise_for_status()
    print(response.json())


if __name__ == "__main__":
    main()
