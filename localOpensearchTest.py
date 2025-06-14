from opensearchpy import OpenSearch
import sys 

# Set up connection
client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
    http_auth=('admin', 'Test@123'),
    use_ssl=True,
    verify_certs=False
)

# Check if connection works
try:
    info = client.info()
    print("Connected to:", info['cluster_name'])
except Exception as e:
    print(f"Could not connect to OpenSearch: {e}")
    sys.exit(1) 

# --- New functionality: List all available indexes ---
print("\n--- Available OpenSearch Indexes ---")
try:
    # Use get_alias to list all indices. Using "*" as a wildcard to get all.
    # The response is a dictionary where keys are index names.
    all_indices = client.indices.get_alias("*")
    if all_indices:
        for index_name in all_indices.keys():
            print(f"- {index_name}")
    else:
        print("No indexes found.")
except Exception as e:
    print(f"Error fetching index list: {e}")
    # Continue execution even if listing fails, as user might still want to create a new one.


# --- Ask to create a new index with dummy data ---
print("\n--- Create New Index ---")
user_create_input = input("Do you want to create a new index? (yes/no): ").lower().strip()

if user_create_input == 'yes':
    new_index_name = input("Enter the name for the new index: ").lower().strip()

    if not new_index_name:
        print("No index name provided. Exiting.")
        sys.exit(0)

    if client.indices.exists(new_index_name):
        print(f"Index '{new_index_name}' already exists. No new index will be created.")
    else:
        try:
            print(f"Attempting to create index '{new_index_name}'...")
            response = client.indices.create(new_index_name)
            print(f"Index created: {response}")

            # Add dummy data to the newly created index
            print(f"Adding dummy data to '{new_index_name}'...")
            dummy_doc1 = {'item': 'Laptop', 'brand': 'XYZ', 'price': 1200, 'in_stock': True}
            dummy_doc2 = {'item': 'Mouse', 'brand': 'ABC', 'price': 25, 'in_stock': False}
            dummy_doc3 = {'item': 'Keyboard', 'brand': 'PQR', 'price': 75, 'in_stock': True}

            client.index(index=new_index_name, id='dummy_1', body=dummy_doc1, refresh=True)
            client.index(index=new_index_name, id='dummy_2', body=dummy_doc2, refresh=True)
            client.index(index=new_index_name, id='dummy_3', body=dummy_doc3, refresh=True)
            print(f"Dummy data added to '{new_index_name}'.")

            # Optionally, fetch and display the dummy data from the new index
            print(f"\nFetching dummy data from '{new_index_name}':")
            fetch_query = {
                'query': {
                    'match_all': {}
                }
            }
            fetch_response = client.search(index=new_index_name, body=fetch_query)
            if fetch_response['hits']['hits']:
                for hit in fetch_response['hits']['hits']:
                    print(f"  ID: {hit['_id']}, Source: {hit['_source']}")
            else:
                print("No documents found in the new index.")

        except Exception as e:
            print(f"Error creating or adding data to index '{new_index_name}': {e}")
            sys.exit(1)
else:
    print("No new index will be created. Exiting.")

sys.exit(0) 
