from flask import Blueprint, request, jsonify
from services.db_service import get_connection
from services.ia_service import demander_a_ia

chat_bp = Blueprint("chat", __name__)


def get_or_create_client(contact_whatsapp):
    conn = get_connection()
    client = conn.execute(
        "SELECT * FROM clients WHERE contact_whatsapp = ?", (contact_whatsapp,)
    ).fetchone()

    if client is None:
        conn.execute(
            "INSERT INTO clients (contact_whatsapp) VALUES (?)", (contact_whatsapp,)
        )
        conn.commit()
        client = conn.execute(
            "SELECT * FROM clients WHERE contact_whatsapp = ?", (contact_whatsapp,)
        ).fetchone()

    conn.close()
    return client["id"]


def get_or_create_conversation(client_id):
    conn = get_connection()
    conv = conn.execute(
        "SELECT * FROM conversations WHERE client_id = ? AND statut = 'ouverte'",
        (client_id,)
    ).fetchone()

    if conv is None:
        conn.execute(
            "INSERT INTO conversations (client_id) VALUES (?)", (client_id,)
        )
        conn.commit()
        conv = conn.execute(
            "SELECT * FROM conversations WHERE client_id = ? AND statut = 'ouverte'",
            (client_id,)
        ).fetchone()

    conn.close()
    return conv["id"]


def get_historique(conversation_id, limite=10):
    conn = get_connection()
    rows = conn.execute(
        "SELECT expediteur, contenu FROM messages WHERE conversation_id = ? "
        "ORDER BY id DESC LIMIT ?",
        (conversation_id, limite)
    ).fetchall()
    conn.close()

    rows = list(reversed(rows))
    return [
        {"role": "user" if r["expediteur"] == "client" else "assistant", "content": r["contenu"]}
        for r in rows
    ]


def save_message(conversation_id, expediteur, contenu):
    conn = get_connection()
    conn.execute(
        "INSERT INTO messages (conversation_id, expediteur, contenu) VALUES (?, ?, ?)",
        (conversation_id, expediteur, contenu)
    )
    conn.commit()
    conn.close()


@chat_bp.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()
    contact_whatsapp = data.get("contact_whatsapp", "invite_anonyme")

    if not message:
        return jsonify({"erreur": "Message vide"}), 400

    client_id = get_or_create_client(contact_whatsapp)
    conversation_id = get_or_create_conversation(client_id)

    save_message(conversation_id, "client", message)

    historique = get_historique(conversation_id)
    reponse = demander_a_ia(historique)

    save_message(conversation_id, "assistant", reponse)

    return jsonify({"reponse": reponse})