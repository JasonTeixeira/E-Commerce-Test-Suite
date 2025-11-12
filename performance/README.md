# Performance Testing

Comprehensive performance and load testing for DemoBlaze.

## Overview

This suite includes:
- **20 pytest performance tests** - Response time, throughput, metrics validation
- **Locust load testing** - Simulate realistic user behavior and load patterns

**Total: 20+ performance tests**

---

## Test Categories

### 1. API Performance (5 tests)
- Response time thresholds
- Average response time over multiple requests
- Login performance
- Cart operations performance
- Concurrent request handling

### 2. Response Time Consistency (2 tests)
- Response time variance
- Performance degradation detection

### 3. Throughput (2 tests)
- Requests per second
- Burst traffic handling

### 4. Endpoint Performance (3 tests)
- Signup endpoint
- Cart view endpoint
- Order placement endpoint

### 5. Load Scenarios (2 tests)
- Sequential user journey
- Repeated operations

### 6. Performance Metrics (4 tests)
- P95 response time
- P99 response time
- Success rate under load
- Error rate threshold

---

## Running Performance Tests

### Run all performance tests
```bash
pytest performance/tests/test_performance.py -v
```

### Run with performance marker
```bash
pytest -m performance -v
```

### Run slow tests (excluded by default)
```bash
pytest -m "performance and slow" -v
```

### Generate performance report
```bash
pytest performance/tests/ --html=reports/performance.html -v
```

---

## Locust Load Testing

### Install Locust
```bash
pip install locust
```

### Run Locust web UI
```bash
locust -f performance/locust/locustfile.py --host https://www.demoblaze.com
```

Then open http://localhost:8089

### Run Locust headless
```bash
# 10 users, 2 users/sec spawn rate, 60 second duration
locust -f performance/locust/locustfile.py \
  --host https://www.demoblaze.com \
  --users 10 \
  --spawn-rate 2 \
  --run-time 60s \
  --headless \
  --html reports/locust_report.html
```

### User Types in Locust

1. **DemoBlazeUser** - General browsing and shopping
2. **BrowsingUser** - Heavy browser (80% browsing, 20% other)
3. **ShoppingUser** - Purchase-focused (60% shopping, 40% other)
4. **FastUser** - Quick operations (1-3s wait)
5. **RealisticUser** - Human-like behavior (2-5s wait)

---

## Performance Thresholds

| Metric | Threshold |
|--------|-----------|
| API Response Time | < 2.0s |
| Login Time | < 2.0s |
| Cart Operations | < 2.0s |
| Order Placement | < 3.0s |
| P95 Response Time | < 3.0s |
| P99 Response Time | < 5.0s |
| Requests/Second | ≥ 5 |
| Success Rate | ≥ 95% |
| Error Rate | ≤ 5% |

---

## Test Structure

```
performance/
├── locust/
│   └── locustfile.py         # Load testing scenarios
├── tests/
│   └── test_performance.py   # Pytest performance tests
├── reports/                  # Generated reports
└── README.md                 # This file
```

---

## Key Features

✅ Response time benchmarking  
✅ Throughput testing  
✅ Concurrent request handling  
✅ Performance degradation detection  
✅ P95/P99 metrics  
✅ Load testing with Locust  
✅ Multiple user behavior patterns  
✅ Burst traffic simulation  
✅ End-to-end journey performance  

---

## CI/CD Integration

Performance tests can be integrated into CI/CD pipelines:

```yaml
# GitHub Actions example
- name: Run Performance Tests
  run: pytest -m performance --maxfail=5

- name: Run Load Tests
  run: |
    locust -f performance/locust/locustfile.py \
      --host https://www.demoblaze.com \
      --users 5 \
      --spawn-rate 1 \
      --run-time 30s \
      --headless
```

---

## Next Steps

1. Establish baseline performance metrics
2. Set up performance monitoring dashboards
3. Create performance regression alerts
4. Integrate with APM tools (New Relic, DataDog, etc.)
5. Add database query performance tests
6. Test with production-like data volumes
