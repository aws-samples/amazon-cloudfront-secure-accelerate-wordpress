import aws_cdk as core
import aws_cdk.assertions as assertions

from worpress_cloudfront.worpress_cloudfront_stack import WorpressCloudfrontStack

# example tests. To run these tests, uncomment this file along with the example
# resource in worpress_cloudfront/worpress_cloudfront_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = WorpressCloudfrontStack(app, "worpress-cloudfront")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
