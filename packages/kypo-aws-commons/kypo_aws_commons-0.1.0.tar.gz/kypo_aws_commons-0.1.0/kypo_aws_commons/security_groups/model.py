"""
Security Group model.
Python object representing security groups configuration specified in .yaml file.
"""
from yamlize import Object as YamlObject, Attribute, Sequence


class Rule(YamlObject):
    direction = Attribute(type=str)  # TODO: make it enum/verify value
    ip_type = Attribute(key='type', type=str)  # TODO: make it enum
    protocol = Attribute(type=str)
    port_range = Attribute(type=str)
    remote_ip = Attribute(type=str, default='')
    remote_group = Attribute(type=str, default='')


class Rules(Sequence):
    item_type = Rule


class Group(YamlObject):
    name = Attribute(type=str)
    rules = Attribute(type=Rules)


class Groups(Sequence):
    item_type = Group


class SecurityGroupModel(YamlObject):
    groups = Attribute(type=Groups)
