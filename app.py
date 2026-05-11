from flask import Flask, render_template, request, session, redirect, url_for
import json

app = Flask(__name__)
app.secret_key = "careerpath_secret_2024"

# ===== بيانات المسارات المهنية =====
CAREER_PATHS = {
    "technical": {
        "id": "technical",
        "title": "المسار التحليلي والتقني",
        "color": "#00d4ff",
        "gradient": "linear-gradient(135deg, #0a0f2e 0%, #0d1b4b 50%, #0a2a4a 100%)",
        "accent": "#00d4ff",
        "description": "أنت شخص يحب التفكير المنطقي والتحليلي، تجد نفسك مرتاحاً مع الأرقام والبيانات والأنظمة. عقلك يعمل بطريقة منهجية ودقيقة.",
        "jobs": [
            "مهندس برمجيات", "مطور ويب / تطبيقات",
            "محلل بيانات / علوم البيانات", "مهندس شبكات وأمن معلومات",
            "مهندس ذكاء اصطناعي", "مدير قواعد بيانات"
        ],
        "skills": [
            "البرمجة (Python, Java, C++)", "تحليل البيانات",
            "التفكير المنطقي والخوارزميات", "حل المشكلات التقنية",
            "الرياضيات والإحصاء", "قواعد البيانات والشبكات"
        ],
        "reason": "إجاباتك تكشف عن عقل تحليلي قوي وشغف بالتكنولوجيا والمنطق. أنت تفضل الحلول الدقيقة القائمة على البيانات، وهذا تماماً ما يحتاجه عالم التقنية."
    },
    "human": {
        "id": "human",
        "title": "المسار الإنساني والرعائي",
        "color": "#ff6b9d",
        "gradient": "linear-gradient(135deg, #1a0a1e 0%, #2d0f35 50%, #1a0a2e 100%)",
        "accent": "#ff6b9d",
        "description": "قلبك مفتوح للناس وتجد معنى حقيقياً في مساعدتهم. لديك قدرة طبيعية على التعاطف والاستماع وفهم المشاعر الإنسانية.",
        "jobs": [
            "طبيب / ممرض / معالج نفسي", "مستشار تربوي وإرشاد",
            "أخصائي اجتماعي", "معلم / مدرب",
            "مدير موارد بشرية", "مدير مجتمع ومنظمات غير ربحية"
        ],
        "skills": [
            "التواصل والاستماع الفعّال", "التعاطف والذكاء العاطفي",
            "حل النزاعات والوساطة", "التربية وعلم النفس",
            "العمل الجماعي والتعاون", "التحدث أمام الجمهور"
        ],
        "reason": "ردود أفعالك تدل على شخصية تضع الإنسان في المركز. إحساسك العالي بمشاعر الآخرين وحرصك على مساعدتهم يجعلانك مثالياً للمجالات التي تخدم المجتمع."
    },
    "creative": {
        "id": "creative",
        "title": "المسار الإبداعي والتصميمي",
        "color": "#ffd700",
        "gradient": "linear-gradient(135deg, #1a1000 0%, #2d1f00 50%, #1a1500 100%)",
        "accent": "#ffd700",
        "description": "خيالك لا حدود له وترى العالم من زاوية مختلفة. لديك حس جمالي مميز وقدرة على التعبير بطرق تلفت الانتباه وتترك أثراً.",
        "jobs": [
            "مصمم جرافيك / UI-UX", "مصور فوتوغرافي / مخرج فيديو",
            "كاتب ومحرر إبداعي", "مصمم أزياء / معماري",
            "مدير إبداعي في التسويق", "رسّام / فنان رقمي"
        ],
        "skills": [
            "التصميم الجرافيكي (Adobe, Figma)", "التفكير الإبداعي والابتكار",
            "الإخراج الفني والجمالي", "رواية القصص البصرية",
            "التصوير والفيديو والمونتاج", "فهم الألوان والتركيبات البصرية"
        ],
        "reason": "عقلك يفكر بالصور والأفكار قبل الكلمات. إجاباتك تكشف عن شخص يبحث عن التميز والجمال في كل شيء، وهذا بالضبط روح الإبداع والتصميم."
    },
    "business": {
        "id": "business",
        "title": "المسار الإداري والتجاري",
        "color": "#00ff88",
        "gradient": "linear-gradient(135deg, #001a0f 0%, #002d1a 50%, #001a10 100%)",
        "accent": "#00ff88",
        "description": "أنت قائد بالفطرة، تحب التخطيط واتخاذ القرارات وترى الصورة الكبيرة. لديك موهبة في التنظيم وإدارة الموارد لتحقيق الأهداف.",
        "jobs": [
            "مدير مشاريع / استشاري أعمال", "رائد أعمال ومؤسس شركات",
            "مدير تسويق ومبيعات", "محلل مالي / اقتصادي",
            "مدير عمليات وسلسلة توريد", "مستشار استراتيجي"
        ],
        "skills": [
            "التخطيط الاستراتيجي وصنع القرار", "التفاوض وإدارة العقود",
            "التسويق والمبيعات", "الإدارة المالية والمحاسبة",
            "قيادة الفرق وإدارة المواهب", "ريادة الأعمال والابتكار"
        ],
        "reason": "إجاباتك تكشف عن عقلية قيادية واضحة. أنت تفكر دائماً في الأثر والنتائج وتحب قيادة الفرق نحو الأهداف، وهذا هو جوهر عالم الأعمال والإدارة."
    }
}

# ===== أسئلة الاختبار =====
# الأوزان: [technical, human, creative, business]
QUESTIONS = [
    {
        "id": 1,
        "text": "ما الذي يستهويك أكثر في وقت الفراغ؟",
        "options": [
            {"text": "حل الألغاز والمسائل المنطقية", "weights": [3, 0, 0, 1]},
            {"text": "مساعدة الأصدقاء والاستماع لمشاكلهم", "weights": [0, 3, 0, 1]},
            {"text": "الرسم أو الكتابة أو صنع الأشياء", "weights": [0, 0, 3, 0]},
            {"text": "تنظيم الفعاليات وقيادة الأنشطة", "weights": [0, 1, 0, 3]},
        ]
    },
    {
        "id": 2,
        "text": "كيف تفضّل التعامل مع المشكلات؟",
        "options": [
            {"text": "بالتحليل المنطقي وجمع البيانات", "weights": [3, 0, 0, 1]},
            {"text": "بالتعاطف وفهم مشاعر الأشخاص المعنيين", "weights": [0, 3, 0, 0]},
            {"text": "بالتفكير الإبداعي وإيجاد حلول غير تقليدية", "weights": [0, 0, 3, 1]},
            {"text": "بالتخطيط الاستراتيجي ووضع خطة عمل", "weights": [1, 0, 0, 3]},
        ]
    },
    {
        "id": 3,
        "text": "ما بيئة العمل المثالية لك؟",
        "options": [
            {"text": "مكتب هادئ مع شاشات وأكواد وأنظمة", "weights": [3, 0, 0, 0]},
            {"text": "مع الناس والمجتمع وجهاً لوجه", "weights": [0, 3, 0, 1]},
            {"text": "استوديو إبداعي مليء بالأفكار والألوان", "weights": [0, 0, 3, 0]},
            {"text": "مكتب احترافي مع فريق عمل منظم وأهداف", "weights": [1, 0, 0, 3]},
        ]
    },
    {
        "id": 4,
        "text": "ما الذي يشعرك بالرضا الحقيقي بعد إنجازه؟",
        "options": [
            {"text": "بناء نظام أو حل تقني يعمل بدقة وكفاءة", "weights": [3, 0, 0, 0]},
            {"text": "تحسين حياة شخص أو مساعدته على التعافي", "weights": [0, 3, 0, 0]},
            {"text": "إنتاج عمل إبداعي يعبّر عنك ويلفت الأنظار", "weights": [0, 0, 3, 0]},
            {"text": "إتمام صفقة أو قيادة مشروع لتحقيق هدف", "weights": [0, 0, 0, 3]},
        ]
    },
    {
        "id": 5,
        "text": "كيف يصفك أصدقاؤك عادةً؟",
        "options": [
            {"text": "ذكي ومحلل ودقيق في كل التفاصيل", "weights": [3, 0, 0, 1]},
            {"text": "متعاطف ومهتم ومساعد للجميع", "weights": [0, 3, 0, 0]},
            {"text": "مبدع وخيالي وفريد في أسلوبه", "weights": [0, 0, 3, 0]},
            {"text": "منظم وقائد وطموح دائماً", "weights": [1, 0, 0, 3]},
        ]
    },
    {
        "id": 6,
        "text": "ما المادة الدراسية التي كانت الأقرب إلى قلبك؟",
        "options": [
            {"text": "الرياضيات والعلوم والحاسوب", "weights": [3, 0, 0, 0]},
            {"text": "علم النفس والاجتماع والصحة", "weights": [0, 3, 0, 1]},
            {"text": "الفنون والأدب والتصميم", "weights": [0, 0, 3, 0]},
            {"text": "الاقتصاد والإدارة والتسويق", "weights": [0, 0, 0, 3]},
        ]
    },
    {
        "id": 7,
        "text": "في المشاريع الجماعية، أنت عادةً...",
        "options": [
            {"text": "المحلل الذي يجمع البيانات ويعمل على الأنظمة", "weights": [3, 0, 0, 1]},
            {"text": "الوسيط الذي يحل الخلافات ويدعم الفريق", "weights": [0, 3, 0, 1]},
            {"text": "المبدع الذي يأتي بالأفكار والتصاميم الجديدة", "weights": [1, 0, 3, 0]},
            {"text": "القائد الذي ينظم الخطة ويوجّه الفريق", "weights": [0, 0, 0, 3]},
        ]
    },
    {
        "id": 8,
        "text": "ما الذي يقلقك أكثر في العالم؟",
        "options": [
            {"text": "تأخر التطور التكنولوجي وضعف الابتكار", "weights": [3, 0, 0, 0]},
            {"text": "معاناة الناس وقلة الرعاية الصحية والاجتماعية", "weights": [0, 3, 0, 0]},
            {"text": "غياب الجمال والإبداع والفن في الحياة", "weights": [0, 0, 3, 0]},
            {"text": "الفوضى وضعف الإدارة وسوء التنظيم", "weights": [0, 0, 0, 3]},
        ]
    },
    {
        "id": 9,
        "text": "ما هدفك المهني الأسمى؟",
        "options": [
            {"text": "اختراع تقنية أو نظام يغير طريقة عمل العالم", "weights": [3, 0, 0, 1]},
            {"text": "مساعدة أكبر عدد ممكن من الناس وتحسين حياتهم", "weights": [0, 3, 0, 0]},
            {"text": "ترك بصمة إبداعية خالدة يتذكرها الناس", "weights": [0, 0, 3, 0]},
            {"text": "قيادة مؤسسة ناجحة وبناء إمبراطورية أعمال", "weights": [0, 0, 1, 3]},
        ]
    },
    {
        "id": 10,
        "text": "ما نوع المحتوى الذي تستمتع بقراءته أو مشاهدته؟",
        "options": [
            {"text": "علوم وتكنولوجيا وبرمجة وذكاء اصطناعي", "weights": [3, 0, 0, 0]},
            {"text": "قصص إنسانية ومقالات نفسية واجتماعية", "weights": [0, 3, 0, 0]},
            {"text": "فن وتصميم وأدب وسينما وموسيقى", "weights": [0, 0, 3, 0]},
            {"text": "ريادة أعمال وإدارة وتسويق واستثمار", "weights": [0, 0, 0, 3]},
        ]
    }
]

def calculate_result(answers):
    """حساب نتيجة الاختبار بناءً على الإجابات"""
    scores = {"technical": 0, "human": 0, "creative": 0, "business": 0}
    keys = ["technical", "human", "creative", "business"]

    for q_idx, a_idx in enumerate(answers):
        if q_idx < len(QUESTIONS) and a_idx < len(QUESTIONS[q_idx]["options"]):
            weights = QUESTIONS[q_idx]["options"][a_idx]["weights"]
            for i, key in enumerate(keys):
                scores[key] += weights[i]

    # إيجاد المسار الأعلى نقاطاً
    winner = max(scores, key=scores.get)
    total = sum(scores.values())

    # حساب النسب المئوية
    percentages = {}
    for k, v in scores.items():
        percentages[k] = round((v / total * 100) if total > 0 else 0)

    return winner, scores, percentages


# ===== المسارات (Routes) =====

@app.route("/")
def index():
    session.clear()
    return render_template("index.html")


@app.route("/quiz")
def quiz():
    session["answers"] = []
    session["current_q"] = 0
    return render_template("quiz.html", questions=QUESTIONS)


@app.route("/answer", methods=["POST"])
def answer():
    answer_idx = int(request.form.get("answer", 0))
    answers = session.get("answers", [])
    answers.append(answer_idx)
    session["answers"] = answers

    if len(answers) >= len(QUESTIONS):
        return redirect(url_for("result"))

    return redirect(url_for("quiz"))


@app.route("/submit", methods=["POST"])
def submit():
    """استقبال جميع الإجابات دفعة واحدة من JavaScript"""
    data = request.get_json()
    answers = data.get("answers", [])
    session["answers"] = answers
    winner, scores, percentages = calculate_result(answers)
    session["result"] = {
        "winner": winner,
        "scores": scores,
        "percentages": percentages
    }
    return {"redirect": url_for("result")}


@app.route("/result")
def result():
    answers = session.get("answers", [])
    if not answers:
        return redirect(url_for("index"))

    result_data = session.get("result")
    if not result_data:
        winner, scores, percentages = calculate_result(answers)
        result_data = {"winner": winner, "scores": scores, "percentages": percentages}
        session["result"] = result_data

    winner = result_data["winner"]
    career = CAREER_PATHS[winner]
    percentages = result_data["percentages"]
    all_paths = CAREER_PATHS

    return render_template(
        "result.html",
        career=career,
        percentages=percentages,
        all_paths=all_paths
    )


@app.route("/detail/<path_id>")
def detail(path_id):
    if path_id not in CAREER_PATHS:
        return redirect(url_for("index"))
    career = CAREER_PATHS[path_id]
    other_paths = {k: v for k, v in CAREER_PATHS.items() if k != path_id}
    return render_template("detail.html", career=career, other_paths=other_paths)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
