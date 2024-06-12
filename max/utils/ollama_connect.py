import ollama

response = ollama.chat(
    model="llama3",
    messages=[
        {
            "role": "user",
            "content": "résume ce texte en 300 caractères: L’exposition vous invite à une plongée au cœur de l’histoire des femmes de l’époque gallo-romaine à l’époque carolingienne dans des domaines aussi variés que la maternité, la gestion du foyer, l’éducation des enfants, le travail textile et agricole, mais également dans des domaines où l’on n’attend pas forcément la femme à cette époque telles que l’artisanat, le commerce, la médecine ou encore l’enseignement ou la littérature.  Tous ces aspects de la place des femmes dans la société se révéleront aussi à travers des objets archéologiques aimablement prêtés par des musées de la région (musée des Beaux-arts de Cambrai, forum antique de Bavay, Arkéos…), objets divers et variés mettant en scène la femme de sa naissance à sa mort au sein de son foyer ou à l’extérieur. Des accessoires liés au vêtements (fibules…), à la maternité (tire-lait), à l’hygiène, à la toilette, à la mise en beauté (maquillage, parures et bijoux), à l’évolution de la mode (représentation de coiffures), mais également des objets témoignant de l’implication de la femme dans la vie économique (outillage textile et agricole), ou dans la vie religieuse (instruments de musique pour les processions...) Oubliez vos idées reçues et venez découvrir ces femmes aux multiples facettes",
        },
    ],
)
print(response["message"]["content"])
