from localstack_cfn_resource_providers.resource_provider import CloudFormationResourceProviderPlugin


class IAMAccessKeyProviderPlugin(CloudFormationResourceProviderPlugin):
    name = "AWS::IAM::AccessKey"

    def __init__(self):
        self.factory = None

    def load(self):
        from .aws_iam_accesskey import (
            IAMAccessKeyProvider,
        )

        self.factory = IAMAccessKeyProvider
