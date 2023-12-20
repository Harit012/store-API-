# CONTRIBUTING

## HOW TO RUN DOCKER FILE LOCALLY

```
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" flask-smorest-api sh -c "flask run"
```