# 📋 API Test Suite for JSONPlaceholder

Automated tests for a REST API that handles blog posts. Tests all the basic operations: create, read, update, and delete posts.

## 🔧 What I Used

**Python + pytest + requests**

- **pytest**: Great for running tests and showing results clearly
- **requests**: Simple way to make HTTP calls to APIs
- **Python**: Easy to read and write test code

I picked these tools because they're simple, reliable, and widely used in the industry.

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



## 🚀 How to Run

### Install what you need:

```bash
pip install pytest requests
```

### Run all tests:

```bash
pytest test_api.py -v
```

### Run specific tests:

```bash
pytest test_api.py::TestGetPosts -v    # Only GET tests
pytest test_api.py::TestCreatePost -v  # Only POST tests
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