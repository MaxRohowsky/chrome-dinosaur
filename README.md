# Team2_DinosaurGame

The Chrome Dinosaur 🦖 Game in build with Pygame in Python.

# Request

---

| Method | URL           | Data Format | Description                                  |
| ------ | ------------- | ----------- | -------------------------------------------- |
| POST   | /user/v1/data | json        | push user's point data                       |
| POST   | /user/v1/info | json        | receive user's rank data in descending order |

# Response

---

| Method | URL           | Data Format |
| ------ | ------------- | ----------- |
| POST   | /user/v1/data | json        |
| POST   | /user/v1/info | json/array  |

## Success Response

---

- Response Code: 200
- Content:

```yaml
{ "StatusCode": 200, "Message": [] }
```

## Error Response

---

- Response Code: 401 UNAUTHORIZED
- Content:

```yaml
{ "StatusCode": 401, "Message": "Invalid Contents." }
```

---

- Response Code: 422 UNPROCESSABLE ENTRY
- Content:

```yaml
{ "Message": "Please Check Your Data sets again." }
```
