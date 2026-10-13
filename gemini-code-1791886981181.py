import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="헷갈리는 맞춤법 대화 학습기",
    page_icon="💬",
    layout="centered"
)

# -----------------------------------------------------------------------------
# 1. 커스텀 CSS (모든 글자색을 진하고 선명하게 고정)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* 전체 배경 설정 및 기본 글자 진하게 */
    .stApp {
        background-color: #f4f6f8;
    }

    /* 모든 텍스트 요소의 색상을 선명한 검은색으로 강제 고정 */
    html, body, [class*="css"], h1, h2, h3, h4, h5, h6, p, span, li, label, div {
        color: #111111 !important;
        font-weight: 500;
    }

    /* 채팅 컨테이너 (카카오톡 배경) */
    .chat-container {
        background-color: #a3c2e0;
        padding: 20px;
        border-radius: 16px;
        max-width: 480px;
        margin: 0 auto 20px auto;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.12);
    }
    
    /* 상대방 말풍선 */
    .chat-bubble-left {
        background-color: #ffffff;
        color: #111111 !important;
        padding: 12px 16px;
        border-radius: 14px;
        border-top-left-radius: 2px;
        margin-bottom: 14px;
        max-width: 85%;
        display: inline-block;
        font-size: 16px;
        line-height: 1.5;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }
    
    /* 나(유저) 말풍선 */
    .chat-bubble-right {
        background-color: #ffe600;
        color: #111111 !important;
        padding: 12px 16px;
        border-radius: 14px;
        border-top-right-radius: 2px;
        margin-bottom: 14px;
        max-width: 85%;
        float: right;
        clear: both;
        font-size: 16px;
        line-height: 1.5;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        font-weight: bold;
    }

    /* 피드백 해설 카드 공통 스타일 */
    .card-box {
        background-color: #ffffff;
        border-radius: 14px;
        padding: 22px;
        margin-top: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #e1e4e8;
    }
    
    .correct-border {
        border-top: 6px solid #198754;
    }

    .wrong-border {
        border-top: 6px solid #dc3545;
    }

    .visual-icon {
        font-size: 52px;
        text-align: center;
        margin: 12px 0;
    }

    /* 구분 팁 강조 박스 */
    .tip-box {
        background-color: #fff9db;
        border-left: 5px solid #fcc419;
        padding: 14px 16px;
        border-radius: 8px;
        margin: 14px 0;
        font-size: 15px;
        line-height: 1.6;
        color: #212529 !important;
    }

    /* 예문 리스트 글자 진하게 */
    .example-list li {
        color: #222222 !important;
        font-size: 15px;
        margin-bottom: 6px;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 검수 완료된 데이터 세트 (지문-선택지-해설 1:1 완벽 일치)
# -----------------------------------------------------------------------------
QUIZ_DATA = [
    {
        "id": 1,
        "title": "우체국 택배와 부침개 (부치다 vs 붙이다)",
        "dialogue": [
            {"sender": "friend", "text": "야, 나 방금 우체국 다녀오는 길이야!"},
            {"sender": "friend", "text": "고향 집에 계신 부모님께 명절 선물 상자를 [ANSWER] 왔지."}
        ],
        "options": ["부치고", "붙이고"],
        "correct": "부치고",
        "wrong_reaction": "응? 상자에 우표나 접착 테이프를 붙이고 왔다는 뜻이야, 아니면 택배로 보냈다는 뜻이야?",
        "card": {
            "correct_word": "부치다 (선택지: 부치고)",
            "correct_icon": "📮",
            "correct_meaning": "편지, 물품, 안건 등을 다른 곳으로 보내거나 넘기다.",
            "correct_tip": "💡 <b>구분 팁:</b> '보내다'의 의미가 있으면 무조건 <b>'부치다'</b>입니다. (풀/접착제 사용 ❌)",
            "correct_desc": """
            <b>'부치다'</b>는 소유나 공간을 이동시키는 행위에 쓰입니다.<br>
            우체국이나 택배를 통해 물건을 다른 곳으로 '보낼 때'는 접착제로 붙이는 것이 아니므로 <b>'부치다'</b>가 올바릅니다.<br>
            또한 '회의 안건에 부치다', '명절 전을 부치다', '힘에 부치다'에도 쓰입니다.
            """,
            "correct_examples": [
                "고향 집에 명절 선물 상자를 <b>부치고</b> 왔다.",
                "편지를 우체통에 <b>부치러</b> 가는 길이다.",
                "오늘 안건을 무기명 투표에 <b>부치기로</b> 했습니다.",
                "명절이라 하루 종일 노릇하게 전을 <b>부쳤다</b>."
            ],
            
            "wrong_word": "붙이다 (선택지: 붙이고)",
            "wrong_icon": "🏷️",
            "wrong_meaning": "맞닿아 떨어지지 않게 접착하거나, 불/조건/이름 등을 더하다.",
            "wrong_tip": "💡 <b>구분 팁:</b> 풀, 테이프, 접착제 등으로 <b>'착 맞닿게 접착하는 동작'</b>일 때만 <b>'붙이다'</b>입니다.",
            "wrong_desc": """
            <b>'붙이다'</b>는 '붙다'의 사동사로, 물리적으로 두 물체를 접착시킬 때 씁니다.<br>
            우체국에서 '상자에 우표를 붙이다'나 '송장을 붙이다'는 맞지만, 선물 상자 자체를 보낼 때는 <b>'부치다'</b>를 써야 합니다.
            """,
            "wrong_examples": [
                "선물 상자 겉면에 택배 송장을 <b>붙이고</b> 왔다.",
                "벽에 메모지를 풀로 <b>붙여</b> 두었다.",
                "캠핑장에 도착하자마자 장작에 불을 <b>붙였다</b>.",
                "강아지에게 귀여운 이름을 <b>붙여</b> 주었다."
            ]
        }
    },
    {
        "id": 2,
        "title": "저녁 약속 시간 정하기 (되 vs 돼)",
        "dialogue": [
            {"sender": "friend", "text": "오늘 저녁에 갑자기 야근 취소됐다!"},
            {"sender": "friend", "text": "혹시 오늘 7시에 만나도 [ANSWER]?"}
        ],
        "options": ["돼", "되"],
        "correct": "돼",
        "wrong_reaction": "'만나도 하?'라고 말하면 어색하지 않아? '해'를 넣어서 '만나도 해(돼)'가 자연스러워!",
        "card": {
            "correct_word": "돼 ('되어'의 줄임말)",
            "correct_icon": "🆗",
            "correct_meaning": "'되-'라는 어간에 어미 '-어'가 결합한 '되어'의 축약 표현.",
            "correct_tip": "💡 <b>[하 / 해 대입 공식]:</b> 문장에 <b>'해'</b>를 넣었을 때 말이 자연스러우면 <b>'돼'</b>가 맞습니다.<br>👉 만나도 <b>해</b>? ➔ 만나도 <b>돼</b>? (자연스러움 ⭕)",
            "correct_desc": """
            어간 '되-'는 홀로 쓰일 수 없으며 반드시 어미가 붙어야 합니다.<br>
            문장의 맨 끝에 올 때는 어미 '-어'와 합쳐진 <b>'되어(돼)'</b> 형태로 써야 합니다.<br>
            "안 돼!", "가도 돼?", "퇴근해도 돼" 모두 문장의 끝이므로 <b>'돼'</b>가 올바른 표기입니다.
            """,
            "correct_examples": [
                "오늘 저녁 7시에 만나도 <b>돼</b>?",
                "지금 약속 장소로 가도 <b>돼</b>.",
                "그렇게 행동하면 절대로 안 <b>돼</b>!"
            ],
            
            "wrong_word": "되 (어간 단독 표기)",
            "wrong_icon": "🛑",
            "wrong_meaning": "동사/형용사 '되다'의 어간. 단독으로는 문장 끝에 올 수 없음.",
            "wrong_tip": "💡 <b>[하 / 해 대입 공식]:</b> 문장에 <b>'하'</b>를 넣었을 때 말이 자연스러우면 <b>'되'</b>가 맞습니다.<br>👉 만나도 <b>하</b>? (어색함 ❌)",
            "wrong_desc": """
            <b>'되'</b>는 뒤에 '-고', '-니', '-면' 같은 자음 어미가 붙을 때만 사용 가능합니다.<br>
            문장 끝에 '되' 혼자 쓰이면 맞춤법에 어긋납니다.
            """,
            "wrong_examples": [
                "준비가 다 <b>되고</b> 나면 출발하자. ('하고' 자연스러움 ⭕)",
                "선생님이 <b>되면</b> 다시 찾아뵐게요. ('하면' 자연스러움 ⭕)",
                "지금 들어가도 <b>되나요</b>? ('하나 요' 자연스러움 ⭕)"
            ]
        }
    },
    {
        "id": 3,
        "title": "황당한 상황 연출 (어이없다 vs 어의없다)",
        "dialogue": [
            {"sender": "friend", "text": "아 아침부터 지하철 반대로 타서 지각했어..."},
            {"sender": "friend", "text": "바쁘게 뛰어왔는데 오늘 휴강이래. 진짜 너무 [ANSWER]..."}
        ],
        "options": ["어이없다", "어의없다"],
        "correct": "어이없다",
        "wrong_reaction": "조선시대 임금님 담당 의사(어의)가 집으로 가버렸다는 뜻이야...?",
        "card": {
            "correct_word": "어이없다 (선택지: 어이없다)",
            "correct_icon": "🤦",
            "correct_meaning": "일이 너무 뜻밖이거나 기가 막혀서 황당하다.",
            "correct_tip": "💡 <b>구분 팁:</b> '어이'는 맷돌 손잡이(어처구니)를 뜻하는 말에서 유래했습니다. 손잡이가 빠져 황당할 때 <b>'어이없다'</b>를 씁니다.",
            "correct_desc": """
            황당하거나 기가 막히는 상황을 표현할 때는 무조건 <b>'어이없다'</b> 또는 <b>'어처구니없다'</b>가 올바른 표준어입니다.<br>
            발음이 비슷하여 '어의'로 잘못 적는 경우가 많지만, 의사를 뜻하는 '어의'와는 아무 관련이 없습니다.
            """,
            "correct_examples": [
                "바쁘게 뛰어왔는데 휴강이라니 너무 <b>어이없다</b>.",
                "그런 <b>어이없는</b> 실수를 저지르다니 믿기지 않아.",
                "상대방의 <b>어이없는</b> 행동에 말문이 막혔다."
            ],
            
            "wrong_word": "어의 (御醫)",
            "wrong_icon": "👨‍⚕️",
            "wrong_meaning": "궁궐에서 임금이나 왕족의 병을 치료하던 의사.",
            "wrong_tip": "💡 <b>구분 팁:</b> 사극에 나오는 '임금님의 전담 의사'를 뜻하는 명사입니다.",
            "wrong_desc": """
            '어의'는 황당하다는 뜻의 형용사가 아니라 직업을 뜻하는 명사입니다.<br>
            따라서 '어의없다'라고 쓰면 "궁중에 의사가 없다"라는 전혀 다른 뜻이 됩니다.
            """,
            "wrong_examples": [
                "<b>어의</b>, 전하의 옥체를 정성껏 보살피거라!",
                "조선 시대 명의로 알려진 <b>어의</b> 허준."
            ]
        }
    }
]

# -----------------------------------------------------------------------------
# 3. 세션 상태 초기화 및 관리
# -----------------------------------------------------------------------------
if 'current_idx' not in st.session_state:
    st.session_state.current_idx = 0
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = None

# 현재 인덱스에 해당하는 문제 데이터 직접 참조
idx = st.session_state.current_idx
current_quiz = QUIZ_DATA[idx]

# -----------------------------------------------------------------------------
# 4. 앱 헤더 및 진행도
# -----------------------------------------------------------------------------
st.title("💬 상황극 맞춤법 학습기")
st.markdown("<b>대화 상황 속에서 올바른 어휘를 고르고, 선명한 비교 해설을 확인해보세요.</b>", unsafe_allow_html=True)

progress = (idx + 1) / len(QUIZ_DATA)
st.progress(progress)
st.markdown(f"<h4 style='color:#111111;'>문제 {idx + 1} / {len(QUIZ_DATA)} : {current_quiz['title']}</h4>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. 카카오톡 스타일 대화창 화면 (현재 인덱스 데이터로 고정)
# -----------------------------------------------------------------------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in current_quiz["dialogue"]:
    if msg["sender"] == "friend":
        text = msg["text"]
        if "[ANSWER]" in text:
            if st.session_state.selected_option is None:
                display_text = text.replace("[ANSWER]", "<b style='color:#d9480f;'>[ ??? ]</b>")
            else:
                display_text = text.replace("[ANSWER]", f"<b style='color:#0d6efd;'><u>{st.session_state.selected_option}</u></b>")
        else:
            display_text = text
            
        st.markdown(f'<div class="chat-bubble-left">👤 <b>친구</b><br>{display_text}</div><div style="clear:both;"></div>', unsafe_allow_html=True)

# 유저가 버튼을 눌렀을 때만 오른쪽 말풍선 표시
if st.session_state.selected_option is not None:
    st.markdown(f'<div class="chat-bubble-right">{st.session_state.selected_option}!</div><div style="clear:both;"></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. 선택지 버튼 영역
# -----------------------------------------------------------------------------
if st.session_state.selected_option is None:
    st.markdown("<h3>💡 알맞은 어휘를 선택하세요</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    for i, opt in enumerate(current_quiz["options"]):
        col = col1 if i == 0 else col2
        # 고유 키(key)를 현재 문제 인덱스와 함께 부여하여 이전 선택값과 충돌 방지
        if col.button(opt, use_container_width=True, key=f"q_{idx}_btn_{opt}"):
            st.session_state.selected_option = opt
            st.rerun()

# -----------------------------------------------------------------------------
# 7. 피드백 & 상세 비교 해설 카드 영역
# -----------------------------------------------------------------------------
if st.session_state.selected_option is not None:
    is_correct = (st.session_state.selected_option == current_quiz["correct"])
    card_data = current_quiz["card"]

    if is_correct:
        st.success("🎉 정답입니다! 문맥에 정확한 표현을 고르셨습니다.")
    else:
        st.error("❌ 오답입니다! 어색한 표현을 선택하셨습니다.")
        st.warning(f"🗣️ **친구 반응:** \"{current_quiz['wrong_reaction']}\"")

    st.write("---")
    st.markdown("<h3 style='color:#111111;'>📚 맞춤법 & 어휘 상세 비교 해설</h3>", unsafe_allow_html=True)

    col_correct, col_wrong = st.columns(2)
    
    # 1) 올바른 표현 카드
    with col_correct:
        ex_list_html = "".join([f"<li>{ex}</li>" for ex in card_data["correct_examples"]])
        st.markdown(f"""
        <div class="card-box correct-border">
            <h3 style="color:#198754 !important;">⭕ 올바른 표현<br><small style="font-size:16px;">{card_data['correct_word']}</small></h3>
            <div class="visual-icon">{card_data['correct_icon']}</div>
            <p><b>[핵심 뜻]</b><br>{card_data['correct_meaning']}</p>
            <div class="tip-box">{card_data['correct_tip']}</div>
            <p><b>[상세 설명]</b><br>{card_data['correct_desc']}</p>
            <hr style="margin:15px 0;">
            <p><b>[대표 예문]</b></p>
            <ul class="example-list" style="padding-left: 18px;">
                {ex_list_html}
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    # 2) 틀린/헷갈리는 표현 카드
    with col_wrong:
        ex_wrong_html = "".join([f"<li>{ex}</li>" for ex in card_data["wrong_examples"]])
        st.markdown(f"""
        <div class="card-box wrong-border">
            <h3 style="color:#dc3545 !important;">❌ 헷갈리는 표현<br><small style="font-size:16px;">{card_data['wrong_word']}</small></h3>
            <div class="visual-icon">{card_data['wrong_icon']}</div>
            <p><b>[핵심 뜻]</b><br>{card_data['wrong_meaning']}</p>
            <div class="tip-box">{card_data['wrong_tip']}</div>
            <p><b>[상세 설명]</b><br>{card_data['wrong_desc']}</p>
            <hr style="margin:15px 0;">
            <p><b>[대표 예문]</b></p>
            <ul class="example-list" style="padding-left: 18px;">
                {ex_wrong_html}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    
    # 다음 문제 이동 시 상태를 완전히 리셋하는 처리
    if idx < len(QUIZ_DATA) - 1:
        if st.button("다음 문제 풀기 ➡️", type="primary", use_container_width=True, key=f"next_{idx}"):
            st.session_state.current_idx += 1
            st.session_state.selected_option = None  # 다음 문제를 위해 선택값 초기화
            st.rerun()
    else:
        st.balloons()
        st.success("🏆 모든 대화 학습을 다 마쳤습니다!")
        if st.button("처음부터 다시 학습하기 🔄", use_container_width=True, key="reset_all"):
            st.session_state.current_idx = 0
            st.session_state.selected_option = None
            st.rerun()
