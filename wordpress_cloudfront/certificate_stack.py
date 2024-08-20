from aws_cdk import (
    CfnParameter as cfnParam,
    aws_certificatemanager as acm,
    aws_route53 as r53,
    Stack,
    Aspects
)
from constructs import Construct
import cdk_nag

# https://www.performancemagic.com/wafv2-cloudfront-cdk/

class certificate_stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, default_action="allow", **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        HostedZoneId = self.node.try_get_context("HostedZoneId")
        HostedZoneName = self.node.try_get_context("HostedZoneName")
        
        self.certif = None
        if HostedZoneId :   
            hosted_zone = r53.HostedZone.from_hosted_zone_id(self, "Hosted_Zone", HostedZoneId)
            
            
            self.certif = acm.Certificate(self, "Certificate",
                # domain_name="*.cheikh-mahaman.com"
                domain_name= "*." + HostedZoneName,
                validation=acm.CertificateValidation.from_dns(hosted_zone)
            )
        
        # cdk_nag.NagSuppressions.add_stack_suppressions(stack=self, suppressions=[
        #     {"id": "AwsSolutions-CFR4", "reason": "Demo : Distributions that use the default CloudFront viewer certificate are non-compliant with this rule"},
        #     {"id": "AwsSolutions-CFR5", "reason": "Demo : Use of default CloudFront viewer certificate"},
        #     {"id": "AwsSolutions-CFR1", "reason": "Demo : No need of Geo restrictions"},
        # ])
        # Aspects.of(self).add(cdk_nag.AwsSolutionsChecks())

        
    @property
    def certificate(self):
        """return the arn of the acl"""
        return self.certif

   