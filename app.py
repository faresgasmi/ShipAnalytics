import streamlit as st
import pdfplumber
import re
import pandas as pd
import numpy as np
import joblib
from io import BytesIO
import os
from ultralytics import YOLO
from PIL import Image

# ====== Fonction format FR ======
def fr_format(n, decimals=0):
    txt = f"{float(n):,.{decimals}f}"
    txt = txt.replace(",", " ").replace(".", ",")
    return txt

# ====== Charger les modèles .pkl ======
@st.cache_resource
def load_model(path):
    if not os.path.exists(path):
        st.error(f"⚠️ Fichier du modèle introuvable : {path}")
        return None
    return joblib.load(path)

model_gt = load_model("modele_gt.pkl")          # Modèle GT
model_port = load_model("rf_model_port.pkl")    # Modèle temps au port
scaler_port = load_model("scaler.pkl")          # Scaler si utilisé pour le modèle port
model_anomaly = load_model("isolation_forest_model.pkl")  # Modèle anomalies
columns_ohe = load_model("columns_after_ohe.pkl")         # Colonnes après OHE anomalies

# ====== Charger YOLOv9 (weights en .pt) ======
@st.cache_resource
def load_yolo_model(path="best.pt"):
    if not os.path.exists(path):
        st.error(f"⚠️ Modèle YOLOv9 introuvable : {path}")
        return None
    return YOLO(path)

yolo_model = load_yolo_model("best.pt")  # change le chemin si nécessaire

# ====== Fonctions OCR ======
def extraire_texte_pdf(file):
    texte_complet = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            texte = page.extract_text()
            if texte:
                texte_complet += texte + "\n"
    return texte_complet

def detecter_type_facture(texte):
    texte = texte.lower()
    if "facture timbrage import" in texte:
        return "ftm"
    elif "facture magasinage" in texte:
        return "fmm"
    return "autre"

def extraire_numero_facture(texte):
    pattern = r"facture timbrage import m\.c\. n° ?:?\s*(\d+)"
    res = re.search(pattern, texte, flags=re.IGNORECASE)
    if res:
        return res.group(1)
    res2 = re.search(r"facture.*?(\d{5,})", texte, flags=re.IGNORECASE)
    return res2.group(1) if res2 else "0"

def extraire_montant(mot_cle, texte):
    pattern = rf"{mot_cle}\s+([\d\s,\.]+)"
    res = re.search(pattern, texte, flags=re.IGNORECASE)
    if res:
        montant_str = res.group(1).replace(' ', '').replace(',', '.')
        try:
            return float(montant_str)
        except:
            return 0
    return 0

def extraire_origine(texte):
    pattern = r"Embarquement ?:?\s*([^\n\r]+)"
    res = re.search(pattern, texte, flags=re.IGNORECASE)
    if res:
        valeur = res.group(1).strip()
        valeur = re.split(r"\b(BL|Corresp\.|M\.F\.|R\.C\.)\b", valeur, flags=re.IGNORECASE)[0].strip()
        return valeur
    return "0"

def extraire_code_correspondant(texte):
    pattern = r"Corresp\. ?:?\s*([^\s\n\r]+)"
    res = re.search(pattern, texte, flags=re.IGNORECASE)
    return res.group(1).strip() if res else "0"

# ====== Colonnes du tableau ======
colonnes = ['N° Facture', 'Type', 'Debarquement + Depotage', 'MISE EN MAGASIN',
            'REST CONT°', 'MISE A FOB', 'FRAIS BL', 'HAM', 'FRAIS DIVERS', 'ISPS',
            'Avis et B A D ', 'Frais Dossier', 'FRET EN TND', 'FRET EN USD',
            'FRET EN EUR', 'Retour de fonds', 'Unnamed: 16', 'Magasinage',
            'Rechargement', 'Assurance', 'Chariot', 'Origine', 'Corrspondant']

# ====== Interface Streamlit ======
st.title("📄 Extraction Factures PDF ")

# --- Section 1 : OCR PDF ---
uploaded_files = st.file_uploader("📤 Importer plusieurs fichiers PDF", type="pdf", accept_multiple_files=True)
df = pd.DataFrame()

if uploaded_files:
    donnees_factures = []

    for file in uploaded_files:
        st.subheader(f"📄 {file.name}")
        texte = extraire_texte_pdf(file)
        st.text(texte[:1000])

        ligne = {
            'N° Facture': extraire_numero_facture(texte),
            'Type': detecter_type_facture(texte),
            'Debarquement + Depotage': extraire_montant("DEBARQUEMENT", texte),
            'MISE EN MAGASIN': extraire_montant("MISE EN MAGASIN", texte),
            'REST CONT°': extraire_montant("REST CONT°", texte),
            'MISE A FOB': extraire_montant("MISE A FOB", texte),
            'FRAIS BL': extraire_montant("FRAIS B/L", texte),
            'HAM': extraire_montant("HAM", texte),
            'FRAIS DIVERS': extraire_montant("FRAIS DIVERS", texte),
            'ISPS': extraire_montant("ISPS", texte),
            'Avis et B A D ': extraire_montant("P V DE DOUANE", texte),
            'Frais Dossier': extraire_montant("FRAIS DOCUMENTATION", texte),
            'FRET EN TND': extraire_montant("FREIGHT", texte),
            'FRET EN USD': extraire_montant("FREIGHT USD", texte),
            'FRET EN EUR': extraire_montant("FREIGHT EUR", texte),
            'Retour de fonds': extraire_montant("RETOUR DE FONDS", texte),
            'Unnamed: 16': 0,
            'Magasinage': extraire_montant("STATIONNEMENT", texte),
            'Rechargement': extraire_montant("RECHARGEMENT", texte),
            'Assurance': extraire_montant("ASSURANCE", texte),
            'Chariot': extraire_montant("CHARIOT", texte),
            'Origine': extraire_origine(texte),
            'Corrspondant': extraire_code_correspondant(texte)
        }

        donnees_factures.append(ligne)

    df = pd.DataFrame(donnees_factures, columns=colonnes)
    st.success("✅ Extraction terminée")
    st.dataframe(df)

    # Télécharger Excel
    buffer = BytesIO()
    df.to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)
    st.download_button("💾 Télécharger le fichier Excel", buffer, file_name="factures_extraites.xlsx")
else:
    st.info("⬆️ Importez un ou plusieurs fichiers PDF à traiter.")

# --- Section 2 : Prédiction GT ---
st.header("🚢 Prédire le GT d'un navire")
if model_gt:
    length = st.number_input("📏 Longueur (m)", min_value=1.0, max_value=500.0, value=200.0)
    width = st.number_input("📐 Largeur (m)", min_value=1.0, max_value=100.0, value=32.0)
    dwt = st.number_input("⚖️ DWT (tonnes)", min_value=1000.0, max_value=500000.0, value=50000.0)

    if st.button("🔮 Prédire GT"):
        X_new_gt = np.array([[length, width, dwt]])
        pred_gt = model_gt.predict(X_new_gt)
        val_gt = float(pred_gt[0])
        st.success(f"📊 GT estimé : {fr_format(val_gt, 2)} unités")

# --- Section 3 : Prédiction Temps au Port ---
st.header("⏱ Prédire le Temps Moyen au Port")
if model_port:
    length_port = st.number_input("📏 Longueur navire (m)", min_value=1.0, max_value=500.0, value=200.0, key="length_port")
    dwt_port = st.number_input("⚖️ DWT (tonnes)", min_value=1000.0, max_value=500000.0, value=50000.0, key="dwt_port")
    max_capacity_port = st.number_input("📦 Capacité maximale (tonnes)", min_value=1000.0, max_value=500000.0, value=50000.0, key="max_capacity_port")

    if st.button("🔮 Prédire Temps au Port"):
        X_new_port = np.array([[length_port, dwt_port, max_capacity_port]])
        if scaler_port:
            X_new_port_scaled = scaler_port.transform(X_new_port)
            pred_days = float(model_port.predict(X_new_port_scaled)[0])
        else:
            pred_days = float(model_port.predict(X_new_port)[0])

        jours = int(pred_days)
        heures = int((pred_days - jours) * 24)
        minutes = int((((pred_days - jours) * 24) - heures) * 60)
        st.info(f"⏱ Temps moyen au port estimé : {jours} jour(s), {heures} heure(s), {minutes} minute(s)")

# --- Section 4 : Détection d'anomalies navire ---
st.header("⚠️ Détection d'anomalies sur un navire")
if model_anomaly:
    navigationalstatus = st.selectbox("Statut de navigation", ["Underway", "At anchor", "Moored"], key="nav_status")
    shiptype = st.selectbox("Type de navire", ["Cargo", "Tanker", "Passenger", "Other"], key="ship_type")
    sog = st.number_input("Vitesse (SOG)", min_value=0.0, max_value=50.0, value=0.0, key="sog")
    cog = st.number_input("Course (COG)", min_value=0.0, max_value=360.0, value=0.0, key="cog")
    heading = st.number_input("Cap (heading)", min_value=0.0, max_value=360.0, value=0.0, key="heading")
    width_nav = st.number_input("Largeur (m)", min_value=0.0, value=32.0, key="width_nav")
    length_nav = st.number_input("Longueur (m)", min_value=0.0, value=200.0, key="length_nav")
    draught = st.number_input("Tirant d'eau (m)", min_value=0.0, value=10.0, key="draught")

    if st.button("🔮 Vérifier anomalie"):
        new_data = pd.DataFrame([{
            "navigationalstatus": navigationalstatus,
            "shiptype": shiptype,
            "sog": sog,
            "cog": cog,
            "heading": heading,
            "width": width_nav,
            "length": length_nav,
            "draught": draught
        }])

        # One-Hot Encoding
        new_data_encoded = pd.get_dummies(new_data)
        for col in columns_ohe:
            if col not in new_data_encoded.columns:
                new_data_encoded[col] = 0
        new_data_encoded = new_data_encoded[columns_ohe]

        # Prédiction anomalies
        prediction = model_anomaly.predict(new_data_encoded)
        if prediction[0] == -1:
            st.error("🚨 Anomalie détectée !")
        else:
            st.success("✅ Navire normal")

# --- Section 5 : Détection de dommages avec YOLOv9 ---
st.header("📷 Détection de dommages (YOLOv9)")
uploaded_img = st.file_uploader("📤 Importer une image de conteneur", type=["jpg", "jpeg", "png"])

if uploaded_img and yolo_model:
    image = Image.open(uploaded_img).convert("RGB")
    st.image(image, caption="🖼️ Image importée", use_container_width=True)

    if st.button("🔍 Détecter les dommages"):
        results = yolo_model.predict(image, conf=0.2)  # seuil confiance abaissé

        if results:
            res = results[0]  # premier résultat
            im_array = res.plot()
            st.image(im_array, caption="📌 Résultat YOLOv9", use_container_width=True)
        else:
            st.info("❌ Aucun dommage détecté")
