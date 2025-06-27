import pytest
import requests
from .constants import *
from .helper import assert_post_fields_exist, assert_post_field_types, assert_post_data_matches , assert_subset_matches

# --------------------------
# GET /posts tests
# --------------------------

def test_get_all_posts():
    # Test that getting all posts returns a list of posts with required fields and correct types
    response = requests.get(POSTS_URL)
    assert response.status_code == HTTP_OK
    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) > 0
    for post in posts:
        assert_post_fields_exist(post)
        assert_post_field_types(post)

@pytest.mark.parametrize("post_id", EXISTING_IDS)
def test_get_post_by_existing_id(post_id):
    # Test that getting a post by a existing ID returns the correct post with all expected fields
    response = requests.get(f"{POSTS_URL}/{post_id}")
    assert response.status_code == HTTP_OK
    data = response.json()
    assert data["id"] == post_id
    assert_post_fields_exist(data)
    assert_post_field_types(data)

@pytest.mark.parametrize("non_existing_id", NON_EXISTING_IDS)
def test_get_post_by_non_existing_id(non_existing_id):
    # Test that getting a post by a non-existing ID returns 404 status and an empty response
    response = requests.get(f"{POSTS_URL}/{non_existing_id}")
    assert response.status_code == HTTP_NOT_FOUND
    assert response.json() == {}

# --------------------------
# POST /posts tests
# --------------------------
# Note: JSONPlaceholder does not persist created posts, so we can't verify by GET

def test_create_new_post():
    # Test that creating a post with valid data returns 201 status and the correct response
    response = requests.post(POSTS_URL, json=VALID_NEW_POST)
    assert response.status_code == HTTP_CREATED
    response_data = response.json()
    assert_post_fields_exist(response_data)
    assert_post_field_types(response_data)
    assert_post_data_matches(VALID_NEW_POST, response_data)


@pytest.mark.parametrize("post_missing_fields", posts_with_missing_fields)
def test_create_post_with_missing_fields(post_missing_fields):
    # Test that creating a post with missing fields still returns 201 and includes only the sent fields
    response = requests.post(POSTS_URL, json=post_missing_fields)
    assert response.status_code == HTTP_CREATED, f"Expected 201, got {response.status_code}"
    response_data = response.json()
    # Check that keys sent are in response with matching values
    assert_subset_matches(post_missing_fields, response_data)
    assert "id" in response_data, "Missing 'id' in response"



@pytest.mark.parametrize("post_with_none", posts_with_none_fields)
def test_create_post_with_none_fields(post_with_none):
    # Test that creating a post with None values returns 201 and includes those values in the response
    response = requests.post(POSTS_URL, json=post_with_none)
    assert response.status_code == HTTP_CREATED , f"Expected 201, got {response.status_code}"
    response_data = response.json()
    assert_subset_matches(post_with_none, response_data)
    assert "id" in response_data, "Missing 'id' in response"


@pytest.mark.parametrize("post_wrong_types", posts_with_wrong_types)
def test_create_post_with_wrong_data_types(post_wrong_types):
    # Test that creating a post with wrong data types returns 201 and includes the same values in the response
    response = requests.post(POSTS_URL, json=post_wrong_types)
    assert response.status_code == HTTP_CREATED
    response_data = response.json()
    assert_post_fields_exist(response_data)
    assert_post_data_matches(post_wrong_types, response_data)

def test_create_post_with_large_input():
    # Test that creating a post with very large input values returns 201 and includes the large data
    response = requests.post(POSTS_URL, json=LARGE_POST)
    assert response.status_code == HTTP_CREATED
    response_data = response.json()
    assert_post_fields_exist(response_data)
    assert_post_field_types(response_data)
    assert_post_data_matches(LARGE_POST, response_data)

def test_create_post_with_one_extra_field():
    # Test that creating a post with an extra unexpected field returns 201 and includes the extra field
    response = requests.post(POSTS_URL, json=POST_WITH_ONE_EXTRA_FIELD)
    assert response.status_code == HTTP_CREATED, f"Expected 201, got {response.status_code}"
    data = response.json()
    assert_post_fields_exist(data)
    assert_post_field_types(data)
    assert_post_data_matches(POST_WITH_ONE_EXTRA_FIELD, data)
    assert "extraField" in data, "extraField not found in response"
    assert data["extraField"] == "unexpected", f"Expected 'unexpected', got {data['extraField']}"

def test_post_with_text_plain_and_invalid_body():
    # Test that creating a post with invalid content-type and body still returns 201 (due to fake API behavior)
    response = requests.post(POSTS_URL, data=INVALID_NON_JSON_BODY, headers=INVALID_CONTENT_TYPE_HEADERS)
    assert response.status_code == HTTP_CREATED
    response_data = response.json()
    assert "id" in response_data

# --------------------------
# PUT /posts/{id} tests
# --------------------------
# Note: JSONPlaceholder accepts update requests and returns the updated data,
# but it does not persist changes, so we can't verify the update by performing a GET request afterwards.

def test_update_post():
    # Test that updating an existing post with valid data returns 200 and correct updated content
    response = requests.put(f"{POSTS_URL}/{EXISTING_ID}", json=UPDATED_POST)
    assert response.status_code == HTTP_OK
    response_data = response.json()
    assert_post_fields_exist(response_data)
    assert_post_data_matches(UPDATED_POST, response_data)
    assert_post_field_types(response_data)

def test_update_non_existing_post_id():
    # Test updating a post that does not exist returns 500 error.
    # Note: In a real API, this would typically return 404 Not Found.
    # JSONPlaceholder returns 500 due to its fake implementation.
    response = requests.put(f"{POSTS_URL}/{NON_EXISTING_ID}", json=UPDATE_INVALID_POST)
    assert response.status_code == HTTP_INTERNAL_SERVER_ERROR


@pytest.mark.parametrize("post_with_none", posts_with_none_fields)
def test_update_post_with_none_fields(post_with_none):
    # Test that updating a post with None values returns 200 and includes those values in the response
    response = requests.put(f"{POSTS_URL}/{EXISTING_ID}", json=post_with_none)
    assert response.status_code == HTTP_OK, f"Expected 200, got {response.status_code}"
    response_data = response.json()
    assert_subset_matches(post_with_none, response_data)
    assert "id" in response_data, "Missing 'id' in response"
    assert response_data["id"] == EXISTING_ID, f"Expected id={EXISTING_ID}, got {response_data['id']}"


@pytest.mark.parametrize("post_missing_fields", posts_with_missing_fields)
def test_update_post_with_missing_fields(post_missing_fields):
    # Test that updating a post with missing fields returns 200 and includes only the updated fields
    response = requests.put(f"{POSTS_URL}/{EXISTING_ID}", json=post_missing_fields)
    assert response.status_code == HTTP_OK, f"Expected 200, got {response.status_code}"
    response_data = response.json()
    assert_subset_matches(post_missing_fields, response_data)
    assert "id" in response_data, "Missing 'id' in response"
    assert response_data["id"] == EXISTING_ID, f"Expected id={EXISTING_ID}, got {response_data['id']}"


@pytest.mark.parametrize("post_wrong_types", posts_with_wrong_types)
def test_update_post_with_wrong_data_types(post_wrong_types):
    # Test that updating a post with wrong data types returns 200 and includes the same values in the response
    response = requests.put(f"{POSTS_URL}/{EXISTING_ID}", json=post_wrong_types)
    assert response.status_code == HTTP_OK
    response_data = response.json()
    assert_post_fields_exist(response_data)
    assert_post_data_matches(post_wrong_types, response_data)

def test_update_post_with_large_input():
    # Test that updating a post with large input values returns 200 and the response includes the large data
    response = requests.put(f"{POSTS_URL}/{EXISTING_ID}", json=LARGE_POST)
    assert response.status_code == HTTP_OK
    response_data = response.json()
    assert_post_fields_exist(response_data)
    assert_post_data_matches(LARGE_POST, response_data)
    assert_post_field_types(response_data)

def test_update_post_with_extra_field():
    # Test that updating a post with an extra unexpected field returns 200 and includes the extra field
    response = requests.put(f"{POSTS_URL}/{EXISTING_ID}", json=POST_WITH_ONE_EXTRA_FIELD)
    assert response.status_code == HTTP_OK
    data = response.json()
    assert_post_fields_exist(data)
    assert_post_data_matches(POST_WITH_ONE_EXTRA_FIELD, data)
    assert_post_field_types(data)
    assert "extraField" in data, "extraField not found in response"
    assert data["extraField"] == "unexpected", f"Expected 'unexpected', got {data['extraField']}"

def test_put_with_text_plain_and_invalid_body():
    # Test PUT request with invalid content-type and non-JSON body returns 500 error.
    # Note: A real API would likely return 400 Bad Request here.
    # JSONPlaceholder returns 500 due to its fake API behavio
    response = requests.put(
        f"{POSTS_URL}/{NON_EXISTING_ID}",
        data=INVALID_NON_JSON_BODY,
        headers=INVALID_CONTENT_TYPE_HEADERS
    )
    assert response.status_code == HTTP_INTERNAL_SERVER_ERROR

# --------------------------
# DELETE /posts/{id} tests
# --------------------------

# Note: JSONPlaceholder simulates delete requests but does not actually remove data,
# so we *can* perform a GET request after DELETE, but it will still return the original post.
# Therefore, we can't reliably verify deletion by GET on this fake API.

def test_delete_existing_post():
    # Test deleting an existing post returns 200 and empty response body
    response = requests.delete(f"{POSTS_URL}/{EXISTING_ID}")
    assert response.status_code == HTTP_OK
    assert response.json() == {}

def test_delete_non_existing_post():
    # Test deleting a non-existing post returns 200 and empty response body
    response = requests.delete(f"{POSTS_URL}/{NON_EXISTING_ID}")
    assert response.status_code == HTTP_OK
    assert response.json() == {}
