import unittest
from unittest import TestCase
from unittest.mock import patch

from main import main


class PluginTest(TestCase):

    @patch("main.subprocess")
    @patch("main.drone")
    def test_main_works_with_correct_data(self, mock_drone, mock_subprocess):
        mock_subprocess.check_call.return_value = None
        mock_drone.plugin.get_input.return_value = {
            "repo": {
                "name": "repo-name",
            },
            "workspace": {
                "path": "/tmp"
            },
            "build": {
                "number": 10,
                "branch": "master",
            },
            "vargs": {
                "url": "$$RANCHER_URL",
                "access_key": "$$RANCHER_ACCESS_KEY",
                "secret_key": "$$RANCHER_SECRET_KEY",
                "compose_file": ".config/dev/docker-compose.yml",
                "rancher_file": ".config/dev/rancher-compose.yml",
                "services": "web"
            }
        }
        main()

if __name__ == '__main__':
    unittest.main()
