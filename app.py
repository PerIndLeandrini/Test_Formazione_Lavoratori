import streamlit as st
import pandas as pd
import os
from datetime import datetime as dt
from math import ceil
from zoneinfo import ZoneInfo
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
# FORM DATI PARTECIPANTE (TEST UNICO – tutte le sezioni in sequenza)
# ------------------------------------------------------------
if not st.session_state.test_avviato:
    with st.form("dati_partecipante"):
        st.subheader("Dati del partecipante")
        nome = st.text_input("Nome e Cognome", max_chars=100)
        cf = st.text_input("Codice Fiscale (obbligatorio)", max_chars=16)
        azienda = st.text_input("Azienda")

        st.subheader("📨 RIFERIMENTI MAIL")
        mail_partecipante = st.text_input(
            "📧 Email a cui inviare il report (può essere multipla, separata da virgole)",
            placeholder="es. mario.rossi@email.com, rspp@azienda.it",
        )
        
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
                st.session_state.email_dest.append("perindleandrini@4step.it")

# ------------------------------------------------------------
# EROGAZIONE TEST (TUTTE LE SEZIONI IN SEQUENZA)
# ------------------------------------------------------------
if st.session_state.test_avviato:
    # Costruisci una lista piatta di (section_key, index_in_section, domanda)
    sequenza = []
    ordine_sezioni = [
        "GEN_NORM",
        "SPEC_ERGO",
        "SPEC_RUMORE",
        "SPEC_INCENDIO",
        "SPEC_ELETTRICO",
        "SPEC_CHIMICO",
    ]
    for sk in ordine_sezioni:
        modulo = MODULI[sk]
        for i, domanda in enumerate(modulo["domande"]):
            sequenza.append((sk, i, domanda))

    st.markdown("---")
    st.subheader("📋 Test unico – tutte le sezioni in sequenza")

    risposte_utente = []
    punteggio = 0

    current_section = None
    # Render con intestazione di sezione quando cambia la chiave
    for global_idx, (sk, i, domanda) in enumerate(sequenza, start=1):
        if sk != current_section:
            current_section = sk
            st.markdown("")
            st.markdown(f"### 🧩 {MODULI[sk]['titolo']}")
        st.markdown(f"**Domanda {global_idx}:** {domanda['testo']}")
        risposta = st.radio(
            "Scegli la risposta:",
            domanda["opzioni"],
            key=f"q_{sk}_{i}"
        )
        risposte_utente.append((sk, i, risposta))

    if st.button("Conferma e correggi il test"):
        st.markdown("---")
        st.subheader("📊 Risultato del test")

        # Correzione e stampa esiti con intestazioni per sezione
        punteggio = 0
        current_section = None
        n = len(sequenza)
        for global_idx, (sk, i, risposta_data) in enumerate(risposte_utente, start=1):
            if sk != current_section:
                current_section = sk
                st.markdown("")
                st.markdown(f"#### 🔹 {MODULI[sk]['titolo']}")
            domanda = MODULI[sk]["domande"][i]
            corretta = domanda["opzioni"][domanda["risposta_corretta"]]
            if risposta_data == corretta:
                punteggio += 1
                st.success(f"✅ Domanda {global_idx}: Corretta")
            else:
                st.error(f"❌ Domanda {global_idx}: Errata – Risposta corretta: {corretta}")

        from math import ceil
        soglia = ceil(n * 0.8)  # 80% arrotondato per eccesso sull'intero test
        superato = punteggio >= soglia
        st.markdown(f"### Totale corrette: **{punteggio}/{n}** (Soglia: {soglia})")
        st.success("✅ Test superato!" if superato else "❌ Test NON superato")

        # Salvataggio risultato in Excel (una riga per partecipante/test)
        data_ora = dt.now(ZoneInfo("Europe/Rome")).strftime('%Y-%m-%d %H:%M')
        risultato = {
            "Data": data_ora,
            "Nome": st.session_state.nome,
            "Codice Fiscale": st.session_state.cf,
            "Azienda": st.session_state.azienda,
            "Punteggio": punteggio,
            "Esito": "Superato" if superato else "Non superato",
            "Sezioni": ", ".join([MODULI[k]["titolo"] for k in ordine_sezioni]),
        }
        # Risposte dettagliate (prefisso sezione)
        for global_idx, (sk, i, r) in enumerate(risposte_utente, start=1):
            risultato[f"Domanda_{global_idx}" ] = r

        df = pd.DataFrame([risultato])
        os.makedirs("risultati_formazione", exist_ok=True)
        file_path = "risultati_formazione/risultati_test.xlsx"

        if os.path.exists(file_path):
            try:
                df_exist = pd.read_excel(file_path)
                df_final = pd.concat([df_exist, df], ignore_index=True)
            except Exception:
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

        corpo = """🧾 TEST COMPLETATO – Formazione Lavoratori (test unico)

"""
        corpo += (
            f"📛 NOMINATIVO: {st.session_state.nome}\n"
            f"🆔 Codice Fiscale: {st.session_state.cf}\n"
            f"🏢 Azienda: {st.session_state.azienda}\n"
            f"🕒 Data/Ora: {data_ora}\n"
            f"📈 Punteggio: {punteggio}/{n}\n"
            f"📌 Esito: {'✅ SUPERATO' if superato else '❌ NON SUPERATO'}\n\n"
            f"🧩 Sezioni: {', '.join([MODULI[k]['titolo'] for k in ordine_sezioni])}\n\n"
            f"📖 RISPOSTE DETTAGLIATE:\n"
        )

        # Aggiungi dettaglio domanda per domanda con intestazioni sezione
        current_section = None
        for global_idx, (sk, i, r) in enumerate(risposte_utente, start=1):
            if sk != current_section:
                current_section = sk
                corpo += f"\n--- {MODULI[sk]['titolo']} ---\n"
            domanda = MODULI[sk]["domande"][i]
            corretta = domanda["opzioni"][domanda["risposta_corretta"]]
            esito = "✅ CORRETTA" if r == corretta else f"❌ ERRATA (Corretto: {corretta})"
            corpo += f"Domanda {global_idx}: {domanda['testo']}\nRisposta: {r} → {esito}\n\n"

        if sender and password and st.session_state.email_dest:
            for destinatario in st.session_state.email_dest:
                msg = MIMEMultipart()
                msg["Subject"] = f"📩 Test Formazione – Test unico – {st.session_state.nome}"
                msg["From"] = sender
                msg["To"] = destinatario

                msg.attach(MIMEText(corpo, "plain"))

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

