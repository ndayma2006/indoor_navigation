# Campus Compass – SITCOE
### AI-Powered 3D Indoor Navigation System for Sharad Institute of Technology College of Engineering

Campus Compass is an engineering-grade 3D indoor navigation system and conversational AI assistant built for the **Sharad Institute of Technology College of Engineering (SITCOE), Yadrav**.

Unlike generic outdoor GPS prototypes (which fail indoors due to wall attenuation and lack of vertical elevation awareness), this system is **mathematically grounded in the verified architectural CAD drawing (`02.Main Building Sheet with lift.dwg`)** of the SITCOE campus main building.

---

## 🌟 Key Features

1. **Native CAD & Architectural Integration**:
   - Parsed from AutoCAD 2013 DWG format (`02.Main Building Sheet with lift.dwg`).
   - True building dimensions: **$65.14\text{ m}$ Width $\times 65.44\text{ m}$ Length** quadrangle layout.
   - Central Open-To-Sky courtyard (**O.T.S. $33.18\text{ m} \times 21.58\text{ m}$**) enclosed by continuous **$3.00\text{ m}$ wide indoor corridors**.
   - True floor elevations: **Ground Floor ($0.00\text{ m}$)**, **First Floor ($4.95\text{ m}$)**, and **Second Floor ($9.00\text{ m}$)**.

2. **Multi-Floor & Staircase Navigation**:
   - **Staircase S1 (South-West Core)**: $8.47\text{ m}$ core with $0.15\text{ m}$ risers and $0.30\text{ m}$ treads connecting Ground, First, and Second floors.
   - **Staircase S2 (North-East Core)**: $5.20\text{ m}$ core connecting all three levels.
   - **Central Lift L1**: Passenger elevator core ($1.80\text{ m} \times 1.80\text{ m}$) facing the south courtyard passage.
   - **NetworkX Dijkstra / A\* Shortest Path Algorithm**: Optimal route calculation across corridors, doors, and staircase transitions with turn-by-turn walking directions.

3. **Interactive 3D & Synchronized 2D Viewers**:
   - **3D Three.js Building Viewer**: OrbitControls (zoom, pan, rotate), floor stacking view (`ALL`), isolated floor slicer (`0`, `1`, `2`), cutaway 3D walls, animated glowing path tube, and destination marker pins.
   - **Synchronized 2D Floor Plan Canvas**: Architectural view with real-time room boundary highlights and navigation path lines.

4. **Functional AI Voice Assistant ("Campus Compass AI")**:
   - Speech-to-Text input via microphone button (Web Speech API).
   - Natural Language Understanding (NLU) with destination entity resolution (Classrooms, Labs, Faculty Cabins, HOD Offices, Emergency contacts).
   - Multi-language support: **English**, **Hindi (हिंदी)**, and **Marathi (मराठी)**.
   - Neural Text-to-Speech (TTS) streaming via `edge-tts` with high-quality neural voices (`EmmaNeural`, `SwaraNeural`, `AarohiNeural`).
   - Offline local rule engine with optional Google Gemini Generative AI enhancement via `.env`.

---

## 🏗️ Python Architecture & Tech Stack

```
campus_compass/
├── app/
│   ├── main.py                     # FastAPI application & lifespan orchestrator
│   ├── api/
│   │   └── routes.py               # REST API endpoints (route, search, chat, tts, cad)
│   ├── cad/
│   │   ├── importer.py             # CAD DWG/DXF loader & validation reporter
│   │   ├── geometry.py             # Spatial math, polygon area, 2D/3D Euclidean distance
│   │   ├── room_extraction.py      # Room polygon generator and centroid mapping
│   │   └── staircase_extraction.py # S1, S2, and Lift vertical core extraction
│   ├── navigation/
│   │   ├── graph_builder.py        # Multi-floor NetworkX indoor graph generator
│   │   ├── pathfinder.py           # Dijkstra & A* pathfinder with lift/stairs preference
│   │   ├── floor_transitions.py    # Multi-floor transition & staircase instruction engine
│   │   └── directions.py           # Turn-by-turn instruction generator (turns, distances)
│   ├── assistant/
│   │   ├── intent_parser.py        # NLU intent parser & destination extractor
│   │   ├── assistant_service.py    # AI coordinator (Local rule engine + Gemini RAG)
│   │   └── speech_service.py       # Asynchronous neural TTS via edge-tts
│   ├── data/
│   │   ├── db.py                   # SQLite database connection & schema
│   │   ├── seed_data.py            # Verified SITCOE rooms, faculty, and staircases seed
│   │   ├── search_service.py       # Fuzzy multi-field search engine
│   │   └── cad_floor_geometry.json # Normalized CAD vector geometry (3,862 polylines)
│   ├── models/
│   │   └── schemas.py              # Pydantic data models & request/response schemas
│   ├── static/
│   │   ├── css/style.css           # Modern collegiate styling
│   │   ├── js/
│   │   │   ├── main.js             # UI state coordinator
│   │   │   ├── viewer3d.js         # Three.js 3D building visualizer
│   │   │   ├── floorplan2d.js      # 2D Canvas architectural floor plan
│   │   │   └── assistant.js        # Voice recording & assistant audio streaming
│   │   └── logo.png                # SITCOE institutional logo
│   └── templates/
│       └── index.html              # Responsive HTML5 interface
├── tests/
│   ├── test_cad.py                 # CAD geometry & import unit tests
│   ├── test_navigation.py          # Shortest path & multi-floor navigation tests
│   ├── test_assistant.py           # Intent parsing & multilingual tests
│   └── test_api.py                 # FastAPI endpoint integration tests
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Quickstart & Local Setup

### 1. Prerequisites
- Python 3.11, 3.12, or 3.13 installed.
- Modern web browser (Chrome, Edge, Firefox, or Safari) with WebGL support.

### 2. Install Dependencies
```powershell
pip install -r campus_compass/requirements.txt
```

### 3. Configure Environment (Optional)
Copy `.env.example` to `.env`:
```powershell
cp campus_compass/.env.example campus_compass/.env
```
To enable Google Gemini Generative AI for conversational questions, add your Gemini API key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
*(If left blank, the application automatically runs in full offline rule-based NLP mode with zero loss of navigation functionality).*

### 4. Run the Application
From the workspace root directory:
```powershell
python -m uvicorn campus_compass.app.main:app --reload --host 0.0.0.0 --port 8000
```

Open your browser and navigate to:
```
http://localhost:8000
```

---

## 🧪 Running Automated Tests

Run the full automated pytest suite:
```powershell
python -m pytest campus_compass/tests -v
```

All 22 unit and integration tests validate:
- Native CAD geometry loading and bounding box calculations ($65.14\text{ m} \times 65.44\text{ m}$).
- Single-floor navigation routes (e.g., Main Entrance $\to$ Principal Cabin).
- Multi-floor routes via Staircase S1 & S2 (e.g., Ground Entrance $\to$ First Floor Classroom 38).
- Multi-floor routes to Second Floor (AIDS Room 701).
- Unreachable destinations and error handling.
- Voice intent parsing for rooms, faculty members, and staircases.
- Multilingual Marathi/Hindi translations ("प्राचार्य केबिन", "लॅब").
- REST API endpoint contracts.

---

## 🌐 Deployment Guidelines

### Why Static GitHub Pages Cannot Run Python Directly:
GitHub Pages only serves static files (`.html`, `.css`, `.js`). A Python backend (FastAPI, NetworkX, SQLite, Edge-TTS) requires an active server runtime.

### Recommended Deployment Options:
1. **Local College Intranet (Recommended for SITCOE Campus)**:
   - Run on a campus server connected to the SITCOE Wi-Fi network.
   - Any student or visitor connecting to campus Wi-Fi can open `http://<campus-server-ip>:8000` on their phone without installing an app.
2. **Cloud Server (Render / Railway / Fly.io / AWS EC2)**:
   - Deploy as a Docker container:
     ```dockerfile
     FROM python:3.13-slim
     WORKDIR /app
     COPY . /app
     RUN pip install --no-cache-dir -r campus_compass/requirements.txt
     CMD ["uvicorn", "campus_compass.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
     ```
3. **Preserving Existing GitHub Repository**:
   - The original static site files remain safely backed up in `existing_project/`.
   - The Python implementation lives cleanly organized in `campus_compass/` ready for version control.
