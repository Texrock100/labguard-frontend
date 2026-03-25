# Medicare Coverage Lookup (MCL) Feature for GougeStop.com

## Overview

This directory contains 21 ready-to-deploy HTML files for the Medicare Coverage Lookup feature on GougeStop.com. All files are static HTML/CSS/JS with no external dependencies.

## File Structure

```
coverage/
├── index.html                      # Landing page (Medicare Coverage Lookup)
├── cpt-80048.html                  # Basic Metabolic Panel (BMP)
├── cpt-80053.html                  # Comprehensive Metabolic Panel (CMP)
├── cpt-80061.html                  # Lipid Panel
├── cpt-80076.html                  # Hepatic Function Panel
├── cpt-81003.html                  # Urinalysis, Automated
├── cpt-82306.html                  # Vitamin D, 25-Hydroxy
├── cpt-82550.html                  # CK / CPK (Creatine Kinase)
├── cpt-82607.html                  # Vitamin B12 (Cyanocobalamin)
├── cpt-82728.html                  # Ferritin
├── cpt-82746.html                  # Folate (Folic Acid)
├── cpt-82947.html                  # Glucose, Blood
├── cpt-83036.html                  # Hemoglobin A1c (HbA1c)
├── cpt-83735.html                  # Magnesium
├── cpt-84153.html                  # PSA (Prostate Specific Antigen)
├── cpt-84403.html                  # Testosterone, Total
├── cpt-84443.html                  # Thyroid Stimulating Hormone (TSH)
├── cpt-84480.html                  # T3, Total (Triiodothyronine)
├── cpt-85025.html                  # Complete Blood Count with Differential (CBC)
├── cpt-85027.html                  # CBC without Differential
├── cpt-86140.html                  # C-Reactive Protein (CRP)
├── generate_coverage_pages.py      # Python generator script (for regeneration)
└── README.md                       # This file
```

## Features

### Landing Page (`index.html`)

- **Hero section** with title and subtitle
- **Data disclaimer box** explaining Medicare rates source and data limitations
- **Real-time search/filter** - client-side JavaScript filters test grid by name or CPT code
- **Responsive grid** - 3 columns (desktop), 2 columns (tablet), 1 column (mobile)
- **20 test cards** showing:
  - Test name
  - CPT code
  - Medicare allowable rate
  - Typical lab charge range
  - Markup percentage
  - "Learn More" link to individual CPT page

### Individual CPT Pages (cpt-XXXXX.html)

Each page includes:

1. **Breadcrumb navigation** - Home > Coverage Lookup > Test Name
2. **Hero with title and subtitle** - "[Test Name] (CPT XXXXX) — Medicare Rate vs. Lab Charges"
3. **Quick answer box** (pull-quote) - Medicare rate vs. lab charge range with markup percentage
4. **What This Test Is** - Plain-language 2-3 sentence definition
5. **Medicare Rate vs. Lab Charges** - Table with:
   - Medicare Allowable Rate
   - Typical Lab Charge Range
   - Average Markup Above Medicare
6. **Does Medicare Cover This Test?** - Yes/conditional answer
7. **Common Reasons for Denial** - Bulleted list (3-5 items)
8. **What To Do If You're Overcharged** - Steps with link to GougeStop app
9. **FAQ Section** - 2-3 Q&As specific to that test
10. **Related Tests** - 3 cross-linked related tests
11. **CTA button** - "Compare Your Lab Bill Now" → /app

### SEO & Schema Markup

Each CPT page includes:

- **Meta description** - Unique, keyword-rich, 150-160 chars
- **Open Graph tags** - og:title, og:description, og:url, og:type
- **JSON-LD schema** (3 blocks per page):
  - MedicalWebPage schema
  - FAQPage schema (for featured snippets)
  - BreadcrumbList schema

### Styling

- **Matches existing GougeStop.com design** exactly:
  - Fonts: System fonts (-apple-system, BlinkMacSystemFont, etc.)
  - Colors: Navy (#1B3A5C), red (#FF6B6B), grays
  - Spacing and border-radius: 14px cards
  - Box shadows: Subtle 0 2px 8px
- **Responsive design** with mobile breakpoints at 768px and 480px
- **All CSS is inline** (no external stylesheets)

## Search Functionality

The landing page search is implemented with vanilla JavaScript:
- Real-time filtering as user types
- Searches across test name, CPT code, and other visible text
- Shows/hides test cards without page reload
- Works on all modern browsers

## Data Source

All Medicare rates are from the **2023 CMS Clinical Lab Fee Schedule (CLFS)**.
All lab charge ranges are from **2023 national pricing data**.

The data is embedded in the Python generator script for easy updates.

## Regenerating Files

If you need to update test data or add new tests:

1. Edit the `TESTS` list in `generate_coverage_pages.py`
2. Run: `python3 generate_coverage_pages.py`
3. All 21 HTML files will be regenerated from the updated data

### Test Data Format

```python
{
    "cpt": "80053",
    "name": "Comprehensive Metabolic Panel (CMP)",
    "medicare": 14.35,
    "lab_min": 45,
    "lab_max": 237,
    "markup_min": 214,
    "markup_max": 1552,
    "description": "Plain language 2-3 sentence description...",
    "coverage": "Yes/conditional coverage answer...",
    "denials": ["Reason 1", "Reason 2", ...],
    "faqs": [
        {
            "q": "Question?",
            "a": "Answer."
        },
        ...
    ],
    "related": ["80048", "80076", "82947"]  # CPT codes of related tests
}
```

## Integration Steps

1. **Deploy files** to `/coverage/` directory on Vercel
2. **Update navigation** on existing pages:
   - Add "Coverage Lookup" link to nav menu
   - Link nav anchor to `/coverage/`
3. **No changes needed** to existing page structure - new nav link blends seamlessly

## Important Notes

- **No external API calls** - all data is static HTML
- **No patient data collected** - fully informational
- **Client-side search** - no server required for landing page filtering
- **Fast page load** - minimal CSS, inline styles, no dependencies
- **SEO optimized** - schema markup, meta descriptions, breadcrumbs
- **Accessible** - semantic HTML, proper heading hierarchy, readable colors

## Technical Stack

- Pure HTML5
- Inline CSS (embedded in each file)
- Vanilla JavaScript (search functionality only, no frameworks)
- JSON-LD schema markup for SEO

## File Sizes

- Landing page: ~18 KB
- Individual CPT pages: ~15-16 KB each
- Total directory: 60 KB

All files are optimized for fast loading and minimal bandwidth.

## Contact

For updates or regeneration of these files, use the Python generator script included in this directory.
