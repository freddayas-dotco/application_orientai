"""
OrientAI — Données partagées pour les rapports
Ce fichier est importé par rapport_v2.py, rapport_pdf.py et app.py
"""

MAPPING_QUESTIONS = [
    ("L'audace (ou le culot)", "Communication", {
        "A": "Vous faites preuve d'une grande audace et prenez des initiatives sans hésiter.",
        "B": "Vous osez prendre des initiatives et vous montrez spontané dans la plupart des situations.",
        "C": "Vous avez tendance à rester en retrait et préférez observer avant d'agir.",
        "D": "Vous manquez d'audace, surtout face à des personnes ou situations impressionnantes.",
    }),
    ("La clarté de communication", "Communication", {
        "A": "Vous vous exprimez avec une grande clarté et vos interlocuteurs vous comprennent sans effort.",
        "B": "Vous êtes généralement clair à l'oral et savez adapter votre discours.",
        "C": "Vous avez parfois du mal à structurer vos idées et à vous faire comprendre.",
        "D": "Vous éprouvez des difficultés à formuler des messages clairs et précis.",
    }),
    ("Le tact et la diplomatie", "Communication", {
        "A": "Vous dites les choses franchement, quitte à blesser.",
        "B": "Vous exposez les faits objectivement, sans chercher à ménager.",
        "C": "Vous mesurez vos mots pour ménager les susceptibilités.",
        "D": "Vous choisissez chaque mot avec soin pour que personne ne soit blessé.",
    }),
    ("La négociation", "Communication", {
        "A": "Vous aimez négocier et cherchez systématiquement des accords profitables pour toutes les parties.",
        "B": "Vous négociez quand c'est nécessaire et savez défendre vos intérêts.",
        "C": "Vous préférez éviter les négociations et cédez souvent pour maintenir la paix.",
        "D": "Vous percevez la négociation comme un conflit et cherchez à l'éviter à tout prix.",
    }),
    ("Prise de parole en public", "Communication", {
        "A": "Vous êtes totalement à l'aise en public et aimez prendre la parole devant un groupe.",
        "B": "Vous vous exprimez sereinement en public, même si ce n'est pas votre activité préférée.",
        "C": "Vous prenez la parole en public quand c'est nécessaire, mais sans enthousiasme particulier.",
        "D": "Vous évitez autant que possible de vous exprimer devant un groupe.",
    }),
    ("Rhétorique ou storytelling", "Communication", {
        "A": "Vous savez captiver votre audience avec des récits vivants et engageants.",
        "B": "Vous parvenez à intéresser vos interlocuteurs quand vous racontez quelque chose.",
        "C": "Vous avez du mal à rendre vos récits captivants pour votre auditoire.",
        "D": "Votre façon de vous exprimer peine à susciter l'intérêt de vos interlocuteurs.",
    }),
    ("Actualisation des connaissances", "Esprit critique", {
        "A": "Vous vous tenez constamment informé et cherchez activement à enrichir vos connaissances.",
        "B": "Vous vous informez régulièrement sur les sujets qui vous intéressent.",
        "C": "Vous n'actualisez pas systématiquement vos connaissances.",
        "D": "Vous ne ressentez pas le besoin de mettre à jour vos connaissances régulièrement.",
    }),
    ("L'acuité et le discernement", "Esprit critique", {
        "A": "Vous analysez les situations avec finesse et identifiez rapidement ce qui est essentiel.",
        "B": "Vous prenez généralement le temps d'évaluer une situation avant de réagir.",
        "C": "Vous avez tendance à vous fier à votre première impression sans toujours approfondir.",
        "D": "Vous réagissez impulsivement sans toujours prendre le recul nécessaire.",
    }),
    ("L'ouverture d'esprit", "Esprit critique", {
        "A": "Vous êtes très ouvert aux nouvelles idées et remettez volontiers vos habitudes en question.",
        "B": "Vous accueillez les nouvelles perspectives avec curiosité et bienveillance.",
        "C": "Vous préférez vos méthodes habituelles et changez difficilement vos habitudes.",
        "D": "Vous êtes peu réceptif aux idées qui diffèrent des vôtres.",
    }),
    ("La créativité ou l'imagination", "Esprit critique", {
        "A": "Vous manquez d'imagination et avez du mal à générer des idées originales.",
        "B": "Votre créativité est limitée et vous avez besoin de stimulation extérieure pour innover.",
        "C": "Vous avez une bonne capacité créative et générez des idées avec relative facilité.",
        "D": "Vous êtes très créatif et imaginez facilement des solutions originales et détaillées.",
    }),
    ("La curiosité", "Esprit critique", {
        "A": "Vous êtes naturellement curieux et cherchez activement à apprendre et découvrir.",
        "B": "Vous vous informez sur les sujets qui vous touchent et restez ouvert à la nouveauté.",
        "C": "Vous attendez que l'information vienne à vous plutôt que de la chercher activement.",
        "D": "Vous n'êtes pas particulièrement curieux et ressentez peu le besoin d'explorer.",
    }),
    ("Savoir rechercher pour résoudre un problème", "Esprit critique", {
        "A": "Vous savez identifier les bonnes sources et trouver des informations fiables rapidement.",
        "B": "Vous cherchez activement des ressources pour résoudre les problèmes que vous rencontrez.",
        "C": "Vous préférez demander de l'aide plutôt que de chercher par vous-même.",
        "D": "Vous avez tendance à improviser plutôt que de rechercher des informations.",
    }),
    ("L'intégrité", "Éthique", {
        "A": "Vous agissez toujours avec honnêteté et préférez perdre plutôt que de tricher.",
        "B": "Vous essayez généralement de faire ce qui est juste et honnête.",
        "C": "Vous profitez parfois des avantages inattendus sans trop vous questionner.",
        "D": "Vous n'hésitez pas à tirer profit des situations, même si cela manque d'intégrité.",
    }),
    ("La conscience professionnelle", "Éthique", {
        "A": "Vous allez toujours au bout de vos engagements avec rigueur et sérieux.",
        "B": "Vous respectez généralement vos engagements professionnels.",
        "C": "Vous êtes parfois tenté d'abandonner vos tâches pour des activités plus agréables.",
        "D": "Vous avez du mal à maintenir un effort soutenu jusqu'à la fin d'une tâche.",
    }),
    ("La loyauté", "Éthique", {
        "A": "Vous êtes d'une loyauté sans faille et soutenez votre équipe même dans les moments difficiles.",
        "B": "Vous restez fidèle à votre groupe et compensez les faiblesses collectives.",
        "C": "Vous n'hésitez pas à quitter un groupe peu performant pour rejoindre de meilleures équipes.",
        "D": "Vous préférez travailler seul pour garantir la qualité du résultat.",
    }),
    ("Le sens des responsabilités", "Éthique", {
        "A": "Vous assumez pleinement vos responsabilités et affrontez les conséquences de vos actes.",
        "B": "Vous prenez vos responsabilités, même si cela vous demande un effort.",
        "C": "Vous avez tendance à minimiser votre rôle quand les choses tournent mal.",
        "D": "Vous évitez d'assumer vos responsabilités face aux conséquences négatives.",
    }),
    ("L'éco-responsabilité", "Éthique", {
        "A": "Vous adoptez un mode de vie très éco-responsable et faites des choix durables au quotidien.",
        "B": "Vous faites des efforts concrets pour réduire votre impact environnemental.",
        "C": "Vous essayez d'être raisonnable sans vous imposer de contraintes excessives.",
        "D": "L'éco-responsabilité n'est pas une priorité dans vos choix quotidiens.",
    }),
    ("L'engagement", "Éthique", {
        "A": "Vous tenez toujours vos engagements, quelles que soient les circonstances.",
        "B": "Vous respectez vos engagements sauf en cas de force majeure.",
        "C": "Vous avez du mal à tenir vos engagements quand d'autres priorités surgissent.",
        "D": "Vous prenez des engagements facilement mais les abandonnez quand ça devient contraignant.",
    }),
    ("Acceptation des retours et critiques", "Intelligence émotionnelle", {
        "A": "Vous accueillez les critiques avec ouverture et les utilisez pour progresser.",
        "B": "Les critiques vous irritent parfois, mais vous savez en tirer des enseignements.",
        "C": "Vous ignorez les critiques qui vous semblent mal intentionnées.",
        "D": "Les critiques vous affectent profondément et déclenchent des réactions défensives.",
    }),
    ("Introspection", "Intelligence émotionnelle", {
        "A": "Vous vous connaissez bien et identifiez facilement vos forces et axes d'amélioration.",
        "B": "Vous arrivez à comprendre vos émotions et comportements, mais pas toujours facilement.",
        "C": "Vous avez du mal à analyser vos propres réactions et besoins.",
        "D": "L'introspection est difficile pour vous et vous peinez à vous analyser.",
    }),
    ("L'empathie", "Intelligence émotionnelle", {
        "A": "Vous êtes très empathique et ressentez profondément les émotions des autres.",
        "B": "Vous êtes sensible aux difficultés des autres et souhaitez les aider.",
        "C": "Vous manquez parfois d'empathie face aux difficultés des autres.",
        "D": "Vous avez du mal à vous mettre à la place des autres et à ressentir de l'empathie.",
    }),
    ("La confiance en soi", "Intelligence émotionnelle", {
        "A": "Vous avez une grande confiance en vous et abordez les défis avec enthousiasme.",
        "B": "Vous avez confiance en vous même si vous ressentez parfois une certaine pression.",
        "C": "Vous manquez parfois de confiance et hésitez avant de vous engager.",
        "D": "Vous manquez de confiance en vous et évitez les situations où vous pourriez échouer.",
    }),
    ("La gestion du stress", "Intelligence émotionnelle", {
        "A": "Vous gardez votre calme face aux imprévus et improvisez avec confiance.",
        "B": "Vous trouvez des solutions alternatives face aux situations stressantes.",
        "C": "Vous avez tendance à éviter ou reporter quand la situation devient trop stressante.",
        "D": "Vous perdez vos moyens face aux imprévus importants.",
    }),
    ("La bienveillance", "Intelligence émotionnelle", {
        "A": "Vous allez spontanément vers les personnes en difficulté pour les soutenir.",
        "B": "Vous manifestez de la bienveillance même envers des personnes que vous connaissez peu.",
        "C": "Vous respectez la vie privée des autres sans vous imposer.",
        "D": "Vous ne ressentez pas le besoin de vous impliquer dans les difficultés des autres.",
    }),
    ("Altruisme", "Intelligence sociale", {
        "A": "Vous partagez vos ressources et avantages avec tous, sans distinction.",
        "B": "Vous partagez en priorité avec ceux qui en ont le plus besoin.",
        "C": "Vous partagez principalement avec ceux qui pourraient vous apporter quelque chose en retour.",
        "D": "Vous gardez vos avantages pour vous afin de préserver votre position.",
    }),
    ("Esprit d'équipe", "Intelligence sociale", {
        "A": "Vous appréciez vraiment le travail en équipe et y trouvez une grande richesse.",
        "B": "Vous aimez collaborer avec les autres et cherchez rapidement à créer du lien.",
        "C": "Vous travaillez en équipe quand c'est nécessaire mais sans enthousiasme particulier.",
        "D": "Vous préférez travailler seul et trouvez le travail collectif épuisant.",
    }),
    ("Intelligence culturelle", "Intelligence sociale", {
        "A": "Vous êtes très ouvert aux autres cultures et cherchez activement à les comprendre.",
        "B": "Vous aimez découvrir d'autres cultures et enrichir votre vision du monde.",
        "C": "Vous préférez vos habitudes et restez dans votre zone de confort même face à la différence.",
        "D": "Vous n'êtes pas particulièrement attiré par la découverte d'autres cultures.",
    }),
    ("La coopération, la collaboration", "Intelligence sociale", {
        "A": "Vous collaborez efficacement avec tout type de profil, quelles que soient les différences.",
        "B": "Vous coopérez bien tant qu'un minimum de respect mutuel existe.",
        "C": "Vous avez du mal à collaborer avec des personnes très différentes de vous.",
        "D": "Vous avez besoin d'apprécier vos partenaires pour être efficace avec eux.",
    }),
    ("L'interaction avec les autres", "Intelligence sociale", {
        "A": "Vous adorez créer des liens et entretenir des relations riches et durables.",
        "B": "Vous aimez les relations durables et investissez dans vos liens sociaux.",
        "C": "Vous préférez un cercle social restreint mais de qualité.",
        "D": "Vous préférez la solitude aux interactions sociales multiples.",
    }),
    ("Sociabilité", "Intelligence sociale", {
        "A": "Vous êtes très sociable et aimez rencontrer de nouvelles personnes.",
        "B": "Vous prenez facilement des initiatives sociales et aimez lancer des conversations.",
        "C": "Vous êtes discret en société et préférez éviter les interactions prolongées.",
        "D": "Vous êtes peu à l'aise en société et évitez les événements sociaux.",
    }),
    ("L'autonomie", "Management de projet", {
        "A": "Vous êtes très autonome et organisez votre travail sans avoir besoin de guidance.",
        "B": "Vous savez chercher les ressources nécessaires pour avancer de façon indépendante.",
        "C": "Vous préférez être accompagné par un expert pour être sûr du résultat.",
        "D": "Vous avez besoin d'un encadrement fort pour avancer efficacement.",
    }),
    ("La fixation d'objectifs", "Management de projet", {
        "A": "Vous fixez des objectifs clairs, planifiez précisément et suivez vos jalons.",
        "B": "Vous vous donnez des objectifs structurés et un rythme régulier pour progresser.",
        "C": "Vous avancez sans plan précis et ajustez au fur et à mesure.",
        "D": "Vous n'avez pas l'habitude de vous fixer des objectifs formels.",
    }),
    ("La gestion des risques", "Management de projet", {
        "A": "Vous anticipez systématiquement les risques et préparez des plans de secours.",
        "B": "Vous avez toujours une solution de rechange en cas d'imprévu.",
        "C": "Vous vous concentrez sur la qualité plutôt que sur la prévention des risques.",
        "D": "Vous privilégiez la satisfaction des parties prenantes avant la gestion des risques.",
    }),
    ("La prise de décision", "Management de projet", {
        "A": "Vous prenez des décisions éclairées en vous appuyant sur une analyse approfondie.",
        "B": "Vous savez décider rapidement quand la situation l'exige.",
        "C": "Vous préférez décider collectivement et cherchez le consensus.",
        "D": "Vous avez du mal à trancher quand les enjeux sont importants.",
    }),
    ("La supervision", "Management de projet", {
        "A": "Vous mettez en place des outils de suivi rigoureux pour contrôler l'avancement du travail.",
        "B": "Vous vérifiez régulièrement que les tâches avancent comme prévu.",
        "C": "Vous préférez avancer vite et corriger les erreurs après coup.",
        "D": "Vous réalisez d'abord les tâches qui vous plaisent, quitte à négliger les autres.",
    }),
    ("La tolérance au changement", "Management de projet", {
        "A": "Vous accueillez le changement avec enthousiasme et y voyez une opportunité.",
        "B": "Vous vous adaptez au changement même si cela vous demande un effort.",
        "C": "Vous avez besoin de temps pour accepter les changements et vous y adapter.",
        "D": "Vous résistez fortement au changement et préférez la stabilité.",
    }),
    ("Equité", "Management et gestion d'équipe", {
        "A": "Vous veillez à ce que chaque membre soit reconnu de façon juste selon sa contribution.",
        "B": "Vous pensez que tout le monde mérite les mêmes opportunités au sein d'une équipe.",
        "C": "Vous pensez que les meilleures performances méritent plus de reconnaissance.",
        "D": "Vous pensez que chacun doit faire valoir son travail par lui-même.",
    }),
    ("Gérer et résoudre les conflits", "Management et gestion d'équipe", {
        "A": "Vous cherchez activement l'origine des conflits et proposez des solutions constructives.",
        "B": "Vous facilitez le dialogue entre les parties pour désamorcer les tensions.",
        "C": "Vous préférez ne pas intervenir dans les conflits par crainte des répercussions.",
        "D": "Vous évitez toute implication dans les conflits pour ne pas aggraver la situation.",
    }),
    ("Inclusivité", "Management et gestion d'équipe", {
        "A": "Vous cherchez activement à intégrer les personnes isolées dans le groupe.",
        "B": "Vous allez vers les personnes seules pour qu'elles se sentent incluses.",
        "C": "Vous laissez les personnes isolées s'intégrer à leur propre rythme.",
        "D": "Vous ne prêtez pas attention aux personnes en marge du groupe.",
    }),
    ("L'esprit d'initiative", "Management et gestion d'équipe", {
        "A": "Vous prenez des initiatives même dans des domaines qui dépassent vos compétences actuelles.",
        "B": "Vous vous adaptez au fur et à mesure, peu importe les obstacles.",
        "C": "Vous prenez des initiatives quand vous pouvez être accompagné.",
        "D": "Vous hésitez à vous lancer quand vous ne maîtrisez pas les compétences nécessaires.",
    }),
    ("Le coaching des autres", "Management et gestion d'équipe", {
        "A": "Vous accompagnez les autres avec des formations adaptées à leurs besoins spécifiques.",
        "B": "Vous prenez le temps de comprendre les difficultés et prodiguez des conseils ciblés.",
        "C": "Vous encouragez les autres à trouver leurs propres solutions de façon autonome.",
        "D": "Vous préférez faire vous-même plutôt que de prendre le temps d'accompagner.",
    }),
    ("Leadership", "Management et gestion d'équipe", {
        "A": "Vous prenez naturellement les rênes et guidez le groupe vers ses objectifs.",
        "B": "Vos idées et votre vision influencent naturellement les décisions du groupe.",
        "C": "Vous participez activement mais préférez soutenir un leader expérimenté.",
        "D": "Vous êtes à l'écoute et préférez suivre plutôt que diriger.",
    }),
    ("L'auto-formation", "Organisation", {
        "A": "Vous cherchez activement des ressources en ligne pour vous autoformer en continu.",
        "B": "Vous utilisez livres et tutoriels pour approfondir vos connaissances.",
        "C": "Vous trouvez l'auto-formation intéressante mais ne passez pas facilement à l'action.",
        "D": "Vous considérez que l'apprentissage est du ressort des enseignants uniquement.",
    }),
    ("La concentration", "Organisation", {
        "A": "Vous gérez efficacement votre concentration en vous fixant des objectifs et des pauses.",
        "B": "Vous alternez les activités pour maintenir votre niveau d'attention.",
        "C": "Vous vous laissez facilement distraire et avez du mal à maintenir votre focus.",
        "D": "Vous procrastinez souvent et avez du mal à vous mettre au travail sur des tâches répétitives.",
    }),
    ("La gestion des ressources", "Organisation", {
        "A": "Vous travaillez à un rythme régulier et gérez bien votre énergie dans le temps.",
        "B": "Vous priorisez intelligemment vos tâches pour optimiser votre efficacité.",
        "C": "Vous travaillez par motivation du moment sans planification précise.",
        "D": "Vous attendez la dernière minute pour travailler, sous pression.",
    }),
    ("La gestion du temps", "Organisation", {
        "A": "Vous planifiez avec précision chaque étape de vos projets et respectez vos délais.",
        "B": "Vous calculez le temps nécessaire pour chaque activité et enchaînez avec méthode.",
        "C": "Vous avez du mal à planifier et préférez une approche souple et peu contraignante.",
        "D": "Vous improvisez et faites confiance aux circonstances plutôt qu'à la planification.",
    }),
    ("La hiérarchisation et la priorisation", "Organisation", {
        "A": "Vous visualisez clairement vos priorités et organisez efficacement vos actions.",
        "B": "Vous utilisez des outils de planification pour structurer vos projets.",
        "C": "Vous vous sentez souvent dépassé et avez du mal à identifier par où commencer.",
        "D": "Vous réagissez aux événements au fur et à mesure sans anticipation.",
    }),
    ("Le respect des délais", "Organisation", {
        "A": "Vous êtes toujours en avance et respectez scrupuleusement vos engagements de temps.",
        "B": "Vous êtes ponctuel et respectez les délais fixés.",
        "C": "Vous arrivez légèrement en retard et avez du mal à être toujours à l'heure.",
        "D": "Vous êtes souvent en retard et avez du mal à respecter les délais.",
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

