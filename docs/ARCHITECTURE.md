# Architecture Decision Records

## Overview

This document records key architectural decisions and their rationales for the Customer Relationship Analytics Dashboard project.

---

## Decision 1: Modular Service Architecture

**Status**: ✅ Implemented

**Decision**: Separate business logic into distinct service modules (preprocessing, prediction, recommendation)

### Rationale
- **Maintainability**: Each service has single responsibility
- **Testability**: Easy to unit test individual services
- **Reusability**: Services can be used independently
- **Scalability**: Services can be deployed separately if needed

### Implementation
```
backend/services/
├── preprocessing.py    # Data handling
├── prediction.py       # ML models
└── recommendation.py   # Business logic
```

### Trade-offs
- ✅ Pros: Clean code, easy testing, flexible
- ❌ Cons: Multiple files to maintain, slightly more overhead

---

## Decision 2: Dual Model Comparison (Logistic Regression + Random Forest)

**Status**: ✅ Implemented

**Decision**: Train both models and auto-select best performer

### Rationale
- **Reliability**: Compare models objectively
- **Learning**: Demonstrate ML knowledge (not just picking one)
- **Robustness**: If one model fails, fallback to other
- **Interview Prep**: Shows model selection methodology

### Implementation
```python
class ModelComparison:
    def add_model(self, name, model, metrics):
        # Track best model by F1 score
        
    def get_best_model(self):
        # Return best performing model
```

### Metrics Used
- Accuracy: Overall correctness
- Precision: True positive rate
- Recall: Coverage of positive cases
- F1: Balanced precision-recall
- AUC: ROC curve area

### Trade-offs
- ✅ Pros: Better decision making, demonstrates rigor
- ❌ Cons: More training time, more complex

---

## Decision 3: Business-First Feature Engineering

**Status**: ✅ Implemented

**Decision**: Generate interpretable business metrics (engagement_score, relationship_score) alongside ML features

### Rationale
- **Business Value**: Scores explain what customers will understand
- **Transparency**: Not just "prediction = 75%"
- **Actionability**: Metrics directly drive recommendations
- **Explainability**: Interview candidates can explain scoring

### Metrics Generated
1. **Engagement Score** (0-100): Activity level
   - Formula: 40% spending + 30% payment_discipline + 30% consistency
   
2. **Relationship Score** (0-100): Loyalty indicator
   - Formula: 50% balance_utilization + 50% spending_efficiency
   
3. **Customer Health** (0-100): Overall status
   - Formula: 40% engagement + 60% relationship
   
4. **Customer Segment**: Classification
   - Premium: High engagement + high relationship
   - Growth: Moderate on both
   - At Risk: Low engagement
   - Dormant: Very low both

### Trade-offs
- ✅ Pros: Interpretable, actionable, business-aligned
- ❌ Cons: Additional computation, requires business input

---

## Decision 4: Recommendation Engine with Business Rules

**Status**: ✅ Implemented

**Decision**: Don't just output predictions, add layer of business recommendations

### Rationale
- **Practical Value**: "What should we DO with this prediction?"
- **Portfolio Strength**: Shows beyond-ML thinking
- **Real-world Relevance**: Banks need actions, not just numbers
- **Interview Edge**: Demonstrates product thinking

### Recommendation Strategy
```python
if high_balance AND high_probability:
    → "Offer Premium Services"
elif low_engagement AND high_relationship:
    → "Personalized Follow-up"
elif high_spending_efficiency AND low_probability:
    → "Reduce Outreach"
```

### Trade-offs
- ✅ Pros: Adds business value, professional appearance
- ❌ Cons: Needs business expertise, hard to validate

---

## Decision 5: Frontend-Backend Separation

**Status**: ✅ Implemented

**Decision**: Flask backend + HTML/CSS/JS frontend, communicating via REST API

### Rationale
- **Separation of Concerns**: Frontend doesn't know about ML
- **Testability**: Backend can be tested independently
- **Scalability**: Frontend and backend can scale separately
- **Maintainability**: Clear contract between layers

### Architecture
```
Frontend (HTML/CSS/JS)
         ↓ (HTTP/JSON)
Flask REST API
         ↓
Business Services
         ↓
ML Models & Data
```

### Trade-offs
- ✅ Pros: Clean architecture, independent deployment
- ❌ Cons: More files, requires API contract management

---

## Decision 6: Real-time Chart Updates with Chart.js

**Status**: ✅ Implemented

**Decision**: Use client-side Chart.js for dynamic visualizations

### Rationale
- **Performance**: No server-side rendering needed
- **Interactivity**: Charts update instantly on new predictions
- **Simplicity**: No additional server dependencies
- **Polish**: Improves user experience significantly

### Charts Implemented
1. **Metrics Radar**: Multi-dimensional view
2. **Score Distribution**: Engagement vs Relationship vs Health
3. **Spending Analysis**: Financial breakdown
4. **Health Gauge**: Visual indicator

### Trade-offs
- ✅ Pros: Responsive, professional appearance
- ❌ Cons: Requires JavaScript knowledge, client-side processing

---

## Decision 7: CSV Storage with MySQL Extensibility

**Status**: ✅ Implemented

**Decision**: Use CSV for initial storage, but design for MySQL migration

### Rationale
- **Simplicity**: No database setup required for local development
- **Version Control**: CSV files can be committed to git
- **Extensibility**: Architecture ready for MySQL later
- **Portability**: Easy to share via file sharing

### CSV Structure
```
data/
├── raw/
│   └── bank_marketing_part1_Data.csv
└── processed/
```

### MySQL Migration Plan
```python
# Future: SQLAlchemy ORM
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://user:pass@localhost/db')
df.to_sql('customers', engine)
```

### Trade-offs
- ✅ Pros: Simple, portable, no setup
- ❌ Cons: Not suitable for production-scale, no ACID guarantees

---

## Decision 8: Comprehensive Input Validation

**Status**: ✅ Implemented

**Decision**: Validate all inputs before processing

### Rationale
- **Security**: Prevent malicious data
- **Reliability**: Fail fast with clear errors
- **UX**: User-friendly error messages
- **Data Quality**: Ensures consistent processing

### Validation Layers
1. **Type Validation**: Ensure numeric types
2. **Range Validation**: Check min/max bounds
3. **Missing Value Detection**: All fields required
4. **Negative Value Check**: No negative amounts

### Trade-offs
- ✅ Pros: Robust, user-friendly, prevents bugs
- ❌ Cons: More code, validation logic to maintain

---

## Decision 9: Logging Throughout Application

**Status**: ✅ Implemented

**Decision**: Add logging at every significant step

### Rationale
- **Debugging**: Track what happened in production
- **Monitoring**: Identify performance issues
- **Audit Trail**: Record all predictions
- **Development**: Fast issue resolution

### Logging Levels
```python
logger.debug()     # Development details
logger.info()      # Important events (predictions, model selection)
logger.warning()   # Potential issues (missing models)
logger.error()     # Error conditions
```

### Trade-offs
- ✅ Pros: Easy debugging, professional monitoring
- ❌ Cons: Overhead, needs log rotation strategy

---

## Decision 10: Render-Compatible Deployment

**Status**: ✅ Implemented

**Decision**: Design for Render deployment platform

### Rationale
- **Accessibility**: Easy deployment for beginners
- **Free Tier**: Good for portfolio projects
- **Simplicity**: No complex DevOps setup
- **Industry Standard**: Used by many startups

### Configuration
- Python 3.8+ compatible
- requirements.txt for dependencies
- Procfile ready
- Environment variables configured

### Trade-offs
- ✅ Pros: Easy deployment, widely supported
- ❌ Cons: Less flexibility than custom setup

---

## Future Architecture Decisions

### D11: WebSocket for Real-time Updates
Would implement for live analytics dashboard

### D12: Cache Layer (Redis)
For frequently accessed predictions

### D13: Async Task Queue (Celery)
For batch predictions

### D14: Advanced ML (XGBoost, Neural Networks)
If accuracy becomes critical

### D15: Multi-tenant Architecture
If converting to SaaS

---

## Architecture Diagram

```
┌─────────────────────────────────────┐
│      Client Browser                 │
│  HTML/CSS/Tailwind + Chart.js        │
└──────────────────┬──────────────────┘
                   │ JSON/HTTP
                   ↓
┌─────────────────────────────────────┐
│    Flask REST API (app.py)          │
│  - Route handling                   │
│  - Error handling                   │
│  - Logging                          │
└──────────────────┬──────────────────┘
                   │
        ┌──────────┼──────────┐
        ↓          ↓          ↓
    ┌────────┐ ┌────────┐ ┌────────┐
    │  Validation  │ │  Processing  │ │  Prediction │
    │  (validators)│ │(preprocessing)│ │ (models)   │
    └────────┘ └────────┘ └────────┘
        ↓          ↓          ↓
        └──────────┼──────────┘
                   ↓
    ┌─────────────────────────────────┐
    │  Recommendation Engine          │
    │  (Business Rules)               │
    └──────────────────┬──────────────┘
                       ↓
    ┌─────────────────────────────────┐
    │  Response JSON                  │
    │  - Metrics                      │
    │  - Predictions                  │
    │  - Recommendations              │
    └─────────────────────────────────┘
```

---

## Key Architectural Patterns Used

### 1. Service Layer Pattern
Business logic separated into services

### 2. Factory Pattern
Flask app creation via `create_app()`

### 3. Strategy Pattern
Multiple model strategies (LR vs RF)

### 4. Pipeline Pattern
Data flows through preprocessing → prediction → recommendation

### 5. Template Method Pattern
Consistent validation and error handling

---

## Scalability Considerations

### Current Capacity
- Single-threaded Flask server
- In-memory model storage
- CSV file-based persistence
- ~100 predictions/sec capacity

### Scaling Strategy
1. **Phase 1** (Current): Single server, CSV storage
2. **Phase 2**: Database (MySQL), connection pooling
3. **Phase 3**: Load balancing, caching (Redis)
4. **Phase 4**: Async processing (Celery), message queues
5. **Phase 5**: Microservices (separate prediction service)

---

## Security Architecture

### Current Implementation
- ✅ Input validation on all endpoints
- ✅ Error messages don't expose internals
- ✅ Type checking
- ✅ CORS configured

### Future Hardening
- 🔄 Authentication (OAuth/JWT)
- 🔄 Rate limiting
- 🔄 SQL injection prevention (prepare for DB)
- 🔄 HTTPS enforcement
- 🔄 API versioning with deprecation

---

## Testing Strategy

### Unit Tests
- Validators (test_validation.py)
- Preprocessing (test_preprocessing.py)
- Prediction (test_prediction.py)

### Integration Tests
- API endpoints (test_api.py)
- Full pipeline

### Manual Testing
- Dashboard interactions
- Edge cases in UI
- Browser compatibility

---

## Performance Optimization

### Current
- Direct model inference (< 20ms)
- Efficient NumPy operations
- Minimal data copying

### Future
- Model quantization for faster inference
- Caching of frequent predictions
- Batch prediction optimization
- GPU acceleration for large batches

---

## Decision Log

| Date | Decision | Status | Impact |
|------|----------|--------|--------|
| 2024-01-01 | Modular services | ✅ | Clean code |
| 2024-01-01 | Dual model comparison | ✅ | Better reliability |
| 2024-01-01 | Business metrics | ✅ | Increased value |
| 2024-01-02 | Flask + HTML frontend | ✅ | Clean architecture |
| 2024-01-02 | Chart.js visualizations | ✅ | Better UX |
| 2024-01-03 | CSV with MySQL path | ✅ | Flexibility |

---

**Document Version**: 1.0.0  
**Last Updated**: 2024-01-15  
**Maintained By**: Development Team
