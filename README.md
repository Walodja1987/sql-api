Start the SQL API Server:
```
python -m uvicorn server:app --host 127.0.0.1 --port 8000
```

Try out the API:
```
http://127.0.0.1:8000/docs
```

Access the frontend:
```
http://127.0.0.1:8000/app
```