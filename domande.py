# domande.py

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
                "opzioni": ["Monitor troppo alto rispetto agli occhi", "Pianificare pause e regolare la postazione", "Illuminazione abbagliante"],
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
                "opzioni": ["Attendere che passi", "Risciacquare abbondantemente e consultare la SDS/medico", "Coprire con guanti"],
                "risposta_corretta": 1,
            },
        ],
    },
}
