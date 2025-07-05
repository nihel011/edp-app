
import streamlit as st
import pandas as pd
from datetime import date
import os

# 📌 Paramètres
retention = 200_000
plafond = 15_000_000
fichier_excel = "traite_excedent_de_plein.xlsx"

st.set_page_config(page_title="Traité en excédent de plein", layout="centered")
st.title("📘 Outil - Traité en excédent de plein")

col1, col2 = st.columns(2)
with col1:
    num_police = st.text_input("N° Police")
    capital_assure = st.number_input("Capital assuré", min_value=0.0, step=1000.0)
    sap = st.number_input("SAP", min_value=0.0)
    date_sinistre = st.date_input("Date sinistre", value=None)
with col2:
    num_sinistre = st.text_input("N° Sinistre")
    prime = st.number_input("Prime", min_value=0.0)
    reglement = st.number_input("Règlement", min_value=0.0)
    date_effet = st.date_input("Date d'effet", value=None)

date_echeance = st.date_input("Date d’échéance", value=None)

if st.button("📥 Calculer et enregistrer"):
    try:
        charge_sinistre = sap + reglement
        retenue = min(capital_assure, retention)

        edp = max(min(capital_assure, plafond) - retention, 0)
        fac = max(capital_assure - plafond, 0)

        taux_ret = retenue / capital_assure * 100 if capital_assure != 0 else 0
        taux_edp = edp / capital_assure * 100 if capital_assure != 0 else 0
        taux_fac = fac / capital_assure * 100 if capital_assure != 0 else 0

        prime_ret = prime * taux_ret / 100
        prime_edp = prime * taux_edp / 100
        prime_fac = prime * taux_fac / 100

        sap_ret = sap * taux_ret / 100
        sap_edp = sap * taux_edp / 100
        sap_fac = sap * taux_fac / 100

        reg_ret = reglement * taux_ret / 100
        reg_edp = reglement * taux_edp / 100
        reg_fac = reglement * taux_fac / 100

        charge_ret = sap_ret + reg_ret
        charge_edp = sap_edp + reg_edp
        charge_fac = sap_fac + reg_fac

        # Charger les anciens enregistrements s'ils existent
        if os.path.exists(fichier_excel):
            old_df = pd.read_excel(fichier_excel)
        else:
            old_df = pd.DataFrame()

        df = pd.DataFrame({
            "Num Police": [num_police],
            "Num de sinistre": [num_sinistre],
            "Date sinistre": [date_sinistre.strftime('%d/%m/%Y') if date_sinistre else ''],
            "Date d'effet": [date_effet.strftime('%d/%m/%Y') if date_effet else ''],
            "Date d’échéance": [date_echeance.strftime('%d/%m/%Y') if date_echeance else ''],
            "Capital assuré": [capital_assure],
            "Prime": [prime],
            "SAP": [sap],
            "Règlement": [reglement],
            "Charge de sinistre": [charge_sinistre],
            "Taux Retention (%)": [taux_ret],
            "Taux EDP (%)": [taux_edp],
            "Taux FAC (%)": [taux_fac],
            "Prime Retenue": [prime_ret],
            "Prime EDP": [prime_edp],
            "Prime FAC": [prime_fac],
            "SAP Retenu": [sap_ret],
            "SAP EDP": [sap_edp],
            "SAP FAC": [sap_fac],
            "Règlement Retenu": [reg_ret],
            "Règlement EDP": [reg_edp],
            "Règlement FAC": [reg_fac],
            "Charge de sinistre Retenue": [charge_ret],
            "Charge de sinistre EDP": [charge_edp],
            "Charge de sinistre FAC": [charge_fac],
        })

        full_df = pd.concat([old_df, df], ignore_index=True)
        full_df.to_excel(fichier_excel, index=False)
        st.success("✅ Contrat enregistré avec succès.")
        with open(fichier_excel, "rb") as f:
            st.download_button("⬇️ Télécharger le fichier Excel", data=f, file_name=fichier_excel, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        st.error(f"❌ Une erreur est survenue : {e}")
