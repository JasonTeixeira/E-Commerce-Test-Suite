# Security Testing

OWASP Top 10 security tests for DemoBlaze.

## Overview

**15 security tests** covering common vulnerabilities and attack vectors.

## Test Categories

### 1. Injection Vulnerabilities (3 tests) - OWASP A03
- SQL injection in login
- SQL injection in signup  
- XSS payload handling

### 2. Authentication Security (4 tests) - OWASP A07
- Weak password acceptance
- Brute force protection
- Session token randomness
- Password exposure in responses

### 3. Security Headers (3 tests) - OWASP A05
- Security headers presence
- HTTPS enforcement
- CORS configuration

### 4. Input Validation (3 tests) - OWASP A03
- Special characters handling
- Integer overflow
- Negative values

### 5. Authorization Security (2 tests) - OWASP A01
- Cart access without cookie
- Unauthorized cart access

### 6. Cryptographic Security (2 tests) - OWASP A02
- Password storage
- SSL certificate validation

### 7. Security Misconfigurations (2 tests) - OWASP A05
- Verbose error messages
- Directory listing

---

## Running Security Tests

```bash
# All security tests
pytest security/tests/ -v

# With marker
pytest -m security -v

# Generate report
pytest security/tests/ --html=reports/security.html
```

---

## OWASP Coverage

✅ **A01:2021** – Broken Access Control  
✅ **A02:2021** – Cryptographic Failures  
✅ **A03:2021** – Injection  
✅ **A05:2021** – Security Misconfiguration  
✅ **A07:2021** – Identification & Authentication Failures  

---

## Security Testing Best Practices

1. **Never test production systems** without permission
2. **Document all findings** with severity ratings
3. **Report vulnerabilities** responsibly
4. **Verify fixes** with regression tests
5. **Keep tests up to date** with OWASP updates

---

## Extending Security Tests

To add OWASP ZAP integration:

```python
from zapv2 import ZAPv2

zap = ZAPv2(apikey='your-key')
zap.urlopen('https://www.demoblaze.com')
zap.spider.scan('https://www.demoblaze.com')
```

To add Burp Suite integration, use the Burp REST API.

---

## Key Findings Template

Document security test results:

```markdown
## Finding: [Vulnerability Name]

**Severity**: Critical/High/Medium/Low
**OWASP**: A0X
**CWE**: XXX

**Description**: 
**Impact**: 
**Steps to Reproduce**:
**Remediation**:
```

---

## Next Steps

1. Integrate OWASP ZAP for automated scanning
2. Add penetration testing scenarios
3. Implement security regression suite
4. Set up security scanning in CI/CD
5. Create security dashboard
