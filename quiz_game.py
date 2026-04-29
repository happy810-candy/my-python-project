from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Danh sách câu hỏi và đáp án
questions = [
    {"question": "Thủ đô của Việt Nam là gì?", "answer": "Hà Nội"},
    {"question": "2 + 2 bằng mấy?", "answer": "4"},
    {"question": "Màu của bầu trời là gì?", "answer": "xanh"},
]

@app.route('/', methods=['GET', 'POST'])
def quiz():
    score = 0
    user_answers = []
    if request.method == 'POST':
        for i, q in enumerate(questions):
            user_answer = request.form.get(f'answer_{i}', '').strip()
            user_answers.append(user_answer)
            if user_answer.lower() == q['answer'].lower():
                score += 1
        return render_template_string(RESULT_TEMPLATE, score=score, total=len(questions), questions=questions, user_answers=user_answers)
    return render_template_string(QUIZ_TEMPLATE, questions=questions)

QUIZ_TEMPLATE = '''
<!doctype html>
<title>Đố Vui</title>
<h1>Web Game Đố Vui</h1>
<form method="post">
  {% for q in questions %}
    <p><b>Câu hỏi {{ loop.index }}:</b> {{ q.question }}</p>
    <input name="answer_{{ loop.index0 }}" autocomplete="off">
  {% endfor %}
  <p><button type="submit">Nộp bài</button></p>
</form>
'''

RESULT_TEMPLATE = '''
<!doctype html>
<title>Kết Quả</title>
<h1>Kết Quả: {{ score }}/{{ total }}</h1>
<ul>
  {% for q, a in zip(questions, user_answers) %}
    <li><b>{{ q.question }}</b><br>
        Đáp án của bạn: {{ a }}<br>
        Đáp án đúng: {{ q.answer }}
        {% if a.lower() == q.answer.lower() %} <span style="color:green">✔</span> {% else %} <span style="color:red">✘</span> {% endif %}
    </li>
  {% endfor %}
</ul>
<a href="/">Chơi lại</a>
'''

if __name__ == '__main__':
    app.run(debug=True)
