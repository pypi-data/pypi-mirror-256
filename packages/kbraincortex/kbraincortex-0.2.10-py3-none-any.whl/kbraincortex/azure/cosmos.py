from azure.cosmos import CosmosClient, PartitionKey
from kbraincortex.common.configuration import COSMOS_CONNECTION_STRING
def query_cosmos_db(query, database_name, container_name, connection_string = COSMOS_CONNECTION_STRING, continuation_token = None, max_item_count = 1000):
    # Create a new Cosmos client
    client = CosmosClient.from_connection_string(connection_string)

    # Get a Cosmos database
    database = client.get_database_client(database_name)

    # Get a Cosmos container
    container = database.get_container_client(container_name)

    # Query the container
    result_iterable = container.query_items(
        query,
        enable_cross_partition_query=True,
        max_item_count=max_item_count
    )

    results = []
    for result_page in result_iterable.by_page(continuation_token):
        for item in result_page:
            results.append(item)
            if len(results) >= max_item_count:
                break
        if len(results) >= max_item_count:
            break
        else:
            # Get the continuation token from the headers
            continuation_token = result_iterable.headers.get('x-ms-continuation')

    return results, continuation_token

def insert_records_into_container(database_name, container_name, items_to_add, connection_string=COSMOS_CONNECTION_STRING):
    client = create_cosmos_client(connection_string)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)

    for item in items_to_add:
        container.upsert_item(body=item)

def create_cosmos_client(connection_string=COSMOS_CONNECTION_STRING):
    client = CosmosClient.from_connection_string(connection_string)
    return client

def create_container(client, database_name, container_name, partition_key="/account_id"):
    database = client.create_database_if_not_exists(id=database_name)
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path=partition_key),
    )
    return container

def create_cosmos_container(connection_string, database_name, container_name, partition_key):
    client = create_cosmos_client(connection_string)
    container = create_container(client, database_name, container_name, partition_key)
    return container
