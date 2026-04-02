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

MODULI_PREPOSTI = {
    "PREPOSTI_GIURIDICO": {
        "titolo": "Formazione preposti – Modulo giuridico normativo",
        "num_domande": 5,
        "domande": [
            {
                "testo": "Il preposto, ai fini della sicurezza, è la figura che:",
                "opzioni": [
                    "Sovrintende all’attività lavorativa e garantisce l’attuazione delle direttive ricevute",
                    "Redige obbligatoriamente il DVR",
                    "Sostituisce sempre il datore di lavoro"
                ],
                "risposta_corretta": 0,
            },
            {
                "testo": "Per accedere al corso per preposti è necessario aver già frequentato:",
                "opzioni": [
                    "Solo la formazione generale lavoratori",
                    "La formazione generale e specifica per lavoratori",
                    "Un corso antincendio"
                ],
                "risposta_corretta": 1,
            },
            {
                "testo": "La durata minima del corso per preposti, secondo l’Accordo Stato-Regioni 2025, è:",
                "opzioni": [
                    "6 ore",
                    "8 ore",
                    "12 ore"
                ],
                "risposta_corretta": 2,
            },
            {
                "testo": "Il cosiddetto 'preposto di fatto' è:",
                "opzioni": [
                    "Una figura non riconosciuta dalla normativa",
                    "Chi esercita concretamente i poteri tipici del preposto anche senza nomina formale",
                    "Un consulente esterno"
                ],
                "risposta_corretta": 1,
            },
            {
                "testo": "Il preposto si relaziona, nel sistema di prevenzione aziendale, principalmente con:",
                "opzioni": [
                    "Solo con i lavoratori",
                    "Lavoratori, dirigenti, datore di lavoro e servizio di prevenzione e protezione",
                    "Solo con il medico competente"
                ],
                "risposta_corretta": 1,
            },
        ],
    },

    "PREPOSTI_VIGILANZA": {
        "titolo": "Formazione preposti – Vigilanza, controllo e intervento",
        "num_domande": 5,
        "domande": [
            {
                "testo": "Una funzione tipica del preposto è:",
                "opzioni": [
                    "Sovrintendere e vigilare sull’osservanza delle disposizioni aziendali",
                    "Approvare il bilancio aziendale",
                    "Effettuare la sorveglianza sanitaria"
                ],
                "risposta_corretta": 0,
            },
            {
                "testo": "Se un lavoratore non utilizza i DPI obbligatori, il preposto deve:",
                "opzioni": [
                    "Ignorare il comportamento se il lavoro è urgente",
                    "Intervenire, richiamare il lavoratore e vigilare sul rispetto delle disposizioni",
                    "Segnalare solo a fine mese"
                ],
                "risposta_corretta": 1,
            },
            {
                "testo": "In presenza di una situazione di pericolo grave e immediato, il preposto deve:",
                "opzioni": [
                    "Consentire comunque la prosecuzione dell’attività",
                    "Adottare le misure previste, anche interrompendo l’attività se necessario",
                    "Attendere sempre l’autorizzazione scritta"
                ],
                "risposta_corretta": 1,
            },
            {
                "testo": "Tra i compiti del preposto rientra anche:",
                "opzioni": [
                    "La segnalazione tempestiva di carenze, anomalie e condizioni di pericolo",
                    "La nomina dell’RSPP",
                    "La firma del POS di cantiere come unica figura responsabile"
                ],
                "risposta_corretta": 0,
            },
            {
                "testo": "Il controllo del preposto sulle attività dei lavoratori serve principalmente a:",
                "opzioni": [
                    "Garantire il rispetto delle direttive ricevute e delle misure di sicurezza",
                    "Sostituire integralmente il dirigente",
                    "Valutare la produttività economica"
                ],
                "risposta_corretta": 0,
            },
        ],
    },

    "PREPOSTI_RISCHI_APPALTI": {
        "titolo": "Formazione preposti – Rischi, appalti e DUVRI",
        "num_domande": 5,
        "domande": [
            {
                "testo": "Il preposto deve conoscere i rischi presenti:",
                "opzioni": [
                    "Solo a livello teorico generale",
                    "Nel contesto specifico in cui opera e nelle attività che sovrintende",
                    "Solo se richiesto dal RLS"
                ],
                "risposta_corretta": 1,
            },
            {
                "testo": "Il DUVRI riguarda principalmente:",
                "opzioni": [
                    "La gestione del rischio interferenziale negli appalti o lavori affidati a terzi",
                    "La sorveglianza sanitaria periodica",
                    "La manutenzione degli estintori"
                ],
                "risposta_corretta": 0,
            },
            {
                "testo": "Quando sono presenti imprese esterne o lavoratori in appalto, il preposto deve prestare attenzione:",
                "opzioni": [
                    "Solo agli aspetti amministrativi",
                    "Ai rischi interferenziali e al rispetto delle modalità operative previste",
                    "Esclusivamente agli orari di ingresso"
                ],
                "risposta_corretta": 1,
            },
            {
                "testo": "Un 'near miss' o infortunio mancato è:",
                "opzioni": [
                    "Un evento che non ha causato danno ma avrebbe potuto causarlo",
                    "Un infortunio con prognosi superiore a 40 giorni",
                    "Un evento che non interessa la sicurezza"
                ],
                "risposta_corretta": 0,
            },
            {
                "testo": "Tra i lavoratori verso cui il preposto deve curare con particolare attenzione comunicazione e sensibilizzazione rientrano:",
                "opzioni": [
                    "Solo i lavoratori esperti",
                    "Neoassunti, somministrati e lavoratori stranieri",
                    "Solo gli addetti d’ufficio"
                ],
                "risposta_corretta": 1,
            },
        ],
    },
}
