#ce fichier est à considerer comme le ficheir utils.py 
#sauf qu'il contient les methode à partir de la q10 de la premiere partie 

import time
import numpy as np
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import make_scorer, accuracy_score, precision_score


# --- Fonction: Comparaison Cross-Validation (run_classifiers_cv) ---
def run_classifiers_cv(X, Y, clfs, cv_folds=10):
    """
    Compare une liste de classifieurs via Cross-Validation (10 folds).
    Affiche : Accuracy, AUC, (Acc+Prec)/2 et Temps d'exécution.
    """
    # Définition du K-Fold
    kf = KFold(n_splits=cv_folds, shuffle=True, random_state=0)
    
    # 2. Définition de la métrique personnalisée (Acc + Prec) / 2
    def custom_metric(y_true, y_pred):
        acc = accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred, zero_division=0)
        return (acc + prec) / 2
    
    custom_scorer = make_scorer(custom_metric)

    # En-tête du tableau de résultats
    print(f"{'Algorithme':<25} | {'Accuracy (Moy +/- Ecart type)':<28} | {'AUC':<8} | {'(Acc+Prec)/2':<15} | {'Temps (s)':<10}")
    print("-" * 100)

    stats = {} # Pour stocker les résultats si besoin

    # Boucle sur chaque algorithme
    for name, clf in clfs.items():
        start_time = time.time()
        
        # Cross-Validation pour l'Accuracy
        cv_acc = cross_val_score(clf, X, Y, cv=kf, scoring='accuracy')
        
        # Cross-Validation pour l'AUC
        # Note : certains modèles ne supportent pas predict_proba nativement sans config, 
        # on gère l'exception au cas où, ou on utilise 'roc_auc' standard
        try:
            cv_auc = cross_val_score(clf, X, Y, cv=kf, scoring='roc_auc')
            auc_mean = np.mean(cv_auc)
        except:
            auc_mean = 0.0 # Cas où le modèle ne gère pas les probas
            
        # Cross-Validation pour (Acc+Prec)/2
        cv_custom = cross_val_score(clf, X, Y, cv=kf, scoring=custom_scorer)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Aff
        acc_str = f"{np.mean(cv_acc):.3f} +/- {np.std(cv_acc):.3f}"
        print(f"{name:<25} | {acc_str:<28} | {auc_mean:.3f}    | {np.mean(cv_custom):.3f}           | {execution_time:.3f}")
        
        # Stock
        stats[name] = np.mean(cv_custom) # On stocke le score "métier" pour trouver le vainqueur

    return stats