# 📊 Unit Conversion Feature Guide

## Overview
Users can now select their preferred unit of measurement for quantity predictions. The system supports 4 common units with automatic conversion.

---

## ✨ Features Added

### 1. **Feed Calculator** (Feed Calculation Page)
- **Display Units**:
  - ✅ **Kilograms (kg)** - Default
  - ✅ **Grams (g)** - For smaller batches
  - ✅ **Metric Tons (MT)** - For large-scale operations
  - ✅ **Pounds (lbs)** - For international markets

**Example**:
- Backend calculates: **500 kg** of feed required
- User selects "grams (g)" → Shows: **500,000 g**
- User selects "tons" → Shows: **0.5 MT**

---

### 2. **Yield Forecast** (Yield Forecast Page)
- **Display Units**:
  - ✅ **Metric Tons (MT)** - Default
  - ✅ **Kilograms (kg)** - For smaller ponds
  - ✅ **Grams (g)** - For experimental farms
  - ✅ **Pounds (lbs)** - For export markets

**Example**:
- Backend calculates: **2.5 MT** yield
- User selects "kg" → Shows: **2,500 kg**
- User selects "pounds" → Shows: **5,511 lbs**

---

## 🔄 Conversion Rates Used

| From | To | Factor |
|------|-----|---------|
| 1 kg | grams | × 1,000 |
| 1 kg | tons (MT) | ÷ 1,000 |
| 1 kg | pounds | × 2.20462 |
| 1 g | kg | ÷ 1,000 |
| 1 ton | kg | × 1,000 |
| 1 pound | kg | ÷ 2.20462 |

---

## 🎯 Result Display

### Before (Single Unit)
```
Feed Quantity: 500kg
Estimated Cost: $600 / ₹49,800 per Day
```

### After (Multiple Unit Options)
```
Feed Quantity: 500 (User selects unit)
Unit: Kilograms (kg) | Estimated Cost: $600 / ₹49,800 per Day
```

---

## 💻 Code Changes

### Frontend (`templates/`)
1. **feed_calculation.html** - Added unit dropdown
2. **yield_forecast.html** - Added unit dropdown

### Backend (`app.py`)
1. **`convert_quantity()` function** - Handles all conversions
   - Input: value, target_unit, from_unit
   - Output: (converted_value, unit_label)
   
2. **`predict_feed()` route** - Updated to use conversion
3. **`predict_yield()` route** - Updated to use conversion

---

## 📝 Usage Instructions for Users

### Step 1: Fill the form
Navigate to Feed Calculator or Yield Forecast

### Step 2: Select display unit
```
📊 Display Unit: [Dropdown with 4 options]
```

### Step 3: Submit
Click "Calculate" or "Forecast"

### Step 4: View result
```
Result: 500
Unit: Kilograms (kg) | [Other info]
```

---

## 🧪 Test Cases

### Feed Calculator Test
1. Fill: Species=Vannamei, Age=60, Temp=27, Feed Type=Pellet
2. Select: "Grams (g)"
3. Expected: Result shows in grams (multiply by 1000)

### Yield Forecast Test
1. Fill: Species=Vannamei, Area=1, Feed=500, Days=120
2. Select: "Pounds (lbs)"
3. Expected: Result shows in pounds (multiply by 2.20462)

---

## 🔧 Backend Logic

```python
def convert_quantity(value, target_unit, from_unit="kg"):
    # Step 1: Convert to kg (standard unit)
    if from_unit == "grams":
        value_kg = value / 1000
    elif from_unit == "tons":
        value_kg = value * 1000
    # ... etc
    
    # Step 2: Convert from kg to target unit
    if target_unit == "grams":
        result = value_kg * 1000
    elif target_unit == "tons":
        result = value_kg / 1000
    # ... etc
    
    return result, label
```

---

## 📱 Mobile Responsiveness
- Unit dropdown is fully responsive
- Works on mobile, tablet, and desktop
- Touch-friendly select options

---

## 🌍 Supported Units Summary

| Unit | Code | Symbol | Scale |
|------|------|--------|-------|
| Grams | `grams` | g | Smallest |
| Kilograms | `kg` | kg | Medium |
| Metric Tons | `tons` | MT | Large |
| Pounds | `pounds` | lbs | Largest* |

*Pounds is primarily for export/international markets

---

## 🚀 Production Notes

✅ **Live on Feed Calculator** - Fully functional
✅ **Live on Yield Forecast** - Fully functional
✅ **Tested & Verified** - All conversions working
✅ **No Breaking Changes** - Backward compatible
✅ **Multi-language Ready** - Unit names are hardcoded (can add to translations.py)

---

## 📚 Future Enhancements

- [ ] Add cubic meters for water volume
- [ ] Add liters for liquid measurements
- [ ] Save user's preferred unit in session
- [ ] Add unit abbreviations in translations
- [ ] Mobile app integration

---

**Date**: January 26, 2026
**Status**: ✅ Production Ready
**Testing**: All 4 units verified
