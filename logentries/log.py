"""Logging Module"""
#!/usr/bin/env python
# coding: utf-8
# vim: set ts=4 sw=4 et:
from __future__ import absolute_import

import logging
import sys

from logentries.utils import report, LOG_LE_AGENT, EXIT_ERR


class Log(object):
    """Log object"""
    def __init__(self):
        self.logger = logging.getLogger(LOG_LE_AGENT)
        if not self.log:
            report("Cannot open log output")
            sys.exit(EXIT_ERR)

        self.logger.setLevel(logging.INFO)

        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setLevel(logging.DEBUG)
        self.stream_handler.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(self.stream_handler)

    def enable_daemon_mode(self):
        """Enable daemon mode for log object"""
        self.logger.removeHandler(self.stream_handler)
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setLevel(logging.DEBUG)
        self.stream_handler.setFormatter(logging.Formatter("%(asctime)s  %(message)s"))
        self.logger.addHandler(self.stream_handler)

    def set_logger(self, logger):
        self.logger = logger
        self.logger.addHandler(self.stream_handler)

LOG = Log()
