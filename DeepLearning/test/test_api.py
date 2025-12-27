import requests
import json

#api addresse
API_URL = "http://127.0.0.1:8000/predict"

def test_scenario(nom_test, donnees_client):
    """Envoie une requête à l'API et affiche le résultat"""
    print(f"\n--- TEST : {nom_test} ---")
    try:
        response = requests.post(API_URL, json=donnees_client)
        
        # Si l'appel a réussi (Code 200)
        if response.status_code == 200:
            result = response.json()
            decision = result['decision']
            message = result['message']
            proba = result['probabilite_bon_payeur']
            
            
            print(f"Statut HTTP : {response.status_code} (OK)")
            print(f"Prédiction  : {decision} -> {message}")
            print(f"Confiance   : {proba*100:.2f}%")
            
            # verif  
            if "Risqué" in nom_test and decision == 0:
                print("Le modèle a refusé ce dossier risqué.")
            elif "Fiable" in nom_test and decision == 1:
                print("Le modèle a accepté ce dossier fiable.")
            else:
                print("ATTENTION : Résultat inattendu.")
                
        else:
            print(f" ERREUR API : {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("CRITIQUE : Impossible de connecter l'API. Vérifiez que 'uvicorn' est lancé.")

# --- DONNÉES DE TEST ---

# Cas 1 : Profil très risqué (Jeune, sans emploi stable, pas d'épargne)
client_risque = {
  "Seniority": 0,
  "Home": 0, 
  "Time": 50,
  "Age": 21,
  "Marital": 1,
  "Records": 5,  # A des incidents bancaires
  "Job": 1,
  "Expenses": 80,
  "Income": 50,
  "Assets": 0,
  "Debt": 2000,
  "Amount": 7000,
  "Price": 5000
}

# Cas 2 : Profil idéal (Ancienneté, revenus, patrimoine)
client_fiable = {
  "Seniority": 20,
  "Home": 1, 
  "Time": 12,
  "Age": 50,
  "Marital": 2,
  "Records": 0,  # Pas d'incidents
  "Job": 3,
  "Expenses": 35,
  "Income": 250,
  "Assets": 10000,
  "Debt": 0,
  "Amount": 500,
  "Price": 1000
}

if __name__ == "__main__":
    print(f"Test de l'API sur : {API_URL}")
    test_scenario("Client Risqué", client_risque)
    test_scenario("Client Fiable", client_fiable)