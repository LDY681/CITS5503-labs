import boto3

def create_db_table():
    # initialize dynamodb service instance
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8001")
        
    table = dynamodb.create_table(
        TableName='CloudFiles',
        KeySchema=[
            {
                'AttributeName': 'userId',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'fileName',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'userId',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'fileName',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

    print("Table status:", table.table_status)


if __name__ == '__main__':
    create_db_table()