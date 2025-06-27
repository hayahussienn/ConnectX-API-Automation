# 📋 API Test Suite for JSONPlaceholder

Automated tests for a REST API that handles blog posts. Tests all the basic operations: create, read, update, and delete posts.

# 🔧 What I Used

## Python + pytest + requests

- **Python**: Easy to read and write test code  
- **pytest**: Great for running tests and displaying results clearly  
- **requests**: Simple and effective way to make HTTP calls to APIs  

## Postman

- Used to manually test the same endpoints for comparison  
- Demonstrates familiarity with UI-based API testing tools  

I chose these tools because they are simple, reliable, and widely used in the industry.

## 🗂️ Project Structure

- **Tests file**  
  All test cases are organized in a single main test file (`test_posts.py`). This helps keep tests focused and easy to locate.

- **Constants file**  
  Test data, such as URLs and input samples, are stored separately in `constants.py` for better manageability and easy reuse across tests.

- **Helper Functions file**  
  Common assertion and validation functions are kept in `helper.py` to reduce duplication and improve code readability.

This modular organization helps keep the codebase clean, maintainable, and easy to extend.



## 📊 Test Coverage

### All Required Endpoints Covered:

- ✅ GET /posts - Get all posts (structure + status code validation)
- ✅ GET /posts/{id} - Get specific post (valid & invalid IDs)  
- ✅ POST /posts - Create new post (with response validation)
- ✅ PUT /posts/{id} - Update existing post (check results)
- ✅ DELETE /posts/{id} - Delete post (confirm deletion)

### Test Types Included:

- ✅ **Positive tests**: Valid data, expected results
- ✅ **Negative tests**: Invalid IDs (0, 999, "abc"), missing fields, wrong data types
- ✅ **Data validation**: Required fields exist, correct data types (int, string)
- ✅ **Status codes**: 200, 201, 404, 500 responses
- ✅ **Response body**: JSON structure, field matching, empty responses

### Edge Cases Tested:

- Null values in required fields (None)
- Missing required fields (e.g., missing title, body, or userId)
- Wrong field types (e.g., userId as string, title as integer)
- Non-existent IDs (e.g., 0, 101, 999)
- Invalid ID formats (e.g., strings like "abc", special characters like "!@#" in path)
- Malformed requests (empty body, missing content)
- Large input strings (very long title and body values to test API limits)
- Extra/unexpected fields in the post

## 📬 Postman Collection

A manual version of the same test scenarios was implemented in Postman for comparison.

### 🔗 View Public Postman Collection:
👉 [JSONPlaceholder API Tests – Postman (Public)](https://www.postman.com/aviation-astronaut-47417982/jsonplaceholder-api-tests/collection/jx5ns9g/jsonplaceholder-api-tests)

You can view and import the collection to inspect or run tests manually.


## 🚀 How to Run

### Install what you need:

```bash
pip install pytest requests
```

### Run all tests:

```bash
pytest test_posts.py -v
```

### Run specific tests:

```bash
pytest test_posts.py::TestGetPosts -v    # Only GET tests
pytest test_posts.py::TestCreatePost -v  # Only POST tests
```

## ⚠️ Challenges I Found

### Main Issues:

1. **Fake API Behavior**: JSONPlaceholder accepts almost anything (even bad data) instead of rejecting it like a real API would. Had to write tests that work with this.

2. **No Real Changes**: Since it's a fake API, nothing actually gets saved. Had to get creative testing if operations "worked."

### 💡 Interesting Discoveries:

- The API is very forgiving - accepts null values and wrong data types
- Always returns consistent JSON structure
- Fast response times (under 1 second)

## 🔮 How to Make This API Better

### For a Real Production API:

1. **Better Validation**: Reject bad data with proper error messages
2. **Proper Error Codes**: Use 404 for "not found" instead of 500
3. **Security**: Add rate limiting and user authentication
4. **More Features**: Add search, pagination, and filtering