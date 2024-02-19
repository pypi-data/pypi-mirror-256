def integration_test(api_key):
    from objective import Client

    client = Client(api_key=api_key)
    
    print("Clearing the object store")
    client.object_store.delete_objects(client.object_store.list_all_objects())

    objects = []
    print("Creating an object without an ID:")
    objects.append(
        {
            "title": "Sevendayz Men's Shady Records Eminem Hoodie Hoody Black Medium",
            "brand": "sevendayz",
            "imageURLHighRes": [
                "https://images-na.ssl-images-amazon.com/images/I/41gMYeiNASL.jpg"
            ],
        },
    )
    
    print("Upserting it...")
    client.object_store.upsert_objects(objects)
    
    print("Creating an object with an ID:")
    objects = []
    from objective import Object
    objects.append(
        Object(
        id="1",
        object={
            "title": "Sevendayz Men's Shady Records Eminem Hoodie Hoody Black Medium",
            "brand": "sevendayz",
            "imageURLHighRes": [
                "https://images-na.ssl-images-amazon.com/images/I/41gMYeiNASL.jpg"
            ],
        },
    ))
    print("Upserting it...")
    client.object_store.upsert_objects(objects)
    
    print("Checking object store size:")
    print("Object store size:", client.object_store.size())
    
    print("Creating an index:")
    index = client.indexes.create_index(
        template_name="text-neural-base", fields={"searchable": ["title", "brand"]}
    )
    import time
    time.sleep(15)
    
    print("Sleeping for 15s, then waiting for indexing to complete.")
    index.status(watch=True)
    
    print("Listing all indexes")
    assert len(client.indexes.list_indexes()) > 0
    
    print("Performing a search")
    assert len(index.search("test")["results"]) > 0

    print("Delete the index")
    index.delete()


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Plain API key.')
    parser.add_argument('api_key', type=str, help='API key for the application')

    args = parser.parse_args()
    api_key = args.api_key

    integration_test(api_key)

if __name__ == "__main__":
    main()