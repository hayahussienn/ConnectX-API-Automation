import pytest
import requests
from .constants import *

# Helper Functions

def assert_post_fields_exist(post):
    assert "userId" in post, "Missing 'userId' in post"
    assert "id" in post, "Missing 'id' in post"
    assert "title" in post, "Missing 'title' in post"
    assert "body" in post, "Missing 'body' in post"

def assert_post_field_types(post):
    assert isinstance(post["userId"], int), "'userId' should be an integer"
    assert isinstance(post["id"], int), "'id' should be an integer"
    assert isinstance(post["title"], str), "'title' should be a string"
    assert isinstance(post["body"], str), "'body' should be a string"

def assert_post_data_matches(input_data, response_data):
    for key in ["userId", "title", "body"]:
        assert response_data[key] == input_data[key], f"{key} does not match"
    assert "id" in response_data, "Expected 'id' in response"

# --------------------------
# GET /posts
# --------------------------

def test_get_all_posts():
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
    response = requests.get(f"{POSTS_URL}/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == post_id
    assert_post_fields_exist(data)
    assert_post_field_types(data)

@pytest.mark.parametrize("invalid_id", INVALID_POST_IDS)
def test_get_post_by_invalid_id(invalid_id):
    response = requests.get(f"{POSTS_URL}/{invalid_id}")
    assert response.status_code == 404
    assert response.json() == {}

# --------------------------
# POST /posts
# --------------------------

def test_create_new_post():
    response = requests.post(POSTS_URL, json=VALID_NEW_POST)
    assert response.status_code == 201
    response_data = response.json()
    assert_post_data_matches(VALID_NEW_POST, response_data)
    assert_post_field_types(response_data)

@pytest.mark.parametrize("post_with_none", posts_with_none_fields)
def test_create_post_with_none_fields(post_with_none):
    response = requests.post(POSTS_URL, json=post_with_none)
    assert response.status_code == 201

@pytest.mark.parametrize("post_missing_fields", posts_with_missing_fields)
def test_create_post_with_missing_fields(post_missing_fields):
    response = requests.post(POSTS_URL, json=post_missing_fields)
    assert response.status_code == 201

@pytest.mark.parametrize("post_wrong_types", posts_with_wrong_types)
def test_create_post_with_wrong_data_types(post_wrong_types):
    response = requests.post(POSTS_URL, json=post_wrong_types)
    assert response.status_code == 201

# --------------------------
# PUT /posts/{id}
# --------------------------

def test_update_post():
    response = requests.put(f"{POSTS_URL}/{UPDATE_ID_VALID}", json=UPDATED_POST)
    assert response.status_code == 200
    response_data = response.json()
    assert_post_data_matches(UPDATED_POST, response_data)
    assert_post_field_types(response_data)

def test_update_non_existing_post_id():
    response = requests.put(f"{POSTS_URL}/{UPDATE_ID_INVALID}", json=UPDATE_INVALID_POST)
    assert response.status_code == 500

@pytest.mark.parametrize("post_with_none", posts_with_none_fields)
def test_update_post_with_none_fields(post_with_none):
    response = requests.put(f"{POSTS_URL}/{UPDATE_ID_VALID}", json=post_with_none)
    assert response.status_code == 200

@pytest.mark.parametrize("post_missing_fields", posts_with_missing_fields)
def test_update_post_with_missing_fields(post_missing_fields):
    response = requests.put(f"{POSTS_URL}/{UPDATE_ID_VALID}", json=post_missing_fields)
    assert response.status_code == 200
    assert "id" in response.json()

@pytest.mark.parametrize("post_wrong_types", posts_with_wrong_types)
def test_update_post_with_invalid_data_types(post_wrong_types):
    response = requests.put(f"{POSTS_URL}/{UPDATE_ID_VALID}", json=post_wrong_types)
    assert response.status_code == 200
    assert "id" in response.json()

# --------------------------
# DELETE /posts/{id}
# --------------------------

def test_delete_existing_post():
    response = requests.delete(f"{POSTS_URL}/{DELETE_EXISTING_ID}")
    assert response.status_code == 200
    assert response.json() == {}

def test_delete_non_existing_post():
    response = requests.delete(f"{POSTS_URL}/{DELETE_NON_EXISTING_ID}")
    assert response.status_code == 200
    assert response.json() == {}
