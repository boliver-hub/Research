# 2336 For-Sale Flyer

One-page, full-bleed US Letter flyer for the craftsman two-story at 2336 Gray Dr, Northlake, TX 76247.

| File | What it is |
| --- | --- |
| `flyer.pdf` | Print-ready flyer (8.5 × 11 in, 1 page) |
| `flyer-preview.png` | Image preview for email or social |
| `flyer.html` | Source layout (edit text here) |
| `render.cjs` | Rebuilds the PDF and PNG from `flyer.html` |
| `images/` | Listing photos. `exterior-flowers.jpg` is `exterior.jpg` with flowers digitally added to the front beds; the original is kept unchanged |
| `add_flowers.py` | Recreates `exterior-flowers.jpg` from the original (`pip install pillow numpy scipy`) |
| `fonts/` | DM Serif Display and Figtree (SIL Open Font License), bundled so the PDF renders the same anywhere |

## Editing

The address (2336 Gray Dr, Northlake, TX 76247) and showing contact (310-920-2211, blake.oliver@gmail.com) are in `flyer.html`. After any edit, re-render:

```sh
npm install playwright   # once, if not already installed
node render.cjs
```

The front photo carries a "Flowers digitally added" label because the plantings aren't there in real life. Most listing rules require that disclosure on altered photos.

## Estimated mortgage payment

The flyer shows principal and interest only, per the seller's direction: **$2,237/mo**.

| Input | Value |
| --- | --- |
| Price | $419,000 |
| Down payment | 20% ($83,800) |
| Loan amount | $335,200 |
| Term and rate | 30-year fixed at 7.03% (Freddie Mac PMMS average, week of Sept. 24, 2026) |

Taxes, insurance and HOA dues are excluded. Because the flyer states a payment amount, federal Truth in Lending advertising rules (12 CFR 1026.24) require saying next to it that taxes and insurance aren't included and the actual payment will be higher. That line sits under the figure, and the footnote carries the down payment and loan terms. The rules also call for an APR whenever a payment or rate is advertised; add one from a lender if available.

## Placeholders to fill

- `[XXXX]` sq ft (Craftsman 4-Bedroom Home block)
- `[XXX]` kWh battery capacity (Power Storage System block)
