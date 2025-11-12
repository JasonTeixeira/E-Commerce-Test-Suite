# Contributing to E-Commerce Test Suite

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this test automation framework.

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- Basic understanding of test automation
- Familiarity with Playwright and Pytest

### Setup Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/JasonTeixeira/E-Commerce-Test-Suite.git
   cd E-Commerce-Test-Suite
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

4. **Setup Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run Tests to Verify Setup**
   ```bash
   pytest -m smoke -v
   ```

---

## 📋 Development Guidelines

### Code Style

We follow PEP 8 and use automated tools to enforce consistency:

- **Black** for code formatting
- **isort** for import sorting
- **Pylint** for code quality
- **mypy** for type checking

**Before committing, run:**
```bash
black .
isort .
pylint **/*.py
mypy .
```

### Code Standards

1. **Type Hints**: Use type hints for all function parameters and return values
   ```python
   def example_function(name: str, count: int) -> bool:
       return True
   ```

2. **Docstrings**: All classes and functions must have docstrings
   ```python
   def test_example():
       """Test that example functionality works correctly."""
       pass
   ```

3. **DRY Principle**: Don't Repeat Yourself - use base classes and utilities

4. **Page Object Model**: UI tests must use Page Object Model pattern

5. **AAA Pattern**: Tests should follow Arrange-Act-Assert structure

---

## 🧪 Writing Tests

### Test Structure

```python
import pytest
from playwright.sync_api import Page

class TestFeatureName:
    """Test suite for feature name."""

    @pytest.mark.ui
    @pytest.mark.critical
    def test_specific_behavior(self, page: Page):
        """Test that specific behavior works as expected."""
        # Arrange
        page.goto("https://www.demoblaze.com")
        
        # Act
        page.click("#element")
        
        # Assert
        assert page.locator("#result").is_visible()
```

### Test Markers

Use appropriate pytest markers:

- `@pytest.mark.smoke` - Critical smoke tests
- `@pytest.mark.ui` - UI automation tests
- `@pytest.mark.api` - API tests
- `@pytest.mark.performance` - Performance tests
- `@pytest.mark.security` - Security tests
- `@pytest.mark.accessibility` - Accessibility tests
- `@pytest.mark.visual` - Visual regression tests
- `@pytest.mark.slow` - Tests taking >5 seconds

### Naming Conventions

- **Test files**: `test_<feature>.py`
- **Test classes**: `Test<FeatureName>`
- **Test functions**: `test_<what_it_tests>`
- **Page objects**: `<PageName>Page`
- **Fixtures**: Descriptive names, lowercase with underscores

---

## 📁 Directory Structure

```
E-Commerce-Test-Suite/
├── ui_tests/              # UI test suites
│   ├── pages/            # Page Object Models
│   └── tests/            # Test files
├── api_tests/            # API test suites
│   ├── clients/          # API clients
│   └── tests/            # Test files
├── performance/          # Performance tests
├── security/             # Security tests
├── accessibility/        # Accessibility tests
├── visual/              # Visual regression tests
├── utils/               # Shared utilities
└── config/              # Configuration
```

---

## 🔄 Pull Request Process

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-number
```

### 2. Make Changes

- Write tests first (TDD approach recommended)
- Implement the feature/fix
- Ensure all tests pass locally
- Add documentation for new features

### 3. Run Quality Checks

```bash
# Format code
black .
isort .

# Type checking
mypy .

# Run tests
pytest -v

# Run specific test categories
pytest -m smoke
pytest -m "not slow"

# Check coverage
pytest --cov=. --cov-report=html
```

### 4. Commit Changes

Follow conventional commit format:

```bash
git commit -m "feat: add new feature"
git commit -m "fix: resolve issue #123"
git commit -m "test: add tests for feature X"
git commit -m "docs: update README"
git commit -m "refactor: improve code structure"
```

Commit types:
- `feat`: New feature
- `fix`: Bug fix
- `test`: Adding tests
- `docs`: Documentation
- `refactor`: Code refactoring
- `style`: Formatting changes
- `perf`: Performance improvements
- `chore`: Maintenance tasks

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title describing the change
- Description of what changed and why
- Reference any related issues
- Screenshots (for UI changes)
- Test results

### 6. PR Review Checklist

- [ ] All tests pass
- [ ] Code coverage maintained or improved
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] CI/CD pipeline passes

---

## 🐛 Reporting Issues

### Bug Reports

Include:
- Clear title
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, browser)
- Screenshots/videos if applicable
- Test logs

### Feature Requests

Include:
- Clear description of the feature
- Use case / business value
- Proposed implementation (optional)
- Examples or mockups

---

## 🧪 Testing Best Practices

### 1. Test Independence
- Tests should not depend on each other
- Use fixtures for setup/teardown
- Generate unique test data (UUIDs)

### 2. Test Readability
- Use descriptive test names
- Keep tests focused on one thing
- Add comments for complex logic

### 3. Test Reliability
- Avoid hardcoded waits (use smart waits)
- Handle timing issues with proper synchronization
- Mark flaky tests with `@pytest.mark.flaky`

### 4. Test Performance
- Keep tests fast where possible
- Mark slow tests with `@pytest.mark.slow`
- Use parallel execution for test suites

### 5. Test Maintainability
- Use Page Object Model for UI tests
- Create reusable utilities
- Keep test data separate from test logic

---

## 📚 Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Playwright Documentation](https://playwright.dev/python/)
- [PEP 8 Style Guide](https://pep8.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

## 💬 Getting Help

- Create an issue for bugs or questions
- Check existing documentation in `/docs`
- Review example tests in test suites

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🙏 Thank You!

Every contribution makes this framework better. Thank you for taking the time to contribute!
