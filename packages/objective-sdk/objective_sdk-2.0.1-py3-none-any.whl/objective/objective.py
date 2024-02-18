# TODO(chandler): Use ruff.

from concurrent.futures import ThreadPoolExecutor
import datetime
from typing import Dict, Generator, List, Optional, Any
from dataclasses import dataclass, field
import requests
import os
import time

__all__ = [
    "ObjectStore",
    "Error",
    "Index",
    "Object",
    "ObjectiveClient",
    "ListObjectsResponse",
    "Pagination",
]


class Error(Exception):
    """Base class for all of this module's exceptions."""


class RequestError(Error, requests.RequestException):
    """An HTTP request failed."""


class EnvironmentError(Error, ValueError):
    """Environment variables are unset or invalid."""


CPU_COUNT = os.cpu_count() if os.cpu_count() is not None else 6

API_BASE_URL = os.getenv("OBJECTIVE_API")
if not API_BASE_URL:
    API_BASE_URL = "https://api.objective.inc/v1/"
else:
    API_BASE_URL = API_BASE_URL.strip('"')


def _preprocess_fields(fields):
    """Helper method to convert index field creations into
    API format."""
    for field in fields.keys():
        if field in [
            "searchable",
            "crawlable",
            "filterable",
        ] and isinstance(fields[field], list):
            fields[field] = {"allow": fields[field]}
    return fields


class ObjectiveClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.http_session = requests.Session()

    def request(
        self,
        method: str,
        endpoint: str = API_BASE_URL,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Issue a request to the Objective API

        Returns the JSON from the request."""
        url = API_BASE_URL + endpoint

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "objective-py/1.0.0",
        }

        MAX_RETRIES = 3
        BACKOFF_FACTOR = 1.5
        for attempt in range(MAX_RETRIES):
            try:
                if method == "GET":
                    response = self.http_session.get(
                        url,
                        headers=headers,
                        params=data,
                    )
                else:
                    response = self.http_session.request(
                        method, url, headers=headers, json=data
                    )
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                if (
                    response.status_code >= 400
                    and response.status_code <= 499
                    and response.status_code != 429
                ):
                    raise (e)

                if attempt < MAX_RETRIES - 1:  # i.e. if it's not the last attempt
                    sleep_time = BACKOFF_FACTOR * (2**attempt)
                    time.sleep(sleep_time)
                    continue
                else:
                    raise (e)

    def list_indexes(self, limit=None, cursor=None) -> List["Index"]:
        data = {}
        if limit:
            data["limit"] = limit
        if cursor:
            data["cursor"] = cursor
        return [
            Index(
                objective_client=self,
                index_id=index["id"],
                created_at=index.get("created_at"),
                updated_at=index.get("updated_at"),
            )
            for index in self.request("GET", "indexes", data=data).get("indexes", [])
        ]

    @property
    def object_store(self):
        return ObjectStore(client=self)

    def create_index(self, template_name, fields, version: str = None):
        index_create = self.request(
            "POST",
            "indexes",
            data={
                "configuration": {
                    "template": {
                        **{"name": template_name},
                        **({"version": version} if version else {}),
                    },
                    "fields": _preprocess_fields(fields),
                }
            },
        )
        if not index_create:
            raise ValueError("Failed to create index!")
        else:
            return Index(
                self,
                index_create["id"],
                created_at=index_create.get("created_at"),
                updated_at=index_create.get("updated_at"),
            )

    def get_index(self, id) -> "Index":
        return Index(self, id)


@dataclass
class Pagination:
    next: Optional[str] = None
    prev: Optional[str] = None


@dataclass
class Object:
    id: Optional[str] = None
    date_created: Optional[str] = None
    date_updated: Optional[str] = None
    object: Optional[Dict] = None
    status: Optional[Dict] = None

    _ops_status: Optional[Any] = (
        None  # Internal field for storing local statuses of operations
    )
    _field_patches: List[Dict] = field(default_factory=list)
    _field_deletes: List[Dict] = field(default_factory=list)

    def is_newer_than(self, date):
        if date is None or self.date_updated is None:
            return True
        else:
            return datetime.datetime.strptime(
                date, "%Y-%m-%dT%H:%M:%S.%fZ"
            ) >= datetime.datetime.strptime(self.date_updated, "%Y-%m-%dT%H:%M:%S.%fZ")

    def __getitem__(self, key):
        return self.object.get(key)

    def __setitem__(self, key, value):
        if self.object.get(key) != value:
            self._field_patches.append({key: value})
        self.object[key] = value

    def __delitem__(self, key):
        if key in self.object:
            self._field_deletes.append(key)
            del self.object[key]


@dataclass
class ListObjectsResponse:
    objects: List[Object]
    pagination: Pagination


@dataclass
class BatchOperation:
    success: List[Object]
    failures: List[Object]


class ObjectStore:
    def __init__(self, client):
        self.objective_client = client

    def __len__(self):
        return self.size()

    def size(self) -> int:
        count = self.count()
        if count and count.get("count"):
            return count["count"]
        else:
            return 0

    def count(self):
        """Make a call to GET /objects/count"""
        return self.objective_client.request("GET", "objects/count")

    def list_objects(
        self,
        limit: Optional[int] = 10,
        cursor: Optional[str] = None,
        include_object: Optional[bool] = False,
    ) -> ListObjectsResponse:
        """Get Objects from the Object Store. Calls GET /objects.

        Returns the API response from GET /objects
        """
        params = {}
        if cursor:
            params["cursor"] = cursor

        if limit:
            params["limit"] = limit

        if include_object:
            params["include_object"] = include_object

        resp = self.objective_client.request("GET", "objects", data=params)
        return ListObjectsResponse(
            objects=[Object(**obj) for obj in resp.get("objects", [])],
            pagination=Pagination(**resp.get("pagination", {})),
        )

    def get_objects(
        self,
        limit: Optional[int] = 10,
        cursor: Optional[str] = None,
    ) -> ListObjectsResponse:
        return self.list_objects(limit=limit, cursor=cursor, include_object=True)

    def list_all_objects(
        self,
        include_object: Optional[bool] = False,
    ) -> Generator[Object, None, None]:
        """List all objects in the object store. Optionally stop at a specified limit.

        Returns a generator that producing objects"""
        cursor = None

        while True:
            list_objects_response = self.list_objects(
                limit=512, cursor=cursor, include_object=include_object
            )
            cursor = list_objects_response.pagination.next

            for obj in list_objects_response.objects:
                yield obj

            if not cursor:
                break

    def get_all_objects(self) -> Generator[Object, None, None]:
        return self.list_all_objects(include_object=True)

    def get_objects_by_id(self, ids: List[str]) -> List[Object]:
        with ThreadPoolExecutor(max_workers=CPU_COUNT * 12) as executor:
            return list(executor.map(self.get_object, ids))

    def get_object(self, id: str) -> Object:
        return Object(**self.objective_client.request("GET", f"objects/{id}"))

    def upsert_objects(self, objects: List[Object]) -> BatchOperation:
        def upsert_object(object):
            try:
                return self.upsert_object(object)
            except Error as e:
                object._ops_status = {"state": "error", "exception": e}
                return object

        with ThreadPoolExecutor(max_workers=CPU_COUNT * 12) as executor:
            success = []
            failures = []

            for obj in executor.map(upsert_object, objects):
                if obj._ops_status.get("state") == "OK":
                    success.append(obj)
                else:
                    failures.append(obj)

            return BatchOperation(
                success=success,
                failures=failures,
            )

    def delete_objects(self, objects: List[Object]):
        def delete_object(object):
            try:
                return self.delete_object(object)
            except Error as e:
                object._ops_status = {"state": "error", "exception": e}
                return object

        with ThreadPoolExecutor(max_workers=CPU_COUNT * 12) as executor:
            success = []
            failures = []

            for obj in executor.map(delete_object, objects):
                if obj._ops_status.get("state") == "OK":
                    success.append(obj)
                else:
                    failures.append(obj)

            return BatchOperation(
                success=success,
                failures=failures,
            )

    def upsert(self, object: Dict, id: Optional[str] = None):
        self.upsert_object(Object(id=id, object=object))

    def upsert_object(self, object):
        if (
            object.id
            and len(object._field_patches) > 0
            and len(object._field_deletes) == 0
        ):
            final_patch = {}
            for field_patch in object._field_patches:
                final_patch.update(field_patch)

            obj_response = self.objective_client.request(
                "PATCH",
                f"objects/{object.id}",
                data=final_patch,
            )
        elif object.id:
            obj_response = self.objective_client.request(
                "PUT",
                f"objects/{object.id}",
                data=object.object,
            )
            object.id = obj_response["id"]
        else:
            obj_response = self.objective_client.request(
                "POST", "objects", data=object.object
            )
            object.id = obj_response["id"]

        if not object._ops_status:
            object._ops_status = {}

        object._ops_status["state"] = "OK"
        return object

    def delete_object(self, object):
        obj_response = self.objective_client.request("DELETE", f"objects/{object.id}")
        if not object._ops_status:
            object._ops_status = {}
        object._ops_status["state"] = "OK"
        return object


@dataclass
class Index:
    objective_client: ObjectiveClient
    index_id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def update(self, new_fields):
        raise NotImplementedError
        # return self.objective_client.request(
        #     "PUT", f"indexes/{self.index_id}", data=new_fields
        # )

    def delete(self):
        return self.objective_client.request("DELETE", f"indexes/{self.index_id}")

    def status(self, status_type: Optional[str] = None):
        if status_type and status_type.lower() not in [
            "pending",
            "processing",
            "processed",
            "live",
            "error",
        ]:
            raise ValueError(
                "Invalid status type. Must be one of: pending, processing, processed, live, error."
            )
        obj_status = self.objective_client.request(
            "GET",
            f"indexes/{self.index_id}/status{f'/{status_type.lower()}'if status_type else ''}",
        )
        return obj_status.get("status")

    def search(
        self,
        query: str,
        filter_query: Optional[str] = None,
        object_fields: Optional[str] = None,
    ):
        params = {"query": query}

        if filter_query is not None:
            params["filter_query"] = filter_query
        if object_fields is not None:
            params["object_fields"] = object_fields

        return self.objective_client.request(
            "GET", f"indexes/{self.index_id}/search", data=params
        )
