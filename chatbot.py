from flask import Flask, request, jsonify
import json
from difflib import get_close_matches

app = Flask(__name__)


def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)

    return data


def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(
        user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


# def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
#     for q in knowledge_base['questions']:
#         if q['question'] == question:
#             return q['answer']

def get_answer_for_question(question: str, knowledge_base: dict) -> tuple[str | None, str | None]:
    for q in knowledge_base['questions']:
        if q['question'] == question:
            return q.get('answer'), q.get('need-login')
    return None, None


@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    user_input = data['question']

    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    best_match: str | None = find_best_match(
        user_input, [q['question'] for q in knowledge_base['questions']])

    if best_match:
        # answer: str = get_answer_for_question(best_match, knowledge_base)
        answer, need_login = get_answer_for_question(
            best_match, knowledge_base)

        return jsonify({'answer': answer, 'need-login': need_login})
    else:
        knowledge_base["questions"].append(
            {"question": user_input, "answer": "", "need-login": ""})
        save_knowledge_base('knowledge_base.json', knowledge_base)
        return jsonify({'answer': 'Paumanhin pero wala akong makitang sagot para sa iyong katanungan. &#128546;', 'need-login': 'no'})


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)
