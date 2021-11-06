# redis-lock
Redis Based API for acquiring and releasing lock on a value for a specified amount of time.

# Running Locally
**Prerequisites**
- Python >=3.7
- Local Redis server running on port 6379

```
# Install dependencies from requirements.txt
pip install -r requirements.txt
# Run the application
uvicorn src.app:app
```

# Test Functionality

Import the cURL command in Postman to test the functionality. Following are the query parameters:

- key - The value on which the lock needs to be acquired
- key_expiry - The duration of the lock in seconds after which the lock will be automatically released

```
curl --location --request GET 'http://127.0.0.1:8000/api/v1/lock?key=12345&key_expiry=300'
```

After the 1st request, the value will be set in Redis the following response will be returned.

```
{
    "status": 201,
    "message": "12345 is unique"
}
```

If you make the second request within the key expiration window, in this case 5 minutes, then you will get the following response

```
{
    "status": 406,
    "message": "12345 is duplicate"
}
```

To manually remove the lock, use the following cURL command

```
curl --location --request GET 'http://127.0.0.1:8000/api/v1/unlock?key=12345'
```

Upon successfully removing a key from Redis, you will get the following response

```
{
    "status": 202,
    "message": "12345 is removed"
}
```

If the key is not present in Redis, you will get the following response

```
{
    "status": 404,
    "message": "12345 didn't exist"
}
```