import unittest
import json
import metrics
from config import Config

CONFIG = Config()

class TestJsonConfig(unittest.TestCase):
    json_file = '''{
      "config": {
        "hostname": "mgarewal",
        "endpoint": "data.logentries.com",
        "user-key": "4a22b0ba-593a-41e9-9271-bf4475b09f38",
        "agent-key": "754302eb-778d-4dc6-8043-c8465826c90b",
        "api-key": "0e099781-bd98-46a5-8c6a-1129a043c058",
        "metrics": {
          "system-stat-token": "226a8d39-d943-4b73-ac8d-099e239ebda7",
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
            "token": "09da4e87-882e-41f1-bf50-5f45273ed180",
            "path": "/var/log/GreenLog",
            "enabled": "true"
          }
        ]
      }
    }'''

    # Read in json config file
    d_conf = json.loads(json_file)
    d_configFile = d_conf['config']

    #    test the metrics.load_json() method correctly pulls the right parameters and associated values.
    def test_metrics_load_json(self):
        self.metrics = metrics.MetricsConfig()
        expected_dict = {'net': 'sum eth0', 'space' : '/', 'disk': 'sum sda4 sda5', 'interval': '60s', 'swap': 'system',
                         'vcpu': 'core', 'cpu': 'system', 'mem': 'system', 'token': None}

        result_dict = self.metrics.load_json(self.d_configFile)
        print('metrics loaded are: ', result_dict)

        self.assertDictEqual(result_dict, expected_dict, msg=None)

    # test the _load_configured_logs_json() method correctly pulls the right parameters and associated values.
    def test_load_configured_logs_json(self):
        expected_dict = {
            'name': 'GreenLog',
            'token': '09da4e87-882e-41f1-bf50-5f45273ed180',
            'path': '/var/log/GreenLog',
            'formatter' : '',
            'entry_identifier' : '',
            'destination' : ''
          }

        result_dict = CONFIG._load_configured_logs_json(self.d_configFile)
        print('configured log parameters are: ', result_dict)

        self.assertDictEqual(result_dict, expected_dict, msg=None)


if __name__ == '__main__':
    unittest.main()
