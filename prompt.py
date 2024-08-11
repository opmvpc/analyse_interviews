system_prompt = """Le but est de réaliser une analyse qualitative par la méthode du codage déductif. Vous devez analyser l'extrait d'entretien suivant pour identifier si l'un des codes prédéfinis est présent.

1. **Réfléchissez dans les notes** : Analysez l'extrait en identifiant les éléments qui pourraient correspondre à chaque code. Soyez attentif aux indices subtils ou implicites qui pourraient indiquer la présence d'un code. Justifiez votre décision avec des éléments concrets. Si le code est absent, expliquez pourquoi. Une phrase négative ou neutre peut également contenir des informations pertinentes pour l'analyse.

2. **Prise de décision** : Décidez si le code est présent (`true`) ou absent (`false`). S'il y a des éléments suggérant la présence du code, considérez-le comme présent (`true`). Si l'extrait ne contient aucune indication, alors la réponse doit être `false`. Si l'information est ambiguë ou pas clairement exprimée et que vous ne pouvez pas conclure de manière définitive, considérez le code comme absent (`false`).

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
- **biais_err** : L'extrait mentionne-t-il des biais ou des erreurs dans le contenu généré par l'assistant, gpt ou avec l'application ?
- **corr_biais** : L'extrait parle-t-il de corrections ou de vérification du contenu généré ?
- **eng_etu** : L'extrait indique-t-il un engagement accru des étudiants grâce aux nouveaux outils ?
- **prat_am** : L'extrait mentionne-t-il une amélioration des pratiques pédagogiques grâce aux modèles de langage ?
- **inno_peda** : L'extrait évoque-t-il l'introduction de nouvelles idées ou méthodes pédagogiques grâce aux modèles de langage ?
- **meth_ens** : L'extrait mentionne-t-il des changements dans les méthodes d'enseignement adoptées suite à l'utilisation des modèles de langage ?"""


# Exemples
# Exemple 1 - Réduction du temps
user_prompt_1 = 'Extrait : "Depuis que j\'utilise cet outil, je trouve que le temps que je passe à préparer mes cours a considérablement diminué. Avant, je passais des heures à chercher des ressources, mais maintenant, tout est à portée de main. J\'ai vraiment l\'impression de gagner du temps."'
assistant_response_1 = """
{
    "tps_gagne": {
        "notes": "L'extrait indique clairement une réduction du temps de préparation des cours, avec l'expression explicite 'le temps que je passe à préparer mes cours a considérablement diminué'. De plus, la phrase 'tout est à portée de main' suggère une optimisation des ressources, ce qui contribue également à ce gain de temps.",
        "present": true
    },
    "prod_aug": {
        "notes": "Bien que l'extrait mentionne une efficacité accrue, il n'y a aucune indication que cette réduction de temps a conduit à une augmentation de la production de matériel pédagogique. Aucun mot ou phrase ne suggère une augmentation de la quantité de contenu créé.",
        "present": false
    },
    "auto": {
        "notes": "L'extrait ne contient aucune indication que l'enseignant se sent plus autonome ou en contrôle du contenu généré. L'accent est mis uniquement sur le gain de temps, sans mention de la gestion ou de la personnalisation du contenu.",
        "present": false
    },
    "prop_cont": {
        "notes": "Il n'est pas fait mention d'un sentiment de propriété sur le contenu créé. L'extrait se concentre sur l'efficacité de la préparation des cours, mais pas sur la création ou la personnalisation du contenu.",
        "present": false
    },
    "biais_err": {
        "notes": "Aucun biais ou erreur dans le contenu généré n'est mentionné. L'accent est exclusivement mis sur la réduction du temps de préparation.",
        "present": false
    },
    "corr_biais": {
        "notes": "Aucune correction ou vérification des contenus n'est évoquée dans cet extrait. La discussion est centrée sur l'efficacité temporelle.",
        "present": false
    },
    "eng_etu": {
        "notes": "L'extrait ne fait aucune mention de l'impact sur l'engagement des étudiants. Il se concentre uniquement sur l'expérience de l'enseignant.",
        "present": false
    },
    "prat_am": {
        "notes": "Il n'y a aucune mention d'amélioration des pratiques pédagogiques. L'extrait ne traite que de l'aspect logistique de la préparation des cours.",
        "present": false
    },
    "inno_peda": {
        "notes": "L'extrait n'évoque aucune introduction de nouvelles idées ou méthodes pédagogiques. Le propos reste centré sur le temps de préparation.",
        "present": false
    },
    "meth_ens": {
        "notes": "Aucune mention de changement dans les méthodes d'enseignement adoptées. L'extrait parle seulement de l'efficacité temporelle.",
        "present": false
    }
}
"""



# Exemple 2 - Productivité accrue
user_prompt_2 = 'Extrait : "Grâce à cet outil, j\'ai réussi à produire plus de matériel pédagogique que jamais auparavant. Non seulement j\'ai pu couvrir plus de sujets, mais j\'ai aussi eu le temps de peaufiner les détails, ce qui a vraiment amélioré la qualité de mon enseignement."'
assistant_response_2 = """
{
    "tps_gagne": {
        "notes": "L'extrait laisse entendre un gain de temps, car l'enseignant indique avoir eu plus de temps pour peaufiner les détails, ce qui sous-entend une optimisation du temps.",
        "present": true
    },
    "prod_aug": {
        "notes": "L'extrait mentionne explicitement une augmentation de la productivité ('produire plus de matériel pédagogique que jamais auparavant'). Cette augmentation est claire et directe, avec des preuves telles que la couverture de plus de sujets et l'amélioration des détails.",
        "present": true
    },
    "auto": {
        "notes": "Bien que l'enseignant mentionne une amélioration de la qualité de l'enseignement, il n'y a aucune indication qu'il se sent plus autonome ou en contrôle du contenu. Le focus est sur la productivité et la qualité, pas sur l'autonomie.",
        "present": false
    },
    "prop_cont": {
        "notes": "L'extrait ne mentionne pas de sentiment de propriété sur le contenu. L'enseignant parle d'une amélioration de la qualité, mais pas de l'appropriation ou de la création personnelle.",
        "present": false
    },
    "biais_err": {
        "notes": "Il n'y a pas de mention de biais ou d'erreurs dans le contenu généré. L'extrait se concentre uniquement sur l'efficacité et la productivité.",
        "present": false
    },
    "corr_biais": {
        "notes": "L'extrait ne parle pas de correction ou de vérification du contenu généré. Le propos est centré sur la quantité et la qualité de la production.",
        "present": false
    },
    "eng_etu": {
        "notes": "Aucune mention de l'engagement des étudiants n'est faite. L'enseignant parle de sa propre productivité et de l'amélioration de son enseignement, mais pas de l'impact sur les étudiants.",
        "present": false
    },
    "prat_am": {
        "notes": "L'enseignant mentionne une amélioration de la qualité de son enseignement ('ce qui a vraiment amélioré la qualité de mon enseignement'). Cela pourrait être interprété comme une amélioration des pratiques pédagogiques, mais l'extrait ne fait pas ce lien explicitement.",
        "present": false
    },
    "inno_peda": {
        "notes": "Aucune innovation pédagogique n'est mentionnée. L'accent est mis sur l'efficacité et la qualité de l'enseignement existant, mais pas sur l'introduction de nouvelles méthodes.",
        "present": false
    },
    "meth_ens": {
        "notes": "L'enseignant mentionne avoir couvert plus de sujets et amélioré les détails, ce qui pourrait indiquer un changement dans les méthodes d'enseignement. Cependant, l'extrait ne fournit pas suffisamment d'informations pour confirmer un changement significatif dans les méthodes pédagogiques.",
        "present": true
    }
}
"""

# Exemple 3 - Autonomie et propriété
user_prompt_3 = 'Extrait : "Avec cet outil, je me sens vraiment maître de ce que je produis. Même si je l\'utilise pour générer du contenu, je le personnalise tellement que je me considère comme le véritable auteur de tout ce que je présente à mes étudiants."'

assistant_response_3 = """
{
    "tps_gagne": {
        "notes": "L'extrait ne fait aucune mention de gain de temps ou de réduction du temps de préparation. Le focus est sur l'autonomie et la propriété du contenu.",
        "present": false
    },
    "prod_aug": {
        "notes": "Aucune indication d'une augmentation de la productivité n'est présente. L'enseignant se concentre sur la personnalisation du contenu plutôt que sur la quantité de production.",
        "present": false
    },
    "auto": {
        "notes": "L'extrait reflète clairement un sentiment d'autonomie. L'enseignant se sent 'maître de ce que je produis' et considère que la personnalisation le rend autonome dans son travail.",
        "present": true
    },
    "prop_cont": {
        "notes": "L'extrait exprime explicitement un sentiment de propriété du contenu. L'enseignant se considère comme le 'véritable auteur' du matériel qu'il présente, malgré l'utilisation de l'outil pour générer ce contenu.",
        "present": true
    },
    "biais_err": {
        "notes": "Aucune mention de biais ou d'erreurs dans le contenu généré n'est faite. L'accent est mis sur la personnalisation et la propriété.",
        "present": false
    },
    "corr_biais": {
        "notes": "L'enseignant ne mentionne aucune correction ou vérification du contenu généré. La discussion reste centrée sur l'autonomie et la personnalisation.",
        "present": false
    },
    "eng_etu": {
        "notes": "L'extrait ne mentionne pas l'engagement des étudiants. Le propos est exclusivement axé sur le rôle de l'enseignant et son sentiment de maîtrise.",
        "present": false
    },
    "prat_am": {
        "notes": "Aucune mention d'amélioration des pratiques pédagogiques n'est faite. L'extrait se concentre sur l'expérience subjective de l'enseignant.",
        "present": false
    },
    "inno_peda": {
        "notes": "L'enseignant ne mentionne pas l'introduction de nouvelles idées ou méthodes pédagogiques. Le propos est centré sur l'appropriation et l'autonomie.",
        "present": false
    },
    "meth_ens": {
        "notes": "Aucun changement dans les méthodes d'enseignement n'est mentionné. L'enseignant parle principalement de son sentiment de contrôle sur le contenu.",
        "present": false
    }
}
"""




# Exemple 4 - Erreur simulée et correction
user_prompt_4 = 'Extrait : "Cet outil m\'a permis d\'introduire une nouvelle méthode pédagogique dans mes cours, ce qui est vraiment innovant."'
assistant_response_4_initial = """
{
    "tps_gagne": {
        "notes": "L'extrait ne mentionne pas de gain de temps ou de réduction du temps de préparation. L'innovation pédagogique est le seul point soulevé.",
        "present": false
    },
    "prod_aug": {
        "notes": "Aucune augmentation de la productivité n'est mentionnée. L'extrait se concentre uniquement sur l'introduction d'une nouvelle méthode pédagogique.",
        "present": false
    },
    "auto": {
        "notes": "Il n'est pas question d'autonomie ou de sentiment de contrôle dans l'extrait. L'accent est mis sur l'innovation.",
        "present": false
    },
    "prop_cont": {
        "notes": "L'extrait ne fait aucune mention de propriété sur le contenu. L'accent est mis sur l'innovation pédagogique.",
        "present": false
    },
    "biais_err": {
        "notes": "L'extrait ne fait aucune mention de biais ou d'erreurs dans le contenu généré.",
        "present": false
    },
    "corr_biais": {
        "notes": "Aucune correction ou vérification du contenu n'est évoquée dans cet extrait.",
        "present": false
    },
    "eng_etu": {
        "notes": "L'extrait ne mentionne pas l'engagement des étudiants. Il se concentre sur l'innovation pédagogique.",
        "present": false
    },
    "prat_am": {
        "notes": "Bien que l'extrait mentionne une nouvelle méthode pédagogique, il n'évoque pas spécifiquement une amélioration des pratiques pédagogiques globales.",
        "present": false
    },
    "inno_peda": {
        "notes": "L'extrait mentionne explicitement l'introduction d'une 'nouvelle méthode pédagogique' et qualifie cela d'innovant, ce qui correspond directement à ce code.",
    },
    "meth_ens": {
        "notes": "L'extrait parle d'une 'nouvelle méthode pédagogique', ce qui peut être interprété comme un changement dans les méthodes d'enseignement, mais il n'est pas certain que cela représente un changement significatif dans l'approche globale de l'enseignement.",
        "present": false
    }
}
"""


# L'utilisateur reçoit une erreur de validation
validation_error = """Erreur rencontrée : 1 validation error for CodeResult innovation.est_present Field required [type=missing, input_value={'carnet_de_notes': 'L'utilisateur mentionne explicitement une innovation pédagogique introduite grâce à l'outil.'}, input_type=dict]"""

# Réponse corrigée par l'assistant
assistant_response_4_corrected = """
{
    "tps_gagne": {
        "notes": "L'extrait ne mentionne pas de gain de temps ou de réduction du temps de préparation. L'innovation pédagogique est le seul point soulevé.",
        "present": false
    },
    "prod_aug": {
        "notes": "Aucune augmentation de la productivité n'est mentionnée. L'extrait se concentre uniquement sur l'introduction d'une nouvelle méthode pédagogique.",
        "present": false
    },
    "auto": {
        "notes": "Il n'est pas question d'autonomie ou de sentiment de contrôle dans l'extrait. L'accent est mis sur l'innovation.",
        "present": false
    },
    "prop_cont": {
        "notes": "L'extrait ne fait aucune mention de propriété sur le contenu. L'accent est mis sur l'innovation pédagogique.",
        "present": false
    },
    "biais_err": {
        "notes": "L'extrait ne fait aucune mention de biais ou d'erreurs dans le contenu généré.",
        "present": false
    },
    "corr_biais": {
        "notes": "Aucune correction ou vérification du contenu n'est évoquée dans cet extrait.",
        "present": false
    },
    "eng_etu": {
        "notes": "L'extrait ne mentionne pas l'engagement des étudiants. Il se concentre sur l'innovation pédagogique.",
        "present": false
    },
    "prat_am": {
        "notes": "Bien que l'extrait mentionne une nouvelle méthode pédagogique, il n'évoque pas spécifiquement une amélioration des pratiques pédagogiques globales.",
        "present": false
    },
    "inno_peda": {
        "notes": "L'extrait mentionne explicitement l'introduction d'une 'nouvelle méthode pédagogique' et qualifie cela d'innovant, ce qui correspond directement à ce code.",
        "present": true
    },
    "meth_ens": {
        "notes": "L'extrait parle d'une 'nouvelle méthode pédagogique', ce qui peut être interprété comme un changement dans les méthodes d'enseignement, mais il n'est pas certain que cela représente un changement significatif dans l'approche globale de l'enseignement.",
        "present": false
    }
}
"""



# Exemple 5 - Ambiguïté et biais
user_prompt_5 = 'Extrait : "Oui ! Je dois toujours vérifier les textes générés avec l\'assistant. Il lui arrive d`écrire des choses incorrectes."'
assistant_response_5 = """
{
    "tps_gagne": {
        "notes": "L'extrait ne fait aucune mention de gain de temps ou de réduction du temps de préparation. Le propos est centré sur la vérification des textes.",
        "present": false
    },
    "prod_aug": {
        "notes": "Aucune indication d'une augmentation de la productivité n'est présente. L'enseignant se concentre sur la nécessité de vérification, non sur la production.",
        "present": false
    },
    "auto": {
        "notes": "L'extrait ne reflète pas un sentiment d'autonomie. L'enseignant semble dépendre de l'outil, mais exprime la nécessité de vérifier son travail.",
        "present": false
    },
    "prop_cont": {
        "notes": "L'extrait ne mentionne pas un sentiment de propriété sur le contenu généré. L'accent est mis sur les erreurs et la vérification.",
        "present": false
    },
    "biais_err": {
        "notes": "L'extrait mentionne explicitement des erreurs ('Il lui arrive d'écrire des choses incorrectes'), ce qui correspond à ce code.",
        "present": true
    },
    "corr_biais": {
        "notes": "L'enseignant mentionne la vérification des textes générés, ce qui peut impliquer une correction, mais l'extrait ne précise pas si des corrections sont effectivement apportées ou simplement envisagées.",
        "present": false
    },
    "eng_etu": {
        "notes": "L'extrait ne mentionne pas l'engagement des étudiants. La discussion porte sur la vérification du contenu.",
        "present": false
    },
    "prat_am": {
        "notes": "Il n'y a aucune mention d'amélioration des pratiques pédagogiques. L'extrait se concentre sur les erreurs et leur vérification.",
        "present": false
    },
    "inno_peda": {
        "notes": "Aucune innovation pédagogique n'est mentionnée. L'extrait parle de la vérification des erreurs.",
        "present": false
    },
    "meth_ens": {
        "notes": "L'extrait ne mentionne aucun changement dans les méthodes d'enseignement. L'enseignant se concentre sur la gestion des erreurs.",
        "present": false
    }
}
"""


# Exemple 6 - Complètement hors sujet
user_prompt_6 = 'Extrait : "L’autre jour, j’ai rencontré un ancien collègue de travail. Nous avons discuté de nos souvenirs passés au sein de l’entreprise, des projets sur lesquels nous avons travaillé ensemble, et des défis que nous avons relevés. C’était agréable de se remémorer ces moments."'
assistant_response_6 = """
{
    "tps_gagne": {
        "notes": "L'extrait est totalement hors sujet par rapport au gain de temps dans la préparation des cours. Aucun élément pertinent ne peut être relevé.",
        "present": false
    },
    "prod_aug": {
        "notes": "Il n'y a aucune mention de productivité ou de création de matériel pédagogique. Le propos est personnel et social, sans lien avec l'enseignement.",
        "present": false
    },
    "auto": {
        "notes": "L'extrait ne traite pas du tout de l'autonomie ou du contrôle sur le contenu pédagogique. Il est centré sur des souvenirs personnels.",
        "present": false
    },
    "prop_cont": {
        "notes": "Il n'est pas question de propriété du contenu ou d'appropriation dans cet extrait, qui se concentre sur une discussion informelle entre collègues.",
        "present": false
    },
    "biais_err": {
        "notes": "L'extrait n'aborde pas les questions de biais ou d'erreurs dans le contenu pédagogique. Le contexte est complètement différent.",
        "present": false
    },
    "corr_biais": {
        "notes": "Aucune correction ou vérification n'est mentionnée, car l'extrait ne traite pas de contenu généré ou de pédagogie.",
        "present": false
    },
    "eng_etu": {
        "notes": "L'extrait ne mentionne rien qui soit en lien avec l'engagement des étudiants. Il s'agit d'une conversation personnelle sans rapport avec l'enseignement.",
        "present": false
    },
    "prat_am": {
        "notes": "Aucune amélioration des pratiques pédagogiques n'est évoquée. Le propos est totalement hors sujet.",
        "present": false
    },
    "inno_peda": {
        "notes": "Il n'est pas question d'innovation pédagogique ou de nouvelles méthodes dans cet extrait. Le sujet est une simple discussion entre collègues.",
        "present": false
    },
    "meth_ens": {
        "notes": "Aucun changement dans les méthodes d'enseignement n'est abordé dans cet extrait, qui est complètement hors contexte par rapport à l'analyse demandée.",
        "present": false
    }
}
"""
