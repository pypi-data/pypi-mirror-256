from constructs import Construct

from aws_commons.security_groups.model import SecurityGroupModel

from cdktf_cdktf_provider_aws.security_group import SecurityGroup
from cdktf_cdktf_provider_aws.security_group_rule import SecurityGroupRule
from cdktf_cdktf_provider_aws.data_aws_security_group import DataAwsSecurityGroup


class PortRangeException(Exception):
    """
    Security Group Port Range Exception
    """
    pass


class SecurityGroupsConstruct(Construct):

    def __init__(self, scope, id, vpc_id: str, security_group_model: SecurityGroupModel):
        super().__init__(scope, id)
        self.security_group_model = security_group_model
        self.aws_groups_dict = {
            group.name: SecurityGroup(self, group.name, name=group.name, vpc_id=vpc_id)
            for group in self.security_group_model.groups
        }

        for group in self.security_group_model.groups:
            for index, rule in enumerate(group.rules):
                from_port = 0
                to_port = 65535
                if ':' in rule.port_range:
                    # got range in a format --> from:to
                    from_port, to_port = rule.port_range.split(':')
                    from_port, to_port = int(from_port), int(to_port)
                elif rule.port_range.isdigit():
                    # got a specific port
                    from_port = int(rule.port_range)
                    to_port = int(rule.port_range)
                elif rule.port_range != 'any':
                    raise PortRangeException(f'Misconfigured "port_range" for group: "{group.name}"')

                if rule.protocol.lower() == 'icmp':
                    from_port = -1
                    to_port = -1

                protocol = '-1' if rule.protocol == 'any' else rule.protocol
                cidr_blocks = [rule.remote_ip] if rule.remote_ip else None
                source_security_group_id = self.aws_groups_dict[rule.remote_group].id if rule.remote_group else None

                # To prevent security groups cycle dependencies, first create groups then it's rules
                SecurityGroupRule(self, f'{group.name}-{index}',
                                  security_group_id=self.aws_groups_dict[group.name].id,
                                  type=rule.direction,
                                  from_port=from_port,
                                  to_port=to_port,
                                  protocol=protocol,
                                  cidr_blocks=cidr_blocks if rule.ip_type == 'IPv4' else None,
                                  ipv6_cidr_blocks=cidr_blocks if rule.ip_type == 'IPv6' else None,
                                  source_security_group_id=source_security_group_id)

    @staticmethod
    def from_file(scope, id: str, vpc_id: str, file_path: str):
        with open(file_path) as file:
            sec_groups = SecurityGroupModel.load(file)

        return SecurityGroupsConstruct(scope, id, vpc_id, sec_groups)

    @staticmethod
    def get_security_group(scope, vpc_id: str, name: str) -> DataAwsSecurityGroup:
        return DataAwsSecurityGroup(scope, 'data-sg', vpc_id=vpc_id, name=name)
