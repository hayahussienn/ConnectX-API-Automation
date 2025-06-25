import pytest
import requests

# Base URL of the JSONPlaceholder API
BASE_URL = "https://jsonplaceholder.typicode.com"
POSTS_URL = f"{BASE_URL}/posts"

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


# Shared test data sets
posts_with_none_fields = [
    {"userId": None, "title": "Title", "body": "Body"},
    {"userId": 1, "title": None, "body": "Body"},
    {"userId": 1, "title": "Title", "body": None},
    {"userId": None, "title": None, "body": None},
]

posts_with_missing_fields = [
    {"userId": 1, "body": "Body without title"},
    {"title": "Title without userId", "body": "Body"},
    {"userId": 1, "title": "Title without body"},
    {},  # completely empty fields
]

posts_with_wrong_types = [
    {"userId": "string_instead_of_int", "title": "Title", "body": "Body"},
    {"userId": 1, "title": 12345, "body": "Body"},
    {"userId": 1, "title": "Title", "body": 67890},
]


# Test Get all posts
def test_get_all_posts():
    # Send GET request to /posts endpoint
    response = requests.get(POSTS_URL)
    assert response.status_code == 200, "Expected status code 200 OK"
    # Convert response to JSON
    posts = response.json()
    # Check that the response is a list
    assert isinstance(posts, list), "Expected response to be a list"
    # Make sure the list is not empty
    assert len(posts) > 0, "Posts list should not be empty"
    # Check each post in the list
    for post in posts:
        # Check that required fields exist
        assert_post_fields_exist(post)
        # Check that the data types are correct
        assert_post_field_types(post)


#Get a specific post by valid ID
@pytest.mark.parametrize("post_id", [1, 2, 3, 50, 100])
def test_get_post_by_valid_id(post_id):
    response = requests.get(f"{POSTS_URL}/{post_id}")
    # Check that the response is OK
    assert response.status_code == 200, f"Expected 200 OK for post ID {post_id}"
    data = response.json()
    # Check that the ID matches
    assert data["id"] == post_id, f"Expected post ID to be {post_id}, got {data['id']}"
    # Required fields
    assert_post_fields_exist(data)
    # Data type validation
    assert_post_field_types(data)



#Get a specific post by invalid ID
@pytest.mark.parametrize("invalid_id", [0, 101, 999, "abc", "!@#"])
def test_get_post_by_invalid_id(invalid_id):
    response = requests.get(f"{POSTS_URL}/{invalid_id}")
    # JSONPlaceholder returns 404 for invalid IDs
    assert response.status_code == 404, f"Expected 404 Not Found for post ID {invalid_id}"
    # Response body should be empty object
    assert response.json() == {}, f"Expected empty JSON object for invalid ID {invalid_id}"


# Create a new post with valid data
def test_create_new_post():
    input_data = {
        "userId": 11,
        "title": "New Post",
        "body": "This is a new post."
    }
    response = requests.post(POSTS_URL, json=input_data)
    # Status code should be 201 Created
    assert response.status_code == 201, "Expected status code 201 for successful post creation"
    response_data = response.json()
    # Response body should include all fields from the request
    assert_post_data_matches(input_data, response_data)
    # Data type validation
    assert_post_field_types(response_data)

# Create a new post with fields set to None values
@pytest.mark.parametrize("post_with_none", posts_with_none_fields)
def test_post_with_none_fields(post_with_none):
    response = requests.post(POSTS_URL, json=post_with_none)
    assert response.status_code == 201, f"Expected 201 when fields are None, got {response.status_code}"


# Create a new post with missing fields
@pytest.mark.parametrize("post_missing_fields", posts_with_missing_fields)
def test_post_with_missing_fields(post_missing_fields):
    response = requests.post(POSTS_URL, json=post_missing_fields)
    assert response.status_code == 201, f"Expected 201 when fields are missing, got {response.status_code}"


# Create a post with fields having wrong data types
@pytest.mark.parametrize("post_wrong_types", posts_with_wrong_types)
def test_post_with_wrong_data_types(post_wrong_types):
    response = requests.post(POSTS_URL, json=post_wrong_types)
    assert response.status_code == 201, f"Expected 201 when fields have wrong types, got {response.status_code}"


# Update an existing post with valid ID and valid data
def test_update_post():
    update_id = 1
    updated_post_data = {
        "userId": 1,
        "title": "Updated Title",
        "body": "This is the updated body."
    }
    response = requests.put(f"{POSTS_URL}/{update_id}", json=updated_post_data)
    # Expect 200 OK for successful update
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    response_data = response.json()
    # Check that response contains updated data
    assert_post_data_matches(updated_post_data, response_data)
    # Validate response field types
    assert_post_field_types(response_data)


# Try to update a post with an invalid/non-existing ID
def test_update_non_existing_post_id():
    invalid_id = 998  # non-existing ID
    updated_post_data = {
        "userId": 1,
        "title": "Attempt to update invalid ID",
        "body": "This should fail on a real API"
    }
    response = requests.put(f"{POSTS_URL}/{invalid_id}", json=updated_post_data)
    assert response.status_code == 500, f"Expected 500 from JSONPlaceholder, got {response.status_code}"


# Update with one or more fields set to None
@pytest.mark.parametrize("post_with_none", posts_with_none_fields)
def test_update_post_with_none_fields(post_with_none):
    update_id = 1
    response = requests.put(f"{POSTS_URL}/{update_id}", json=post_with_none)
    # JSONPlaceholder still returns 200; real API might return 400 or 500
    assert response.status_code == 200, f"Expected 200 when updating with None values, got {response.status_code}"


# Update with missing fields
@pytest.mark.parametrize("post_missing_fields", posts_with_missing_fields)
def test_update_post_with_missing_fields(post_missing_fields):
    update_id = 1
    response = requests.put(f"{POSTS_URL}/{update_id}", json=post_missing_fields)
    # JSONPlaceholder returns 200 even with missing fields
    assert response.status_code == 200, f"Expected 200 when fields are missing (due to permissive API), got {response.status_code}"
    assert "id" in response.json(), "Expected 'id' in response"


# Update with wrong data types for one or more fields
@pytest.mark.parametrize("post_wrong_types", posts_with_wrong_types)
def test_update_post_with_invalid_data_types(post_wrong_types):
    update_id = 1
    response = requests.put(f"{POSTS_URL}/{update_id}", json=post_wrong_types)
    # JSONPlaceholder accepts incorrect types and still returns 200
    assert response.status_code == 200, f"Expected 200 when using wrong data types (due to permissive API), got {response.status_code}"
    assert "id" in response.json(), "Expected 'id' in response"


# Delete an existing post
def test_delete_existing_post():
    delete_id = 5
    response = requests.delete(f"{POSTS_URL}/{delete_id}")
    assert response.status_code == 200, f"Expected status code 200 when deleting existing post, got {response.status_code}"
    assert response.json() == {}, "Expected empty JSON when deleting a post"


# Delete a non-existing post
def test_delete_non_existing_post():
    non_existing_id = 666
    response = requests.delete(f"{POSTS_URL}/{non_existing_id}")
    # JSONPlaceholder returns 200 even if the post doesn't exist , In real APIs this should be 404 Not Found
    assert response.status_code == 200, f"Expected status code 200 (as per JSONPlaceholder behavior), got {response.status_code}"
    assert response.json() == {}, "Expected empty JSON when deleting a non-existing post"




