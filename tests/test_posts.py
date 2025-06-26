import pytest
import requests

# Base URL of the JSONPlaceholder API
BASE_URL = "https://jsonplaceholder.typicode.com"
POSTS_URL = f"{BASE_URL}/posts"

# Helper Functions

# Check that all required fields exist in the post
def assert_post_fields_exist(post):
    assert "userId" in post, "Missing 'userId' in post"
    assert "id" in post, "Missing 'id' in post"
    assert "title" in post, "Missing 'title' in post"
    assert "body" in post, "Missing 'body' in post"

# Check that fields have the correct data types
def assert_post_field_types(post):
    assert isinstance(post["userId"], int), "'userId' should be an integer"
    assert isinstance(post["id"], int), "'id' should be an integer"
    assert isinstance(post["title"], str), "'title' should be a string"
    assert isinstance(post["body"], str), "'body' should be a string"

# Check that the response matches the sent input data
def assert_post_data_matches(input_data, response_data):
    for key in ["userId", "title", "body"]:
        assert response_data[key] == input_data[key], f"{key} does not match"
    assert "id" in response_data, "Expected 'id' in response"

# Shared Test Data

# Posts with one or more fields set to None
posts_with_none_fields = [
    {"userId": None, "title": "Title", "body": "Body"},
    {"userId": 1, "title": None, "body": "Body"},
    {"userId": 1, "title": "Title", "body": None},
    {"userId": None, "title": None, "body": None},
]

# Posts with missing fields
posts_with_missing_fields = [
    {"userId": 1, "body": "Body without title"},
    {"title": "Title without userId", "body": "Body"},
    {"userId": 1, "title": "Title without body"},
    {},  # completely empty fields
]

# Posts with wrong field types
posts_with_wrong_types = [
    {"userId": "string_instead_of_int", "title": "Title", "body": "Body"},
    {"userId": 1, "title": 12345, "body": "Body"},
    {"userId": 1, "title": "Title", "body": 67890},
]

# Tests

# Get all posts and validate structure
def test_get_all_posts():
    response = requests.get(POSTS_URL)
    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) > 0
    for post in posts:
        assert_post_fields_exist(post)
        assert_post_field_types(post)

# Get post by valid ID and check correctness
@pytest.mark.parametrize("post_id", [1, 2, 3, 50, 100])
def test_get_post_by_valid_id(post_id):
    response = requests.get(f"{POSTS_URL}/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == post_id
    assert_post_fields_exist(data)
    assert_post_field_types(data)

# Get post by invalid ID (should return 404)
@pytest.mark.parametrize("invalid_id", [0, 101, 999, "abc", "!@#"])
def test_get_post_by_invalid_id(invalid_id):
    response = requests.get(f"{POSTS_URL}/{invalid_id}")
    assert response.status_code == 404
    assert response.json() == {}

# Create a new post with valid data
def test_create_new_post():
    input_data = {
        "userId": 11,
        "title": "New Post",
        "body": "This is a new post."
    }
    response = requests.post(POSTS_URL, json=input_data)
    assert response.status_code == 201
    response_data = response.json()
    assert_post_data_matches(input_data, response_data)
    assert_post_field_types(response_data)

# Create post with None values in fields
@pytest.mark.parametrize("post_with_none", posts_with_none_fields)
def test_create_post_with_none_fields(post_with_none):
    response = requests.post(POSTS_URL, json=post_with_none)
    assert response.status_code == 201

# Create post with missing fields
@pytest.mark.parametrize("post_missing_fields", posts_with_missing_fields)
def test_create_post_with_missing_fields(post_missing_fields):
    response = requests.post(POSTS_URL, json=post_missing_fields)
    assert response.status_code == 201

# Create post with wrong data types
@pytest.mark.parametrize("post_wrong_types", posts_with_wrong_types)
def test_create_post_with_wrong_data_types(post_wrong_types):
    response = requests.post(POSTS_URL, json=post_wrong_types)
    assert response.status_code == 201

# Update a post with valid ID and valid data
def test_update_post():
    update_id = 1
    updated_post_data = {
        "userId": 1,
        "title": "Updated Title",
        "body": "This is the updated body."
    }
    response = requests.put(f"{POSTS_URL}/{update_id}", json=updated_post_data)
    assert response.status_code == 200
    response_data = response.json()
    assert_post_data_matches(updated_post_data, response_data)
    assert_post_field_types(response_data)

# Try to update a non-existing post
def test_update_non_existing_post_id():
    invalid_id = 998
    updated_post_data = {
        "userId": 1,
        "title": "Attempt to update invalid ID",
        "body": "This should fail on a real API"
    }
    response = requests.put(f"{POSTS_URL}/{invalid_id}", json=updated_post_data)
    assert response.status_code == 500

# Update a post with None fields
@pytest.mark.parametrize("post_with_none", posts_with_none_fields)
def test_update_post_with_none_fields(post_with_none):
    update_id = 1
    response = requests.put(f"{POSTS_URL}/{update_id}", json=post_with_none)
    assert response.status_code == 200

# Update a post with missing fields
@pytest.mark.parametrize("post_missing_fields", posts_with_missing_fields)
def test_update_post_with_missing_fields(post_missing_fields):
    update_id = 1
    response = requests.put(f"{POSTS_URL}/{update_id}", json=post_missing_fields)
    assert response.status_code == 200
    assert "id" in response.json()

# Update post with wrong data types
@pytest.mark.parametrize("post_wrong_types", posts_with_wrong_types)
def test_update_post_with_invalid_data_types(post_wrong_types):
    update_id = 1
    response = requests.put(f"{POSTS_URL}/{update_id}", json=post_wrong_types)
    assert response.status_code == 200
    assert "id" in response.json()

# Delete an existing post
def test_delete_existing_post():
    delete_id = 5
    response = requests.delete(f"{POSTS_URL}/{delete_id}")
    assert response.status_code == 200
    assert response.json() == {}

# Delete a non-existing post
def test_delete_non_existing_post():
    non_existing_id = 666
    response = requests.delete(f"{POSTS_URL}/{non_existing_id}")
    assert response.status_code == 200
    assert response.json() == {}
