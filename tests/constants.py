# constants.py

# Base URL for the JSONPlaceholder API
BASE_URL = "https://jsonplaceholder.typicode.com"
# Endpoint URL for posts
POSTS_URL = f"{BASE_URL}/posts"

# Valid and invalid post IDs for testing
EXISTING_ID=3
NON_EXISTING_ID=666
EXISTING_IDS = [1, 2, 3, 50, 100]
NON_EXISTING_IDS = [-5,0, 101, 999, "abc", "!@#"]

# Sample data for creating a new post
VALID_NEW_POST = {
    "userId": 11,
    "title": "New Post",
    "body": "This is a new post."
}

# Sample data for updating a post
UPDATED_POST = {
    "userId": 1,
    "title": "Updated Title",
    "body": "This is the updated body."
}

# Sample data for updating a non-existing post
UPDATE_INVALID_POST = {
    "userId": 1,
    "title": "Attempt to update invalid ID",
    "body": "This should fail on a real API"
}

# Posts with None values in various fields for edge case testing
posts_with_none_fields = [
    {"userId": None, "title": "Title", "body": "Body"},
    {"userId": 1, "title": None, "body": "Body"},
    {"userId": 1, "title": "Title", "body": None},
    {"userId": None, "title": None, "body": None},
]

# Posts missing some fields to test partial/malformed data
posts_with_missing_fields = [
    {"userId": 1, "body": "Body without title"},
    {"title": "Title without userId", "body": "Body"},
    {"userId": 1, "title": "Title without body"},
    {},  # completely empty post
]

# Posts with wrong data types in fields for validation testing
posts_with_wrong_types = [
    {"userId": "string_instead_of_int", "title": "Title", "body": "Body"},
    {"userId": 1, "title": 12345, "body": "Body"},
    {"userId": 1, "title": "Title", "body": 67890},
]

# Post with large input strings for stress testing
LARGE_POST = {
    "userId": 1,
    "title": "A" * 1000,   # 1000-character title
    "body": "B" * 10000    # 10,000-character body
}

# Post with extra field
POST_WITH_ONE_EXTRA_FIELD = {
    "userId": 1,
    "title": "Post with Extra Field",
    "body": "This post includes an extra field.",
    "extraField": "unexpected"
}

# Invalid content type and body
INVALID_CONTENT_TYPE_HEADERS = {"Content-Type": "text/plain"}
INVALID_NON_JSON_BODY = "This is not JSON"




