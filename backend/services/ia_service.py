import requests
from config import OPENROUTER_API_KEY
from services.db_service import get_connection


def get_catalogue_produits():
    """Récupère le catalogue actuel directement depuis la base."""
    conn = get_connection()
    produits = conn.execute(
        "SELECT nom, categorie, description, prix FROM produits WHERE disponible = 1"
    ).fetchall()
    conn.close()

    lignes = [
        f"- {p['nom']} ({p['categorie']}) : {p['description']} — {p['prix']} FCFA"
        for p in produits
    ]
    return "\n".join(lignes)


def build_system_prompt():
    catalogue = get_catalogue_produits()

    return f"""Tu es l'assistante virtuelle de Secret Beauty, une entreprise camerounaise
de cosmétique et de soins de beauté (basée à Yaoundé, vente principalement en ligne).

INFORMATIONS SUR L'ENTREPRISE (tu peux tout partager librement) :
- Services proposés : manucure, pédicure, soins du visage, vente de produits cosmétiques
  (parfums, savons de beauté, laits de toilette, produits pour le teint, produits pour ongles).
- Clientèle : ouverte à tous, à partir de 13 ans environ.
- Horaires : du lundi au samedi de 8h-18h.
- Fonctionnement : tout se fait sur rendez-vous, pris via WhatsApp.
- Remise des produits/soins : à un point de rendez-vous fixe communiqué au client.
- Pas de local physique fixe — activité principalement en ligne / directe.

CATALOGUE ACTUEL DES PRODUITS :
{catalogue}

RÈGLES DE COMPORTEMENT :
1. Réponds à TOUTES les questions des clients sur l'entreprise, les services, les produits,
   les horaires, la façon de commander — de façon chaleureuse, claire et précise.
2. Tu peux discuter de sujets généraux liés à la beauté (conseils simples) si le client le demande.
3. NE RÉVÈLE JAMAIS d'informations confidentielles, notamment :
   - les fournisseurs ou sources d'approvisionnement,
   - les coûts internes, marges ou chiffre d'affaires,
   - les informations personnelles de la gérante (Ebah Malaurie) au-delà de son rôle,
   - toute donnée qui ne t'a pas été explicitement fournie ici.
4. Si on te pose une question confidentielle, réponds poliment que cette information
   n'est pas communicable, sans donner de détails sur pourquoi.
5. Ne jamais inventer un prix, une info ou un produit qui n'est pas dans le catalogue ci-dessus.
6. Reste toujours dans le ton d'une conseillère beauté professionnelle et bienveillante.
"""


def demander_a_ia(historique_messages):
    """
    historique_messages : liste de dicts [{"role": "user"/"assistant", "content": "..."}]
    """
    messages = [{"role": "system", "content": build_system_prompt()}] + historique_messages

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
            "messages": messages
        }
    )

    data = response.json()

    if "choices" not in data:
        return "Désolée, je rencontre un souci technique. Réessaie dans un instant."

    return data["choices"][0]["message"]["content"]