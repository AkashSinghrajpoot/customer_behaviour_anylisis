# API Documentation

## Base Configuration

**Base URL**: `http://localhost:5000`

**Default Port**: `5000`

**Content-Type**: `application/json`

---

## Endpoints Overview

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/predict` | Main prediction & recommendation endpoint |
| GET | `/api/health` | Health check |
| GET | `/api/status` | Application status |
| GET | `/` | Dashboard homepage |

---

## POST /api/predict

### Purpose
Generate customer analysis, metrics, predictions, and actionable recommendations.

### Request

**Headers**:
```
Content-Type: application/json
```

**Body**:
```json
{
  "spending": 19.94,
  "advance_payments": 16.92,
  "current_balance": 6.675,
  "credit_limit": 3.763,
  "min_payment_amt": 3.252,
  "max_spent_in_single_shopping": 6.55
}
```

### Field Descriptions

| Field | Type | Range | Required | Description |
|-------|------|-------|----------|-------------|
| spending | float | 0-1000 | Yes | Total spending amount |
| advance_payments | float | 0-1000 | Yes | Advance payment amount |
| current_balance | float | 0-100 | Yes | Current account balance |
| credit_limit | float | 0-100 | Yes | Credit limit |
| min_payment_amt | float | 0-50 | Yes | Minimum payment required |
| max_spent_in_single_shopping | float | 0-100 | Yes | Max amount spent in one transaction |

### Responses

#### Success Response (200 OK)

```json
{
  "status": "success",
  "customer_metrics": {
    "engagement_score": 72.5,
    "relationship_score": 68.3,
    "customer_segment": "Growth",
    "customer_health": 70.1,
    "offer_priority": 4
  },
  "prediction": {
    "subscription_probability": 75.8,
    "confidence": "High"
  },
  "recommendation": {
    "primary_action": "Cross-sell High-Value Financial Products",
    "secondary_actions": [
      "Consider loyalty program enrollment",
      "Offer dedicated account manager"
    ],
    "priority_level": "High",
    "reasoning": "Strong engagement patterns detected | Positive relationship indicators | High likelihood of subscription conversion",
    "next_steps": {
      "immediate": "Execute: Present tailored financial products",
      "timeline": "Within 2 weeks",
      "preferred_channel": "Multi-channel",
      "segment_note": "Priority handling for Growth segment customers"
    }
  }
}
```

#### Validation Error (400 Bad Request)

```json
{
  "error": "Validation failed",
  "details": [
    "Spending must be between 0 and 1000",
    "Min Payment Amount must be between 0 and 50"
  ]
}
```

#### Missing Data (400 Bad Request)

```json
{
  "error": "Validation failed",
  "details": [
    "Missing required field: spending",
    "Missing required field: credit_limit"
  ]
}
```

#### Server Error (500 Internal Server Error)

```json
{
  "error": "Internal server error",
  "message": "Detailed error message for debugging"
}
```

### Response Field Details

**customer_metrics**:
- `engagement_score`: 0-100, measures customer activity level
- `relationship_score`: 0-100, measures customer loyalty
- `customer_segment`: Premium|Growth|At Risk|Dormant
- `customer_health`: 0-100, overall customer status
- `offer_priority`: 1-5, recommended contact priority

**prediction**:
- `subscription_probability`: 0-100, likelihood of conversion
- `confidence`: Low|Medium|High|Very High

**recommendation**:
- `primary_action`: Recommended main strategy
- `secondary_actions`: 2-3 supporting actions
- `priority_level`: Critical|High|Medium|Low
- `reasoning`: Explanation of recommendation
- `next_steps`: Timeline, channel, and implementation notes

---

## GET /api/health

### Purpose
Health check endpoint for monitoring application status.

### Response (200 OK)

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

---

## GET /api/status

### Purpose
Get application status and version information.

### Response (200 OK)

```json
{
  "status": "running",
  "version": "1.0.0",
  "environment": "development"
}
```

---

## Error Handling

### Common Error Scenarios

#### 1. Missing Required Fields
```json
{
  "error": "Validation failed",
  "details": ["Missing required field: spending"]
}
```

#### 2. Invalid Field Type
```json
{
  "error": "Validation failed",
  "details": ["spending must be a number"]
}
```

#### 3. Out of Range Value
```json
{
  "error": "Validation failed",
  "details": ["spending must be between 0 and 1000"]
}
```

#### 4. Negative Values
```json
{
  "error": "Validation failed",
  "details": ["All values must be positive"]
}
```

#### 5. No JSON Data
```json
{
  "error": "No JSON data provided"
}
```

---

## cURL Examples

### Basic Prediction Request

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "spending": 19.94,
    "advance_payments": 16.92,
    "current_balance": 6.675,
    "credit_limit": 3.763,
    "min_payment_amt": 3.252,
    "max_spent_in_single_shopping": 6.55
  }'
```

### Health Check

```bash
curl http://localhost:5000/api/health
```

### Status Check

```bash
curl http://localhost:5000/api/status
```

---

## Python Requests Examples

### Using Python requests library

```python
import requests
import json

# API endpoint
url = "http://localhost:5000/api/predict"

# Customer data
payload = {
    "spending": 19.94,
    "advance_payments": 16.92,
    "current_balance": 6.675,
    "credit_limit": 3.763,
    "min_payment_amt": 3.252,
    "max_spent_in_single_shopping": 6.55
}

# Make request
response = requests.post(url, json=payload)

# Check status
if response.status_code == 200:
    data = response.json()
    print(f"Subscription Probability: {data['prediction']['subscription_probability']}%")
    print(f"Recommendation: {data['recommendation']['primary_action']}")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
```

---

## JavaScript Examples

### Using Fetch API

```javascript
const data = {
    "spending": 19.94,
    "advance_payments": 16.92,
    "current_balance": 6.675,
    "credit_limit": 3.763,
    "min_payment_amt": 3.252,
    "max_spent_in_single_shopping": 6.55
};

fetch('/api/predict', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
})
.then(response => response.json())
.then(data => {
    if (data.status === 'success') {
        console.log(`Probability: ${data.prediction.subscription_probability}%`);
        console.log(`Action: ${data.recommendation.primary_action}`);
    } else {
        console.error('Error:', data.error);
    }
});
```

---

## Rate Limiting & Quotas

Currently no rate limiting implemented. Future versions will include:
- Requests per minute (100/min)
- Concurrent requests limit (10)
- Bulk prediction batch limit (100 customers)

---

## CORS Configuration

CORS is enabled for development. In production, restrict to specific origins:

```python
CORS(app, resources={
    r"/api/*": {"origins": "https://yourdomain.com"}
})
```

---

## Authentication

Currently no authentication required. Future versions will include:
- API key authentication
- OAuth 2.0 integration
- JWT tokens for sessions

---

## Versioning

Current API version: **1.0.0**

Future versioning strategy:
- Base URL versioning: `/api/v1/predict`
- Backward compatibility for 2 versions
- Deprecation notices 6 months in advance

---

## Changelog

### v1.0.0 (Initial Release)
- POST /api/predict - Main prediction endpoint
- GET /api/health - Health check
- GET /api/status - Application status
- Support for 6 customer features
- Dual model comparison (LR + RF)
- Recommendation generation
