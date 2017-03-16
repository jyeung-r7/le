import unittest
import json
import metrics


class TestJsonConfig(unittest.TestCase):


    def test_metrics_load_json(self):
        self.metrics = metrics.MetricsConfig()
        expected_list = ['net', 'sum eth0', 'space', '/', 'disk', 'sum sda4 sda5', 'interval', '60s', 'swap', 'system', 'vcpu', 'core', 'cpu', 'system', 'mem', 'system', 'token', None]


        # Read in json config file
        with open('/home/mgarewal/rapid7/logs-json/logging.json') as data_file:
            d_conf = json.loads(data_file.read())
        d_configFile = d_conf['config']

        result_list = self.metrics.load_json(d_configFile)
        print(result_list)

        self.assertEqual(result_list, expected_list)

if __name__ == '__main__':
    unittest.main()