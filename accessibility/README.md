# Accessibility Testing

WCAG 2.1 Level AA accessibility tests for DemoBlaze.

## Overview

**25 accessibility tests** ensuring compliance with web accessibility standards.

## Test Categories

### 1. Keyboard Navigation (5 tests) - WCAG 2.1.1
- Tab navigation order
- Keyboard-only navigation
- ESC closes modals
- Enter activates buttons
- Skip navigation links

### 2. Focus Management (3 tests) - WCAG 2.4.3, 2.4.7
- Focus indicators visible
- Modal focus trap
- Focus restoration after modal close

### 3. ARIA Attributes (6 tests) - WCAG 4.1.2
- Buttons have labels
- Images have alt text
- Form inputs have labels
- Links have descriptive text
- ARIA live regions
- Form validation messages

### 4. Color and Contrast (3 tests) - WCAG 1.4.3, 1.4.11
- Text color contrast
- Not relying on color alone
- Focus indicator contrast

### 5. Text and Content (4 tests) - WCAG 1.4
- Text resize (200% zoom)
- Text spacing adjustments
- Language attribute
- Descriptive page title

### 6. Responsive & Mobile (3 tests) - WCAG 1.4.4, 1.4.10
- Touch target sizes (44x44px)
- Mobile orientation support
- Content reflow without horizontal scroll

### 7. Screen Reader Compatibility (3 tests)
- Heading hierarchy
- Landmark regions
- Form validation messages

---

## Running Accessibility Tests

```bash
# All accessibility tests
pytest accessibility/tests/ -v

# With marker
pytest -m accessibility -v

# Mobile tests only
pytest -m "accessibility and mobile" -v

# Generate report
pytest accessibility/tests/ --html=reports/accessibility.html
```

---

## WCAG 2.1 Coverage

### Level A
✅ **1.1.1** Non-text Content (Alt text)  
✅ **2.1.1** Keyboard accessible  
✅ **2.4.1** Bypass blocks (Skip links)  
✅ **4.1.2** Name, Role, Value (ARIA)  

### Level AA
✅ **1.4.3** Contrast (Minimum)  
✅ **1.4.10** Reflow  
✅ **1.4.11** Non-text Contrast  
✅ **2.4.3** Focus Order  
✅ **2.4.7** Focus Visible  

---

## Accessibility Testing Tools

### Automated Testing
- **Playwright**: Built-in accessibility testing
- **axe-core**: Comprehensive accessibility engine
- **Pa11y**: Automated accessibility testing
- **Lighthouse**: Chrome DevTools auditing

### Manual Testing
- **Screen readers**: NVDA, JAWS, VoiceOver
- **Keyboard**: Tab, Enter, ESC, Arrow keys
- **Browser zoom**: 200%+ zoom levels
- **Color tools**: Contrast checkers

---

## Integration with axe-core

```python
from axe_playwright_python import Axe

def test_accessibility_with_axe(page: Page):
    page.goto("https://www.demoblaze.com")
    axe = Axe()
    results = axe.run(page)
    assert len(results.violations) == 0
```

---

## Accessibility Checklist

- [ ] Keyboard navigation works completely
- [ ] Focus indicators are visible
- [ ] Color contrast meets 4.5:1 (text) / 3:1 (large text)
- [ ] All images have alt text
- [ ] Forms have proper labels
- [ ] Links are descriptive
- [ ] Page has proper heading structure
- [ ] Content reflows at mobile widths
- [ ] Touch targets are 44x44px minimum
- [ ] Modals trap focus properly
- [ ] ARIA attributes used correctly
- [ ] Lang attribute present
- [ ] Page title is descriptive

---

## Severity Levels

**Critical**: Blocks access for users with disabilities
- Missing alt text on informative images
- Keyboard traps
- Insufficient color contrast (below 3:1)

**High**: Significant barriers  
- No focus indicators
- Missing form labels
- Poor heading structure

**Medium**: Noticeable issues
- Non-descriptive link text
- Missing skip links
- Small touch targets

**Low**: Minor improvements
- Missing ARIA landmarks
- Suboptimal focus order

---

## Common Accessibility Issues

1. **Missing alt text** → Add descriptive alt attributes
2. **Poor contrast** → Adjust colors to meet 4.5:1 ratio
3. **Keyboard traps** → Ensure ESC exits, Tab cycles
4. **No focus indicators** → Add visible outlines
5. **Missing labels** → Use `<label>` or aria-label
6. **Non-semantic HTML** → Use proper elements (nav, main, button)

---

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [A11y Project Checklist](https://www.a11yproject.com/checklist/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)

---

## Next Steps

1. Integrate axe-core for automated scanning
2. Add Pa11y for CI/CD integration
3. Create accessibility regression suite
4. Manual screen reader testing
5. Generate WCAG compliance report
6. Set up continuous accessibility monitoring
