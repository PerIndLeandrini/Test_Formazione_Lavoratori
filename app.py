import streamlit as st
import pandas as pd
import os
from datetime import datetime as dt
from math import ceil
from zoneinfo import ZoneInfo
from domande import MODULI
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# ------------------------------------------------------------
# CONFIGURAZIONE BASE
# ------------------------------------------------------------
st.set_page_config(page_title="Test Formazione Lavoratori", layout="wide", page_icon="🧑‍🏫")
st.markdown("<h2 style='color:#00c3ff'>🧑‍🏫 Test – Formazione Lavoratori (D.Lgs. 81/08)</h2>", unsafe_allow_html=True)

# Stato iniziale
if "test_avviato" not in st.session_state:
    st.session_state.test_avviato = False

# ------------------------------------------------------------
# DOMANDE (SOLO TESTO, SCELTA MULTIPLA) – organizzate per MODULO
# Le risposte corrette sono indicate dall'indice (0-based) in "risposta_corretta"
# ------------------------------------------------------------
MODULI = {
    "GEN_NORM": {
        "titolo": "Formazione generale – Parte normativa",
        "num_domande": 5,
        "domande": [
            {
                "testo": "Il D.Lgs. 81/08 identifica il datore di lavoro come il soggetto responsabile della sicurezza?",
                "opzioni": ["Sì, sempre", "No, mai", "Solo se lo delega"],
                "risposta_corretta": 0,
            },
            {
                "testo": "Chi è il RSPP?",
                "opzioni": [
                    "Il Responsabile del Servizio di Prevenzione e Protezione",
                    "Il Rappresentante dei Lavoratori per la Sicurezza",
                    "Il Referente Sindacale per i Procedimenti Penali"
                ],
                "risposta_corretta": 0,
            },
            {
                "testo": "La valutazione dei rischi deve essere:",
                "opzioni": ["Solo orale", "Scritta nel DVR e aggiornata", "Facoltativa"],
                "risposta_corretta": 1,
            },
            {
                "testo": "Chi ha l'obbligo di utilizzare i DPI messi a disposizione?",
                "opzioni": ["Solo il preposto", "Tutti i lavoratori", "Solo i neoassunti"],
                "risposta_corretta": 1,
            },
            {
                "testo": "Il RLS:",
                "opzioni": [
                    "È nominato dall'INAIL",
                    "È eletto/designato dai lavoratori e partecipa alla prevenzione",
                    "È un consulente esterno sempre obbligatorio"
                ],
                "risposta_corretta": 1,
            },
        ],
    },
    "SPEC_ERGO": {
        "titolo": "Formazione specifica – Rischi ergonomici",
        "num_domande": 3,
        "domande": [
            {
                "testo": "Un rischio ergonomico tipico negli uffici è:",
                "opzioni": ["Rumore impulsivo", "Postura incongrua prolungata", "Rischio biologico elevato"],
                "risposta_corretta": 1,
            },
            {
                "testo": "Quale misura aiuta a ridurre il rischio da movimentazione manuale carichi?",
                "opzioni": ["Aumentare il peso dei colli", "Uso di ausili/meccanizzazione e tecniche corrette", "Ignorare i limiti di peso"],
                "risposta_corretta": 1,
            },
            {
                "testo": "Per il lavoro al videoterminale è utile:",
                "opzioni": ["Monitor troppo alto rispetto agli occhi", "Pianificare pause e micro-pause e regolare la postazione", "Illuminazione abbagliante"],
                "risposta_corretta": 1,
            },
        ],
    },
    "SPEC_RUMORE": {
        "titolo": "Formazione specifica – Rischio rumore",
        "num_domande": 3,
        "domande": [
            {
                "testo": "Quando si usano le cuffie antirumore?",
                "opzioni": [
                    "Solo se danno fastidio",
                    "Quando i livelli superano i valori di azione o quando richiesto dalle procedure",
                    "Mai, se l'esposizione è breve"
                ],
                "risposta_corretta": 1,
            },
            {
                "testo": "Qual è una buona pratica contro il rumore?",
                "opzioni": ["Lasciare le protezioni aperte", "Manutenzione macchine e barriere fonoassorbenti", "Aumentare la velocità delle macchine"],
                "risposta_corretta": 1,
            },
            {
                "testo": "Il rischio rumore può causare:",
                "opzioni": ["Irritazioni cutanee", "Ipoacusia nel tempo", "Problemi esclusivamente visivi"],
                "risposta_corretta": 1,
            },
        ],
    },
    "SPEC_INCENDIO": {
        "titolo": "Formazione specifica – Incendio ed emergenze",
        "num_domande": 5,
        "domande": [
            {
                "testo": "Qual è la prima azione in caso di incendio?",
                "opzioni": ["Nascondersi sotto la scrivania", "Dare l'allarme e seguire le procedure di emergenza", "Usare sempre l'ascensore"],
                "risposta_corretta": 1,
            },
            {
                "testo": "Durante l'evacuazione è corretto:",
                "opzioni": ["Chiudere le porte dietro di sé", "Tornare indietro per recuperare oggetti", "Usare l'ascensore"],
                "risposta_corretta": 0,
            },
            {
                "testo": "Quale estintore si usa su apparecchiature elettriche?",
                "opzioni": ["Acqua", "CO2 o polvere idonea", "Schiuma sempre"],
                "risposta_corretta": 1,
            },
            {
                "testo": "Chi coordina le emergenze in azienda?",
                "opzioni": ["Il primo che passa", "La squadra di emergenza secondo il piano di emergenza", "Sempre il RLS"],
                "risposta_corretta": 1,
            },
            {
                "testo": "In presenza di fumo nei corridoi conviene:",
                "opzioni": ["Procedere bassi vicino al pavimento", "Correre a testa alta", "Aprire tutte le finestre"],
                "risposta_corretta": 0,
            },
        ],
    },
    "SPEC_ELETTRICO": {
        "titolo": "Formazione specifica – Rischio elettrico (base)",
        "num_domande": 2,
        "domande": [
            {
                "testo": "Una buona pratica per il rischio elettrico è:",
                "opzioni": ["Usare prese multiple sovraccaricate", "Verificare integrità cavi e prese, non improvvisare riparazioni", "Togliere sempre le protezioni"],
                "risposta_corretta": 1,
            },
            {
                "testo": "Se si nota un cavo danneggiato:",
                "opzioni": ["Si continua ad usarlo se funziona", "Lo si segnala e si mette fuori servizio", "Lo si copre con nastro adesivo"],
                "risposta_corretta": 1,
            },
        ],
    },
    "SPEC_CHIMICO": {
        "titolo": "Formazione specifica – Rischi chimico",
        "num_domande": 3,
        "domande": [
            {
                "testo": "Le SDS (Schede di Sicurezza) servono a:",
                "opzioni": ["Scopi commerciali", "Informare su pericoli, DPI e misure di emergenza", "Sono opzionali"],
                "risposta_corretta": 1,
            },
            {
                "testo": "Quale misura riduce l'esposizione a sostanze pericolose?",
                "opzioni": ["Ventilazione/aspirazione localizzata e contenimento", "Mangiare nell'area di lavoro", "Tenere i contenitori aperti"],
                "risposta_corretta": 0,
            },
            {
                "testo": "In caso di contatto cutaneo con un prodotto corrosivo:",
                "opzioni": ["Attendere che passi", "Risciacquare abbondantemente e consultare la SDS/medico", "Coprirlo con guanti"],
                "risposta_corretta": 1,
            },
        ],
    },
}

# ------------------------------------------------------------
# FORM DATI PARTECIPANTE + SCELTA MODULO
# ------------------------------------------------------------
if not st.session_state.test_avviato:
    with st.form("dati_partecipante"):
        st.subheader("Dati del partecipante")
        nome = st.text_input("Nome e Cognome", max_chars=100)
        cf = st.text_input("Codice Fiscale (obbligatorio)", max_chars=16)
        azienda = st.text_input("Azienda")

        st.subheader("🧩 Seleziona il modulo di test")
        elenco_moduli = {v["titolo"]: k for k, v in MODULI.items()}
        modulo_nome = st.selectbox("Modulo", list(elenco_moduli.keys()))
        modulo_key = elenco_moduli[modulo_nome]

        st.subheader("📨 RIFERIMENTI MAIL")
        mail_partecipante = st.text_input(
            "📧 Email a cui inviare il report (può essere multipla, separata da virgole)",
            placeholder="es. mario.rossi@email.com, rspp@azienda.it",
        )
        invia_copia_me = st.checkbox("✅ Invia copia anche a Simone Leandrini")

        accetto = st.checkbox("✅ Dichiaro di accettare il trattamento dei dati ai fini formativi (privacy)")
        avvia = st.form_submit_button("Inizia il test")

        if avvia:
            if not (nome and cf and azienda and accetto and mail_partecipante):
                st.error("Compila tutti i campi richiesti e accetta la privacy.")
            else:
                st.session_state.test_avviato = True
                st.session_state.nome = nome
                st.session_state.cf = cf.upper()
                st.session_state.azienda = azienda
                st.session_state.email_dest = [email.strip() for email in mail_partecipante.split(",") if email.strip()]
                if invia_copia_me:
                    st.session_state.email_dest.append("perindleandrini@4step.it")
                st.session_state.modulo_key = modulo_key

# ------------------------------------------------------------
# EROGAZIONE TEST
# ------------------------------------------------------------
if st.session_state.test_avviato:
    key = st.session_state.modulo_key
    modulo = MODULI[key]
    domande = modulo["domande"]

    st.markdown("---")
    st.subheader(f"📋 {modulo['titolo']} – {modulo['num_domande']} domande a risposta multipla")

    risposte_utente = []
    punteggio = 0

    for i, domanda in enumerate(domande):
        st.markdown(f"**Domanda {i+1}:** {domanda['testo']}")
        risposta = st.radio("Scegli la risposta:", domanda["opzioni"], key=f"q_{i}")
        risposte_utente.append(risposta)

    if st.button("Conferma e correggi il test"):
        st.markdown("---")
        st.subheader("📊 Risultato del test")

        for i, domanda in enumerate(domande):
            scelta = risposte_utente[i]
            corretta = domanda["opzioni"][domanda["risposta_corretta"]]
            if scelta == corretta:
                punteggio += 1
                st.success(f"✅ Domanda {i+1}: Corretta")
            else:
                st.error(f"❌ Domanda {i+1}: Errata – Risposta corretta: {corretta}")

        n = len(domande)
        soglia = ceil(n * 0.8)  # 80% arrotondato per eccesso
        superato = punteggio >= soglia
        st.markdown(f"### Totale corrette: **{punteggio}/{n}** (Soglia: {soglia})")
        st.success("✅ Test superato!" if superato else "❌ Test NON superato")

        # Salvataggio risultato in Excel (una riga per partecipante/test)
        data_ora = dt.now(ZoneInfo("Europe/Rome")).strftime('%Y-%m-%d %H:%M')
        risultato = {
            "Data": data_ora,
            "Modulo": modulo["titolo"],
            "Nome": st.session_state.nome,
            "Codice Fiscale": st.session_state.cf,
            "Azienda": st.session_state.azienda,
            "Punteggio": punteggio,
            "Esito": "Superato" if superato else "Non superato",
        }
        for i, r in enumerate(risposte_utente):
            risultato[f"Domanda_{i+1}"] = r

        df = pd.DataFrame([risultato])
        os.makedirs("risultati_formazione", exist_ok=True)
        file_path = "risultati_formazione/risultati_test.xlsx"

        if os.path.exists(file_path):
            try:
                df_exist = pd.read_excel(file_path)
                df_final = pd.concat([df_exist, df], ignore_index=True)
            except Exception:
                # fallback: se il file è aperto altrove o corrotto, scrivi solo la nuova riga
                df_final = df
        else:
            df_final = df

        df_final.to_excel(file_path, index=False)
        st.info("📁 Risultati salvati in `risultati_formazione/risultati_test.xlsx`.")

        # Email con riepilogo (allega l'Excel cumulativo)
        try:
            sender = st.secrets["email"]["sender"]
            password = st.secrets["email"]["password"]
        except Exception:
            sender = None
            password = None

        corpo = f"""🧾 TEST COMPLETATO – {modulo['titolo']}

📛 NOMINATIVO: {st.session_state.nome}
🆔 Codice Fiscale: {st.session_state.cf}
🏢 Azienda: {st.session_state.azienda}
🕒 Data/Ora: {data_ora}
📈 Punteggio: {punteggio}/{n}
📌 Esito: {'✅ SUPERATO' if superato else '❌ NON SUPERATO'}

📖 RISPOSTE DETTAGLIATE:
"""
        for i, domanda in enumerate(domande):
            testo = domanda["testo"]
            risposta_data = risposte_utente[i]
            corretta = domanda["opzioni"][domanda["risposta_corretta"]]
            esito = "✅ CORRETTA" if risposta_data == corretta else f"❌ ERRATA (Corretto: {corretta})"
            corpo += f"\nDomanda {i+1}: {testo}\nRisposta: {risposta_data} → {esito}\n"

        if sender and password and st.session_state.email_dest:
            for destinatario in st.session_state.email_dest:
                msg = MIMEMultipart()
                msg["Subject"] = f"📩 Test Formazione – {modulo['titolo']} – {st.session_state.nome}"
                msg["From"] = sender
                msg["To"] = destinatario

                msg.attach(MIMEText(corpo, "plain"))

                # Allegato Excel cumulativo
                try:
                    with open(file_path, "rb") as f:
                        excel = MIMEApplication(f.read(), _subtype="xlsx")
                        excel.add_header('Content-Disposition', 'attachment', filename="risultati_test.xlsx")
                        msg.attach(excel)
                except Exception as e:
                    st.warning(f"⚠️ Impossibile allegare l'Excel: {e}")

                try:
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                        server.login(sender, password)
                        server.send_message(msg)
                    st.success(f"📤 Email inviata correttamente a: {destinatario}")
                except Exception as e:
                    st.warning(f"❌ Errore nell'invio email a {destinatario}: {e}")
        else:
            st.info("✉️ Email non inviata: configura le credenziali in .streamlit/secrets.toml o nessun destinatario.")
