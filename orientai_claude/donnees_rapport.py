"""
OrientAI — Données partagées pour les rapports
Ce fichier est importé par rapport_v2.py, rapport_pdf.py et app.py
"""

MAPPING_QUESTIONS = [
    ("Communication écrite", "Communication", {
        "A": "Vous êtes particulièrement doué à l'écrit.",
        "B": "Vous savez vous exprimer à l'écrit. Les gens comprennent facilement vos propos.",
        "C": "Vous faites beaucoup de fautes de français à l'écrit.",
        "D": "Vous avez des difficultés à structurer vos phrases à l'écrit.",
    }),
    ("L'audace (ou le culot)", "Communication", {
        "A": "Vous avez de l'audace et êtes relativement spontané.",
        "B": "Vous avez de l'audace et êtes relativement spontané.",
        "C": "Vous êtes quelqu'un de timide et réservé.",
        "D": "Vous avez peu d'audace quand il s'agit de s'adresser aux personnes impressionnantes.",
    }),
    ("La clarté de communication", "Communication", {
        "A": "Vous savez vous exprimer extrêmement bien.",
        "B": "Vous êtes clair à l'oral, vos interlocuteurs comprennent facilement vos propos.",
        "C": "Vous avez du mal à vous exprimer correctement.",
        "D": "Vous avez du mal à structurer des phrases claires et précises.",
    }),
    ("La négociation", "Communication", {
        "A": "Vous aimez négocier et trouver des accords profitables pour tous.",
        "B": "Vous aimez entamer des négociations quand ça peut vous avantager.",
        "C": "Vous préférez éviter les négociations corsées, quitte à perdre des opportunités.",
        "D": "Vous considérez les phases de négociation comme des échanges agressifs et inutiles.",
    }),
    ("Prise de parole en public", "Communication", {
        "A": "Vous aimez la prise de parole en public. C'est votre truc.",
        "B": "Vous êtes à l'aise quand vous devez vous exprimer en public.",
        "C": "Vous n'aimez pas trop ça, mais vous faites l'effort quand il le faut.",
        "D": "Vous avez tendance à éviter les prises de paroles en public.",
    }),
    ("Rhétorique ou storytelling", "Communication", {
        "A": "Vous savez raconter les histoires et les anecdotes de façon captivante.",
        "B": "Vous aimez motiver les autres à s'amuser.",
        "C": "Vous avez du mal à captiver vos interlocuteurs quand vous racontez quelque chose.",
        "D": "Votre manière de vous exprimer n'est pas toujours engageante.",
    }),
    ("Actualisation des connaissances", "Esprit critique", {
        "A": "Vous lisez les articles et ouvrages les plus récents sur les sujets qui vous intéressent.",
        "B": "Vous vous informez régulièrement pour rester à jour sur les sujets importants.",
        "C": "Vous n'actualisez pas systématiquement vos connaissances.",
        "D": "Vous ne voyez pas l'intérêt d'investir du temps sur un sujet si ça ne vous apporte rien maintenant.",
    }),
    ("L'acuité et le discernement", "Esprit critique", {
        "A": "Vous avez une faculté de discernement élevé. Vous vérifiez l'information avant de la croire.",
        "B": "Vous vérifiez les informations importantes avant de les accepter.",
        "C": "Vous avez tendance à partager les informations sans toujours les vérifier.",
        "D": "Vous avez tendance à réagir rapidement sans toujours vérifier les faits.",
    }),
    ("L'ouverture d'esprit", "Esprit critique", {
        "A": "Vous pouvez vous montrer très fermé aux nouvelles idées.",
        "B": "Vous n'aimez pas remettre en question vos méthodes habituelles.",
        "C": "Vous vous renseignez sur les nouvelles méthodes avant d'en adopter une.",
        "D": "Vous êtes curieux et ouvert aux nouvelles idées, même quand elles challengent vos habitudes.",
    }),
    ("La créativité ou l'imagination", "Esprit critique", {
        "A": "Vous n'arrivez pas à imaginer quoi que ce soit dans des exercices créatifs.",
        "B": "Vous avez besoin d'aide d'une personne plus imaginative pour les exercices créatifs.",
        "C": "Vous avez de l'imagination et arrivez à créer rapidement une trame.",
        "D": "Vous êtes très créatif. Vous imaginez facilement des univers détaillés.",
    }),
    ("La curiosité", "Esprit critique", {
        "A": "Vous êtes quelqu'un de curieux. Vous aimez vous renseigner de façon proactive.",
        "B": "Vous essayez de vous tenir informé sur les sujets qui vous touchent.",
        "C": "Vous préférez que l'information vienne à vous plutôt que de la chercher.",
        "D": "Vous n'êtes pas quelqu'un de curieux.",
    }),
    ("Savoir rechercher pour résoudre un problème", "Esprit critique", {
        "A": "Vous contactez les bonnes sources pour obtenir des informations fiables.",
        "B": "Vous cherchez des tutoriels et des ressources pour résoudre vos problèmes.",
        "C": "Vous préférez demander à quelqu'un de compétent plutôt que de chercher vous-même.",
        "D": "Vous avez tendance à improviser plutôt que de chercher des informations.",
    }),
    ("L'intégrité", "Éthique", {
        "A": "En général, vous préférez perdre dans l'honneur que gagner dans le déshonneur.",
        "B": "Vous essayez généralement de faire ce qui est juste.",
        "C": "Vous gardez les avantages inattendus sans trop vous poser de questions.",
        "D": "Vous profitez des erreurs des autres si ça peut vous avantager.",
    }),
    ("La conscience professionnelle", "Éthique", {
        "A": "Vous avez une conscience professionnelle accrue. Vous terminez toujours ce que vous commencez.",
        "B": "Vous essayez de respecter vos engagements professionnels.",
        "C": "Vous êtes parfois tenté de lâcher votre travail pour des activités plus agréables.",
        "D": "Vous demandez aux autres de finir le travail quand vous n'en avez plus envie.",
    }),
    ("La loyauté", "Éthique", {
        "A": "Vous restez et cherchez à remotiver votre équipe même quand les choses vont mal.",
        "B": "Vous restez fidèle et compensez les manques de votre équipe en travaillant plus.",
        "C": "Vous quittez les groupes non performants pour rejoindre de meilleures équipes.",
        "D": "Vous préférez travailler seul pour être sûr que le travail soit bien fait.",
    }),
    ("Le sens des responsabilités", "Éthique", {
        "A": "Vous fuyez vos responsabilités quand les choses tournent mal.",
        "B": "Vous évitez la confrontation directe et cherchez à minimiser votre rôle.",
        "C": "Vous attendez pour assumer vos responsabilités et affronter les conséquences.",
        "D": "Vous assumez pleinement vos responsabilités.",
    }),
    ("L'éco-responsabilité", "Éthique", {
        "A": "Vous êtes particulièrement éco-responsable dans vos choix.",
        "B": "Vous faites des efforts pour réduire votre impact environnemental.",
        "C": "Vous essayez de faire des choix raisonnables sans vous imposer de contraintes excessives.",
        "D": "Vous n'êtes pas particulièrement éco-responsable dans vos choix.",
    }),
    ("L'engagement", "Éthique", {
        "A": "Vous pouvez prendre en considération des opinions différentes des vôtres.",
        "B": "Vous pouvez écouter sans être entièrement d'accord.",
        "C": "Vous préférez éviter les opinions qui contredisent vos valeurs.",
        "D": "Il vous est impossible de prendre en considération une opinion qui bafoue vos principes.",
    }),
    ("Acceptation des retours et critiques", "Intelligence émotionnelle", {
        "A": "Vous acceptez les critiques et les utilisez pour vous améliorer.",
        "B": "Les critiques vous irritent, mais vous préférez les écouter pour progresser.",
        "C": "Vous ignorez les critiques quand elles vous semblent mal intentionnées.",
        "D": "Les critiques vous affectent profondément et vous mettent en colère.",
    }),
    ("Introspection", "Intelligence émotionnelle", {
        "A": "Vous arrivez à identifier et expliquer facilement vos émotions et défauts.",
        "B": "Vous arrivez à comprendre vos émotions, mais pas toujours facilement.",
        "C": "Vous avez besoin d'aide pour identifier vos qualités et défauts.",
        "D": "Vous n'arrivez pas à vous analyser vous-même.",
    }),
    ("L'empathie", "Intelligence émotionnelle", {
        "A": "Vous ressentez fortement les émotions des autres et souhaitez les aider.",
        "B": "Vous vous sentez mal à l'aise quand les autres traversent des difficultés.",
        "C": "Vous trouvez ça comique quand les autres se retrouvent dans des situations gênantes.",
        "D": "Vous êtes déçu par les manques de professionnalisme sans ressentir d'empathie.",
    }),
    ("La confiance en soi", "Intelligence émotionnelle", {
        "A": "Vous êtes confiant et enthousiaste face aux nouvelles responsabilités.",
        "B": "Vous ressentez une certaine pression mais êtes prêt à assumer.",
        "C": "Vous êtes inquiet de ne pas être à la hauteur et hésitez.",
        "D": "Vous préférez décliner les nouvelles responsabilités par peur de l'échec.",
    }),
    ("La gestion du stress", "Intelligence émotionnelle", {
        "A": "Vous perdez vos moyens face aux imprévus importants.",
        "B": "Vous cherchez à annuler ou reporter face aux imprévus.",
        "C": "Vous respirez et trouvez des solutions alternatives face aux imprévus.",
        "D": "Vous improvisez avec confiance face aux imprévus.",
    }),
    ("La bienveillance", "Intelligence émotionnelle", {
        "A": "Vous ne vous souciez pas des problèmes des personnes que vous ne connaissez pas bien.",
        "B": "Vous respectez la vie privée des autres et ne vous immiscez pas.",
        "C": "Vous voulez aider et réconforter même les personnes peu proches de vous.",
        "D": "Vous allez spontanément vers les gens en difficulté pour les soutenir.",
    }),
    ("Altruisme", "Intelligence sociale", {
        "A": "Vous partagez vos avantages avec tout le monde sans distinction.",
        "B": "Vous partagez en priorité avec ceux qui ont le plus besoin.",
        "C": "Vous partagez uniquement avec ceux qui pourraient vous apporter quelque chose en retour.",
        "D": "Vous gardez vos avantages pour vous pour préserver votre position.",
    }),
    ("Esprit d'équipe", "Intelligence sociale", {
        "A": "Vous êtes heureux de travailler à plusieurs, c'est plus riche.",
        "B": "Vous êtes pressé de connaître vos collaborateurs.",
        "C": "Vous faites le travail de groupe uniquement parce que vous n'avez pas le choix.",
        "D": "Cette idée vous fatigue déjà, vous détestez les travaux de groupe.",
    }),
    ("Intelligence culturelle", "Intelligence sociale", {
        "A": "Vous apprenez la langue locale et essayez les coutumes d'autres cultures.",
        "B": "Vous aimez découvrir les cultures en visitant les lieux historiques.",
        "C": "Vous préférez les habitudes familières même en voyage.",
        "D": "Vous restez dans votre zone de confort même à l'étranger.",
    }),
    ("La coopération, la collaboration", "Intelligence sociale", {
        "A": "Vous collaborez efficacement avec n'importe quel profil.",
        "B": "Vous collaborez bien tant qu'il y a un minimum de respect mutuel.",
        "C": "Vous avez du mal à collaborer sans points communs avec vos partenaires.",
        "D": "Vous avez besoin d'apprécier les personnes pour être efficace avec elles.",
    }),
    ("L'interaction avec les autres", "Intelligence sociale", {
        "A": "Vous adorez nouer des liens et entretenir des relations sur le long terme.",
        "B": "Vous aimez plutôt les relations durables même si vous n'êtes pas expert.",
        "C": "Vous préférez avoir un petit cercle proche.",
        "D": "Vous préférez être seul plutôt que de multiplier les relations.",
    }),
    ("Sociabilité", "Intelligence sociale", {
        "A": "Vous allez parler à tout le monde en soirée, vous voulez savoir qui est qui.",
        "B": "Vous lancez des conversations même si vous n'y êtes pas obligé.",
        "C": "Vous cherchez un moyen de vous échapper pour éviter de trop parler.",
        "D": "Vous faites tout pour ne pas aller aux soirées ou événements sociaux.",
    }),
    ("L'autonomie", "Management de projet", {
        "A": "Vous vous fixez vos propres objectifs et organisez votre travail de façon autonome.",
        "B": "Vous recherchez des ressources pour trouver la meilleure approche.",
        "C": "Vous préférez être accompagné par un expert pour être sûr du résultat.",
        "D": "Vous demandez de l'aide à des collègues qui s'y connaissent mieux.",
    }),
    ("La fixation d'objectifs", "Management de projet", {
        "A": "Vous planifiez des heures de travail et fixez des jalons précis.",
        "B": "Vous vous inscrivez à des cours avec des objectifs clairs et un rythme régulier.",
        "C": "Vous achetez des ressources sans plan précis sur quand les utiliser.",
        "D": "Vous apprendrez quand vous aurez du temps libre, sans objectif ni calendrier.",
    }),
    ("La gestion des risques", "Management de projet", {
        "A": "Vous prenez en compte les événements qui pourraient annuler un projet.",
        "B": "Vous avez toujours un plan de secours pour chaque imprévu.",
        "C": "Vous veillez à ce que la qualité soit au rendez-vous avant tout.",
        "D": "Vous priorisez la satisfaction des participants avant les risques.",
    }),
    ("La prise de décision", "Management de projet", {
        "A": "Vous lisez toutes les études disponibles et prenez une décision éclairée.",
        "B": "Vous prenez des décisions rapides face à l'urgence.",
        "C": "Vous réunissez les proches pour décider collectivement.",
        "D": "Vous avez du mal à prendre des décisions quand les enjeux sont lourds.",
    }),
    ("La supervision", "Management de projet", {
        "A": "Vous établissez des outils pour contrôler l'avancée du travail.",
        "B": "Vous vérifiez au fur et à mesure que les tâches ont bien été réalisées.",
        "C": "Vous terminez vite puis corrigez la qualité globalement.",
        "D": "Vous faites d'abord les tâches qui vous plaisent le plus.",
    }),
    ("La tolérance au changement", "Management de projet", {
        "A": "Vous arrêtez quand les règles changent en cours de route.",
        "B": "Vous êtes perturbé et énervé par les changements soudains.",
        "C": "Vous lisez les nouvelles règles et essayez de vous adapter.",
        "D": "Vous continuez avec enthousiasme, les changements peuvent être amusants.",
    }),
    ("Equité", "Management et gestion d'équipe", {
        "A": "Vous pensez que les pays riches devraient aider les pays pauvres.",
        "B": "Vous pensez que tout le monde devrait avoir assez pour vivre correctement.",
        "C": "Vous pensez que la répartition actuelle reflète la compétence individuelle.",
        "D": "Vous pensez que la redistribution n'est pas nécessaire.",
    }),
    ("Gérer et résoudre les conflits", "Management et gestion d'équipe", {
        "A": "Vous cherchez l'origine du conflit et proposez une solution.",
        "B": "Vous mettez en place une médiation pour que les parties s'expriment.",
        "C": "Vous préférez ne pas intervenir par peur des répercussions.",
        "D": "Vous ne vous impliquez pas, de peur d'aggraver la situation.",
    }),
    ("Inclusivité", "Management et gestion d'équipe", {
        "A": "Vous allez chercher les personnes isolées pour les intégrer au groupe.",
        "B": "Vous allez parler aux personnes seules pour qu'elles se sentent moins isolées.",
        "C": "Vous les laissez tranquilles, ils se feront des amis par eux-mêmes.",
        "D": "Vous faites comme si vous ne les aviez pas vus.",
    }),
    ("L'esprit d'initiative", "Management et gestion d'équipe", {
        "A": "Vous ne tentez pas de réaliser un travail qui dépasse vos compétences.",
        "B": "Vous tentez uniquement si un expert peut vous aider.",
        "C": "Vous vous autoformez grâce à internet pour acquérir la compétence.",
        "D": "Vous vous adaptez au fur et à mesure, peu importe les obstacles.",
    }),
    ("Le coaching des autres", "Management et gestion d'équipe", {
        "A": "Vous cherchez à comprendre les difficultés et accompagnez avec une formation adaptée.",
        "B": "Vous prenez le temps de comprendre et prodigues des conseils ciblés.",
        "C": "Vous laissez les autres trouver les solutions par eux-mêmes.",
        "D": "Vous prenez en charge les tâches vous-même pour éviter de perdre du temps.",
    }),
    ("Leadership", "Management et gestion d'équipe", {
        "A": "On vous laisse prendre la direction pour montrer la voie.",
        "B": "Vos idées sont écoutées et mises en œuvre par le groupe.",
        "C": "Vous suivez le plan rigoureusement pour que tout se passe bien.",
        "D": "Vous écoutez les autres sans vous imposer.",
    }),
    ("L'auto-formation", "Organisation", {
        "A": "Vous recherchez des cours en ligne et des articles pour vous autoformer.",
        "B": "Vous empruntez des livres et cherchez des tutoriels pour approfondir.",
        "C": "Vous trouvez ça intéressant mais ne voyez pas l'intérêt d'en apprendre plus.",
        "D": "C'est le rôle des enseignants d'enseigner, pas besoin d'explorer seul.",
    }),
    ("La concentration", "Organisation", {
        "A": "Vous vous fixez des petits objectifs et prenez de courtes pauses régulières.",
        "B": "Vous alternez avec d'autres activités plus stimulantes pour rester alerte.",
        "C": "Vous vous laissez souvent distraire, notamment par votre téléphone.",
        "D": "Vous avez tendance à procrastiner car les tâches répétitives vous ennuient.",
    }),
    ("La gestion des ressources", "Organisation", {
        "A": "Vous travaillez à un rythme régulier chaque jour pour avancer.",
        "B": "Vous identifiez les tâches simples et les finissez vite pour mieux vous concentrer sur les autres.",
        "C": "Vous travaillez en fonction de votre motivation du moment.",
        "D": "Vous attendez le dernier moment car c'est là que vous êtes le plus performant.",
    }),
    ("La gestion du temps", "Organisation", {
        "A": "Vous planifiez chaque étape avec dates, lieux et budgets.",
        "B": "Vous calculez les délais de chaque activité pour les enchaîner au bon moment.",
        "C": "Vous préférez vous reposer et vous prélasser sans trop planifier.",
        "D": "Vous improvisez sur place car le spontané est plus amusant.",
    }),
    ("La hiérarchisation et la priorisation", "Organisation", {
        "A": "Vous visualisez clairement toutes les étapes avant un projet important.",
        "B": "Vous utilisez des cartes mentales ou listes pour organiser vos pensées.",
        "C": "Vous vous sentez souvent dépassé et ne savez pas par où commencer.",
        "D": "Vous attendez que les choses se présentent et réagissez au fur et à mesure.",
    }),
    ("Le respect des délais", "Organisation", {
        "A": "Vous arrivez en avance pour ne pas faire attendre les autres.",
        "B": "Vous arrivez pile à l'heure.",
        "C": "Vous arrivez légèrement en retard.",
        "D": "Vous arrivez souvent en retard car vous mettez beaucoup de temps à vous préparer.",
    }),
]

SS_RAPPORT_NOMS = {
    0: "Communication",
    1: "Esprit critique",
    2: "Éthique",
    3: "Intelligence émotionnelle",
    4: "Intelligence sociale",
    5: "Management de projet",
    6: "Management et gestion d'équipe",
    7: "Organisation",
}

SS_NIVEAUX = {1: "À développer", 2: "Intermédiaire", 3: "Très développée"}
SS_COULEURS_HEX = {1: "E8A87C", 2: "C9A84C", 3: "6B9E7E"}
SS_COULEURS_RGB = {
    1: (0xe8, 0xa8, 0x7c),
    2: (0xc9, 0xa8, 0x4c),
    3: (0x6b, 0x9e, 0x7e),
}

# Mention légale salaires — à afficher dans tous les modules qui affichent un salaire
MENTION_SALAIRE = (
    "💡 Salaires indicatifs — Sources : ONISEP, APEC, INSEE, observatoires sectoriels. "
    "Les fourchettes peuvent varier selon l'expérience, la région et la taille de l'entreprise."
)
MENTION_SALAIRE_COURTE = (
    "Salaires indicatifs — Sources : ONISEP, APEC, INSEE. "
    "Fourchettes variables selon expérience, région et entreprise."
)

