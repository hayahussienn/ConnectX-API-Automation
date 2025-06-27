# Helper Functions

def assert_post_fields_exist(post):
    # Check that all required fields exist in a post object
    assert "userId" in post, "Missing 'userId' in post"
    assert "id" in post, "Missing 'id' in post"
    assert "title" in post, "Missing 'title' in post"
    assert "body" in post, "Missing 'body' in post"

def assert_post_field_types(post):
    # Check that post fields have the correct data types
    assert isinstance(post["userId"], int), "'userId' must be int"
    assert isinstance(post["id"], int), "'id' must be int"
    assert isinstance(post["title"], str), "'title' must be str"
    assert isinstance(post["body"], str), "'body' must be str"

def assert_post_data_matches(input_data, response_data):
    # Check that response data matches input data except for 'id' field
    for key in ["userId", "title", "body"]:
        assert response_data[key] == input_data[key], f"{key} mismatch"
    # Ensure response contains an 'id' field
    assert "id" in response_data, "'id' should be present"

def assert_subset_matches(input_data, response_data):
    # Assert all keys and values from input_data exist in response_data
    for key in input_data:
        assert key in response_data, f"Missing key '{key}' in response"
        assert response_data[key] == input_data[key], f"Value mismatch for key '{key}'"
