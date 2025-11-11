# E-Commerce Test Automation Suite 🛒

[![CI/CD](https://github.com/JasonTeixeira/E-Commerce-Test-Suite/actions/workflows/main.yml/badge.svg)](https://github.com/JasonTeixeira/E-Commerce-Test-Suite/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/playwright-1.41-green.svg)](https://playwright.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Enterprise-grade full-stack test automation framework with 300+ tests covering UI, API, Performance, Security, Accessibility, and Integration testing for e-commerce applications.**

## 🎯 Project Overview

This comprehensive testing framework demonstrates professional QA automation across the entire testing pyramid, showcasing expertise in:

- ✅ **UI Automation** (80+ tests) - Playwright + Selenium
- ✅ **API Testing** (60+ tests) - REST API validation
- ✅ **Visual Regression** (30+ tests) - Screenshot comparison
- ✅ **Performance Testing** (20+ scenarios) - Locust load testing
- ✅ **Security Testing** (15+ scans) - OWASP ZAP integration
- ✅ **Accessibility Testing** (25+ tests) - WCAG 2.1 AA compliance
- ✅ **Integration Testing** (30+ workflows) - E2E user journeys
- ✅ **Database Testing** (20+ tests) - Data integrity validation
- ✅ **Contract Testing** (15+ contracts) - API contract verification
- ✅ **Mobile Testing** (40+ tests) - Responsive design validation

**Total: 300+ Professional Tests | 10,000+ Lines of Production Code**

## 📊 Test Coverage Matrix

| Test Type | Tests | Coverage | Tool/Framework |
|-----------|-------|----------|----------------|
| **UI Tests** | 80+ | Login, Products, Cart, Checkout | Playwright, Selenium |
| **API Tests** | 60+ | CRUD, Auth, Data validation | Requests, httpx |
| **Visual Tests** | 30+ | Critical pages, components | Pillow, OpenCV |
| **Performance** | 20+ | Load, stress, spike testing | Locust, K6 |
| **Security** | 15+ | XSS, SQL injection, auth bypass | OWASP ZAP |
| **Accessibility** | 25+ | WCAG compliance, screen readers | axe-core |
| **Integration** | 30+ | Complete user workflows | Pytest |
| **Database** | 20+ | Data integrity, constraints | SQLAlchemy |
| **Contract** | 15+ | API contracts, schemas | Pact |
| **Mobile** | 40+ | Responsive, mobile-first | Playwright mobile |
| **Total** | **300+** | **Full-stack coverage** | **Multi-framework** |

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CI/CD Pipeline (20+ jobs)                 │
│  Quality Checks | UI Tests | API Tests | Performance | Security│
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Test Execution Layer                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │    UI    │ │   API    │ │   Perf   │ │ Security │      │
│  │  Tests   │ │  Tests   │ │  Tests   │ │  Tests   │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     Framework Layer                          │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Page Objects | API Clients | Data Models | Utils  │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  Application Under Test                      │
│                    DemoBlaze E-Commerce                      │
│                 (https://www.demoblaze.com)                  │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+ (for Playwright)
- Docker (optional, for containerized execution)

### Installation

```bash
# Clone repository
git clone https://github.com/JasonTeixeira/E-Commerce-Test-Suite.git
cd E-Commerce-Test-Suite

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Copy environment configuration
cp .env.example .env
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test suites
pytest ui_tests/           # UI tests only
pytest api_tests/          # API tests only
pytest performance/        # Performance tests
pytest security/           # Security scans
pytest accessibility/      # Accessibility tests

# Run by markers
pytest -m smoke           # Smoke tests
pytest -m regression      # Full regression
pytest -m critical        # Critical path tests

# Parallel execution
pytest -n 8               # 8 parallel workers

# Generate reports
pytest --html=reports/html/report.html --self-contained-html
pytest --alluredir=reports/allure-results

# With coverage
pytest --cov=. --cov-report=html --cov-report=term
```

## 📁 Project Structure

```
E-Commerce-Test-Suite/
├── ui_tests/                    # UI automation tests
│   ├── pages/                  # Page Object Models
│   │   ├── base_page.py       # Base page class
│   │   ├── home_page.py       # Home page
│   │   ├── login_page.py      # Login page
│   │   ├── product_page.py    # Product catalog
│   │   ├── cart_page.py       # Shopping cart
│   │   └── checkout_page.py   # Checkout flow
│   ├── tests/                 # UI test suites
│   │   ├── test_login.py      # 15+ login tests
│   │   ├── test_products.py   # 20+ product tests
│   │   ├── test_cart.py       # 20+ cart tests
│   │   └── test_checkout.py   # 25+ checkout tests
│   ├── fixtures/              # UI test fixtures
│   └── visual/                # Visual regression tests
│
├── api_tests/                  # API testing
│   ├── clients/               # API client layer
│   ├── tests/                 # API test suites
│   ├── schemas/               # Pydantic models
│   └── data/                  # Test data
│
├── performance/                # Performance testing
│   ├── locust/                # Locust load tests
│   └── k6/                    # K6 performance tests
│
├── security/                   # Security testing
│   ├── zap/                   # OWASP ZAP scripts
│   └── tests/                 # Security test suites
│
├── accessibility/              # Accessibility testing
│   ├── tests/                 # a11y test suites
│   └── reports/               # Accessibility reports
│
├── integration/                # Integration tests
│   ├── workflows/             # E2E workflows
│   └── tests/                 # Integration test suites
│
├── utils/                      # Shared utilities
│   ├── helpers/               # Helper functions
│   ├── logger/                # Custom logging
│   ├── data_factory/          # Test data generation
│   └── reporters/             # Custom reporters
│
├── config/                     # Configuration
│   ├── environments/          # Environment configs
│   └── settings/              # Settings management
│
├── reports/                    # Test reports
│   ├── html/                  # HTML reports
│   ├── allure/                # Allure reports
│   └── coverage/              # Coverage reports
│
├── docs/                       # Documentation
│   ├── architecture/          # Architecture docs
│   ├── guides/                # User guides
│   └── examples/              # Code examples
│
├── .github/workflows/          # CI/CD pipelines
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Project configuration
├── docker-compose.yml         # Docker orchestration
└── README.md                  # This file
```

## 🎯 Test Types

### 1. UI Automation Tests (80+)

**Coverage:**
- User authentication (login, logout, session management)
- Product browsing (catalog, search, filters, sorting)
- Shopping cart (add, remove, update quantities)
- Checkout process (forms, validation, order completion)
- Navigation (menus, breadcrumbs, links)
- Responsive design (mobile, tablet, desktop)

**Technologies:** Playwright, Selenium, Page Object Model

### 2. API Tests (60+)

**Coverage:**
- Product API (CRUD operations)
- User API (authentication, profile management)
- Cart API (session management, operations)
- Order API (creation, tracking)
- Schema validation (Pydantic models)
- Error handling (4xx, 5xx responses)

**Technologies:** Requests, httpx, Pydantic

### 3. Visual Regression Tests (30+)

**Coverage:**
- Homepage layout
- Product pages
- Cart page
- Checkout flow
- Component rendering
- Cross-browser consistency

**Technologies:** Pillow, OpenCV, Playwright screenshots

### 4. Performance Tests (20+)

**Coverage:**
- User load testing (100, 500, 1000 users)
- API stress testing
- Page load times
- Checkout flow performance
- Spike testing
- Endurance testing

**Technologies:** Locust, K6

### 5. Security Tests (15+)

**Coverage:**
- XSS vulnerabilities
- SQL injection attempts
- Authentication bypass
- CSRF protection
- Input validation
- Security headers

**Technologies:** OWASP ZAP, Bandit

### 6. Accessibility Tests (25+)

**Coverage:**
- WCAG 2.1 Level AA compliance
- Screen reader compatibility
- Keyboard navigation
- Color contrast
- ARIA attributes
- Focus management

**Technologies:** axe-core, pa11y

## 📈 CI/CD Pipeline

### GitHub Actions Workflow (20+ jobs)

```
Code Quality → Lint/Format → Type Check
      ↓
  UI Tests → API Tests → Visual Tests
      ↓
Performance → Security → Accessibility
      ↓
Integration Tests → Coverage Analysis
      ↓
    Reports → Notifications
```

**Features:**
- Parallel execution across test types
- Matrix testing (multiple browsers, OS)
- Automated reporting (Allure, HTML)
- Coverage tracking (>85% target)
- Security scanning
- Performance benchmarking

## 🐳 Docker Support

```bash
# Build images
docker-compose build

# Run all tests
docker-compose up test-runner

# Run specific suites
docker-compose up ui-tests
docker-compose up api-tests
docker-compose up performance-tests
```

## 📊 Reporting

### Allure Reports

```bash
# Generate Allure report
allure serve reports/allure-results
```

**Features:**
- Test execution timeline
- Historical trends
- Failure analysis
- Screenshots and videos
- Request/response logs

### Coverage Reports

```bash
# Generate coverage report
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

**Target:** >85% code coverage

## 🎓 What This Project Demonstrates

### Technical Excellence

- **Multi-Framework Mastery**: Playwright, Selenium, Requests, Locust, OWASP ZAP
- **Test Architecture**: Page Object Model, API clients, data factories
- **Design Patterns**: Factory, Builder, Strategy, Observer
- **Clean Code**: Type hints, docstrings, SOLID principles
- **Test Strategy**: Complete testing pyramid coverage

### Professional Practices

- **CI/CD Integration**: 20+ automated jobs
- **Code Quality**: Linting, formatting, type checking
- **Documentation**: Comprehensive guides and examples
- **Security**: Security-first testing approach
- **Accessibility**: WCAG compliance testing
- **Performance**: Load and stress testing
- **Scalability**: Parallel execution, containerization

### QA Leadership Skills

- **Framework Design**: Scalable, maintainable architecture
- **Tool Selection**: Best-in-class tools for each test type
- **Strategy Development**: Complete test coverage planning
- **Team Enablement**: Comprehensive documentation
- **Quality Metrics**: Coverage, performance, security tracking

## 💼 Portfolio Highlights

**For Senior QA/SDET Roles:**
- 300+ production-grade tests
- 10,000+ lines of code
- 10 different testing types
- Complete CI/CD integration
- Enterprise-grade architecture

**Resume Bullets:**
- "Architected full-stack test automation framework with 300+ tests covering UI, API, Performance, Security, and Accessibility testing"
- "Implemented comprehensive CI/CD pipeline with 20+ jobs achieving 85%+ code coverage across enterprise e-commerce application"
- "Designed scalable test architecture using Page Object Model, API clients, and microservices patterns for maintainable test suites"

## 📚 Documentation

- [Architecture Guide](docs/architecture/ARCHITECTURE.md)
- [Test Strategy](docs/guides/TEST_STRATEGY.md)
- [Contributing Guide](CONTRIBUTING.md)
- [API Documentation](docs/api/API.md)
- [Examples](docs/examples/)

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

## 📝 License

MIT License - see [LICENSE](LICENSE)

## 📞 Contact

**Jason Teixeira**  
GitHub: [@JasonTeixeira](https://github.com/JasonTeixeira)  
Project: [E-Commerce-Test-Suite](https://github.com/JasonTeixeira/E-Commerce-Test-Suite)

---

**⭐ Star this repo to showcase comprehensive QA automation expertise!**

**Built with ❤️ for enterprise-grade quality assurance**
