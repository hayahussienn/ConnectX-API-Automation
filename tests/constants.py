# constants.py

BASE_URL = "https://jsonplaceholder.typicode.com"
POSTS_URL = f"{BASE_URL}/posts"

VALID_POST_IDS = [1, 2, 3, 50, 100]
INVALID_POST_IDS = [0, 101, 999, "abc", "!@#"]

VALID_NEW_POST = {
    "userId": 11,
    "title": "New Post",
    "body": "This is a new post."
}

UPDATED_POST = {
    "userId": 1,
    "title": "Updated Title",
    "body": "This is the updated body."
}

UPDATE_INVALID_POST = {
    "userId": 1,
    "title": "Attempt to update invalid ID",
    "body": "This should fail on a real API"
}

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

DELETE_EXISTING_ID = 5
DELETE_NON_EXISTING_ID = 666
UPDATE_ID_VALID = 1
UPDATE_ID_INVALID = 998
