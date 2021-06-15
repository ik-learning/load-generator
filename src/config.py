# -*- coding: utf-8 -*-

import json


class Config:
    def __init__(self, file):
        self.cfg = self._read_config_file(file)
        self.flat_config = self._flatten(self.cfg)
        # TODO: validate all the fields with json schema
        self.host: str = self.flat_config["host"]
        self.path: str = self.flat_config["attack.path"]
        self.rps: int = self.flat_config["attack.rps"]
        self.requests_count = self.flat_config["attack.requests_count"]
        self.warmup_requests_count = self.flat_config["attack.warmup_requests_count"]
        self.schemas = dict()
        for el in self.cfg["attack"]["schemas"]:
            self.schemas[el] = self.cfg["attack"]["schemas"].get(el)

    def _flatten(self, data):
        new_dict = {}
        for key, value in data.items():
            if type(value) == dict:
                _dict = {
                    ".".join([key, _key]): _value
                    for _key, _value in self._flatten(value).items()
                }
                new_dict.update(_dict)
            else:
                new_dict[key] = value
        return new_dict

    @staticmethod
    def _read_config_file(file):
        return json.loads(open(file).read())
