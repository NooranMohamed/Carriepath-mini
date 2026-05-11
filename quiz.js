/* =============================================
   CareerPath Mini — Quiz Logic
   ============================================= */

let currentQuestion = 0;
let answers = [];

// تهيئة عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', () => {
    if (!document.querySelector('.quiz-section')) return;

    answers = new Array(TOTAL_QUESTIONS).fill(null);
    updateUI();
});

/**
 * اختيار إجابة
 * @param {number} qIndex - رقم السؤال (0-based)
 * @param {number} aIndex - رقم الخيار (0-based)
 */
function selectAnswer(qIndex, aIndex) {
    // حفظ الإجابة
    answers[currentQuestion] = aIndex;

    // تحديث الواجهة البصرية
    const slide = document.getElementById(`q${currentQuestion + 1}`);
    slide.querySelectorAll('.option-btn').forEach((btn, i) => {
        btn.classList.toggle('selected', i === aIndex);
    });

    // تفعيل زر التالي
    const nextBtn = document.getElementById('nextBtn');
    nextBtn.disabled = false;

    // الانتقال التلقائي بعد 400ms
    setTimeout(() => {
        if (currentQuestion < TOTAL_QUESTIONS - 1) {
            nextQuestion();
        } else {
            submitQuiz();
        }
    }, 450);
}

/**
 * الانتقال للسؤال التالي
 */
function nextQuestion() {
    if (answers[currentQuestion] === null) return;
    if (currentQuestion >= TOTAL_QUESTIONS - 1) {
        submitQuiz();
        return;
    }

    // تأثير الخروج
    const currentSlide = document.getElementById(`q${currentQuestion + 1}`);
    currentSlide.style.animation = 'slideOut 0.3s ease forwards';

    setTimeout(() => {
        currentSlide.classList.remove('active');
        currentSlide.style.animation = '';
        currentQuestion++;

        const nextSlide = document.getElementById(`q${currentQuestion + 1}`);
        nextSlide.classList.add('active');
        nextSlide.style.animation = 'slideIn 0.35s cubic-bezier(0.4,0,0.2,1)';

        updateUI();
    }, 280);
}

/**
 * العودة للسؤال السابق
 */
function prevQuestion() {
    if (currentQuestion === 0) return;

    const currentSlide = document.getElementById(`q${currentQuestion + 1}`);
    currentSlide.style.animation = 'slideOutReverse 0.3s ease forwards';

    setTimeout(() => {
        currentSlide.classList.remove('active');
        currentSlide.style.animation = '';
        currentQuestion--;

        const prevSlide = document.getElementById(`q${currentQuestion + 1}`);
        prevSlide.classList.add('active');
        prevSlide.style.animation = 'slideInReverse 0.35s cubic-bezier(0.4,0,0.2,1)';

        updateUI();
    }, 280);
}

/**
 * تحديث واجهة المستخدم
 */
function updateUI() {
    // عداد الأسئلة
    document.getElementById('currentQ').textContent = currentQuestion + 1;

    // شريط التقدم
    const progress = Math.round((currentQuestion / TOTAL_QUESTIONS) * 100);
    document.getElementById('progressBar').style.width = progress + '%';
    document.getElementById('progressPercent').textContent = progress + '%';

    // زر الرجوع
    const backBtn = document.getElementById('backBtn');
    if (backBtn) {
        backBtn.style.display = currentQuestion > 0 ? 'flex' : 'none';
    }

    // زر التالي
    const nextBtn = document.getElementById('nextBtn');
    if (nextBtn) {
        const isAnswered = answers[currentQuestion] !== null;
        nextBtn.disabled = !isAnswered;

        if (currentQuestion === TOTAL_QUESTIONS - 1) {
            nextBtn.innerHTML = `إرسال النتيجة <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>`;
        } else {
            nextBtn.innerHTML = `التالي <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>`;
        }
    }

    // استعادة الإجابة المختارة مسبقاً إن وجدت
    const savedAnswer = answers[currentQuestion];
    if (savedAnswer !== null) {
        const slide = document.getElementById(`q${currentQuestion + 1}`);
        if (slide) {
            slide.querySelectorAll('.option-btn').forEach((btn, i) => {
                btn.classList.toggle('selected', i === savedAnswer);
            });
        }
        if (nextBtn) nextBtn.disabled = false;
    } else {
        const slide = document.getElementById(`q${currentQuestion + 1}`);
        if (slide) {
            slide.querySelectorAll('.option-btn').forEach(btn => {
                btn.classList.remove('selected');
            });
        }
        if (nextBtn) nextBtn.disabled = true;
    }
}

/**
 * إرسال الاختبار
 */
async function submitQuiz() {
    // تأكد أن كل الأسئلة أُجيب عليها
    const unanswered = answers.filter(a => a === null);
    if (unanswered.length > 0) {
        alert('من فضلك أجب على جميع الأسئلة');
        return;
    }

    // عرض مؤشر التحميل
    const nextBtn = document.getElementById('nextBtn');
    if (nextBtn) {
        nextBtn.disabled = true;
        nextBtn.innerHTML = `<span style="opacity:0.7">جاري التحليل...</span>`;
    }

    try {
        const response = await fetch('/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ answers: answers })
        });

        const data = await response.json();
        if (data.redirect) {
            window.location.href = data.redirect;
        }
    } catch (err) {
        console.error('Submit error:', err);
        // Fallback - استخدام الفورم التقليدي
        const form = document.getElementById('submitForm');
        if (form) {
            document.getElementById('answersInput').value = JSON.stringify(answers);
            form.submit();
        }
    }
}

/* =============================================
   Animations CSS-in-JS fallback
   ============================================= */
const extraStyles = document.createElement('style');
extraStyles.textContent = `
    @keyframes slideOutReverse {
        from { opacity: 1; transform: translateX(0); }
        to { opacity: 0; transform: translateX(-30px); }
    }
    @keyframes slideInReverse {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }
`;
document.head.appendChild(extraStyles);
