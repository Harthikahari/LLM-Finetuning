# Deployment Guide

Deploy Text2SQL models to production.

## Docker Deployment

### Build and Run

```bash
# Build API image
docker-compose build api

# Start API service
docker-compose up api
```

### Environment Variables

Configure via `.env` file:

```bash
MODEL_PATH=./models/text2sql
API_HOST=0.0.0.0
API_PORT=8000
```

## API Endpoints

### Prediction

```bash
curl -X POST "http://localhost:8000/predict" \
    -H "Content-Type: application/json" \
    -d '{
        "question": "Show all employees",
        "schema": "employees(id, name, dept)"
    }'
```

### Health Check

```bash
curl http://localhost:8000/health
```

## Performance Optimization

- Use model quantization for faster inference
- Enable batching for throughput
- Configure GPU memory management

## Security

- Add authentication middleware
- Implement rate limiting
- Validate input queries
- Use HTTPS in production
