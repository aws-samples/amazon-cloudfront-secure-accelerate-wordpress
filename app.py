#!/usr/bin/env python3

import os
import aws_cdk as cdk
from wordpress_cloudfront.cloudfront_stack import WordpressCloudfrontStack
from wordpress_cloudfront.waf_acls_stack import waf_acls_stack
from wordpress_cloudfront.certificate_stack import certificate_stack
from cdk_nag import NagPack


env_us_east_1 = cdk.Environment(region="us-east-1")

app = cdk.App()

waf_acls = waf_acls_stack(app, 'WafAclsStack', env=env_us_east_1)
certif_stack = certificate_stack(app, "CertificateStack", env=env_us_east_1)
wordpress_stack = WordpressCloudfrontStack(app, "WorpressCloudfrontStack", Certificate=certif_stack.certificate, web_acl_for_consumers=waf_acls.consumers_web_acl_arn, web_acl_for_publishers= waf_acls.publishers_web_acl_arn, env=env_us_east_1)

app.synth()
