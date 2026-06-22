# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Prerequisites Check
```bash
python --version  # Should be 3.8+
pip --version     # Should be present
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python run.py develop
```

You should see:
```
INFO - Starting Flask development server...
WARNING - Running on http://0.0.0.0:5000 (Press CTRL+C to quit)
```

### 4. Open in Browser
Navigate to: **http://localhost:5000**

### 5. Try a Prediction
1. Fill in the form with customer data:
   - Spending: 19.94
   - Advance Payments: 16.92
   - Current Balance: 6.675
   - Credit Limit: 3.763
   - Min Payment Amount: 3.252
   - Max Spent: 6.55

2. Click **"Analyze Customer"**

3. View results:
   - KPI cards with metrics
   - Recommendation
   - Interactive charts

---

## 📁 Project Structure at a Glance

```
customer_relationship_analytics_dashboard/
├── backend/              # Python backend (Flask)
│   ├── app.py           # Flask app
│   ├── routes/          # API endpoints
│   ├── services/        # Business logic
│   └── utils/           # Utilities
├── frontend/            # Web frontend
│   ├── templates/       # HTML files
│   └── static/js        # JavaScript
├── data/               # Data files
├── tests/              # Unit tests
├── docs/               # Documentation
├── run.py              # Main entry point
└── README.md           # Full documentation
```

---

## 🔧 Common Tasks

### Train ML Models
```bash
python run.py develop
# Models train automatically on first run
```

### Run Tests
```bash
python -m pytest tests/ -v
```

### Check API Status
```bash
curl http://localhost:5000/api/health
```

### Make Prediction via API
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

---

## ⚠️ Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution**: `pip install -r requirements.txt`

### Issue: "Address already in use"
**Solution**: Change port in `run.py` or kill existing process on 5000

### Issue: "No data found" error
**Solution**: Ensure `data/bank_marketing_part1_Data.csv` exists

### Issue: "Template not found"
**Solution**: Ensure you run from project root: `cd customer_relationship_analytics_dashboard`

### Issue: Models not loading
**Solution**: First run automatically trains models. Wait for completion.

---

## 📚 Learn More

- Full documentation: See [README.md](README.md)
- API reference: See [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)
- Architecture details: See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- Interview prep: See [docs/INTERVIEW_GUIDE.md](docs/INTERVIEW_GUIDE.md)

---

## 🎯 Next Steps

1. **Explore the Code**: 
   - Start with `backend/app.py`
   - Check `backend/services/` for business logic
   - Review `frontend/templates/dashboard.html` for UI

2. **Run Tests**:
   - `python -m pytest tests/test_validation.py -v`
   - `python -m pytest tests/test_api.py -v`

3. **Deploy**:
   - Push to GitHub
   - Connect to Render
   - It's live!

4. **Customize**:
   - Add more features
   - Integrate database
   - Deploy on your server

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Application runs (`python run.py develop`)
- [ ] Dashboard accessible (http://localhost:5000)
- [ ] Form can be filled and submitted
- [ ] Results display correctly
- [ ] Charts render properly
- [ ] API endpoint works (`/api/predict`)
- [ ] Health check passes (`/api/health`)

---

## 💡 Tips

- **Faster Startup**: Models only train if not found, so first run is slow
- **Debug Mode**: Open browser DevTools (F12) to see API calls
- **Terminal Logs**: All important events logged—watch for errors
- **Hot Reload**: Flask auto-reloads on code changes in dev mode

---

## 🆘 Need Help?

1. Check the full README: [README.md](README.md)
2. Review API docs: [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)
3. Understand architecture: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
4. Prepare for interviews: [docs/INTERVIEW_GUIDE.md](docs/INTERVIEW_GUIDE.md)

---

**You're all set! Start exploring the application and have fun! 🚀**
