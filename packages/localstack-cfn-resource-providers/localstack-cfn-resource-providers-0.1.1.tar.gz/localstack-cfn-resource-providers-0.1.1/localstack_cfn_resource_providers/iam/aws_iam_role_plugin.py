from typing import Optional, Type

from localstack_cfn_resource_providers.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class IAMRoleProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::IAM::Role"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from localstack_cfn_resource_providers.iam.aws_iam_role import IAMRoleProvider

        self.factory = IAMRoleProvider
