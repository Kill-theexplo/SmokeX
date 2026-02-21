import streamlit as st
import time
from openai import OpenAI

# ==================================================
# CONFIG / CONSTANTS
# ==================================================

MODEL = "arcee-ai/trinity-large-preview:free"

QUESTIONS = [
    "หลังตื่นนอนตอนเช้า คุณต้องสูบบุหรี่ภายใน 30 นาทีแรกหรือไม่?",
    "คุณรู้สึกหงุดหงิด กระวนกระวาย หรือไม่มีสมาธิเมื่อไม่ได้สูบบุหรี่เป็นเวลานานหรือไม่?",
    "คุณเคยพยายามจะเลิกหรือลดการสูบบุหรี่/บุหรี่ไฟฟ้าแล้ว แต่ทำไม่สำเร็จหรือไม่?",
    "คุณแอบสูบบุหรี่ในสถานที่ที่กฎหมายหรือโรงเรียนสั่งห้ามหรือไม่?",
    "ในหนึ่งวัน คุณสูบบุหรี่เกิน 5 มวนหรือไม่?",
    "คุณรู้สึกว่าต้องสูบมากขึ้นเพื่อให้รู้สึกพอใจเท่าเดิมหรือไม่?",
    "คุณเคยทิ้งกิจกรรมสำคัญเพื่อออกไปสูบบุหรี่หรือไม่?",
    "แม้ในช่วงที่เจ็บป่วย คุณก็ยังฝืนสูบบุหรี่อยู่หรือไม่?",
    "คุณรู้สึกกังวลเมื่อต้องอยู่ในที่ที่สูบบุหรี่ไม่ได้หรือไม่?",
    "คุณใช้การสูบบุหรี่เป็นวิธีหลักในการจัดการความเครียดหรือไม่?"
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
    page_title="ระดับสุขภาพ",
    page_icon=r"C:\Users\Lenovo\Desktop\AI\icon.png",
)

st.logo(r"C:\Users\Lenovo\Desktop\AI\icon.png")

# ----------------------------
# Title
# ----------------------------


# ----------------------------
# SETUP
# ----------------------------

# ----------------------------
# Survey
# ----------------------------

def predict_future(answers):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system","content": "You will get a survey result from a user about their smoking \
                   habits, your job is to ONLY predict what would happen to their body and their mental health \
                   if they continue these habits. You must answer in ONLY Thai, No english, no spanish, no other \
                   languages, just Thai. You must speak in casual tone, friendly enough to get teenagers to be interested in you. \
                    Maybe put a little joke that's not offensive and hurt feelings. A funny joke that's real and relatable, helping them.\
                    Your respond will be short but effective. 1-2 lines but covers all of things they should know. Focus on what they do\
                    and what they dont and use those as bullet points. If they dont do all smoking habits, say they are fine and also give them some advice to become even healtier."},
                {"role": "user", "content": answers}],
    )
    return response.choices[0].message.content

def summarize_answers():
    total_answer = ''
    for q, a in st.session_state.answers.items():
        total_answer += q
        total_answer += f'\nUser answer: {a}\n\n'
    
    st.session_state.total_answer = total_answer

def analyze_answers():
    score = sum(st.session_state.answers.values())

    if score >= 7:
        return (
            "<div style='text-align:center;'><span style='font-size:20px; font-weight:600; color:red;'>ช่วงที่ร่างกายต้องการการดูแลเป็นพิเศษ</span></div>",
            "ช่วงนี้ดูเหมือนร่างกายคุณจะเริ่มชินกับนิโคตินมากเกินไปแล้วนะ ไม่ต้องตกใจไปครับ หลายคนก็เคยผ่านจุดนี้มาได้ ลองหาใครสักคนที่ไว้ใจคุยด้วย หรือปรึกษาพี่ๆ สายด่วน 1600 ดูไหม? พวกเขาใจดีและพร้อมช่วยให้คุณกลับมาสดชื่นเหมือนเดิมนะ",
        )
    elif score >= 4:
        return (
            "<div style='text-align:center;'><span style='font-size:26px; font-weight:600; color:orange;'>ช่วงที่ต้องฟังเสียงร่างกาย</span></div>",
            "คุณเริ่มมีความผูกพันกับมันบ้างแล้วนะเนี่ย ลองสังเกตดูว่าเราใช้มันเพื่อแก้เครียดหรือเปล่า? ลองเปลี่ยนมาดื่มน้ำเย็นๆ หรือฟังเพลงที่ชอบดูไหม ร่างกายคุณเก่งอยู่แล้ว คุณจัดการมันได้แน่นอนก่อนที่มันจะคุมเรานะ",
        )
    elif score >= 1:
        return (
            "<div style='text-align:center;'><span style='font-size:26px; font-weight:600; color:yellow;'>ช่วงเริ่มต้น</span></div>",
            "ดูเหมือนคุณแค่กำลังอยากรู้อยากลองหรือทำตามกระแสเฉยๆ นะ ซึ่งเป็นเรื่องปกติของวัยเรา แต่เชื่อเถอะว่าไลฟ์สไตล์แบบเท่ๆ โดยไม่ต้องพึ่งควันมันดูคูลกว่าเยอะเลย รีบถอยออกมาตอนนี้ง่ายที่สุดครับ",
        )
    else:
        return (
            "<div style='text-align:center;'><span style='font-size:26px; font-weight:600; color:green;'>ช่วงสุขภาพดีเยี่ยม</span></div>",
            "สุดยอดไปเลย! คุณดูแลตัวเองได้ดีมาก ปอดและสมองของคุณกำลังขอบคุณที่คุณเลือกสิ่งดีๆ ให้เขา รักษาความเจ๋งแบบนี้ไว้นะครับ",
        )


def survey_dialog():
    print(f"survey {st.session_state.dialog_stage}")
    st.markdown("## ระดับสุขภาพของคุณ")
    st.markdown("คุณอยู่ในช่วงไหนของการเสพติดบุหรี่ ให้เราช่วยวิเคราะห์คุณจากคำถาม 10 ข้อนี้")
    for i, q in enumerate(QUESTIONS):
        st.radio(q, ["ใช่", "ไม่"], horizontal=True, key=f"q{i}")

    if st.button("บันทึก"):
        st.session_state.answers = {
            q: (st.session_state[f"q{i}"] == "ใช่")
            for i, q in enumerate(QUESTIONS)
        }
        summarize_answers()
        st.session_state.dialog_stage = 2
        print(f"after answer {st.session_state.dialog_stage}")
        st.rerun()

def result_dialog():
    status, _ = analyze_answers()
    st.write("จากผลการประเมินเบื้องต้น พบว่า คุณอยู่ใน")
    st.markdown(status, unsafe_allow_html=True)
    st.write("\n")
    if "ช่วงสุขภาพดีเยี่ยม" not in status:
        st.image(
            "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExdDd6eXZhd20zYmM1MWZjeHc2dWQ5a2RtenlrMW44cHNvZWRwY21nYiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/RBvQaFrHtau1psibrg/giphy.gif",
            use_container_width=True
        )
    else:
        st.image(
            "https://media1.tenor.com/m/6vjzHxepwDkAAAAd/pout-kiss.gif",
            use_container_width=True
        )
    st.write("\n")
    with st.spinner("..."):
        st.markdown(f"{predict_future(st.session_state.total_answer)}")

    if st.button("ทำแบบสำรวจใหม่"):
        st.session_state.dialog_stage = 1
        print(st.session_state.dialog_stage)
        st.rerun()


if st.session_state.dialog_stage == 1:
    survey_dialog()
elif st.session_state.dialog_stage == 2:
    result_dialog()