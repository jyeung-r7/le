import unittest
from unittest import main
import json
import logging
import mock
from logentries.config import Config
import logentries.metrics as metrics
from logentries.configured_log import ConfiguredLog
from collections import Counter

class TestJsonConfig(unittest.TestCase):
    json_file = '''{
      "config": {
        "hostname": "hgreenland",
        "endpoint": "data.logentries.com",
        "user-key": "3d7946d4-0d97-11e7-9b83-6c0b84a93740",
        "agent-key": "498fa2ba-0d97-11e7-9b83-6c0b84a93740",
        "api-key": "555e7094-0d97-11e7-9b83-6c0b84a93740",
        "metrics": {
          "system-stat-token": "627d011e-0d97-11e7-9b83-6c0b84a93740",
          "system-stat-enabled": "true",
          "metrics-interval": "60s",
          "metrics-cpu": "system",
          "metrics-vcpu": "core",
          "metrics-mem": "system",
          "metrics-swap": "system",
          "metrics-net": "sum eth0",
          "metrics-disk": "sum sda4 sda5",
          "metrics-space": "/"
        },
        "logs": [
          {
            "name": "GreenLog",
            "token": "a7f9625e-0d98-11e7-9b83-6c0b84a93740",
            "path": "/var/log/GreenLog",
            "enabled": "true"
          }
        ]
      }
    }'''

    json_file_incorrect_token = '''{
      "config": {
        "hostname": "hgreenland",
        "endpoint": "data.logentries.com",
        "user-key": "3d7946d4-0d97-11e7-9b83-6c0b84a93740",
        "agent-key": "498fa2ba-0d97-11e7-9b83-6c0b84a93740",
        "api-key": "555e7094-0d97-11e7-9b83-6c0b84a93740",
        "metrics": {
          "system-stat-token": "627d011e-0d97-11e7-9b83-6c0b84a93740",
          "system-stat-enabled": "true",
          "metrics-interval": "60s",
          "metrics-cpu": "system",
          "metrics-vcpu": "core",
          "metrics-mem": "system",
          "metrics-swap": "system",
          "metrics-net": "sum eth0",
          "metrics-disk": "sum sda4 sda5",
          "metrics-space": "/"
        },
        "logs": [
          {
            "name": "incorrect_token",
            "token": "incorrect_token",
            "path": "/var/log/incorrect_token",
            "enabled": "true"
          }
        ]
      }
    }'''

    json_file_no_path = '''{
      "config": {
        "hostname": "hgreenland",
        "endpoint": "data.logentries.com",
        "user-key": "3d7946d4-0d97-11e7-9b83-6c0b84a93740",
        "agent-key": "498fa2ba-0d97-11e7-9b83-6c0b84a93740",
        "api-key": "555e7094-0d97-11e7-9b83-6c0b84a93740",
        "metrics": {
          "system-stat-token": "627d011e-0d97-11e7-9b83-6c0b84a93740",
          "system-stat-enabled": "true",
          "metrics-interval": "60s",
          "metrics-cpu": "system",
          "metrics-vcpu": "core",
          "metrics-mem": "system",
          "metrics-swap": "system",
          "metrics-net": "sum eth0",
          "metrics-disk": "sum sda4 sda5",
          "metrics-space": "/"
        },
        "logs": [
          {
            "name": "GreenLog",
            "token": "09da4e87-882e-41f1-bf50-5f8888888888",
            "enabled": "true"
          }
        ]
      }
    }'''

    json_file_incorrect_names = '''{
      "config": {
        "hostname": "hgreenland",
        "endpoint": "data.logentries.com",
        "user-key": "3d7946d4-0d97-11e7-9b83-6c0b84a93740",
        "agent-key": "498fa2ba-0d97-11e7-9b83-6c0b84a93740",
        "api-key": "555e7094-0d97-11e7-9b83-6c0b84a93740",
        "metrics": {
          "system-stat-token-false": "627d011e-0d97-11e7-9b83-6c0b84a93740",
          "system-stat-enabled-false": "true",
          "metrics-false": "60s",
          "metrics-false": "system",
          "metrics-false": "core",
          "metrics-false": "system",
          "metrics-false": "system",
          "metrics-false": "sum eth0",
          "metrics-false": "sum sda4 sda5",
          "metrics-false": "/"
        },
        "logs": [
          {
            "name_false": "GreenLog",
            "token_false": "09da4e87-882e-41f1-bf50-5f8888888888",
            "path_false": "/var/log/incorrect_token",
            "enabled_false": "true"
          }
        ]
      }
    }'''

    windows_json_file = '''{
      "config": {
        "hostname": "hgreenland",
        "endpoint": "data.logentries.com",
        "user-key": "3d7946d4-0d97-11e7-9b83-6c0b84a93740",
        "agent-key": "498fa2ba-0d97-11e7-9b83-6c0b84a93740",
        "api-key": "555e7094-0d97-11e7-9b83-6c0b84a93740",
        "metrics": {
          "system-stat-token": "627d011e-0d97-11e7-9b83-6c0b84a93740",
          "system-stat-enabled": "true",
          "metrics-interval": "60s",
          "metrics-cpu": "system",
          "metrics-vcpu": "core",
          "metrics-mem": "system",
          "metrics-swap": "system",
          "metrics-net": "sum eth0",
          "metrics-disk": "sum sda4 sda5",
          "metrics-space": "/"
        },
        "logs": [
          {
            "name": "GreenLog",
            "token": "a7f9625e-0d98-11e7-9b83-6c0b84a93740",
            "path": "/var/log/GreenLog",
            "enabled": "true"
          }
        ],
        "windows-eventlog":{
        "enabled": true,
        "token": "e684dc57-7240-4669-aa67-317e5493040a"
       }
      }
    }'''

    windows_json_file_incorrect_token = '''{
      "config": {
        "hostname": "hgreenland",
        "endpoint": "data.logentries.com",
        "user-key": "3d7946d4-0d97-11e7-9b83-6c0b84a93740",
        "agent-key": "498fa2ba-0d97-11e7-9b83-6c0b84a93740",
        "api-key": "555e7094-0d97-11e7-9b83-6c0b84a93740",
        "metrics": {
          "system-stat-token": "627d011e-0d97-11e7-9b83-6c0b84a93740",
          "system-stat-enabled": "true",
          "metrics-interval": "60s",
          "metrics-cpu": "system",
          "metrics-vcpu": "core",
          "metrics-mem": "system",
          "metrics-swap": "system",
          "metrics-net": "sum eth0",
          "metrics-disk": "sum sda4 sda5",
          "metrics-space": "/"
        },
        "logs": [
          {
            "name": "GreenLog",
            "token": "a7f9625e-0d98-11e7-9b83-6c0b84a93740",
            "path": "/var/log/GreenLog",
            "enabled": "true"
          }
        ],
        "windows-eventlog":{
        "enabled": true,
        "token": "incorrect_token"
       }
      }
    }'''

    # test _load_windows_configured_logs_json() with the correct parameters given.
    @mock.patch('logging.log')
    def test_load_windows_configured_json(self, mock_logger):
        # Read in json config file
        d_conf = json.loads(self.windows_json_file)
        d_configFile = d_conf['config']
        CONFIG = Config()

        expected_dict = {'enabled' : True, 'token' : 'e684dc57-7240-4669-aa67-317e5493040a'}

        CONFIG._load_windows_configured_json(d_configFile, mock_logger)
        result_dict = CONFIG.windows_eventlogs

        self.assertDictEqual(result_dict, expected_dict, msg=None)

    # test load_windows_configured_logs_json() with an incorrect token given.
    @mock.patch('logging.log')
    def test_load_windows_configured_json_token(self, mock_logger):
        name = "windows-eventlog"
        token = None
        CONFIG = Config()

        # Read in json config file
        d_conf = json.loads(self.windows_json_file_incorrect_token)
        d_configFile = d_conf['config']

        CONFIG._load_windows_configured_json(d_configFile, mock_logger)

        # result matches error message
        mock_logger.warn.assert_called_with("Invalid log token `%s' in application `%s'.",
                        token, name)

    # test load_windows_configured_logs_json() with no windows-eventlog section.
    @mock.patch('logging.log')
    def test_load_windows_configured_json_empty(self, mock_logger):
        # Read in json config file
        d_conf = json.loads(self.json_file)
        d_configFile = d_conf['config']
        CONFIG = Config()

        expected_dict = {'enabled' : False, 'token' : None}

        CONFIG._load_windows_configured_json(d_configFile, mock_logger)
        result_dict = CONFIG.windows_eventlogs

        self.assertDictEqual(result_dict, expected_dict, msg=None)


    # test the metrics.load_json() method correctly pulls the right parameters and associated values.
    def test_should_metrics_json(self):
        # Read in json config file
        d_conf = json.loads(self.json_file)
        d_configFile = d_conf['config']
        self.metrics = metrics.MetricsConfig()
        expected_dict = {'processes': [], 'net': 'sum eth0', 'space' : '/', 'disk': 'sum sda4 sda5', 'interval': '60s',
                         'swap': 'system', 'vcpu': 'core', 'cpu': 'system', 'mem': 'system',
                         'token': '627d011e-0d97-11e7-9b83-6c0b84a93740', 'enabled': 'true'}

        self.metrics.load_json(d_configFile)
        result_dict = self.metrics.__dict__

        self.assertDictEqual(result_dict, expected_dict, msg=None)

    # test the metrics.load_json() method when incorrect parameter names are given.
    def test_should_not_load_metrics_json(self):
        # Read in json config file
        d_conf = json.loads(self.json_file_incorrect_names)
        d_configFile = d_conf['config']
        self.metrics = metrics.MetricsConfig()
        expected_dict = {'processes': [], 'net': None, 'space' : None, 'disk': None, 'interval': None, 'swap': None,
                         'vcpu': None, 'cpu': None, 'mem': None, 'token': None, 'enabled': None}

        self.metrics.load_json(d_configFile)
        result_dict = self.metrics.__dict__

        self.assertDictEqual(result_dict, expected_dict, msg=None)

    # test the _load_configured_logs_json() method correctly pulls the right parameters and associated values.
    @mock.patch('logging.log')
    def test_load_correct_configured_logs_json(self, mock_logger):
        # Read in json config file
        d_conf = json.loads(self.json_file)
        d_configFile = d_conf['config']
        CONFIG = Config()

        expected_log_list = []
        expected_configured_log = ConfiguredLog('GreenLog', 'a7f9625e-0d98-11e7-9b83-6c0b84a93740', '', '/var/log/GreenLog', '', '')
        expected_log_list.append(expected_configured_log)

        CONFIG._load_configured_logs_json(d_configFile, mock_logger)
        actual_log_result = CONFIG.configured_logs

        self.assertCountEqual(expected_log_list, actual_log_result, msg=None)

    # test the _load_configured_logs_json() when incorrect parameter names are given.
    @mock.patch('logging.log')
    def test_load_incorrect_configured_logs_json(self, mock_logger):
        # Read in json config file
        d_conf = json.loads(self.json_file_incorrect_names)
        d_configFile = d_conf['config']
        CONFIG = Config()

        expected_log_list = []

        CONFIG._load_configured_logs_json(d_configFile, mock_logger)
        actual_log_result = CONFIG.configured_logs

        self.assertCountEqual(expected_log_list, actual_log_result, msg=None)

    # test the _load_configured_logs_json() when incorrect token entered.
    @mock.patch('logging.log')
    def test_load_incorrect_token_configured_logs_json_token(self, mock_logger):
        CONFIG = Config()
        name = "incorrect_token"
        token = "incorrect_token"

        # Read in json config file
        d_conf = json.loads(self.json_file_incorrect_token)
        d_configFile = d_conf['config']

        CONFIG._load_configured_logs_json(d_configFile, mock_logger)

        # result matches error message
        mock_logger.warn.assert_called_with("Invalid log token `%s' in application `%s'.",
                        token, name)

    # test the _load_configured_logs_json() when path does not exist.
    @mock.patch('logging.log')
    def test_load_configured_incorrect_path_logs_json_path(self, mock_logger):
        CONFIG = Config()
        name = 'GreenLog'
        path = None

        # Read in json config file
        d_conf = json.loads(self.json_file_no_path)
        d_configFile = d_conf['config']

        CONFIG._load_configured_logs_json(d_configFile, mock_logger)

        # result matches error message
        mock_logger.debug.assert_called_with("Not following logs for application `%s' as `%s' "
         "parameter is not specified", name, path)

if __name__ == '__main__':
    unittest.main()


