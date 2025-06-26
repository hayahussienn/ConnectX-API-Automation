import pytest
import requests
from .constants import *

# Helper Functions

def assert_post_fields_exist(post):
    # Check that all required fields exist in a post
    assert "userId" in post, "Missing 'userId' in post"
    assert "id" in post, "Missing 'id' in post"
    assert "title" in post, "Missing 'title' in post"
    assert "body" in post, "Missing 'body' in post"

def assert_post_field_types(post):
    # Check that post fields have correct data types
    assert isinstance(post["userId"], int), "'userId' must be int"
    assert isinstance(post["id"], int), "'id' must be int"
    assert isinstance(post["title"], str), "'title' must be str"
    assert isinstance(post["body"], str), "'body' must be str"

def assert_post_data_matches(input_data, response_data):
    # Verify response matches the input data (except 'id')
    for key in ["userId", "title", "body"]:
        assert response_data[key] == input_data[key], f"{key} mismatch"
    assert "id" in response_data, "'id' should be present"


# --------------------------
# GET /posts tests
# --------------------------

def test_get_all_posts():
    # Test getting all posts returns list with correct fields and types
    response = requests.get(POSTS_URL)
    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) > 0
    for post in posts:
        assert_post_fields_exist(post)
        assert_post_field_types(post)

@pytest.mark.parametrize("post_id", VALID_POST_IDS)
def test_get_post_by_valid_id(post_id):
    # Test getting a post by valid ID returns correct post data
    response = requests.get(f"{POSTS_URL}/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == post_id
    assert_post_fields_exist(data)
    assert_post_field_types(data)

@pytest.mark.parametrize("invalid_id", INVALID_POST_IDS)
def test_get_post_by_invalid_id(invalid_id):
    # Test getting post by invalid ID returns 404 and empty response
    response = requests.get(f"{POSTS_URL}/{invalid_id}")
    assert response.status_code == 404
    assert response.json() == {}


# --------------------------
# POST /posts tests
# --------------------------

def test_create_new_post():
    # Test creating a post with valid data returns 201 and correct response
    response = requests.post(POSTS_URL, json=VALID_NEW_POST)
    assert response.status_code == 201
    response_data = response.json()
    assert_post_data_matches(VALID_NEW_POST, response_data)
    assert_post_field_types(response_data)

@pytest.mark.parametrize("post_with_none", posts_with_none_fields)
def test_create_post_with_none_fields(post_with_none):
    # Test creating posts with None fields (accepted by API)
    response = requests.post(POSTS_URL, json=post_with_none)
    assert response.status_code == 201

@pytest.mark.parametrize("post_missing_fields", posts_with_missing_fields)
def test_create_post_with_missing_fields(post_missing_fields):
    # Test creating posts missing some fields (accepted by API)
    response = requests.post(POSTS_URL, json=post_missing_fields)
    assert response.status_code == 201

@pytest.mark.parametrize("post_wrong_types", posts_with_wrong_types)
def test_create_post_with_wrong_data_types(post_wrong_types):
    # Test creating posts with wrong data types (accepted by API)
    response = requests.post(POSTS_URL, json=post_wrong_types)
    assert response.status_code == 201


# --------------------------
# PUT /posts/{id} tests
# --------------------------

def test_update_post():
    # Test updating existing post with valid data returns 200 and correct response
    response = requests.put(f"{POSTS_URL}/{UPDATE_ID_VALID}", json=UPDATED_POST)
    assert response.status_code == 200
    response_data = response.json()
    assert_post_data_matches(UPDATED_POST, response_data)
    assert_post_field_types(response_data)

def test_update_non_existing_post_id():
    # Test updating non-existing post returns 500 error
    response = requests.put(f"{POSTS_URL}/{UPDATE_ID_INVALID}", json=UPDATE_INVALID_POST)
    assert response.status_code == 500

@pytest.mark.parametrize("post_with_none", posts_with_none_fields)
def test_update_post_with_none_fields(post_with_none):
    # Test updating post with None fields returns 200 (edge case)
    response = requests.put(f"{POSTS_URL}/{UPDATE_ID_VALID}", json=post_with_none)
    assert response.status_code == 200

@pytest.mark.parametrize("post_missing_fields", posts_with_missing_fields)
def test_update_post_with_missing_fields(post_missing_fields):
    # Test updating post missing some fields returns 200 and response has 'id'
    response = requests.put(f"{POSTS_URL}/{UPDATE_ID_VALID}", json=post_missing_fields)
    assert response.status_code == 200
    assert "id" in response.json()

@pytest.mark.parametrize("post_wrong_types", posts_with_wrong_types)
def test_update_post_with_invalid_data_types(post_wrong_types):
    # Test updating post with wrong data types returns 200 and response has 'id'
    response = requests.put(f"{POSTS_URL}/{UPDATE_ID_VALID}", json=post_wrong_types)
    assert response.status_code == 200
    assert "id" in response.json()


# --------------------------
# DELETE /posts/{id} tests
# --------------------------

def test_delete_existing_post():
    # Test deleting existing post returns 200 and empty response
    response = requests.delete(f"{POSTS_URL}/{DELETE_EXISTING_ID}")
    assert response.status_code == 200
    assert response.json() == {}

def test_delete_non_existing_post():
    # Test deleting non-existing post returns 200 and empty response
    response = requests.delete(f"{POSTS_URL}/{DELETE_NON_EXISTING_ID}")
    assert response.status_code == 200
    assert response.json() == {}
