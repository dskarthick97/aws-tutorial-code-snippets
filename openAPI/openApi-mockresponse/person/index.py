import json

from person import Person

def lambda_handler(event, context):
    
    print(f'Event object: {event}')
    print(f'Context object: {context}')
    
    batman = Person('Bruce', 'Wayne')
    identity = batman.get_identity()

    return {
        'statusCode': 200,
        'body': json.dumps(identity),
        'headers': {
            'Content-Type': 'appication/json'
        }
    }
