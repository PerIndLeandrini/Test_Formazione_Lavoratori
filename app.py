import streamlit as st
import pandas as pd
import os
from domande import MODULI
from datetime import datetime as dt
from math import ceil
from zoneinfo import ZoneInfo
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm


# ------------------------------------------------------------
# CONFIGURAZIONE BASE
# ------------------------------------------------------------
st.set_page_config(page_title="Test Formazione Lavoratori", layout="wide", page_icon="🧑‍🏫")
st.markdown("<h2 style='color:#00c3ff'>🧑‍🏫 Test – Formazione (D.Lgs. 81/08)</h2>", unsafe_allow_html=True)

# Stato iniziale
if "test_avviato" not in st.session_state:
    st.session_state.test_avviato = False

# ------------------------------------------------------------
# FORM DATI PARTECIPANTE (TEST UNICO – tutte le sezioni in sequenza)
# ------------------------------------------------------------
if not st.session_state.test_avviato:
    with st.form("dati_partecipante"):
        st.subheader("Dati del partecipante")
        nome = st.text_input("Nome e Cognome", max_chars=100)
        cf = st.text_input("Codice Fiscale (obbligatorio)", max_chars=16)
        azienda = st.text_input("Azienda")

        st.caption("Il report verrà archiviato internamente e inviato automaticamente all'organizzatore.")

        accetto = st.checkbox("✅ Dichiaro di accettare il trattamento dei dati ai fini formativi (privacy)")
        avvia = st.form_submit_button("Inizia il test")

        if avvia:
            if not (nome and cf and azienda and accetto):
                st.error("Compila tutti i campi richiesti e accetta la privacy.")
            else:
                st.session_state.test_avviato = True
                st.session_state.nome = nome
                st.session_state.cf = cf.upper()
                st.session_state.azienda = azienda
                # invio solo all'organizzatore
                st.session_state.email_dest = ["perindleandrini@4step.it"]

# ------------------------------------------------------------
# EROGAZIONE TEST (TUTTE LE SEZIONI IN SEQUENZA)
# ------------------------------------------------------------
if st.session_state.test_avviato:
    # Lista piatta di (section_key, index_in_section, domanda)
    sequenza = []
    ordine_sezioni = [
        "PREPOSTI_GIURIDICO",
        "PREPOSTI_VIGILANZA",
        "PREPOSTI_RISCHI_APPALTI",
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
    for global_idx, (sk, i, domanda) in enumerate(sequenza, start=1):
        if sk != current_section:
            current_section = sk
            st.markdown("")
            st.markdown(f"### 🧩 {MODULI[sk]['titolo']}")
        st.markdown(f"**Domanda {global_idx}:** {domanda['testo']}")
        risposta = st.radio("Scegli la risposta:", domanda["opzioni"], key=f"q_{sk}_{i}")
        risposte_utente.append((sk, i, risposta))

    if st.button("Conferma e correggi il test"):
        st.markdown("---")
        st.subheader("📊 Risultato del test")

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

        soglia = ceil(n * 0.8)  # 80% arrotondato per eccesso sull'intero test
        superato = punteggio >= soglia
        st.markdown(f"### Totale corrette: **{punteggio}/{n}** (Soglia: {soglia})")
        st.success("✅ Test superato!" if superato else "❌ Test NON superato")

        # Salvataggio risultato
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
        for global_idx, (sk, i, r) in enumerate(risposte_utente, start=1):
            risultato[f"Domanda_{global_idx}"] = r

        os.makedirs("risultati_formazione", exist_ok=True)
        file_path = "risultati_formazione/risultati_test.xlsx"
        df = pd.DataFrame([risultato])

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

        # --- PDF individuale scaricabile ---
        
        def build_pdf_buffer():
            buf = BytesIO()

            # A4 orizzontale + margini
            left = right = 12 * mm
            top = bottom = 12 * mm
            doc = SimpleDocTemplate(
                buf,
                pagesize=landscape(A4),
                leftMargin=left,
                rightMargin=right,
                topMargin=top,
                bottomMargin=bottom,
            )

            styles = getSampleStyleSheet()
            small = styles['BodyText']; small.fontSize = 8; small.leading = 10
            meta_style = styles['BodyText']; meta_style.fontSize = 9; meta_style.leading = 11

            story = []
            story.append(Paragraph("Test Formazione Lavoratori – Esito", styles['Title']))

            meta_html = (
                f"<b>Nome:</b> {st.session_state.nome}<br/>"
                f"<b>Codice Fiscale:</b> {st.session_state.cf}<br/>"
                f"<b>Azienda:</b> {st.session_state.azienda}<br/>"
                f"<b>Data/Ora:</b> {dt.now(ZoneInfo('Europe/Rome')).strftime('%Y-%m-%d %H:%M')}<br/>"
                f"<b>Punteggio:</b> {punteggio}/{n} – <b>Esito:</b> {'SUPERATO' if superato else 'NON SUPERATO'}"
            )
            story.append(Paragraph(meta_html, meta_style))
            story.append(Spacer(1, 6))

            # Larghezze colonne per landscape: somma ≈ 255 mm (resta dentro i margini)
            col_widths = [
                8 * mm,    # #
                42 * mm,   # Sezione
                105 * mm,  # Domanda
                40 * mm,   # Tua risposta
                40 * mm,   # Corretta
                20 * mm,   # Esito
            ]

            # Intestazione
            rows = [[
                Paragraph("#", small),
                Paragraph("Sezione", small),
                Paragraph("Domanda", small),
                Paragraph("Tua risposta", small),
                Paragraph("Corretta", small),
                Paragraph("Esito", small),
            ]]

            # Righe (Paragraph = wrapping automatico)
            for idx, (sk, i, r) in enumerate(risposte_utente, start=1):
                domanda = MODULI[sk]["domande"][i]
                corretta = domanda["opzioni"][domanda.get("risposta_corretta", 0)]
                esito = "OK" if r == corretta else "ERR"
                rows.append([
                    Paragraph(str(idx), small),
                    Paragraph(MODULI[sk]['titolo'], small),
                    Paragraph(domanda['testo'], small),
                    Paragraph(str(r), small),
                    Paragraph(str(corretta), small),
                    Paragraph(esito, small),
                ])

            table = Table(rows, colWidths=col_widths, repeatRows=1)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 9),
                ('ALIGN', (0,0), (0,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
                ('LEFTPADDING', (0,0), (-1,-1), 3),
                ('RIGHTPADDING', (0,0), (-1,-1), 3),
                ('TOPPADDING', (0,0), (-1,-1), 2),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ]))
            story.append(table)

            doc.build(story)
            buf.seek(0)
            return buf

        pdf_buffer = build_pdf_buffer()
        filename_pdf = f"Esito_Test_{st.session_state.cf}_{dt.now(ZoneInfo('Europe/Rome')).strftime('%Y%m%d_%H%M')}.pdf"
        st.download_button(
            label="📥 Scarica PDF con correzione",
            data=pdf_buffer,
            file_name=filename_pdf,
            mime="application/pdf",
        )

        # Email con riepilogo (allega l'Excel cumulativo) – invio SOLO all'organizzatore
        try:
            sender = st.secrets["email"]["sender"]
            password = st.secrets["email"]["password"]
        except Exception:
            sender = None
            password = None

        corpo = f"""🧾 TEST COMPLETATO – Formazione Lavoratori (test unico)

📛 NOMINATIVO: {st.session_state.nome}
🆔 Codice Fiscale: {st.session_state.cf}
🏢 Azienda: {st.session_state.azienda}
🕒 Data/Ora: {data_ora}
📈 Punteggio: {punteggio}/{n}
📌 Esito: {'✅ SUPERATO' if superato else '❌ NON SUPERATO'}

🧩 Sezioni: {', '.join([MODULI[k]['titolo'] for k in ordine_sezioni])}

📖 RISPOSTE DETTAGLIATE:
"""

        current_section = None
        for global_idx, (sk, i, r) in enumerate(risposte_utente, start=1):
            if sk != current_section:
                current_section = sk
                corpo += f"\n--- {MODULI[sk]['titolo']} ---\n"
            domanda = MODULI[sk]["domande"][i]
            corretta = domanda["opzioni"][domanda["risposta_corretta"]]
            esito = "✅ CORRETTA" if r == corretta else f"❌ ERRATA (Corretto: {corretta})"
            corpo += f"Domanda {global_idx}: {domanda['testo']}\nRisposta: {r} → {esito}\n\n"

        if sender and password:
            for destinatario in ["perindleandrini@4step.it"]:
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
            st.info("✉️ Email non inviata: configura le credenziali in .streamlit/secrets.toml.")


