import logging

logger = logging.getLogger(__name__)

def generate_analysis_prompt(subject_text: str) -> str:
    prompt = (
        "Vous êtes un professeur de philosophie expérimenté. Voici le sujet d'une épreuve de philosophie du baccalauréat pour la session 2024. "
        "Votre tâche est d'analyser ce sujet en identifiant les enjeux philosophiques et les problématiques qui y sont soulevées. "
        "Pour chacun des trois sujets proposés, proposez des pistes d'argumentation, les difficultés potentielles et des conseils méthodologiques permettant d'aborder efficacement le sujet. \n\n"
        "Sujet :\n"
        f"{subject_text}\n\n"
        "Merci de fournir une analyse claire, détaillée et pédagogique."
    )
    return prompt

def generate_student_answer_prompt(subject_text: str) -> str:
    prompt = (
        "Tu es un élève de 4ème et tu dois répondre à une évaluation de mathématiques, fait des fautes "
        "Rédige ta copie en respectant le format suivant, de manière claire et lisible, en **évitablement toute notation LaTeX** "
        "et **sans** utiliser de symboles comme $ ou \\square. Utilise simplement du texte brut pour tes réponses.\n\n"
        "1. [Intitulé de la question 1]\n"
        "   Réponse: [Ta réponse en texte simple]\n\n"
        "2. [Intitulé de la question 2]\n"
        "   Réponse: [Ta réponse en texte simple]\n\n"
        "3. [Intitulé de la question 3]\n"
        "   Réponse: [Ta réponse en texte simple]\n\n"
        "...\n\n"

        "Voici le sujet à traiter. Rédige ta copie en respectant ce format et sans insérer de LaTeX ou de symboles spéciaux :\n\n"
        f"{subject_text}\n\n"
        "Fin de l'énoncé. Merci de respecter strictement le format demandé."
    )
    return prompt