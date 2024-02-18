import pytest
from unittest.mock import patch

from objective import ObjectiveClient, ListObjectsResponse, Object, Pagination


@pytest.mark.parametrize(
    "params,expected",
    [
        ({}, {"limit": 10}),
        ({"limit": 10}, {"limit": 10}),
        ({"cursor": "abc"}, {"cursor": "abc", "limit": 10}),
        ({"include_object": True}, {"include_object": True, "limit": 10}),
    ],
)
def test_list_objects(params, expected):
    with patch(
        "objective.ObjectiveClient.request",
        return_value={"objects": [], "pagination": {"next": None, "prev": None}},
    ) as mock_get:
        client = ObjectiveClient(api_key="test_key")
        store = client.object_store
        store.list_objects(**params)

        mock_get.assert_called_with("GET", "objects", data=expected)


@pytest.mark.parametrize(
    "params,expected",
    [
        ({}, {"limit": 512, "cursor": "abc", "include_object": False}),
        (
            {"include_object": True},
            {"limit": 512, "cursor": "abc", "include_object": True},
        ),
    ],
)
def test_list_all_objects(params, expected):
    # By passing these to side_effect, we will update the output of
    # get_objects to create the desired pagination to test that
    # get_all_objects paginates through results correctly.
    results = [
        ListObjectsResponse(
            objects=[Object()],
            pagination=Pagination(**{"next": "abc", "prev": None}),
        ),
        ListObjectsResponse(
            objects=[Object(id="1"), Object(id="2")],
            pagination=Pagination(**{"next": None, "prev": "abc"}),
        ),
    ]
    with patch(
        "objective.ObjectStore.list_objects", side_effect=results
    ) as mock_get_objects:
        client = ObjectiveClient(api_key="test_key")
        list(
            client.object_store.list_all_objects(**params)
        )  # returns a generator, invoke to trigger test

        mock_get_objects.assert_called_with(**expected)


@pytest.mark.parametrize(
    "ret_val",
    [
        {"objects": [], "pagination": {"next": None, "prev": None}},
        {
            "objects": [
                {
                    "id": "123",
                    "object": {"test": "test"},
                    "date_updated": "123",
                    "date_created": "123",
                }
            ],
            "pagination": {"next": "123", "prev": "123"},
        },
    ],
)
def test_get_objects_response_type(ret_val):
    """Test that the response type is correctly parsed as a ListObjectsResponse"""
    with patch("objective.ObjectiveClient.request", return_value=ret_val):
        client = ObjectiveClient(api_key="test_key")
        store = client.object_store
        resp = store.get_objects()
        assert isinstance(resp, ListObjectsResponse)
