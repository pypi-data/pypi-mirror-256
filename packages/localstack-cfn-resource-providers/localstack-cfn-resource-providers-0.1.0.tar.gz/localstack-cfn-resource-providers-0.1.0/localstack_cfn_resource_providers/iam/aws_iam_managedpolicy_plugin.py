from typing import Optional, Type

from localstack_cfn_resource_providers.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class IAMManagedPolicyProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::IAM::ManagedPolicy"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from localstack_cfn_resource_providers.iam.aws_iam_managedpolicy import (
            IAMManagedPolicyProvider,
        )

        self.factory = IAMManagedPolicyProvider
