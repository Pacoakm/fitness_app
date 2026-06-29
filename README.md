# Fitness Trainer App

An AI fitness-coach web app built with **Streamlit + MediaPipe Pose**. Through the
browser webcam, it analyses your motion in real time, automatically counts your
squats / bicep curls / leg exercises, and provides live posture feedback. It also
includes a nutrition-label OCR feature with an AI dietary advisor.

## Features

| Module | Path | Description |
|---|---|---|
| Landing page | `main.py` | Two entry points: "Start" (workouts) and "Nutrition info" (OCR) |
| Workout hub | `pages/home.py` | Lists three exercises: Squatting / Curls / Leg |
| Squat counter + posture correction | `pages/squat.py`, `process_frame.py` | Streams the webcam via `streamlit-webrtc`, computes hip / knee / ankle angles with MediaPipe, and counts reps with a state machine |
| Bicep curl counter | `pages/curls.py` | Counts reps by detecting elbow-angle threshold crossings |
| Leg exercise counter | `pages/leg.py` | Counts reps by detecting knee-angle threshold crossings |
| Nutrition-label OCR | `pages/ocr.py` | Tesseract OCR for Calories / Fat / Sodium / Sugars / Protein, plus GPT-based advice |

## Project Layout

```
fitness_app/
├── main.py                # Streamlit landing page
├── pages/
│   ├── home.py            # Exercise hub
│   ├── squat.py           # Squat counter (main feature)
│   ├── curls.py           # Bicep curl counter
│   ├── leg.py             # Leg-exercise counter
│   └── ocr.py             # Nutrition-label OCR + GPT advisor
├── PoseModule.py          # Generic MediaPipe Pose wrapper
├── process_frame.py       # Squat posture state machine
├── thresholds.py          # Beginner / Pro angle thresholds
├── utils.py               # Angle math, drawing helpers, landmark utilities
├── squat.py               # Legacy root-level version (prefer pages/squat.py)
├── requirements.txt
├── package.json
├── samples/               # Sample nutrition-label photos
├── test/                  # Early test scripts
└── .devcontainer/         # GitHub Codespaces / VS Code Dev Container config
```

## Environment & Dependencies

### Python 3.10 / 3.11

```bash
pip install -r requirements.txt
```

Core dependencies:

- `streamlit`
- `streamlit-webrtc` — browser-side WebRTC camera streaming
- `mediapipe` — pose landmark detection
- `opencv-python-headless` — image processing (headless build, no GUI deps)
- `numpy`, `Pillow`
- `av`, `aiortc` — video frame decoding
- `pytesseract` + [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- `openai>=0.27` — used by the OCR page for GPT dietary advice

### Tesseract

The OCR page hardcodes this path:

```python
pytesseract.pytesseract.tesseract_cmd = r"/opt/homebrew/bin/tesseract"
```

On macOS install with `brew install tesseract`. On other platforms, adjust the
path accordingly.

### OpenAI API Key

The GPT feature on the OCR page requires an API key.

Store it as an environment variable:

```bash
export OPENAI_API_KEY="***"
```

Then update `pages/ocr.py`: replace the hardcoded `openai.api_key = "***"` line
with:

```python
import os
openai.api_key = os.environ["OPENAI_API_KEY"]
```

Never hardcode the key in source, and never commit it back to GitHub.

## Running the App

```bash
streamlit run main.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser and grant
camera permission.

- `http://localhost:8501/home` — workout hub
- `http://localhost:8501/ocr` — nutrition OCR advisor

> Some pages reference absolute image paths like
> `/Users/pacoakm/Documents/AI/...`. On another machine, either update the
> paths in `main.py` and `pages/home.py`, or place the images at those exact
> locations.

## How the Squat Counter Works (Core Module)

`ProcessFrame` combines MediaPipe Pose's 33 body landmarks with the angle
thresholds in `thresholds.py` and maintains a `state_seq`:

- `s1` — standing / NORMAL
- `s2` — transition / TRANS
- `s3` — pass / PASS

A valid squat is the full cycle `s1 → s2 → s3 → s2 → s1`.
`CNT_FRAME_THRESH = 50` requires 50 consecutive frames in the same state before
it counts, which prevents false triggers.

Live feedback messages:

- `LOWER YOUR HIPS` — hips are not deep enough
- `BEND BACKWARDS` / `BEND FORWARD` — upper-back posture
- `KNEE FALLING OVER TOE` — knees extending past the toes
- `SQUAT TOO DEEP` — squatting too deep (knee-stress risk)
- `INACTIVE_THRESH = 15s` — no user in front of the camera for 15s
- `OFFSET_THRESH = 35°` — body is offset too far from the camera frame

`thresholds.py` ships two presets: **Beginner** (more forgiving) and **Pro**
(tighter knee/ankle ranges).

## Dev Container

`.devcontainer/devcontainer.json` provisions Python 3.11 and forwards the
Streamlit port 8501, so it works out-of-the-box inside GitHub Codespaces or a
VS Code Dev Container.

## Notes

- The camera feature relies on browser WebRTC, so it needs HTTPS or
  `localhost`. Local Streamlit development supports this by default.
- OCR accuracy depends on label image clarity. The `samples/` folder contains
  several real nutrition-label photos you can try.
- This is an experimental demo. The squat counter and posture feedback are
  reference only — they cannot replace a professional coach.
