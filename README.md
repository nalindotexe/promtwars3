# TerraByte — The Eco-Action Intelligence Assistant

🌱 **TerraByte** is a context-aware carbon footprint tracker and smart ecological recommendation engine built for competitive hackathons. By evaluating user commute, dietary, and energy consumption metrics completely locally, TerraByte provides immediate carbon transparency and generates actionable, quantified micro-actions to guide users towards sustainable living.

---

## 🎯 Project Vertical & Persona
- **Project Vertical:** ClimateTech / Personal Sustainability / AI Decision Support.
- **Persona:** *"The Eco-Action Intelligence Assistant"* — A smart, friction-free companion that doesn't just calculate carbon numbers but translates them into immediately actionable, personalized advice with real-world savings estimates.

---

## 🧠 Approach & Logic

### 1. Calculation Engine (`CarbonEngine`)
All calculations are performed using standardized, regional carbon intensity coefficients. To ensure extreme efficiency and offline compatibility, these factors are defined locally:
- **Commute Distance Emissions:**
  - **Driving:** $0.20 \text{ kg CO}_2 / \text{km}$
  - **Public Transit:** $0.05 \text{ kg CO}_2 / \text{km}$
  - **Walking/Cycling:** $0.00 \text{ kg CO}_2 / \text{km}$
- **Dietary Footprint (Daily Baseline):**
  - **Vegan:** $1.5 \text{ kg CO}_2 / \text{day}$
  - **Vegetarian:** $2.0 \text{ kg CO}_2 / \text{day}$
  - **Balanced:** $2.5 \text{ kg CO}_2 / \text{day}$
  - **Meat-Heavy:** $3.3 \text{ kg CO}_2 / \text{day}$
- **Home Energy Emissions:**
  - **Electricity usage:** $0.40 \text{ kg CO}_2 / \text{kWh}$

### 2. Context-Aware Assistant (`EcoAssistant`)
Instead of displaying generic environmental tips, the recommendation engine targets the user's specific high-emission categories:
- **Commute optimization:** Suggests public transit, active commuting, or carpooling, calculating the exact difference in carbon savings.
- **Dietary transitions:** Quantifies carbon reduction by shifting down one tier of dietary impact (e.g., from meat-heavy to vegetarian, vegetarian to vegan).
- **Home energy efficiency:** Projects a 15% reduction in electricity demand using smart home management habits.
- **Sorting & Prioritization:** Recommendations are dynamically ranked by potential carbon impact (High, Medium, Low) based on their quantitative savings.

---

## 🔒 Security & Efficiency
- **Zero Remote Calls / API Latency:** Computations are completed locally, respecting privacy and offering offline support.
- **Zero Third-Party Data Pipelines:** No personal or lifestyle data leaves the user's machine.
- **Strict Dependency Management:** We only rely on standard, highly optimized, pinned dependencies: `streamlit`, `pandas`, and `pytest`, fitting well under the **10 MB** package limit constraint.

---

## ♿ Accessibility & UI design
- **High-Contrast Typography:** Built with *Outfit* (Google Fonts) and clean weights, rendering clearly against a dark aesthetic backdrop.
- **Visual Hierarchy:** Clean separation between KPI summaries, interactive baseline charts, and custom styled color-coded recommendation cards.
- **Responsive Layout:** Designed to scale beautifully from wide desktop monitors to mobile displays.

---

## 🚀 Setup & Execution Instructions

### Prerequisites
- Python 3.9 or higher installed.

### 1. Install Dependencies
Initialize a virtual environment and install dependencies listed in `requirements.txt`:
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Run Unit Tests
Validate calculations and recommendation logic:
```bash
pytest tests/test_assistant.py
```

### 3. Launch Streamlit Application
Start the Streamlit application server:
```bash
streamlit run app.py
```
A browser window should automatically open displaying the TerraByte dashboard at `http://localhost:8501`.
