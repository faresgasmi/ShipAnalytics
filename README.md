<h1>Genmar – AI & BI Marine Analytics Platform</h1>
<h2>📝 Overview</h2>

Genmar is an advanced Artificial Intelligence (AI) and Business Intelligence (BI) project designed to assist port authorities and maritime companies in automating document extraction, predicting ship metrics, detecting anomalies, and identifying damages through computer vision.

This project integrates multiple AI models and an interactive dashboard built with Streamlit, providing an all-in-one solution for maritime data analysis and automation.

Main Objectives:

Automate data extraction from PDF invoices using OCR

Predict Gross Tonnage (GT) and Average Port Time for vessels

Detect operational anomalies in ships using ML

Identify container or ship damages with YOLOv9

Visualize and monitor key KPIs via a BI dashboard

<h2>🚀 Key Features</h2>
<h3>📄 Automated PDF Invoice Extraction (OCR)</h3>

Uses PDFPlumber to extract structured data from invoices automatically.

Extracts fields like Invoice Number, Type, Debarquement + Dépotage, Fret Charges, Magasinage, and more.

Exports clean data to Excel format for financial and logistics analysis.

<h3>⚙️ Gross Tonnage (GT) Prediction</h3>

Predicts the GT (Gross Tonnage) of a vessel using a pre-trained regression model (modele_gt.pkl).

Input features: Length, Width, and Deadweight (DWT).

Helps estimate vessel capacity for port operations.

<h3>⏱️ Average Port Time Prediction</h3>

Predicts the average stay time of ships in port using a Random Forest regression model (rf_model_port.pkl).

Inputs: Length, DWT, and Maximum Capacity.

Data normalized using scaler.pkl for consistent results.

<h3>⚠️ Anomaly Detection (AIS Data)</h3>

Detects anomalous ship behavior (e.g., abnormal navigation patterns).

Uses Isolation Forest trained on vessel navigation and physical data.

Encodes categorical features (Ship Type, Navigational Status) using One-Hot Encoding (columns_after_ohe.pkl).

Output: 🚨 Anomaly detected or ✅ Normal ship behavior.

<h3>📷 Damage Detection with YOLOv9</h3>

Integrates a YOLOv9 model (best.pt) to detect visible damages on containers or ships.

Runs inference directly in Streamlit and displays annotated detection results.

Useful for automating visual inspection during port entry.

<h3>📊 BI Dashboard & Analytics</h3>

Built-in dashboard in Streamlit to visualize key performance indicators:

Average unloading and loading times

Total freight costs (TND, USD, EUR)

Anomalies per ship type

Damage detection statistics

Combines AI predictions and business data for operational decision-making.

<h2>🛠 Technologies Used</h2>
Category	Tools & Libraries
Programming	Python, Streamlit
Machine Learning	Scikit-learn, Joblib
Computer Vision	YOLOv9 (Ultralytics)
OCR & NLP	PDFPlumber, Regex
Data Handling	Pandas, NumPy
Visualization	Streamlit Charts, BI Dashboard
Deployment	Streamlit Cloud / Local Server
<h2>📁 Project Structure</h2>
<pre> ├── app.py # Main Streamlit application ├── best.pt # YOLOv9 model weights ├── modele_gt.pkl # Gross Tonnage prediction model ├── rf_model_port.pkl # Port Time prediction model ├── scaler.pkl # Scaler for model normalization ├── isolation_forest_model.pkl # Anomaly detection model ├── columns_after_ohe.pkl # OHE columns for anomalies ├── factures_extraites.xlsx # Example of extracted invoice data ├── dashboard/ # BI Dashboard folder │ ├── kpi_overview.py │ ├── charts.py │ └── ... ├── README.md # Documentation </pre>
<h2>📸 Screenshots</h2>
<h3>📄 PDF Invoice Extraction</h3>

Automatically extracts invoice details from multiple uploaded PDFs.
<img width="407" height="510" alt="Image" src="https://github.com/user-attachments/assets/8428a314-a70f-4dcb-8657-59881ebe3337" />


<h3>⚙️ GT & Port Time Prediction</h3>

Predicts vessel Gross Tonnage and estimated time at port.
<img width="726" height="352" alt="Image" src="https://github.com/user-attachments/assets/01732715-2bcf-4c15-a22e-fb0e057d2806" />
<img width="735" height="354" alt="Image" src="https://github.com/user-attachments/assets/80214858-bd59-4979-b785-7d5ae0aa4772" />


<h3>⚠️ Anomaly Detection</h3>

Detects abnormal ship behavior (speed, heading, draft, etc.).
<img width="570" height="533" alt="Image" src="https://github.com/user-attachments/assets/7fc2ed34-770c-4f80-87e3-3803668c8670" />


<h3>📷 Damage Detection with YOLOv9</h3>

YOLOv9 detects visible damages directly from uploaded images.
<img width="352" height="479" alt="Image" src="https://github.com/user-attachments/assets/07ca56d0-3944-48f9-9ff1-da76297c8cd6" />


<h3>📊 Dashboard Overview</h3>

Visual BI dashboard summarizing key maritime KPIs.
<img width="710" height="384" alt="Image" src="https://github.com/user-attachments/assets/485eadb3-f188-4334-9528-5a305e444fed" />
<img width="713" height="380" alt="Image" src="https://github.com/user-attachments/assets/49f5b291-d670-498a-a0c5-887273df898c" />


<h2>🧠 Insights & Benefits</h2>

🚀 Automation of manual PDF data extraction and inspection

📈 Predictive insights on port operations and ship metrics

🧩 Unified platform combining OCR, ML, and Computer Vision

🔍 Early anomaly detection for risk prevention

💡 Data-driven decisions supported by real-time analytics

<h2>📌 Why This Project?</h2>

This project demonstrates the ability to build a complete AI pipeline combining:

OCR document processing

Predictive analytics

Anomaly detection

Computer vision

Business Intelligence visualization

It supports maritime organizations in optimizing efficiency, minimizing inspection time, and improving decision-making.

<h2>⚙️ Tech Stack Summary</h2>

Frontend: Streamlit

Models: Scikit-learn, YOLOv9 (Ultralytics)

Data Extraction: PDFPlumber, Regex

Visualization: Streamlit Charts / BI Dashboards

Deployment: Streamlit Cloud

<h2>🌐 Connect with Me</h2>

📧 Email: faresguesmi815@gmail.com

🔗 LinkedIn: Fares Guesmi

<h2>⭐ Give It a Star!</h2>

If you like this project, don’t forget to star ⭐ the repository and share it with others!
