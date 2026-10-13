import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="헷갈리는 맞춤법 대화 학습기",
    page_icon="💬",
    layout="centered"
)

# -----------------------------------------------------------------------------
# 1. 커스텀 CSS (카카오톡 스타일 대화창 & 모바일 뷰 연출)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* 전체 배경색 */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* 채팅 컨테이너 스타일 */
    .chat-container {
        background-color: #bacee0;
        padding: 20px;
        border-radius: 15px;
        max-width: 450px;
        margin: 0 auto 20px auto;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    }
    
    /* 상대방 말풍선 */
    .chat-bubble-left {
        background-color: #ffffff;
        color: #333333;
        padding: 10px 14px;
        border-radius: 12px;
        border-top-left-radius: 2px;
        margin-bottom: 12px;
        max-width: 80%;
        display: inline-block;
        font-size: 15px;
        line-height: 1.4;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    /* 나(유저) 말풍선 */
    .chat-bubble-right {
        background-color: #ffe812;
        color: #333333;
        padding: 10px 14px;
        border-radius: 12px;
        border-top-right-radius: 2px;
        margin-bottom: 12px;
        max-width: 80%;
        float: right;
        clear: both;
        font-size: 15px;
        line-height: 1.4;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }

    /* 피드백 카드 스타일 */
    .feedback-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 18px;
        border-left: 5px solid #ff4b4b;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-top: 15px;
    }

    .correct-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 18px;
        border-left: 5px solid #28a745;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-top: 15px;
    }

    .visual-box {
        background-color: #f1f3f5;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        font-size: 40px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 데이터 세트 (대화 상황 + 비주얼 어휘 정보)
# -----------------------------------------------------------------------------
QUIZ_DATA = [
    {
        "id": 1,
        "title": "우체국과 부침개 (부치다 vs 붙이다)",
        "dialogue": [
            {"sender": "friend", "text": "야, 나 방금 우체국 다녀오는 길이야!"},
            {"sender": "friend", "text": "고향 집에 어머니 드실 명절 선물을 [ANSWER] 왔어."}
        ],
        "options": ["부치고", "붙이고"],
        "correct": "부치고",
        "wrong_reaction": "응? 봉투에 우표나 스티커를 붙이고 왔다는 거야, 아니면 짐을 택배로 보냈다는 거야?",
        "card": {
            "correct_word": "부치다",
            "correct_icon": "📮",
            "correct_meaning": "편지, 물품 따위를 보내다 / 기름을 둘러 구워내다",
            "correct_example": "• 고향에 편지를 부치다.\n• 안건을 회의에 부치다.\n• 전을 부치다.",
            
            "wrong_word": "붙이다",
            "wrong_icon": "🏷️",
            "wrong_meaning": "맞닿아 떨어지지 않게 하다 / 불을 일으키다",
            "wrong_example": "• 봉투에 우표를 붙이다.\n• 가구에 불을 붙이다."
        }
    },
    {
        "id": 2,
        "title": "저녁 약속 잡기 (되 vs 돼)",
        "dialogue": [
            {"sender": "friend", "text": "오늘 저녁에 갑자기 야근 취소됐다!"},
            {"sender": "friend", "text": "혹시 오늘 7시에 시간 [ANSWER]?"}
        ],
        "options": ["되", "돼"],
        "correct": "돼",
        "wrong_reaction": "'시간 하?'라고 말하면 어색하지 않아? '해'를 넣어야 자연스러워!",
        "card": {
            "correct_word": "돼 ('되어'의 줄임말)",
            "correct_icon": "🆗",
            "correct_meaning": "'해'를 넣었을 때 자연스러운 문장에는 '돼'",
            "correct_example": "• 시간 돼? (시간 해? ⭕)\n• 이제 가도 돼. (가도 해 ⭕)",
            
            "wrong_word": "되 (어간)",
            "wrong_icon": "🛑",
            "wrong_meaning": "'하'를 넣었을 때 자연스러운 문장에는 '되'",
            "wrong_example": "• 안 되나요? (안 하나요? ⭕)\n• 되어서 -> 돼서"
        }
    },
    {
        "id": 3,
        "title": "황당한 상황 연출 (어이없다 vs 어의없다)",
        "dialogue": [
            {"sender": "friend", "text": "아 아침부터 지하철 반대로 타서 지각했어..."},
            {"sender": "friend", "text": "진짜 너무 [ANSWER]..."}
        ],
        "options": ["어이없다", "어의없다"],
        "correct": "어이없다",
        "wrong_reaction": "조선시대 임금님 담당 의사(어의)가 집으로 가버렸다는 뜻이야...?",
        "card": {
            "correct_word": "어이없다",
            "correct_icon": "🤦",
            "correct_meaning": "너무 뜻밖이거나 황당해서 기가 막히다",
            "correct_example": "• 어이없는 실수를 저질렀다.\n• 하는 행동이 너무 어이가 없다.",
            
            "wrong_word": "어의 (御醫)",
            "wrong_icon": "👨‍⚕️",
            "wrong_meaning": "궁궐에서 임금이나 왕족의 병을 치료하던 의원",
            "wrong_example": "• 어의, 전하의 옥체를 보살피거라!"
        }
    }
]

# -----------------------------------------------------------------------------
# 3. 세션 상태 관리
# -----------------------------------------------------------------------------
if 'current_idx' not in st.session_state:
    st.session_state.current_idx = 0
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = None
if 'score' not in st.session_state:
    st.session_state.score = 0

current_quiz = QUIZ_DATA[st.session_state.current_idx]

# -----------------------------------------------------------------------------
# 4. 앱 헤더 및 진행도
# -----------------------------------------------------------------------------
st.title("💬 상황극 맞춤법 학습기")
st.caption("대화 속에서 헷갈리는 어휘를 찾아내고, 시각적 비교 카드로 학습해보세요.")

progress = (st.session_state.current_idx + 1) / len(QUIZ_DATA)
st.progress(progress)
st.write(f"**문제 {st.session_state.current_idx + 1} / {len(QUIZ_DATA)}:** {current_quiz['title']}")

# -----------------------------------------------------------------------------
# 5. 카카오톡 스타일 대화창 화면 구현
# -----------------------------------------------------------------------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in current_quiz["dialogue"]:
    if msg["sender"] == "friend":
        # 빈칸([ANSWER])이 포함된 문장 처리
        text = msg["text"]
        if "[ANSWER]" in text:
            if st.session_state.selected_option is None:
                display_text = text.replace("[ANSWER]", "<b>[ ??? ]</b>")
            else:
                display_text = text.replace("[ANSWER]", f"<b><u>{st.session_state.selected_option}</u></b>")
        else:
            display_text = text
            
        st.markdown(f'<div class="chat-bubble-left">👤 친구<br>{display_text}</div><div style="clear:both;"></div>', unsafe_allow_html=True)

# 사용자가 선택했을 때 유저 말풍선 표시
if st.session_state.selected_option is not None:
    st.markdown(f'<div class="chat-bubble-right">{st.session_state.selected_option}!</div><div style="clear:both;"></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. 선택지 버튼 UI
# -----------------------------------------------------------------------------
if st.session_state.selected_option is None:
    st.subheader("💡 알맞은 어휘를 선택하세요")
    col1, col2 = st.columns(2)
    
    for i, opt in enumerate(current_quiz["options"]):
        col = col1 if i == 0 else col2
        if col.button(opt, use_container_width=True, key=f"btn_{opt}"):
            st.session_state.selected_option = opt
            st.rerun()

# -----------------------------------------------------------------------------
# 7. 피드백 & 비주얼 카드 영역 (틀렸거나 맞았을 때)
# -----------------------------------------------------------------------------
if st.session_state.selected_option is not None:
    is_correct = (st.session_state.selected_option == current_quiz["correct"])
    card_data = current_quiz["card"]

    if is_correct:
        st.success("🎉 정답입니다! 정확한 표현이에요.")
        st.markdown(f"""
        <div class="correct-card">
            <h3>⭕ {card_data['correct_word']}</h3>
            <div class="visual-box">{card_data['correct_icon']}</div>
            <p><b>뜻:</b> {card_data['correct_meaning']}</p>
            <p><b>예문:</b><br>{card_data['correct_example'].replace('\n', '<br>')}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error(f"❌ 오답입니다!")
        
        # 친구의 황당하다는 반응 연출
        st.warning(f"🗣️ **친구 반응:** \"{current_quiz['wrong_reaction']}\"")
        
        # 올바른 표현 vs 내가 틀린 표현 비교 비주얼 카드
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown(f"""
            <div class="correct-card">
                <h4>⭕ 올바른 표현: {card_data['correct_word']}</h4>
                <div class="visual-box">{card_data['correct_icon']}</div>
                <p><b>뜻:</b> {card_data['correct_meaning']}</p>
                <p><b>예문:</b><br>{card_data['correct_example'].replace('\n', '<br>')}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col_b:
            st.markdown(f"""
            <div class="feedback-card">
                <h4>❌ 틀린 표현: {card_data['wrong_word']}</h4>
                <div class="visual-box">{card_data['wrong_icon']}</div>
                <p><b>뜻:</b> {card_data['wrong_meaning']}</p>
                <p><b>예문:</b><br>{card_data['wrong_example'].replace('\n', '<br>')}</p>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    # 다음 문제로 넘어가기 버튼
    if st.session_state.current_idx < len(QUIZ_DATA) - 1:
        if st.button("다음 문제 풀기 ➡️", type="primary", use_container_width=True):
            st.session_state.current_idx += 1
            st.session_state.selected_option = None
            st.rerun()
    else:
        st.balloons()
        st.success("🏆 모든 대화 학습 문제를 완료했습니다!")
        if st.button("처음부터 다시 학습하기 🔄", use_container_width=True):
            st.session_state.current_idx = 0
            st.session_state.selected_option = None
            st.rerun()