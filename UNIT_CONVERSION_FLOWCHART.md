# 🔄 Unit Conversion Flow Diagram

## User Journey - Feed Calculator

```
┌─────────────────────────────────────────────┐
│  User visits Feed Calculation Page          │
│  (/farmer/feed_calculation)                 │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│  Fill Form Fields:                          │
│  • Species: Vannamei                        │
│  • Age: 60 days                             │
│  • Temperature: 27°C                        │
│  • Feed Type: Pellet                        │
│  • 📊 Display Unit: [Dropdown ▼]            │  ◄── NEW
│      ├─ kg (selected)                       │
│      ├─ grams                               │
│      ├─ tons                                │
│      └─ pounds                              │
└────────────────┬────────────────────────────┘
                 │
                 ▼ (User clicks Calculate)
┌─────────────────────────────────────────────┐
│  POST /predict_feed                         │
│  Form Data: {species, age, temp, ...        │
│             unit_preference: "kg"}          │  ◄── NEW
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│  Backend Processing:                        │
│                                             │
│  1. Load form data                          │
│  2. Run ML model → quantity_kg = 500 kg     │
│  3. Get unit_preference = "kg"   (or user)  │
│  4. convert_quantity(500, "kg", "kg")       │  ◄── NEW
│     Returns: (500.0, "Kilograms (kg)")      │
│  5. Convert cost calculation                │
│  6. Get precautions                         │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│  Render Result Page:                        │
│                                             │
│  Title: "Feed Optimizer"                    │
│  Result: 500                                │
│  Unit: "Kilograms (kg) | Cost: $600 ..."    │  ◄── NEW
│  Precautions: [list of tips]                │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│  Display to User (result.html)              │
└─────────────────────────────────────────────┘
```

---

## Unit Conversion Logic

```
Input: value=500, target_unit="grams", from_unit="kg"

Step 1: Normalize to kg (standard unit)
        from_unit == "kg" → value_kg = 500

Step 2: Convert to target unit
        target_unit == "grams" → result = 500 × 1000 = 500,000

Step 3: Return result + label
        return (500000, "grams (g)")

Output: (500000, "grams (g)")
        Result displays as: "500000 grams (g)"
```

---

## Parallel Processing - Yield Forecast

```
Same flow as Feed Calculator, but:
- Default input unit: TONS (from model)
- Default output unit: TONS
- Conversion examples:
  • 2.5 tons → grams = 2,500,000 g
  • 2.5 tons → kg = 2,500 kg
  • 2.5 tons → pounds = 5,511.55 lbs
```

---

## All Supported Unit Conversions

```
From Kilograms (kg):
├─ To Grams:        multiply by 1,000
├─ To Metric Tons:  divide by 1,000
├─ To Pounds:       multiply by 2.20462

From Grams (g):
├─ To Kilograms:    divide by 1,000
├─ To Metric Tons:  divide by 1,000,000
├─ To Pounds:       divide by 453.592

From Metric Tons (MT):
├─ To Kilograms:    multiply by 1,000
├─ To Grams:        multiply by 1,000,000
├─ To Pounds:       multiply by 2,204.62

From Pounds (lbs):
├─ To Kilograms:    divide by 2.20462
├─ To Grams:        multiply by 453.592
├─ To Metric Tons:  divide by 2,204.62
```

---

## Data Structure

### Request Data (POST)
```json
{
  "species": "Vannamei",
  "age": "60",
  "temp": "27",
  "feed_type": "Pellet",
  "unit_preference": "kg"  ← NEW FIELD
}
```

### Response Data (Render)
```json
{
  "title": "Feed Optimizer",
  "result": "500",  ← Converted value
  "unit": "Kilograms (kg) | Estimated Cost: ...",  ← INCLUDES UNIT
  "precautions": [...]
}
```

---

## Error Handling

```
If unit_preference not provided:
→ Default to "kg" for feed
→ Default to "tons" for yield

If invalid unit_preference:
→ Fall through to else case
→ Return in original unit (kg or tons)
```

---

## Performance Impact

```
Conversion Overhead:
- Simple arithmetic operation
- ~0.0001ms per conversion
- Negligible impact on total request time

Memory:
- No additional storage
- Conversion done on-the-fly
- No caching needed
```

---

## Future Enhancement Points

```
1. Add water volume conversions
   ├─ Liters
   ├─ Cubic Meters
   └─ Gallons

2. Save unit preference
   ├─ Store in user session
   ├─ Remember across visits
   └─ Default next time

3. Add custom units
   ├─ Allow farmers to define their own
   ├─ Regional standards
   └─ Import/export standards

4. Multi-unit display
   ├─ Show all 4 units at once
   ├─ Quick comparison
   └─ Copy to clipboard
```

---

**Visual Guide Created**: January 26, 2026
