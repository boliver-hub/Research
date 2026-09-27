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

## Monthly payment estimate

| Item | Monthly | Basis |
| --- | --- | --- |
| Principal & interest | $2,237 | $335,200 loan ($419,000 − 20% down of $83,800), 30-year fixed at 7.03% |
| Property taxes | $768 | Assumed 2.2% of price per year |
| Homeowners insurance | $200 | Assumed $2,400 per year |
| PMI | $0 | Not required with 20% down |
| **Total** | **$3,205** | HOA dues and utilities not included |

The 7.03% rate is Freddie Mac's Primary Mortgage Market Survey 30-year fixed average for the week of Sept. 24, 2026. Replace the tax rate and insurance figure with the property's actual numbers if you have them. The figures are hardcoded in `flyer.html`, so update the breakdown and the total together.
