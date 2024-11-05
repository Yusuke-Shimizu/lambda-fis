import json
import os
import uuid
import boto3
from datetime import datetime
from typing import Dict, Any

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('TABLE_NAME', 'FisTable'))

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    http_method = event['httpMethod']
    
    if http_method == 'GET':
        # GETリクエスト（全アイテム取得）
        response = table.scan()
        items = response.get('Items', [])
        
        return {
            'statusCode': 200,
            'body': json.dumps(items, ensure_ascii=False)
        }
        
    elif http_method == 'POST':
        # POSTリクエスト（新規アイテム作成）
        try:
            body = json.loads(event['body'])
            item = {
                'id': str(uuid.uuid4()),
                'data': body,
                'createdAt': datetime.now().isoformat()
            }
            
            table.put_item(Item=item)
            
            return {
                'statusCode': 201,
                'body': json.dumps(item, ensure_ascii=False)
            }
            
        except Exception as e:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': str(e)
                }, ensure_ascii=False)
            }
    
    return {
        'statusCode': 405,
        'body': json.dumps({
            'error': 'Method not allowed'
        }, ensure_ascii=False)
    }