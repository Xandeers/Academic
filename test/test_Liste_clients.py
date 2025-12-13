import requests
import yaml 

API_URL = "http://127.0.0.1:8000/predict"
YAML_FILE = "clients.yaml"

def run_clients_tests():
    """Charge le YAML et lance les tests pour chaque client"""
    
    # chargement des donner 
    try:
        with open(YAML_FILE, 'r') as file:
            clients = yaml.safe_load(file)
        print(f" Fichier '{YAML_FILE}' chargé : {len(clients)} clients trouvés.\n")
    except FileNotFoundError:
        print(f" Erreur : Le fichier '{YAML_FILE}' n'existe pas.")
        return

    # client
    for i, client in enumerate(clients):
        nom = client['nom']
        attendu = client['attendu']
        features = client['features']
        
        print(f"🔹 Test {i+1} : {nom}")
        
        try:
            # Appel API
            response = requests.post(API_URL, json=features)
            
            if response.status_code == 200:
                result = response.json()
                pred_decision = result['decision']
                proba = result['probabilite_bon_payeur']
                
                # Affichage des infos
                decision_txt = "Accordé" if pred_decision == 1 else "Refusé"
                confiance_txt = f"{proba*100:.1f}%"
                
                print(f"   -> Résultat API : {decision_txt} (Confiance: {confiance_txt})")
                
                # VERIFICATION AUTOMATIQUE
                if pred_decision == attendu:
                    print(f"  SUCCÈS : Le modèle prédit ce qui était attendu ({attendu}).")
                else:
                    print(f" ECHEC  : Attendu {attendu}, mais obtenu {pred_decision}.")
                    
            else:
                print(f"ERREUR API : Code {response.status_code}")
                print(f"   {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("CRITIQUE : L'API ne répond pas. Lancez 'uvicorn' !")
            break
        
        print("-" * 50) # juste pou le visuel 

if __name__ == "__main__":
    run_clients_tests()