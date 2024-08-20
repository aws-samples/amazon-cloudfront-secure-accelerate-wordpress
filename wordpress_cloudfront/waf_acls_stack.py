from aws_cdk import (
    aws_wafv2 as waf,
    Stack,
    Aspects
)
from constructs import Construct
import cdk_nag

# https://www.performancemagic.com/wafv2-cloudfront-cdk/


class waf_acls_stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, default_action="allow", **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
                
        self.web_acl_for_consumers = waf.CfnWebACL(self, "waf_acl_consumers",
                                                   default_action={
                                                       default_action: {}},
                                                   scope="CLOUDFRONT",
                                                   visibility_config={
                                                       "sampledRequestsEnabled": True,
                                                       "cloudWatchMetricsEnabled": True,
                                                       "metricName": "web-acl",
                                                   },
                                                   rules=[
                                                       {
                                                           "priority": 0,
                                                           "overrideAction": {"none": {}},
                                                           "visibilityConfig": {
                                                               "sampledRequestsEnabled": True,
                                                               "cloudWatchMetricsEnabled": True,
                                                               "metricName": "AWS-AWSManagedRulesWordPressRuleSet",
                                                           },
                                                           "name": "AWS-AWSManagedRulesWordPressRuleSet",
                                                           "statement": {
                                                               "managedRuleGroupStatement": {
                                                                   "vendorName": "AWS",
                                                                   "name": "AWSManagedRulesWordPressRuleSet",
                                                               },
                                                           },
                                                       },
                                                       {
                                                           "priority": 1,
                                                           "overrideAction": {"none": {}},
                                                           "visibilityConfig": {
                                                               "sampledRequestsEnabled": True,
                                                               "cloudWatchMetricsEnabled": True,
                                                               "metricName": "AWS-AWSManagedRulesBotControlRuleSet",
                                                           },
                                                           "name": "AWS-AWSManagedRulesBotControlRuleSet",
                                                           "statement": {
                                                               "managedRuleGroupStatement": {
                                                                   "vendorName": "AWS",
                                                                   "name": "AWSManagedRulesBotControlRuleSet",
                                                               },
                                                           },
                                                       },
                                                       {
                                                           "priority": 2,
                                                           "overrideAction": {"none": {}},
                                                           "visibilityConfig": {
                                                               "sampledRequestsEnabled": True,
                                                               "cloudWatchMetricsEnabled": True,
                                                               "metricName": "AWS-AWSManagedRulesAdminProtectionRuleSet"
                                                           },
                                                           "name": "AWS-AWSManagedRulesAdminProtectionRuleSet",
                                                           "statement": {
                                                               "managedRuleGroupStatement": {
                                                                   "vendorName": "AWS",
                                                                   "name": "AWSManagedRulesAdminProtectionRuleSet",
                                                                   "scopeDownStatement": {
                                                                       "andStatement": {
                                                                           "statements": [
                                                                               {
                                                                                   "notStatement": {
                                                                                       "statement": {
                                                                                           "byteMatchStatement": {
                                                                                               "searchString": "/wp-admin/css/",
                                                                                               "fieldToMatch": {
                                                                                                   "uriPath": {}
                                                                                               },
                                                                                               "textTransformations": [
                                                                                                   {
                                                                                                       "priority": 0,
                                                                                                       "type": "NONE"
                                                                                                   }
                                                                                               ],
                                                                                               "positionalConstraint": "CONTAINS"
                                                                                           }
                                                                                       }
                                                                                   }
                                                                               },
                                                                               {
                                                                                   "notStatement": {
                                                                                       "statement": {
                                                                                           "byteMatchStatement": {
                                                                                               "searchString": "/wp-admin/js/",
                                                                                               "fieldToMatch": {
                                                                                                   "uriPath": {}
                                                                                               },
                                                                                               "textTransformations": [
                                                                                                   {
                                                                                                       "priority": 0,
                                                                                                       "type": "NONE"
                                                                                                   }
                                                                                               ],
                                                                                               "positionalConstraint": "CONTAINS"
                                                                                           }
                                                                                       }
                                                                                   }
                                                                               },
                                                                               {
                                                                                   "notStatement": {
                                                                                       "statement": {
                                                                                           "byteMatchStatement": {
                                                                                               "searchString": "/wp-admin/images/",
                                                                                               "fieldToMatch": {
                                                                                                   "uriPath": {}
                                                                                               },
                                                                                               "textTransformations": [
                                                                                                   {
                                                                                                       "priority": 0,
                                                                                                       "type": "NONE"
                                                                                                   }
                                                                                               ],
                                                                                               "positionalConstraint": "CONTAINS"
                                                                                           }
                                                                                       }
                                                                                   }
                                                                               }
                                                                           ]
                                                                       }
                                                                   }
                                                               }
                                                           }
                                                       },
                                                       {
                                                           "priority": 3,
                                                           "overrideAction": {"none": {}},
                                                           "visibilityConfig": {
                                                               "sampledRequestsEnabled": True,
                                                               "cloudWatchMetricsEnabled": True,
                                                               "metricName": "AWS-AWSManagedRulesPHPRuleSet",
                                                           },
                                                           "name": "AWS-AWSManagedRulesPHPRuleSet",
                                                           "statement": {
                                                               "managedRuleGroupStatement": {
                                                                   "vendorName": "AWS",
                                                                   "name": "AWSManagedRulesPHPRuleSet",
                                                               },

                                                           },
                                                       },
                                                       {
                                                           "priority": 4,
                                                           "overrideAction": {"none": {}},
                                                           "visibilityConfig": {
                                                               "sampledRequestsEnabled": True,
                                                               "cloudWatchMetricsEnabled": True,
                                                               "metricName": "AWS-AWSManagedRulesCommonRuleSet",
                                                           },
                                                           "name": "AWS-AWSManagedRulesCommonRuleSet",
                                                           "statement": {
                                                               "managedRuleGroupStatement": {
                                                                   "vendorName": "AWS",
                                                                   "name": "AWSManagedRulesCommonRuleSet",
                                                               },
                                                           },
                                                       },
                                                       {
                                                           "priority": 5,
                                                           "overrideAction": {"none": {}},
                                                           "visibilityConfig": {
                                                               "sampledRequestsEnabled": True,
                                                               "cloudWatchMetricsEnabled": True,
                                                               "metricName": "AWS-AWSManagedRulesKnownBadInputsRuleSet",
                                                           },
                                                           "name": "AWS-AWSManagedRulesKnownBadInputsRuleSet",
                                                           "statement": {
                                                               "managedRuleGroupStatement": {
                                                                   "vendorName": "AWS",
                                                                   "name": "AWSManagedRulesKnownBadInputsRuleSet",
                                                               },
                                                           },
                                                       },
                                                       {
                                                           "priority": 6,
                                                           "overrideAction": {"none": {}},
                                                           "visibilityConfig": {
                                                               "sampledRequestsEnabled": True,
                                                               "cloudWatchMetricsEnabled": True,
                                                               "metricName": "AWS-AWSManagedRulesSQLiRuleSet",
                                                           },
                                                           "name": "AWS-AWSManagedRulesSQLiRuleSet",
                                                           "statement": {
                                                               "managedRuleGroupStatement": {
                                                                   "vendorName": "AWS",
                                                                   "name": "AWSManagedRulesSQLiRuleSet",
                                                               },
                                                           },
                                                       },

                                                   ]
                                                   )

        self.web_acl_for_publishers = waf.CfnWebACL(self, "waf_acl_publishers",
                                                    default_action={
                                                        default_action: {}},
                                                    scope="CLOUDFRONT",
                                                    visibility_config={
                                                        "sampledRequestsEnabled": True,
                                                        "cloudWatchMetricsEnabled": True,
                                                        "metricName": "web-acl",
                                                    },
                                                    rules=[
                                                        {
                                                            "priority": 0,
                                                            "overrideAction": {"none": {}},
                                                            "visibilityConfig": {
                                                                "sampledRequestsEnabled": True,
                                                                "cloudWatchMetricsEnabled": True,
                                                                "metricName": "AWS-AWSManagedRulesWordPressRuleSet",
                                                            },
                                                            "name": "AWS-AWSManagedRulesWordPressRuleSet",
                                                            "statement": {
                                                                "managedRuleGroupStatement": {
                                                                    "vendorName": "AWS",
                                                                    "name": "AWSManagedRulesWordPressRuleSet",
                                                                },
                                                            },
                                                        },
                                                        {
                                                            "priority": 1,
                                                            "overrideAction": {"none": {}},
                                                            "visibilityConfig": {
                                                                "sampledRequestsEnabled": True,
                                                                "cloudWatchMetricsEnabled": True,
                                                                "metricName": "AWS-AWSManagedRulesBotControlRuleSet",
                                                            },
                                                            "name": "AWS-AWSManagedRulesBotControlRuleSet",
                                                            "statement": {
                                                                "managedRuleGroupStatement": {
                                                                    "vendorName": "AWS",
                                                                    "name": "AWSManagedRulesBotControlRuleSet",
                                                                },
                                                            },
                                                        },
                                                        {
                                                            "priority": 2,
                                                            "overrideAction": {"none": {}},
                                                            "visibilityConfig": {
                                                                "sampledRequestsEnabled": True,
                                                                "cloudWatchMetricsEnabled": True,
                                                                "metricName": "AWS-AWSManagedRulesPHPRuleSet",
                                                            },
                                                            "name": "AWS-AWSManagedRulesPHPRuleSet",
                                                            "statement": {
                                                                "managedRuleGroupStatement": {
                                                                    "vendorName": "AWS",
                                                                    "name": "AWSManagedRulesPHPRuleSet",
                                                                },
                                                            },
                                                        },
                                                        {
                                                            "priority": 3,
                                                            "overrideAction": {"none": {}},
                                                            "visibilityConfig": {
                                                                "sampledRequestsEnabled": True,
                                                                "cloudWatchMetricsEnabled": True,
                                                                "metricName": "AWS-AWSManagedRulesCommonRuleSet",
                                                            },
                                                            "name": "AWS-AWSManagedRulesCommonRuleSet",
                                                            "statement": {
                                                                "managedRuleGroupStatement": {
                                                                    "vendorName": "AWS",
                                                                    "name": "AWSManagedRulesCommonRuleSet",
                                                                },
                                                            },
                                                        },
                                                        {
                                                            "priority": 4,
                                                            "overrideAction": {"none": {}},
                                                            "visibilityConfig": {
                                                                "sampledRequestsEnabled": True,
                                                                "cloudWatchMetricsEnabled": True,
                                                                "metricName": "AWS-AWSManagedRulesKnownBadInputsRuleSet",
                                                            },
                                                            "name": "AWS-AWSManagedRulesKnownBadInputsRuleSet",
                                                            "statement": {
                                                                "managedRuleGroupStatement": {
                                                                    "vendorName": "AWS",
                                                                    "name": "AWSManagedRulesKnownBadInputsRuleSet",
                                                                },
                                                            },
                                                        },
                                                        {
                                                            "priority": 5,
                                                            "overrideAction": {"none": {}},
                                                            "visibilityConfig": {
                                                                "sampledRequestsEnabled": True,
                                                                "cloudWatchMetricsEnabled": True,
                                                                "metricName": "AWS-AWSManagedRulesSQLiRuleSet",
                                                            },
                                                            "name": "AWS-AWSManagedRulesSQLiRuleSet",
                                                            "statement": {
                                                                "managedRuleGroupStatement": {
                                                                    "vendorName": "AWS",
                                                                    "name": "AWSManagedRulesSQLiRuleSet",
                                                                },
                                                            },
                                                        },

                                                    ]
                                                    )
        
        # cdk_nag.NagSuppressions.add_stack_suppressions(stack=self, suppressions=[
        #     {"id": "AwsSolutions-CFR4", "reason": "Demo : Distributions that use the default CloudFront viewer certificate are non-compliant with this rule"},
        #     {"id": "AwsSolutions-CFR5", "reason": "Demo : Use of default CloudFront viewer certificate"},
        #     {"id": "AwsSolutions-CFR1", "reason": "Demo : No need of Geo restrictions"},
        # ])
        # Aspects.of(self).add(cdk_nag.AwsSolutionsChecks())

    @property
    def consumers_web_acl_arn(self):
        """return the arn of the acl"""
        return self.web_acl_for_consumers.attr_arn

    @property
    def publishers_web_acl_arn(self):
        """return the arn of the acl"""
        return self.web_acl_for_publishers.attr_arn
