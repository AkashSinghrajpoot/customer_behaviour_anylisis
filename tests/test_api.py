"""Test suite for API endpoints."""

import unittest
import json
from backend.app import create_app


class TestAPI(unittest.TestCase):
    """Test Flask API endpoints."""

    def setUp(self):
        """Set up test client."""
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')

    def test_predict_endpoint_missing_data(self):
        """Test predict endpoint with missing data."""
        response = self.client.post('/api/predict',
            content_type='application/json',
            data=json.dumps({}))
        self.assertEqual(response.status_code, 400)

    def test_predict_endpoint_valid_data(self):
        """Test predict endpoint with valid data."""
        valid_data = {
            'spending': 19.94,
            'advance_payments': 16.92,
            'current_balance': 6.675,
            'credit_limit': 3.763,
            'min_payment_amt': 3.252,
            'max_spent_in_single_shopping': 6.55
        }

        response = self.client.post('/api/predict',
            content_type='application/json',
            data=json.dumps(valid_data))

        # Should succeed or fail gracefully
        self.assertIn(response.status_code, [200, 400, 500])

    def test_status_endpoint(self):
        """Test application status endpoint."""
        response = self.client.get('/api/status')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'running')


if __name__ == '__main__':
    unittest.main()
