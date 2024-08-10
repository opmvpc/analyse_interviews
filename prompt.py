system_prompt = """Le but est de réaliser une analyse qualitative par la méthode du codage déductif. Vous devez analyser l'extrait d'entretien suivant pour identifier si l'un des codes prédéfinis est présent.

1. **Réfléchissez dans les notes** : Analysez l'extrait en identifiant les éléments qui pourraient correspondre à chaque code. Soyez attentif aux indices subtils ou implicites qui pourraient indiquer la présence d'un code. Justifiez votre décision avec des éléments concrets. Si le code est absent, expliquez pourquoi.

2. **Prise de décision** : Décidez si le code est présent (`true`) ou absent (`false`). Si l'information est ambiguë mais qu'il y a des éléments suggérant la présence du code, considérez-le comme présent (`true`). Si l'extrait ne contient aucune indication, alors la réponse doit être `false`.

**Exigences de sortie** :
- Retournez un JSON valide avec les clés suivantes pour chaque code :
  - **notes** : Explication textuelle.
  - **present** : Booléen (`true` ou `false`).
  - Ne retournez que du JSON valide, sans texte supplémentaire ou erreurs de formatage.

**Les codes à évaluer (avec leurs descriptions)** :
- **tps_gagne** : L'extrait mentionne-t-il, même de manière implicite, une réduction du temps nécessaire pour préparer les cours grâce aux modèles de langage ?
- **prod_aug** : L'extrait indique-t-il, même indirectement, une augmentation de la productivité, comme la création de plus de matériel pédagogique ?
- **auto** : L'extrait reflète-t-il, explicitement ou implicitement, un sentiment d'autonomie et de contrôle sur le contenu généré par l'enseignant ?
- **prop_cont** : L'extrait mentionne-t-il, directement ou indirectement, un sentiment de propriété sur le contenu créé, malgré l'assistance des modèles de langage ?
- **biais_cult** : L'extrait mentionne-t-il des biais culturels ou des erreurs dans le contenu généré ?
- **corr_biais** : L'extrait parle-t-il de corrections de biais ou d'erreurs dans le contenu généré ?
- **eng_etu** : L'extrait indique-t-il un engagement accru des étudiants grâce aux nouveaux outils ?
- **prat_am** : L'extrait mentionne-t-il une amélioration des pratiques pédagogiques grâce aux modèles de langage ?
- **inno** : L'extrait évoque-t-il l'introduction de nouvelles idées ou méthodes pédagogiques grâce aux modèles de langage ?
- **nouv_meth** : L'extrait mentionne-t-il des nouvelles méthodes d'enseignement adoptées suite à l'utilisation des modèles de langage ?"""


# Exemples
# Exemple 1 - Réduction du temps
user_prompt_1 = 'Extrait : "Depuis que j\'utilise cet outil, je trouve que le temps que je passe à préparer mes cours a considérablement diminué. Avant, je passais des heures à chercher des ressources, mais maintenant, tout est à portée de main. J\'ai vraiment l\'impression de gagner du temps."'
assistant_response_1 = """
{
    "tps_gagne": {
        "notes": "Réduction explicite du temps pour préparer les cours.",
        "present": true
    },
    "prod_aug": {
        "notes": "Aucune mention d'augmentation de productivité.",
        "present": false
    },
    "auto": {
        "notes": "Pas de mention d'autonomie.",
        "present": false
    },
    "prop_cont": {
        "notes": "Pas de mention de propriété.",
        "present": false
    },
    "biais_cult": {
        "notes": "Pas de mention de biais culturels.",
        "present": false
    },
    "corr_biais": {
        "notes": "Pas de mention de correction de biais.",
        "present": false
    },
    "eng_etu": {
        "notes": "Pas de mention de l'engagement des étudiants.",
        "present": false
    },
    "prat_am": {
        "notes": "Pas de mention d'amélioration pédagogique.",
        "present": false
    },
    "inno": {
        "notes": "Pas de mention d'innovation.",
        "present": false
    },
    "nouv_meth": {
        "notes": "Pas de mention de nouvelles méthodes.",
        "present": false
    }
}
"""


# Exemple 2 - Productivité accrue
user_prompt_2 = 'Extrait : "Grâce à cet outil, j\'ai réussi à produire plus de matériel pédagogique que jamais auparavant. Non seulement j\'ai pu couvrir plus de sujets, mais j\'ai aussi eu le temps de peaufiner les détails, ce qui a vraiment amélioré la qualité de mon enseignement."'
assistant_response_2 = """
{
    "tps_gagne": {
        "notes": "Gain de temps implicite en mentionnant la possibilité de peaufiner les détails.",
        "present": true
    },
    "prod_aug": {
        "notes": "Augmentation claire de la productivité, mentionnée directement.",
        "present": true
    },
    "auto": {
        "notes": "Pas de sentiment d'autonomie mentionné.",
        "present": false
    },
    "prop_cont": {
        "notes": "Aucune mention de propriété du contenu.",
        "present": false
    },
    "biais_cult": {
        "notes": "Pas de biais culturels mentionnés.",
        "present": false
    },
    "corr_biais": {
        "notes": "Pas de correction de biais mentionnée.",
        "present": false
    },
    "eng_etu": {
        "notes": "Pas de mention de l'engagement des étudiants.",
        "present": false
    },
    "prat_am": {
        "notes": "Amélioration mentionnée mais pas spécifiquement pédagogique.",
        "present": false
    },
    "inno": {
        "notes": "Pas de mention d'innovation.",
        "present": false
    },
    "nouv_meth": {
        "notes": "Pas de nouvelles méthodes mentionnées.",
        "present": false
    }
}
"""


# Exemple 3 - Autonomie et propriété
user_prompt_3 = 'Extrait : "Avec cet outil, je me sens vraiment maître de ce que je produis. Même si je l\'utilise pour générer du contenu, je le personnalise tellement que je me considère comme le véritable auteur de tout ce que je présente à mes étudiants."'
assistant_response_3 = """
{
    "tps_gagne": {
        "notes": "Pas de gain de temps mentionné.",
        "present": false
    },
    "prod_aug": {
        "notes": "Pas de productivité accrue mentionnée.",
        "present": false
    },
    "auto": {
        "notes": "Autonomie clairement exprimée par l'utilisateur.",
        "present": true
    },
    "prop_cont": {
        "notes": "Sentiment explicite de propriété du contenu.",
        "present": true
    },
    "biais_cult": {
        "notes": "Pas de mention de biais culturels.",
        "present": false
    },
    "corr_biais": {
        "notes": "Pas de correction de biais mentionnée.",
        "present": false
    },
    "eng_etu": {
        "notes": "Pas de mention de l'engagement des étudiants.",
        "present": false
    },
    "prat_am": {
        "notes": "Pas de mention d'amélioration pédagogique.",
        "present": false
    },
    "inno": {
        "notes": "Pas d'innovation mentionnée.",
        "present": false
    },
    "nouv_meth": {
        "notes": "Pas de nouvelles méthodes mentionnées.",
        "present": false
    }
}
"""


# Exemple 4 - Erreur simulée et correction
user_prompt_4 = 'Extrait : "Cet outil m\'a permis d\'introduire une nouvelle méthode pédagogique dans mes cours, ce qui est vraiment innovant."'
assistant_response_4_initial = """
{
    "tps_gagne": {
        "notes": "Pas de gain de temps mentionné.",
        "present": false
    },
    "prod_aug": {
        "notes": "Pas de productivité accrue mentionnée.",
        "present": false
    },
    "auto": {
        "notes": "Pas d'autonomie mentionnée.",
        "present": false
    },
    "prop_cont": {
        "notes": "Pas de mention de propriété.",
        "present": false
    },
    "biais_cult": {
        "notes": "Pas de biais culturels mentionnés.",
        "present": false
    },
    "corr_biais": {
        "notes": "Pas de correction de biais mentionnée.",
        "present": false
    },
    "eng_etu": {
        "notes": "Pas de mention de l'engagement des étudiants.",
        "present": false
    },
    "prat_am": {
        "notes": "Pas d'amélioration pédagogique mentionnée.",
        "present": false
    },
    "inno": {
        "notes": "Innovation pédagogique mentionnée mais clé manquante.",
        # "present": true -> Clé manquante pour simuler une erreur
    },
    "nouv_meth": {
        "notes": "Nouvelle méthode d'enseignement introduite.",
        "present": true
    }
}
"""

# L'utilisateur reçoit une erreur de validation
validation_error = """Erreur rencontrée : 1 validation error for CodeResult innovation.est_present Field required [type=missing, input_value={'carnet_de_notes': 'L'utilisateur mentionne explicitement une innovation pédagogique introduite grâce à l'outil.'}, input_type=dict]"""

# Réponse corrigée par l'assistant
assistant_response_4_corrected = """
{
    "tps_gagne": {
        "notes": "Pas de gain de temps mentionné.",
        "present": false
    },
    "prod_aug": {
        "notes": "Pas de productivité accrue mentionnée.",
        "present": false
    },
    "auto": {
        "notes": "Pas d'autonomie mentionnée.",
        "present": false
    },
    "prop_cont": {
        "notes": "Pas de mention de propriété.",
        "present": false
    },
    "biais_cult": {
        "notes": "Pas de biais culturels mentionnés.",
        "present": false
    },
    "corr_biais": {
        "notes": "Pas de correction de biais mentionnée.",
        "present": false
    },
    "eng_etu": {
        "notes": "Pas de mention de l'engagement des étudiants.",
        "present": false
    },
    "prat_am": {
        "notes": "Pas d'amélioration pédagogique mentionnée.",
        "present": false
    },
    "inno": {
        "notes": "Innovation pédagogique mentionnée.",
        "present": true  # Clé ajoutée pour corriger l'erreur
    },
    "nouv_meth": {
        "notes": "Nouvelle méthode d'enseignement introduite.",
        "present": true
    }
}
"""

# Exemple 5 - Ambiguïté et biais culturels
user_prompt_5 = 'Extrait : "Je me demande parfois si cet outil comprend vraiment la diversité culturelle de ma classe. Il y a des moments où les réponses semblent un peu biaisées."'
assistant_response_5 = """
{
    "tps_gagne": {
        "notes": "Pas de gain de temps mentionné.",
        "present": false
    },
    "prod_aug": {
        "notes": "Pas de productivité accrue mentionnée.",
        "present": false
    },
    "auto": {
        "notes": "Pas d'autonomie mentionnée.",
        "present": false
    },
    "prop_cont": {
        "notes": "Pas de mention de propriété.",
        "present": false
    },
    "biais_cult": {
        "notes": "Préoccupation sur la diversité culturelle, possible biais.",
        "present": true
    },
    "corr_biais": {
        "notes": "Pas de correction de biais mentionnée.",
        "present": false
    },
    "eng_etu": {
        "notes": "Pas de mention de l'engagement des étudiants.",
        "present": false
    },
    "prat_am": {
        "notes": "Pas d'amélioration pédagogique mentionnée.",
        "present": false
    },
    "inno": {
        "notes": "Pas d'innovation mentionnée.",
        "present": false
    },
    "nouv_meth": {
        "notes": "Pas de nouvelles méthodes mentionnées.",
        "present": false
    }
}
"""

# Exemple 6 - Complètement hors sujet
user_prompt_6 = 'Extrait : "L’autre jour, j’ai rencontré un ancien collègue de travail. Nous avons discuté de nos souvenirs passés au sein de l’entreprise, des projets sur lesquels nous avons travaillé ensemble, et des défis que nous avons relevés. C’était agréable de se remémorer ces moments."'
assistant_response_6 = """
{
    "tps_gagne": {
        "notes": "Rien du tout.",
        "present": false
    },
    "prod_aug": {
        "notes": "Non.",
        "present": false
    },
    "auto": {
        "notes": "Pas du tout.",
        "present": false
    },
    "prop_cont": {
        "notes": "Non.",
        "present": false
    },
    "biais_cult": {
        "notes": "Non.",
        "present": false
    },
    "corr_biais": {
        "notes": "Rien.",
        "present": false
    },
    "eng_etu": {
        "notes": "Pas du tout.",
        "present": false
    },
    "prat_am": {
        "notes": "Non.",
        "present": false
    },
    "inno": {
        "notes": "Rien.",
        "present": false
    },
    "nouv_meth": {
        "notes": "Non.",
        "present": false
    }
}
"""
