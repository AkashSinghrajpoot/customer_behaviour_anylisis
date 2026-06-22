/**
 * Customer Relationship Analytics Dashboard
 * Frontend JavaScript Logic
 */

// Global state
let lastPredictionData = null;
let charts = {};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    console.log('Dashboard initialized');
});

/**
 * Setup event listeners for form interactions
 */
function setupEventListeners() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resetBtn = document.getElementById('resetBtn');
    const themeToggle = document.getElementById('themeToggle');

    analyzeBtn.addEventListener('click', handleAnalyze);
    resetBtn.addEventListener('click', handleReset);
    themeToggle.addEventListener('click', toggleTheme);

    // Enter key support on inputs
    document.querySelectorAll('input[type="number"]').forEach(input => {
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                handleAnalyze();
            }
        });

        input.addEventListener('input', () => {
            updateSidebarSummary();
            updateThemeToggleText();
        });
    });

    // Show sidebar when user engages with the form
    const sidebar = document.getElementById('sidebarSummary');
    if (sidebar) {
        sidebar.classList.add('visible');
    }

    loadTheme();
    updateSidebarSummary();
}

/**
 * Collect customer input data
 */
function collectCustomerData() {
    return {
        spending: parseFloat(document.getElementById('spending').value) || 0,
        advance_payments: parseFloat(document.getElementById('advance_payments').value) || 0,
        current_balance: parseFloat(document.getElementById('current_balance').value) || 0,
        credit_limit: parseFloat(document.getElementById('credit_limit').value) || 0,
        min_payment_amt: parseFloat(document.getElementById('min_payment_amt').value) || 0,
        max_spent_in_single_shopping: parseFloat(document.getElementById('max_spent_in_single_shopping').value) || 0
    };
}

function updateSidebarSummary() {
    const data = collectCustomerData();
    const filledCount = Object.values(data).filter(val => val > 0).length;
    document.getElementById('sidebarValueSummary').textContent = `Fields filled: ${filledCount} / 6`;

    const nearLimit = [];
    if (data.advance_payments > 800) nearLimit.push('Advance payments high');
    if (data.current_balance > 80) nearLimit.push('Balance near max');
    if (data.credit_limit > 80) nearLimit.push('Credit limit close');
    if (data.min_payment_amt > 40) nearLimit.push('Min payment high');
    if (data.max_spent_in_single_shopping > 80) nearLimit.push('Shopping spend high');

    const status = nearLimit.length > 0 ? 'Attention required' : 'Healthy range';
    document.getElementById('sidebarRiskStatus').textContent = `Risk status: ${status}`;
    document.getElementById('sidebarBadge').textContent = status === 'Healthy range' ? 'All clear' : 'Review values';
}

function toggleTheme() {
    const body = document.body;
    const isDark = body.classList.toggle('dark');
    localStorage.setItem('dashboardTheme', isDark ? 'dark' : 'light');
    updateThemeToggleText();
}

function loadTheme() {
    const saved = localStorage.getItem('dashboardTheme') || 'light';
    if (saved === 'dark') {
        document.body.classList.add('dark');
    } else {
        document.body.classList.remove('dark');
    }
    updateThemeToggleText();
}

function updateThemeToggleText() {
    const button = document.getElementById('themeToggle');
    if (!button) return;
    button.textContent = document.body.classList.contains('dark') ? 'Light Mode' : 'Dark Mode';
}

/**
 * Handle customer analysis
 */
async function handleAnalyze() {
    const loading = document.getElementById('loading');
    const analyzeBtn = document.getElementById('analyzeBtn');

    try {
        // Show loading
        loading.classList.add('active');
        analyzeBtn.disabled = true;
        clearAlerts();

        // Collect data
        const customerData = collectCustomerData();

        // Validate
        if (!validateInput(customerData)) {
            return;
        }

        // Call API
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(customerData)
        });

        const result = await response.json();

        if (!response.ok) {
            showAlert('Error: ' + (result.details ? result.details.join(', ') : result.error), 'error');
            return;
        }

        // Store and display results
        lastPredictionData = result;
        displayResults(result);
        showAlert('Analysis completed successfully!', 'success');

    } catch (error) {
        console.error('Analysis error:', error);
        showAlert('Analysis failed: ' + error.message, 'error');
    } finally {
        loading.classList.remove('active');
        analyzeBtn.disabled = false;
    }
}

/**
 * Validate customer input
 */
function validateInput(data) {
    const errors = [];

    // Check for empty fields
    if (data.spending === 0) errors.push('Spending is required');
    if (data.advance_payments === 0) errors.push('Advance payments is required');
    if (data.current_balance === 0) errors.push('Current balance is required');
    if (data.credit_limit === 0) errors.push('Credit limit is required');
    if (data.min_payment_amt === 0) errors.push('Min payment amount is required');
    if (data.max_spent_in_single_shopping === 0) errors.push('Max spent is required');

    // Check for negative values
    const allValues = Object.values(data);
    if (allValues.some(v => v < 0)) {
        errors.push('All values must be positive');
    }

    if (errors.length > 0) {
        showAlert('Validation errors: ' + errors.join(', '), 'error');
        return false;
    }

    return true;
}

/**
 * Display prediction results
 */
function displayResults(result) {
    const resultsSection = document.getElementById('resultsSection');
    const metrics = result.customer_metrics;
    const prediction = result.prediction;
    const recommendation = result.recommendation;

    // Update KPI cards
    document.getElementById('kpiProbability').textContent = 
        prediction.subscription_probability.toFixed(1) + '%';
    document.getElementById('kpiEngagement').textContent = 
        metrics.engagement_score.toFixed(1);
    document.getElementById('kpiRelationship').textContent = 
        metrics.relationship_score.toFixed(1);
    document.getElementById('kpiSegment').textContent = 
        metrics.customer_segment;

    // Update recommendation section
    document.getElementById('recommendationAction').textContent = 
        recommendation.primary_action;
    document.getElementById('recommendationPriority').textContent = 
        recommendation.priority_level;
    document.getElementById('recommendationReasoning').textContent = 
        recommendation.reasoning;

    // Update next steps
    const nextStepsContainer = document.getElementById('nextStepsContainer');
    nextStepsContainer.innerHTML = '';
    const nextSteps = recommendation.next_steps;
    Object.entries(nextSteps).forEach(([key, value]) => {
        const div = document.createElement('div');
        div.className = 'flex items-start gap-2';
        div.innerHTML = `
            <span class="text-blue-500 font-bold mt-1">✓</span>
            <div>
                <div class="font-semibold text-gray-800 capitalize">${key.replace(/_/g, ' ')}</div>
                <div class="text-xs text-gray-600">${value}</div>
            </div>
        `;
        nextStepsContainer.appendChild(div);
    });

    // Update secondary actions
    const secondaryActionsContainer = document.getElementById('secondaryActionsContainer');
    secondaryActionsContainer.innerHTML = '';
    recommendation.secondary_actions.forEach(action => {
        const div = document.createElement('div');
        div.className = 'bg-blue-50 border-l-4 border-blue-500 p-3 rounded text-sm';
        div.innerHTML = `
            <span class="text-blue-600 font-semibold">→</span> ${action}
        `;
        secondaryActionsContainer.appendChild(div);
    });

    // Update charts
    updateCharts(metrics, result);

    // Show results
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Update all dashboard charts
 */
function updateCharts(metrics, fullResult) {
    updateMetricsChart(metrics);
    updateScoreChart(metrics);
    updateSpendingChart(fullResult);
    updateHealthChart(metrics);
}

/**
 * Update metrics radar chart
 */
function updateMetricsChart(metrics) {
    const ctx = document.getElementById('metricsChart').getContext('2d');

    // Destroy existing chart
    if (charts.metrics) {
        charts.metrics.destroy();
    }

    const data = {
        labels: ['Engagement', 'Relationship', 'Health', 'Offer Priority'],
        datasets: [{
            label: 'Customer Metrics',
            data: [
                metrics.engagement_score,
                metrics.relationship_score,
                metrics.customer_health,
                metrics.offer_priority * 20  // Scale to 0-100
            ],
            fill: true,
            backgroundColor: 'rgba(14, 165, 233, 0.18)',
            borderColor: '#0ea5e9',
            pointBackgroundColor: '#0ea5e9',
            pointBorderColor: '#f8fafc',
            pointBorderWidth: 2,
            pointRadius: 6,
            pointHoverRadius: 8,
            tension: 0.4
        }]
    };

    charts.metrics = new Chart(ctx, {
        type: 'radar',
        data: data,
        options: {
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        stepSize: 20
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom'
                }
            }
        }
    });
}

/**
 * Update score distribution chart
 */
function updateScoreChart(metrics) {
    const ctx = document.getElementById('scoreChart').getContext('2d');

    if (charts.score) {
        charts.score.destroy();
    }

    const data = {
        labels: ['Engagement', 'Relationship', 'Health'],
        datasets: [{
            label: 'Scores (/100)',
            data: [
                metrics.engagement_score,
                metrics.relationship_score,
                metrics.customer_health
            ],
            backgroundColor: [
                'rgba(248, 113, 113, 0.85)',
                'rgba(56, 189, 248, 0.85)',
                'rgba(96, 165, 250, 0.85)'
            ],
            borderRadius: 8,
            borderWidth: 0
        }]
    };

    charts.score = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            indexAxis: 'y',
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

/**
 * Update spending analysis chart
 */
function updateSpendingChart(fullResult) {
    const ctx = document.getElementById('spendingChart').getContext('2d');

    if (charts.spending) {
        charts.spending.destroy();
    }

    const spending = parseFloat(document.getElementById('spending').value) || 0;
    const advance = parseFloat(document.getElementById('advance_payments').value) || 0;
    const balance = parseFloat(document.getElementById('current_balance').value) || 0;

    const data = {
        labels: ['Spending', 'Advance Payments', 'Current Balance'],
        datasets: [{
            label: 'Amount ($)',
            data: [spending, advance, balance],
            backgroundColor: [
                'rgba(59, 130, 246, 0.85)',
                'rgba(6, 182, 212, 0.85)',
                'rgba(248, 113, 113, 0.85)'
            ],
            borderRadius: 8,
            borderWidth: 0
        }]
    };

    charts.spending = new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: {
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

/**
 * Update health score gauge
 */
function updateHealthChart(metrics) {
    const ctx = document.getElementById('healthChart').getContext('2d');

    if (charts.health) {
        charts.health.destroy();
    }

    const health = metrics.customer_health;
    const remaining = 100 - health;

    const data = {
        labels: ['Customer Health', 'Remaining'],
        datasets: [{
            data: [health, remaining],
            backgroundColor: [
                health > 75 ? 'rgba(22, 163, 74, 0.8)' : 
                health > 50 ? 'rgba(251, 146, 60, 0.8)' : 
                'rgba(220, 38, 38, 0.8)',
                'rgba(209, 213, 219, 0.3)'
            ],
            borderWidth: 0,
            circumference: 180,
            rotation: 270
        }]
    };

    charts.health = new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: {
            plugins: {
                tooltip: {
                    enabled: true
                },
                legend: {
                    display: false
                }
            },
            cutout: '70%'
        }
    });
}

/**
 * Handle reset form
 */
function handleReset() {
    document.querySelectorAll('input[type="number"]').forEach(input => {
        input.value = '';
    });

    document.getElementById('resultsSection').style.display = 'none';
    clearAlerts();
    lastPredictionData = null;
    updateSidebarSummary();

    // Destroy charts
    Object.values(charts).forEach(chart => {
        if (chart) chart.destroy();
    });
    charts = {};
}

/**
 * Show alert message
 */
function showAlert(message, type) {
    const container = document.getElementById('alert-container');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} show`;
    alert.innerHTML = message;
    container.appendChild(alert);

    setTimeout(() => {
        alert.remove();
    }, 5000);
}

/**
 * Clear all alerts
 */
function clearAlerts() {
    document.getElementById('alert-container').innerHTML = '';
}
