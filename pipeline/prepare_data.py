from clean_data import clean_data
from normalize_skills import normalize_skills
from role_skill_mapping import build_role_skill_mapping
from prepare_documents import prepare_documents

if __name__ == "__main__":
    clean_data()
    normalize_skills()
    build_role_skill_mapping()
    prepare_documents()
    print("Data pipeline completed.")
