from typing import Optional, Type

from localstack_cfn_resource_providers.resource_provider import (
    CloudFormationResourceProviderPlugin,
    ResourceProvider,
)


class IAMInstanceProfileProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::IAM::InstanceProfile"

    def __init__(self):
        self.factory: Optional[Type[ResourceProvider]] = None

    def load(self):
        from localstack_cfn_resource_providers.iam.aws_iam_instanceprofile import (
            IAMInstanceProfileProvider,
        )

        self.factory = IAMInstanceProfileProvider
