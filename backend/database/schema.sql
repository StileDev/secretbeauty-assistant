CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    contact_whatsapp TEXT UNIQUE NOT NULL,
    date_creation TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    date_debut TEXT DEFAULT (datetime('now')),
    statut TEXT DEFAULT 'ouverte',
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL,
    expediteur TEXT NOT NULL,
    contenu TEXT NOT NULL,
    date_envoi TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);

CREATE TABLE IF NOT EXISTS produits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    categorie TEXT NOT NULL,
    description TEXT,
    prix REAL,
    disponible INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS rendez_vous (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    service_demande TEXT NOT NULL,
    date_souhaitee TEXT,
    statut TEXT DEFAULT 'en_attente',
    point_rdv TEXT,
    date_creation TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (client_id) REFERENCES clients(id)
);