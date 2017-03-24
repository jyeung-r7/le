"""Configured Log Module"""
#!/usr/bin/env python
# coding: utf-8
# vim: set ts=4 sw=4 et:


class ConfiguredLog(object):

    """Configured Log Class"""

    def __init__(self, name, token, destination, path, formatter, entry_identifier):
        self.name = name
        self.token = token
        self.destination = destination
        self.path = path
        self.formatter = formatter
        self.entry_identifier = entry_identifier
        self.logset = None
        self.logset_id = None
        self.log_id = None

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.name == other.name and
                self.token == other.token and
                self.destination == other.destination and
                self.path == other.path and
                self.formatter == other.formatter and
                self.entry_identifier == other.entry_identifier and
                self.logset == other.logset and
                self.logset_id == other.logset_id and
                self.log_id == other.logset_id)
        return False
