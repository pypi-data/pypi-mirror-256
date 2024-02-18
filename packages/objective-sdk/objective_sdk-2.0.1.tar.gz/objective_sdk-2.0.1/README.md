# Objective, Inc. Python Library

This is the official python library for the Objective APIs. It provides convenient methods for using Objective's APIs. 

## Documentation

Our documentation can be found at https://objective.inc/docs.

## Installation

```bash
pip install objective-sdk
```

## Usage

To get an API key, create an account at https://app.objective.inc.

### Add your objects to the object store
```python
from objective import ObjectiveClient
import os

OBJECTIVE_API_KEY = os.environ.get("OBJECTIVE_API_KEY")

client = ObjectiveClient(OBJECTIVE_API_KEY)

# Add an object to the object store
client.object_store.upsert(
    id="1",
    object={
        "title": "Sevendayz Men's Shady Records Eminem Hoodie Hoody Black Medium",
        "brand": "sevendayz",
        "imageURLHighRes": [
            "https://images-na.ssl-images-amazon.com/images/I/41gMYeiNASL.jpg"
        ],
    },
)
```

### Create an index
```python
index = client.create_index(
    template_name="text-neural-base", fields={"searchable": ["title", "brand"]}
)
```

### Check indexing status
```python
index.status()
```
```json
{"PENDING": 0, "PROCESSING": 1, "PROCESSED": 0, "LIVE": 0, "ERROR": 0}
```

### Search
```python
index.search(query="rapper hoodies", object_fields="*")
```
```json
{
    "results": [
        {
            "id": 1,
            "object": {"title": "Sevendayz Men's Shady Records Eminem Hoodie Hoody Black Medium", "brand": "sevendayz", "imageURLHighRes": ["https://images-na.ssl-images-amazon.com/images/I/41gMYeiNASL.jpg"]}
        }
    ],
    "pagination": {
        "pages": 1,
        "page": 1,
        "next": null
    }
}
```



## Development

Use python build to build this package:

```python
python -m pip install --upgrade pip

# Install dependencies
pip install .

# Build package:
pip install build
python -m build
````
