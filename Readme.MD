# 🎨 iPaletteFinder — Colour Extractor

Upload any image and get its top dominant colours using KMeans clustering.

## Project Structure

```
iPaletteFinder/
├── app.py              # Streamlit entry point — UI only, no business logic
├── config.py           # Loads .env, exposes typed Settings dataclass
├── colour_model.py     # ColourResult dataclass (domain model)
├── colour_service.py   # ColourService class — extraction logic
├── ui_helper.py        # HTML rendering helpers (no business logic)
├── templates/          # CSS and HTML templates loaded by ui_helper.py
│   ├── styles.css
│   ├── swatch_card.html
│   └── strip_segment.html
├── .env                # All configurable values (one source of truth)
├── sample.env          # Safe-to-commit .env template (no secrets)
├── requirements.txt
└── README.md
```

## Setup

```bash
pip install -r requirements.txt
```

Copy `sample.env` to `.env` and adjust values as needed:

```bash
cp sample.env .env
```

## Run

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## Configuration

All settings live in `.env` — no hardcoded values anywhere else:

| Variable              | Default | Description                             |
|-----------------------|---------|-----------------------------------------|
| `DEFAULT_N_COLOURS`   | 5       | Default number of colours on the slider |
| `MIN_COLOURS`         | 1       | Slider minimum                          |
| `MAX_COLOURS`         | 9       | Slider maximum                          |
| `SAMPLE_SIZE`         | 200     | Max px per dimension for KMeans input   |
| `KMEANS_RANDOM_STATE` | 42      | Reproducibility seed                    |
| `ALLOWED_EXTENSIONS`  | png,... | Accepted upload file types              |

## How it works

1. **Pillow** opens the uploaded image and normalises it to RGB
2. **NumPy** resizes it to `SAMPLE_SIZE` and reshapes pixels into a flat `(H×W, 3)` array
3. **scikit-learn KMeans** clusters the pixels — each cluster centre is a dominant colour
4. Cluster sizes determine the percentage of the image each colour occupies
5. Results are returned as typed `ColourResult` dataclass instances, sorted by dominance
6. The UI renders a proportional colour strip and a ranked swatch list with relative percentage bars