from aws_cdk import (
    Stack,
    aws_lambda_python_alpha as lambda_python,
    aws_apigateway as apigw,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
)
from constructs import Construct

class LambdaFisStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDBテーブル
        table = dynamodb.Table(
            self, 'FisTable',
            partition_key={'name': 'id', 'type': dynamodb.AttributeType.STRING},
        )

        # Lambda関数
        handler = lambda_python.PythonFunction(
            self, 'FisHandler',
            entry='lambda',
            runtime=_lambda.Runtime.PYTHON_3_9,
        )

        # DynamoDBへのアクセス権限をLambdaに付与
        table.grant_read_write_data(handler)

        # API Gateway
        api = apigw.RestApi(self, 'FisApi')
        integration = apigw.LambdaIntegration(handler)
        api.root.add_method('GET', integration)
        api.root.add_method('POST', integration)
