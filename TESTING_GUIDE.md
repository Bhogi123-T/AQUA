# 🧪 Unit Conversion Testing Guide

## Quick Start Testing

### Test 1: Feed Calculator - Basic Conversion
**Objective**: Verify feed quantity converts correctly

```
1. Open: http://localhost:5000/farmer/feed_calculation
2. Fill Form:
   - Species: Vannamei Shrimp
   - Age: 60
   - Temperature: 27
   - Feed Type: Pellet
   - Display Unit: Kilograms (kg) ← DEFAULT
3. Click: "Calculate"
4. Expected Result:
   ├─ Shows: "500" (or similar value)
   ├─ Unit: "Kilograms (kg) | Estimated Cost: ..."
   └─ Status: ✅ PASS

5. Go Back, Try Again:
   - Display Unit: Grams (g)
   - Expected: "500000" (500 × 1000)
   - Status: Check if conversion math correct

6. Go Back, Try Again:
   - Display Unit: Metric Tons (MT)
   - Expected: "0.5" (500 ÷ 1000)
   - Status: Check if conversion math correct

7. Go Back, Try Again:
   - Display Unit: Pounds (lbs)
   - Expected: "1102.31" (500 × 2.20462)
   - Status: Check if conversion math correct
```

---

### Test 2: Yield Forecast - Tons Conversion
**Objective**: Verify yield quantity converts correctly

```
1. Open: http://localhost:5000/farmer/yield_forecast
2. Fill Form:
   - Species: Vannamei Shrimp
   - Pond Area: 1.5
   - Total Feed: 1000
   - Culture Duration: 120
   - Display Unit: Metric Tons (MT) ← DEFAULT
3. Click: "Forecast"
4. Expected Result:
   ├─ Shows: "2.5" (or similar value in tons)
   ├─ Unit: "Metric Tons (MT)"
   └─ Status: ✅ PASS

5. Go Back, Try Again:
   - Display Unit: Kilograms (kg)
   - Expected: "2500" (2.5 × 1000)
   - Status: Check if conversion math correct

6. Go Back, Try Again:
   - Display Unit: Grams (g)
   - Expected: "2500000" (2.5 × 1,000,000)
   - Status: Check if conversion math correct

7. Go Back, Try Again:
   - Display Unit: Pounds (lbs)
   - Expected: "5511.55" (2.5 × 2,204.62)
   - Status: Check if conversion math correct
```

---

## Advanced Testing

### Test 3: Edge Cases - Very Small Values
```
Scenario: Small farm operations

1. Feed Calculator with small quantities:
   - Species: Milkfish
   - Age: 30 days
   - Temperature: 25°C
   - Feed Type: Floating
   - Display Unit: Grams (g)

Expected: Small value in grams
Example: If model returns 2kg → 2000g
Status: ✅ PASS if shows small value in grams
```

---

### Test 4: Edge Cases - Large Scale Operations
```
Scenario: Industrial-scale farming

1. Yield Forecast for large operations:
   - Species: Carp
   - Pond Area: 50 hectares
   - Total Feed: 500000 kg
   - Culture Duration: 180 days
   - Display Unit: Metric Tons (MT)

Expected: Large value in tons
Example: If model returns 500 tons → shows as 500 MT
Status: ✅ PASS if shows large value correctly scaled
```

---

### Test 5: Conversion Accuracy Check
```
Manual Verification:

From 100 kg:
├─ To grams: 100 × 1,000 = 100,000 g ✓
├─ To tons: 100 ÷ 1,000 = 0.1 MT ✓
└─ To pounds: 100 × 2.20462 = 220.462 lbs ✓

From 1 ton:
├─ To kg: 1 × 1,000 = 1,000 kg ✓
├─ To grams: 1 × 1,000,000 = 1,000,000 g ✓
└─ To pounds: 1 × 2,204.62 = 2,204.62 lbs ✓

If math matches, conversion is accurate!
```

---

## Performance Testing

### Test 6: Response Time Impact
```
Measurement: Does unit conversion add noticeable delay?

Method:
1. Time request WITHOUT unit selection
2. Time request WITH unit selection
3. Compare timing

Expected Result:
├─ Time Difference: < 0.001 seconds
├─ User Notice: No (imperceptible)
└─ Status: ✅ PASS

How to test:
- Open DevTools (F12)
- Go to Network tab
- Submit form with unit selected
- Check Response Time
- Should be < 200ms total request time
```

---

## Mobile Responsiveness Testing

### Test 7: Mobile Devices
```
Devices to test:
├─ iPhone 12 (375×667)
├─ Samsung Galaxy S21 (360×800)
├─ iPad (768×1024)
└─ Desktop (1920×1080)

Checklist:
- [ ] Dropdown opens properly
- [ ] All 4 units visible and clickable
- [ ] Form submits successfully
- [ ] Result displays without cutoff
- [ ] Unit label is readable
- [ ] No layout shifts after conversion

Expected: ✅ All tests PASS on all devices
```

---

## Browser Compatibility Testing

### Test 8: Cross-Browser Verification
```
Browsers to test:
├─ Chrome 120+
├─ Firefox 121+
├─ Safari 17+
├─ Edge 120+
└─ Mobile Safari (iOS 17+)

For each browser, verify:
- [ ] Unit dropdown renders correctly
- [ ] All options are selectable
- [ ] Form submits with unit_preference
- [ ] Result page displays correctly
- [ ] Conversions are accurate

Expected: ✅ All browsers work identically
```

---

## Form Validation Testing

### Test 9: Missing Unit Selection
```
Scenario: What if user doesn't select a unit?

Test:
1. Open feed_calculation.html
2. Don't change unit preference (keep default)
3. Fill other fields normally
4. Submit form

Expected:
├─ Uses default: "kg" for feed
└─ Conversion still works: ✅ PASS

Test:
1. Manually remove unit_preference from request
2. Submit via browser console:
   document.querySelector('form').submit()

Expected:
├─ Backend defaults to "kg"
├─ Still shows conversion result
└─ Status: ✅ PASS (error handling works)
```

---

## Regression Testing

### Test 10: Ensure No Breaking Changes
```
Verify existing functionality:

1. Feed optimization still works
   - Without unit selection
   - With default settings
   - Result displays correctly
   Status: ✅ PASS or ❌ FAIL

2. Yield forecasting still works
   - Without unit selection
   - With default settings
   - Result displays correctly
   Status: ✅ PASS or ❌ FAIL

3. Cost calculations still work
   - Feed cost in USD shown
   - Feed cost in INR shown
   Status: ✅ PASS or ❌ FAIL

4. Precautions still display
   - Growth Advisory shown
   - Tips displayed
   Status: ✅ PASS or ❌ FAIL

5. Back button still works
   - Returns to previous page
   - Resets form correctly
   Status: ✅ PASS or ❌ FAIL
```

---

## Automated Test Cases (For Developers)

### Python Unit Tests
```python
def test_convert_kg_to_grams():
    result, label = convert_quantity(100, 'grams', 'kg')
    assert result == 100000, f"Expected 100000, got {result}"
    assert label == "grams (g)", f"Expected 'grams (g)', got {label}"
    print("✅ PASS: kg to grams conversion")

def test_convert_tons_to_kg():
    result, label = convert_quantity(1, 'kg', 'tons')
    assert result == 1000, f"Expected 1000, got {result}"
    assert label == "Kilograms (kg)", f"Expected 'Kilograms (kg)', got {label}"
    print("✅ PASS: tons to kg conversion")

def test_convert_kg_to_pounds():
    result, label = convert_quantity(1, 'pounds', 'kg')
    assert abs(result - 2.20462) < 0.001, f"Expected ~2.20462, got {result}"
    assert label == "Pounds (lbs)", f"Expected 'Pounds (lbs)', got {label}"
    print("✅ PASS: kg to pounds conversion")

def test_default_unit_feed():
    # If no unit_preference provided, should default to kg
    result, label = convert_quantity(500, 'kg', 'kg')
    assert result == 500
    assert label == "Kilograms (kg)"
    print("✅ PASS: default unit for feed")

def test_default_unit_yield():
    # If no unit_preference provided, should default to tons
    result, label = convert_quantity(2.5, 'tons', 'tons')
    assert result == 2.5
    assert label == "Metric Tons (MT)"
    print("✅ PASS: default unit for yield")

# Run all tests
test_convert_kg_to_grams()
test_convert_tons_to_kg()
test_convert_kg_to_pounds()
test_default_unit_feed()
test_default_unit_yield()
print("\n✅ ALL TESTS PASSED!")
```

---

## Sign-Off Checklist

```
Testing Checklist:
- [ ] Test 1: Feed Calculator - Basic Conversion ✅
- [ ] Test 2: Yield Forecast - Tons Conversion ✅
- [ ] Test 3: Edge Cases - Small Values ✅
- [ ] Test 4: Edge Cases - Large Scale ✅
- [ ] Test 5: Conversion Accuracy ✅
- [ ] Test 6: Performance Impact ✅
- [ ] Test 7: Mobile Responsiveness ✅
- [ ] Test 8: Cross-Browser Compatibility ✅
- [ ] Test 9: Form Validation ✅
- [ ] Test 10: Regression Testing ✅

Overall Status:
- [ ] All tests PASSED ✅
- [ ] Ready for production ✅
- [ ] No issues found ✅

Signature: _________________
Date: January 26, 2026
```

---

## Troubleshooting

### If conversion results look wrong:
```
1. Check the conversion formula
   - Verify math manually: 100 kg × 2.20462 = ?
   
2. Check the unit_preference value
   - Open DevTools
   - Check Network tab
   - Look at form data sent
   
3. Check Python function
   - Run convert_quantity() manually
   - Test with known values
   
4. Check template rendering
   - Inspect HTML result element
   - Verify value is displayed correctly
```

---

**Testing Guide Created**: January 26, 2026
**Estimated Testing Time**: 30 minutes for all tests
