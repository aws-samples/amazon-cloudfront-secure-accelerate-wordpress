from aws_cdk import (
    aws_cloudfront as cf,
    aws_s3 as s3,
    aws_cloudfront_origins as origins,
    aws_route53 as r53,
    Stack,
    CfnOutput,
    RemovalPolicy,
    Aspects
    
)
from constructs import Construct
import cdk_nag


# TODO 
# Param to access the backend or HTTP or HTTPS 
# If ZoneID and ZoneName not provided - do not create DNS nor certificate

class WordpressCloudfrontStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, Certificate, web_acl_for_consumers, web_acl_for_publishers, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        WordpressOriginURL = self.node.try_get_context("WordpressOriginURL")
        WordpressOriginIsHTTPS = self.node.try_get_context("WordpressOriginIsHTTPS")
        WordpressDomainConsumers = self.node.try_get_context("WordpressDomainConsumers")
        WordpressDomainPublishers = self.node.try_get_context("WordpressDomainPublishers")
        HostedZoneId = self.node.try_get_context("HostedZoneId")
        HostedZoneName = self.node.try_get_context("HostedZoneName")
        
        if WordpressOriginIsHTTPS == None:
            WordpressOriginIsHTTPS = "false"
            
        if WordpressOriginURL == None:
            WordpressOriginURL = ""
            
        if WordpressDomainConsumers == None:
            WordpressDomainConsumers = ""
        
        if WordpressDomainPublishers == None:
            WordpressDomainPublishers = ""
            
        #Create S3 Bucket for CloudFront logs
        S3_Bucket_CloudFront_logs =s3.Bucket(self, 
                                             "CloudFrontLogs", 
                                             removal_policy= RemovalPolicy.DESTROY,
                                             auto_delete_objects=True,
                                             access_control=s3.BucketAccessControl.LOG_DELIVERY_WRITE,
                                             encryption=s3.BucketEncryption.S3_MANAGED,
                                             block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                                             object_ownership=s3.ObjectOwnership.OBJECT_WRITER,
                                             public_read_access=False,
                                             server_access_logs_prefix='CloudFrontLogs/serverAccessLogging_',
                                             enforce_ssl = True
    
                                             )
        
        # Create cache policy for static content
        static_cache_policy = cf.CachePolicy(self, "static_cache_policy",
                                                        cache_policy_name="static_cache_policy",
                                                        comment="Policy for static content",
                                                        # default_ttl=Duration.days(2),
                                                        # min_ttl=Duration.minutes(1),
                                                        # max_ttl=Duration.days(10),
                                                        header_behavior=cf.CacheHeaderBehavior.none(),
                                                        cookie_behavior=cf.CacheCookieBehavior.none(),
                                                        query_string_behavior=cf.CacheQueryStringBehavior.all(),
                                                        enable_accept_encoding_gzip=True,
                                                        enable_accept_encoding_brotli=True
                                                        )

        # Create cache policy for dynamic admin content
        dynamic_cache_policy = cf.CachePolicy(self, "dynamic_cache_policy",
                                                 cache_policy_name="dynamic_cache_policy",
                                                 comment="Policy for dynamic content (admin)",
                                                 # default_ttl=Duration.days(2),
                                                 # min_ttl=Duration.minutes(1),
                                                 # max_ttl=Duration.days(10),
                                                 header_behavior=cf.CacheHeaderBehavior.allow_list("Accept", "Accept-Charset", "Accept-Datetime", "Accept-Language", "Authorization", "Host", "Origin",
                                                                                                   "Referer", "Access-Control-Request-Method", "Access-Control-Request-Headers"),  # "Accept-Encoding" - nb max header = 10 / no possibility to do .all()
                                                 cookie_behavior=cf.CacheCookieBehavior.all(),
                                                 query_string_behavior=cf.CacheQueryStringBehavior.all(),
                                                 enable_accept_encoding_gzip=True,
                                                 enable_accept_encoding_brotli=True
                                                 )

        
        # Create cache policy for dynamic frontend content
        dynamic_frontent_cache_policy = cf.CachePolicy(self, "dynamic_frontent_cache_policy",
                                              cache_policy_name="dynamic_frontent_cache_policy",
                                              comment="Policy for dynamic content(front end)",
                                              # default_ttl=Duration.days(2),
                                              # min_ttl=Duration.minutes(1),
                                              # max_ttl=Duration.days(10),
                                              header_behavior=cf.CacheHeaderBehavior.allow_list(
                                                  "Host", "CloudFront-Is-Mobile-Viewer", "CloudFront-Is-Desktop-Viewer", "CloudFront-Is-Tablet-Viewer", "CloudFront-Forwarded-Proto"),
                                              cookie_behavior=cf.CacheCookieBehavior.allow_list(
                                                  "comment_*", "wordpress_*", "wp-settings-*"),
                                              query_string_behavior=cf.CacheQueryStringBehavior.all(),
                                              enable_accept_encoding_gzip=True,
                                              enable_accept_encoding_brotli=True
                                              )

        # Create CloudFront function to redirect publishers to login page if not logged
        cff_redirect_auth = cf.Function(self, "cff_redirect_auth",code=cf.FunctionCode.from_file(file_path="wordpress_cloudfront/cff_redirect_auth.js"))
        
        # Initialize Origin 
        originProtocolPolicy = cf.OriginProtocolPolicy.HTTPS_ONLY
        if WordpressOriginIsHTTPS.lower() == "false" : 
            originProtocolPolicy = cf.OriginProtocolPolicy.HTTP_ONLY
        origin = origins.HttpOrigin(WordpressOriginURL, protocol_policy= originProtocolPolicy)


        # Create distribution for viewers/consumers
        consumersDomain = None
        certificate = None
        if WordpressDomainConsumers != None and HostedZoneName != None: 
            consumersDomain = []
            consumersDomain.append(WordpressDomainConsumers + "." + HostedZoneName)
            certificate = Certificate
        
        print(consumersDomain)

        wordpress_consumers_dist = cf.Distribution(self,
                                         "CloudFront-Wordpress-Consumers",
                                         default_behavior=cf.BehaviorOptions(origin=origin,
                                                                             allowed_methods=cf.AllowedMethods.ALLOW_ALL,
                                                                             viewer_protocol_policy=cf.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                                                                             cache_policy=dynamic_frontent_cache_policy,
                                                                             response_headers_policy = cf.ResponseHeadersPolicy.SECURITY_HEADERS,
                                                                             compress=True),
                                                                             
                                         additional_behaviors={
                                             "wp-content/*": cf.BehaviorOptions(
                                                 origin=origin,
                                                 allowed_methods=cf.AllowedMethods.ALLOW_GET_HEAD,
                                                 viewer_protocol_policy=cf.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                                                 response_headers_policy = cf.ResponseHeadersPolicy.SECURITY_HEADERS,
                                                 cache_policy=static_cache_policy,
                                                 compress=True,
                                                 
                                             ),
                                             "wp-includes/*": cf.BehaviorOptions(
                                                 origin=origin,
                                                 allowed_methods=cf.AllowedMethods.ALLOW_GET_HEAD,
                                                 viewer_protocol_policy=cf.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                                                 response_headers_policy = cf.ResponseHeadersPolicy.SECURITY_HEADERS,
                                                 cache_policy=static_cache_policy,
                                                 compress=True,
                                                 
                                             ),
                                             "wp-admin/*": cf.BehaviorOptions(
                                                 origin=origin,
                                                 allowed_methods=cf.AllowedMethods.ALLOW_ALL,
                                                 viewer_protocol_policy=cf.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                                                 response_headers_policy = cf.ResponseHeadersPolicy.SECURITY_HEADERS,
                                                 cache_policy=dynamic_cache_policy,
                                                 compress=True,
                                                 
                                             ),
                                             "wp-login.php": cf.BehaviorOptions(
                                                 origin=origin,
                                                 allowed_methods=cf.AllowedMethods.ALLOW_ALL,
                                                 viewer_protocol_policy=cf.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                                                 response_headers_policy = cf.ResponseHeadersPolicy.SECURITY_HEADERS,
                                                 cache_policy=dynamic_cache_policy,
                                                 compress=True,
                                                 
                                             ),
                                         },
                                         domain_names=consumersDomain,
                                         certificate=certificate,
                                         minimum_protocol_version=cf.SecurityPolicyProtocol.TLS_V1_2_2021,
                                         ssl_support_method=cf.SSLMethod.SNI,
                                         enable_logging=True,  # Optional, this is implied if logBucket is specified
                                         log_bucket=S3_Bucket_CloudFront_logs,
                                         log_file_prefix="consumers-distribution-access-logs/",
                                         log_includes_cookies=True,
                                         web_acl_id=web_acl_for_consumers,
                                         )
       
        # Create distribution for publishers/admins
        publishersDomain = None
        certificate = None
        if WordpressDomainPublishers != None and HostedZoneName != None: 
            publishersDomain = []
            publishersDomain.append(WordpressDomainPublishers + "." + HostedZoneName)
            certificate = Certificate
        
        print(publishersDomain)
        
        wordpress_publishers_dist = cf.Distribution(self,
                                         "CloudFront-Wordpress-Publishers",
                                         default_behavior=cf.BehaviorOptions(origin=origin,
                                                                             allowed_methods=cf.AllowedMethods.ALLOW_ALL,
                                                                             viewer_protocol_policy=cf.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                                                                             response_headers_policy = cf.ResponseHeadersPolicy.SECURITY_HEADERS,
                                                                             cache_policy=dynamic_frontent_cache_policy,
                                                                             compress=True,),
                                         additional_behaviors={
                                             "wp-content/*": cf.BehaviorOptions(
                                                 origin=origin,
                                                 allowed_methods=cf.AllowedMethods.ALLOW_GET_HEAD,
                                                 viewer_protocol_policy=cf.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                                                 response_headers_policy = cf.ResponseHeadersPolicy.SECURITY_HEADERS,
                                                 cache_policy=static_cache_policy,
                                                 compress=True,
                                             ),
                                             "wp-includes/*": cf.BehaviorOptions(
                                                 origin=origin,
                                                 allowed_methods=cf.AllowedMethods.ALLOW_GET_HEAD,
                                                 viewer_protocol_policy=cf.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                                                 response_headers_policy = cf.ResponseHeadersPolicy.SECURITY_HEADERS,
                                                 cache_policy=static_cache_policy,
                                                 compress=True,
                                             ),
                                             "wp-admin/*": cf.BehaviorOptions(
                                                 origin=origin,
                                                 allowed_methods=cf.AllowedMethods.ALLOW_ALL,
                                                 viewer_protocol_policy=cf.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                                                 response_headers_policy = cf.ResponseHeadersPolicy.SECURITY_HEADERS,
                                                 cache_policy=dynamic_cache_policy,
                                                 compress=True,
                                                 function_associations=[cf.FunctionAssociation(event_type=cf.FunctionEventType.VIEWER_REQUEST, function=cff_redirect_auth)],
                                                
                                             ),
                                             "wp-login.php": cf.BehaviorOptions(
                                                 origin=origin,
                                                 allowed_methods=cf.AllowedMethods.ALLOW_ALL,
                                                 viewer_protocol_policy=cf.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                                                 response_headers_policy = cf.ResponseHeadersPolicy.SECURITY_HEADERS,
                                                 cache_policy=dynamic_cache_policy,
                                                 compress=True,
                                             ),
                                         },
                                         domain_names=publishersDomain,
                                         certificate=certificate,
                                         minimum_protocol_version=cf.SecurityPolicyProtocol.TLS_V1_2_2021,
                                         ssl_support_method=cf.SSLMethod.SNI,
                                         enable_logging=True,  # Optional, this is implied if logBucket is specified
                                         log_bucket=S3_Bucket_CloudFront_logs,
                                         log_file_prefix="publishers-distribution-access-logs/",
                                         log_includes_cookies=True,
                                         web_acl_id=web_acl_for_publishers,
                                         
                                         
                                         )
        
        # Create CNAME for both distibutions
        if HostedZoneId != None and HostedZoneName != None and WordpressDomainConsumers != None and WordpressDomainPublishers != None: 
            hosted_zone = r53.HostedZone.from_hosted_zone_attributes(self, "Hosted_Zone", hosted_zone_id=HostedZoneId, zone_name=HostedZoneName)
            
            
            if WordpressDomainConsumers != None:  
                consumersCname = r53.CnameRecord(self, "CnameConsumerDistribution",
                    record_name=WordpressDomainConsumers,
                    zone=hosted_zone,
                    domain_name=wordpress_consumers_dist.distribution_domain_name
                )
                CfnOutput(self, "Consumers URL",
                        value="https://" + consumersCname.domain_name)
            
            if WordpressDomainPublishers != None: 
                publishersCname = r53.CnameRecord(self, "CnamePublishDistribution",
                    record_name=WordpressDomainPublishers,
                    zone=hosted_zone,
                    domain_name=wordpress_publishers_dist.distribution_domain_name
                )
            
                # Outputs of the stack
                CfnOutput(self, "Publishers URL",
                        value="https://" + publishersCname.domain_name)
        else : 
            # Outputs of the stack
            CfnOutput(self, "Consumers URL",
                    value="https://" + wordpress_consumers_dist.distribution_domain_name)
            CfnOutput(self, "Publishers URL",
                        value="https://" + wordpress_publishers_dist.distribution_domain_name)
        
        # Suppress rules 
        # https://github.com/cdklabs/cdk-nag/blob/main/RULES.md
        
        
        # cdk_nag.NagSuppressions.add_stack_suppressions(stack=self, suppressions=[
        #     # {"id": "AwsSolutions-CFR4", "reason": "Demo : Distributions that use the default CloudFront viewer certificate are non-compliant with this rule"},
        #     # {"id": "AwsSolutions-CFR5", "reason": "Demo : Use of default CloudFront viewer certificate"},
        #     {"id": "AwsSolutions-CFR1", "reason": "Demo : No need of Geo restrictions"},
        # ])
        # Aspects.of(self).add(cdk_nag.AwsSolutionsChecks())