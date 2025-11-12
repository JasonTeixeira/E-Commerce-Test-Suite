# Visual Regression Testing

Automated screenshot comparison for detecting visual regressions.

## Overview

**30+ visual regression tests** ensuring UI consistency across:
- Pages (5 tests)
- Components (5 tests)
- Modals (3 tests)
- Cross-browser (5 tests with parametrize)
- Responsive viewports (7 viewport tests with parametrize)
- UI states (4 tests)
- Loading states (2 tests)

---

## Test Categories

### 1. Page Visual Regression (5 tests)
- Homepage (desktop, mobile, tablet)
- Product detail page
- Cart page

### 2. Component Visual Regression (5 tests)
- Navbar
- Product cards
- Footer
- Category sidebar
- Carousel

### 3. Modal Visual Regression (3 tests)
- Login modal
- Signup modal
- Checkout modal

### 4. Cross-Browser Visual Regression (5 tests)
- Homepage across Chromium, Firefox, WebKit (3 tests)
- Login modal across Chromium, Firefox (2 tests)

### 5. Responsive Visual Regression (7 tests)
Parametrized tests across viewports:
- iPhone SE (320x568)
- iPhone 8 (375x667)
- iPhone 11 (414x896)
- iPad (768x1024)
- iPad Landscape (1024x768)
- Desktop HD (1920x1080)
- Desktop 2K (2560x1440)

### 6. State Visual Regression (4 tests)
- Hover states
- Active category
- Cart with items
- Empty cart

### 7. Loading State Visual (2 tests)
- Page skeleton/spinner
- Modal transitions

---

## Running Visual Tests

```bash
# All visual tests
pytest visual/tests/ -v

# With marker
pytest -m visual -v

# Specific test classes
pytest visual/tests/test_visual_regression.py::TestPageVisualRegression -v
pytest visual/tests/test_visual_regression.py::TestResponsiveVisualRegression -v

# Update baselines (run tests to create new baselines)
pytest visual/tests/ -v  # First run creates baselines

# Generate visual report
pytest visual/tests/ --html=reports/visual_regression.html
```

---

## Baseline Management

### Initial Setup
```bash
# Create baselines (run tests once)
pytest visual/tests/ -v

# Baselines saved to: visual/baselines/
```

### Updating Baselines
```python
from visual.utils.screenshot_compare import ScreenshotCompare

compare = ScreenshotCompare()
compare.update_baseline("path/to/new/screenshot.png", "baseline_name")
```

### Clearing Baselines
```bash
# Remove all baselines
rm -rf visual/baselines/*

# Remove all diffs
rm -rf visual/diffs/*
```

---

## Screenshot Comparison Utility

```python
from visual.utils.screenshot_compare import ScreenshotCompare

# Initialize
compare = ScreenshotCompare(
    baseline_dir="visual/baselines",
    diff_dir="visual/diffs"
)

# Compare with baseline
is_similar, difference, diff_path = compare.compare_with_baseline(
    screenshot_path="temp/current.png",
    name="homepage_desktop",
    threshold=0.05  # 5% difference allowed
)

# Compare two images
is_similar, diff = compare.compare_images(
    "image1.png",
    "image2.png",
    threshold=0.1
)

# Create diff image
compare.create_diff_image(
    baseline_path="baseline.png",
    current_path="current.png",
    output_path="diff.png"
)

# Compare regions
is_similar, diff = compare.compare_regions(
    "image1.png",
    "image2.png",
    region=(0, 0, 100, 100),  # (left, top, right, bottom)
    threshold=0.05
)
```

---

## Diff Images

When visual differences are detected, diff images are automatically generated:

```
visual/diffs/
├── homepage_desktop_diff.png     # Side-by-side comparison
├── navbar_diff.png
└── login_modal_diff.png
```

Each diff image shows:
1. **Left**: Baseline (expected)
2. **Middle**: Current (actual)
3. **Right**: Difference (highlighted)

---

## Thresholds

Different thresholds for different scenarios:

| Scenario | Threshold | Reason |
|----------|-----------|--------|
| **Same page, same browser** | 0.03 (3%) | Tight tolerance |
| **Full pages** | 0.05 (5%) | Allow minor differences |
| **Cross-browser** | 0.08 (8%) | Rendering differences |
| **Components** | 0.03 (3%) | Precise matching |
| **Modals** | 0.03 (3%) | Consistent UI |

---

## CI/CD Integration

```yaml
# GitHub Actions example
- name: Run Visual Regression Tests
  run: |
    pytest visual/tests/ -v --html=reports/visual.html
    
- name: Upload Visual Diffs
  if: failure()
  uses: actions/upload-artifact@v3
  with:
    name: visual-diffs
    path: visual/diffs/

- name: Upload Baseline Images
  uses: actions/upload-artifact@v3
  with:
    name: baselines
    path: visual/baselines/
```

---

## Best Practices

### 1. Stable Baselines
- Ensure consistent test environment
- Wait for animations to complete
- Use `networkidle` state

### 2. Appropriate Thresholds
- Start with 5% threshold
- Tighten for critical components
- Loosen for cross-browser tests

### 3. Baseline Updates
- Review diffs before updating baselines
- Version control baseline images
- Document intentional changes

### 4. Test Stability
- Add waits for dynamic content
- Mask dynamic elements (timestamps, ads)
- Use fixed viewport sizes

---

## Directory Structure

```
visual/
├── baselines/              # Baseline screenshots
│   ├── homepage_desktop.png
│   ├── homepage_mobile.png
│   └── navbar.png
├── diffs/                  # Diff images (on failure)
│   └── homepage_diff.png
├── temp/                   # Temporary screenshots
│   └── current.png
├── tests/                  # Visual regression tests
│   └── test_visual_regression.py
├── utils/                  # Comparison utilities
│   └── screenshot_compare.py
└── README.md              # This file
```

---

## Troubleshooting

### Issue: Tests fail on first run
**Solution**: First run creates baselines, subsequent runs compare

### Issue: High false positive rate
**Solution**: Increase threshold or add waits for animations

### Issue: Cross-browser differences
**Solution**: Use separate baselines per browser

### Issue: Dynamic content causes failures
**Solution**: Mask dynamic regions or use region comparison

---

## Advanced Features

### Perceptual Hash
```python
hash1 = compare.get_image_hash("image1.png")
hash2 = compare.get_image_hash("image2.png")
# Quick comparison without pixel-by-pixel
```

### Region Comparison
```python
# Compare only header region
is_similar, diff = compare.compare_regions(
    "page1.png",
    "page2.png",
    region=(0, 0, 1920, 100)  # Header area
)
```

### Cleanup
```python
compare.clear_diffs()       # Remove all diff images
compare.clear_baselines()   # Remove all baselines
```

---

## Next Steps

1. ✅ Integrate Percy or Chromatic for cloud-based visual testing
2. ✅ Add visual regression to CI/CD pipeline
3. ✅ Create visual test dashboard
4. ✅ Implement automatic baseline updates
5. ✅ Add visual testing metrics and trends
