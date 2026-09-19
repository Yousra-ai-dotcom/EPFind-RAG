"""
Modèles SQLAlchemy — tables PostgreSQL
Responsable : Personne 2

Tables à modéliser :
- User (id, name, email, microsoft_id, created_at)
- Conversation (id, user_id, title, created_at)
- Message (id, conversation_id, role, content, created_at)
- Quiz (id, user_id, course, score, number_questions, created_at)
- QuizQuestion / QuizAnswer si vous voulez le détail question par question
"""

# TODO (Personne 2) :
# - Définir les classes de modèles avec SQLAlchemy (declarative_base)
