import streamlit as st
import time
from openai import OpenAI

# ==================================================
# CONFIG / CONSTANTS
# ==================================================

MODEL = "arcee-ai/trinity-large-preview:free"

QUESTIONS = [
    {"q": "สารใดในบุหรี่ที่เป็นสาเหตุหลักของการเสพติด?", "c": ["a) นิโคติน", "b) คาเฟอีน", "c) กลูโคส", "d) คลอโรฟิลล์"], "a": "a"},
    {"q": "การสูบบุหรี่เพิ่มความเสี่ยงต่อโรคใดมากที่สุด?", "c": ["a) โรคกระดูกหัก", "b) โรคมะเร็งปอด", "c) โรคสายตาสั้น", "d) โรคหูชั้นนอกอักเสบ"], "a": "b"},
    {"q": "ควันบุหรี่มือสองส่งผลต่อคนรอบข้างอย่างไร?", "c": ["a) ทำให้สุขภาพดีขึ้น", "b) ไม่มีผลใดๆ", "c) เพิ่มความเสี่ยงโรคทางเดินหายใจ", "d) ช่วยให้หลับสบาย"], "a": "c"},
    {"q": "สารทาร์ในบุหรี่มีผลต่อร่างกายส่วนใดมากที่สุด?", "c": ["a) เล็บ", "b) ผม", "c) กระดูก", "d) ปอด"], "a": "d"},
    {"q": "การสูบบุหรี่มีผลต่อหัวใจอย่างไร?", "c": ["a) ช่วยให้หัวใจแข็งแรง", "b) เพิ่มความเสี่ยงโรคหัวใจ", "c) ทำให้หัวใจเต้นช้าลงเสมอ", "d) ไม่มีผลต่อหัวใจ"], "a": "b"},
    {"q": "หญิงตั้งครรภ์ที่สูบบุหรี่มีความเสี่ยงต่อทารกอย่างไร?", "c": ["a) ทารกตัวใหญ่ผิดปกติ", "b) ไม่มีผลต่อทารก", "c) ทารกน้ำหนักน้อย", "d) ทารกมีภูมิคุ้มกันสูง"], "a": "c"},
    {"q": "สารคาร์บอนมอนอกไซด์ในควันบุหรี่มีผลอย่างไร?", "c": ["a) เพิ่มออกซิเจนในเลือด", "b) ลดการลำเลียงออกซิเจน", "c) เพิ่มวิตามินในเลือด", "d) ทำให้เลือดแข็งตัวเร็ว"], "a": "b"},
    {"q": "การสูบบุหรี่มีผลต่อผิวหนังอย่างไร?", "c": ["a) ทำให้ผิวแก่เร็ว", "b) ทำให้ผิวชุ่มชื้น", "c) ทำให้ผิวขาวทันที", "d) ทำให้ผิวหนาขึ้น"], "a": "a"},
    {"q": "โรคใดเกี่ยวข้องกับการสูบบุหรี่โดยตรง?", "c": ["a) ไส้ติ่งอักเสบ", "b) นิ้วล็อก", "c) ถุงลมโป่งพอง", "d) ต้อกระจกจากอุบัติเหตุ"], "a": "c"},
    {"q": "ประโยชน์ของการเลิกสูบบุหรี่คืออะไร?", "c": ["a) ทำให้ติดบุหรี่มากขึ้น", "b) ทำให้ปอดอ่อนแอ", "c) ไม่มีผลต่อสุขภาพ", "d) ลดความเสี่ยงโรคหลายชนิด"], "a": "d"}
]

# ==================================================
# CLIENT INIT
# ==================================================

client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1",
)

# ----------------------------
# App Config
# ----------------------------
st.set_page_config(
    page_title="ทดสอบความรู้ของคุณหน่อย",
    page_icon=r"icon.png",
)

st.logo(r"icon.png")

def check_answer():
    correct_answers = [q["a"] for q in QUESTIONS]
    user_answers = [a[0] for a in st.session_state.test_answers]

    if len(correct_answers) != len(user_answers) and len(correct_answers) == 10 and len(user_answers) == 10:
        print("Both do not have 10 answers")
        print(f"Correct answers count: {correct_answers}")
        print(f"User answers count: {user_answers}")
        raise KeyError

    score = sum([1 for i in range(len(correct_answers)) if user_answers[i] == correct_answers[i]])

    return score

def feedback_message(score: int) -> str:
    if score < 0 or score > 10:
        return "คะแนนต้องอยู่ระหว่าง 0 ถึง 10 เท่านั้นนะ"

    messages = {
        0: "ยังไม่ได้เลยนะ ระวังไว้ ความไม่รู้เรื่องโทษบุหรี่อาจทำให้พลาดตัดสินใจผิดได้ ลองศึกษาใหม่อีกครั้ง",
        1: "คะแนนยังต่ำอยู่ ความเข้าใจเรื่องอันตรายบุหรี่สำคัญมาก เพราะมันส่งผลต่อชีวิตจริง",
        2: "ยังต้องพัฒนาอีกเยอะนะ บุหรี่ไม่ได้อันตรายเล่นๆ การรู้ทันช่วยป้องกันตัวเองได้",
        3: "เริ่มรู้บ้างแล้ว แต่ยังไม่พอ ความเข้าใจเรื่องโทษบุหรี่ช่วยให้เราหลีกเลี่ยงความเสี่ยงได้",
        4: "เกือบครึ่งทางแล้ว เพิ่มความรู้เรื่องพิษภัยบุหรี่อีกนิด จะยิ่งปลอดภัยกับสุขภาพ",
        5: "ครึ่งทางพอดี ความรู้เรื่องโทษบุหรี่ระดับนี้ถือว่าโอเค แต่ยังเพิ่มได้อีก",
        6: "ดีขึ้นมาก ความเข้าใจแบบนี้ช่วยให้ตัดสินใจไม่เข้าใกล้บุหรี่ได้",
        7: "เก่งมาก ความรู้ระดับนี้แสดงว่ารู้ทันอันตรายของบุหรี่แล้ว",
        8: "ยอดเยี่ยม เข้าใจโทษบุหรี่ชัดเจนแบบนี้ โอกาสพลาดไปลองมีน้อยมาก",
        9: "เก่งสุดๆ ความรู้แน่นขนาดนี้ พร้อมเตือนคนอื่นเรื่องอันตรายบุหรี่ได้เลย",
        10: "สมบูรณ์แบบ! คุณเข้าใจโทษบุหรี่อย่างแท้จริง แบบนี้สุขภาพระยะยาวปลอดภัยแน่นอน"
    }

    return messages[score]

def score_color(score: int) -> str:
    if score in (0, 1):
        color = "gray"
    elif score <= 3:
        color = "red"
    elif score == 4:
        color = "orange"
    elif score == 5:
        color = "yellow"
    elif score == 6:
        color = "green"
    elif score == 7:
        color = "blue"
    elif score == 8:
        color = "violet"
    elif score in (9, 10):
        color = "rainbow"
    else:
        raise ValueError("score must be between 0 and 10")

    return f":{color}["

def score_gif(score: int) -> str:
    if score < 0 or score > 10:
        raise ValueError("score must be between 0 and 10")

    if score <= 4:
        return "https://media1.tenor.com/m/zkBl3Bx3RYkAAAAC/yellowsad.gif"
    elif score <= 6:
        return "https://media1.tenor.com/m/1F0IiaZR5ckAAAAd/edp-i-mean-its-all-right.gif"
    elif score <= 8:
        return "https://media1.tenor.com/m/8Cl-QhmKqzMAAAAC/spinniung-cool-guy.gif"
    else:  # score <= 10
        return "https://media1.tenor.com/m/si86CrSOUZIAAAAd/horrified-funny.gif"

def test_exam():
    st.markdown("## นี้คือแบบทดสอบความรู้!!")
    st.markdown("คุณรู้เกี่ยวกับบุหรี่และโทษของมันขนาดไหน?!!? มาลองทดสอบความรู้ของคุณกัน")
    for i, q in enumerate(QUESTIONS):
        st.radio(f"{i}. {q["q"]}", q["c"], horizontal=True, key=f"testq{i}")

    if st.button("บันทึก"):
        st.session_state.test_answers = [st.session_state[f"testq{i}"] for i, _ in enumerate(QUESTIONS)]
        
        st.session_state.test_stage = 2
        
        st.rerun()

def after_test():
    score = check_answer()
    st.markdown("## คุณได้คะแนน!!", text_alignment="center")
    st.markdown(f"# {score_color(score)}{score} คะแนน]", text_alignment="center")
    st.markdown(f"{feedback_message(score)}", text_alignment="center")

    st.image(score_gif(score), use_container_width=True)

    if st.button("ทำใหม่"):
        st.session_state.test_stage = 1
        st.rerun()


if st.session_state.test_stage == 1:
    test_exam()
elif st.session_state.test_stage == 2:

    after_test()
