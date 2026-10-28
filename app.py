import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from database import init_db, create_user, login_user, insert_survey_data, fetch_survey_data


# ---------------------------------------------------------
# 외부 웹사이트(게임)를 하나의 프레임 안에 꼭 맞게 보여주는 함수
#  - 바깥 컴포넌트 높이와 안쪽 iframe 높이를 동일하게 맞춰
#    이중 스크롤과 화면 잘림을 방지합니다.
# ---------------------------------------------------------
def embed_site(url: str, height: int = 760, title: str = "embedded") -> None:
    # 최신 Streamlit(st.iframe 지원): URL을 바로 지정한 높이의 iframe으로 표시
    if hasattr(st, "iframe"):
        st.iframe(url, height=height)
        return
    # 구버전 Streamlit: components.html 사용 (바깥/안쪽 높이를 동일하게 맞춤)
    components.html(
        f"""
        <style>
          html, body {{ margin: 0; padding: 0; height: 100%; overflow: hidden; }}
          iframe {{ display: block; width: 100%; height: 100%; border: 0; }}
        </style>
        <iframe src="{url}" title="{title}" allow="fullscreen; autoplay; gamepad" allowfullscreen></iframe>
        """,
        height=height,
        scrolling=False,
    )


def game_page(page_title: str, url: str, key: str) -> None:
    """게임 페이지 공통 레이아웃: 제목 + 높이 조절 + 새 창 열기 + 프레임"""
    head_col, ctrl_col = st.columns((3, 2))
    with head_col:
        st.title(page_title)
    with ctrl_col:
        frame_h = st.slider("화면 높이(px)", 500, 1200, 760, 20, key=f"{key}_height")
        st.link_button("🔗 새 창에서 크게 열기", url, use_container_width=True)
    embed_site(url, height=frame_h, title=page_title)
    st.caption("화면이 잘리면 위의 슬라이더로 높이를 조절하거나, 새 창에서 열어 보세요.")

# DB 초기화 및 테이블 생성
init_db()

st.set_page_config(page_title="AI 교육 앱", layout="wide")

# 게임 화면이 한 프레임 안에 잘 보이도록 기본 여백 축소
st.markdown(
    "<style>.block-container{padding-top:1.5rem; padding-bottom:1rem;}</style>",
    unsafe_allow_html=True,
)

# menu = ["Home", "Login", "SignUp", "설문참여",]
menu = ["Home", "Login", "SignUp", "설문참여", "pythonid", "블록리게임", "테트리스게임"]
choice = st.sidebar.selectbox("Menu", menu)

# 세션 상태 초기화 (로그인 관리)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_id'] = ''

if choice == "Home":
    st.title("홈 화면")
    st.write("환영합니다. AI 교육적 효과 인식 설문 앱입니다.")
    if st.session_state['logged_in']:
        st.success(f"{st.session_state['user_id']}님, 로그인 상태입니다.")

elif choice == "SignUp":
    st.title("회원가입")
    with st.form("signup_form"):
        new_user = st.text_input("ID")
        new_name = st.text_input("Name")
        new_password = st.text_input("Password", type='password')
        new_email = st.text_input("Email")
        submit = st.form_submit_button("가입하기")
        
        if submit:
            if create_user(new_user, new_name, new_password, new_email):
                st.success("계정이 성공적으로 생성되었습니다. Login 메뉴에서 로그인해 주세요.")
            else:
                st.error("오류: 이미 존재하는 ID이거나 이메일입니다.")

elif choice == "Login":
    st.title("로그인")
    with st.form("login_form"):
        userid = st.text_input("ID")
        password = st.text_input("Password", type='password')
        submit = st.form_submit_button("로그인")
        
        if submit:
            result = login_user(userid, password)
            if result:
                st.session_state['logged_in'] = True
                st.session_state['user_id'] = userid
                st.success(f"{userid}님 환영합니다.")
            else:
                st.error("ID 또는 비밀번호가 틀렸습니다.")

elif choice == "pythonid":
    game_page("📝 파이썬 학습", "https://www.online-python.com/", "python")

elif choice == "블록리게임":
    game_page("🧩 블록리게임", "https://blockly.games/?lang=ko", "blockly")

elif choice == "테트리스게임":
    game_page("🎮 테트리스게임", "https://play.tetris.com/", "tetris")


elif choice == "설문참여":
    st.title("📝 AI의 교육적 효과에 대한 인식 설문조사")
    
    # 탭 생성
    tab1, tab2 = st.tabs(["📋 설문응시", "📊 설문결과 시각화"])
    
    # 설문 문항 및 척도 정의
    questions = [
        "1. AI는 학습자의 학업 성취도를 향상시키는 데 도움이 된다.",
        "2. AI는 개별 학습자의 수준에 맞춘 맞춤형 학습을 제공하는 데 효과적이다.",
        "3. AI를 활용한 교육은 학습자의 흥미와 참여도를 높인다.",
        "4. AI는 교사의 업무 부담을 줄이고 교육의 질을 높이는 데 기여한다.",
        "5. AI 기반 평가 시스템은 공정하고 객관적인 결과를 제공한다.",
        "6. AI 교육 도구는 자기주도적 학습 능력을 기르는 데 유용하다.",
        "7. 교육 현장에서 AI를 도입하는 것은 필수적인 흐름이다.",
        "8. AI는 복잡한 개념이나 원리를 이해하는 데 도움을 준다.",
        "9. AI 활용 교육은 창의력과 문제해결능력 향상에 긍정적인 영향을 미친다.",
        "10. 전반적으로 AI 기술은 미래 교육 발전에 핵심적인 역할을 할 것이다."
    ]
    options = ["1 (전혀 아니다)", "2 (아니다)", "3 (보통이다)", "4 (그렇다)", "5 (매우 그렇다)"]
    
    # ---------------------------
    # 탭 1: 설문응시
    # ---------------------------
    with tab1:
        st.subheader("설문에 참여해 주세요.")
        with st.form("survey_form"):
            # 로그인 되어있는 경우 ID 자동 입력
            if st.session_state['logged_in']:
                user_id = st.text_input("사용자 ID", value=st.session_state['user_id'], disabled=True)
            else:
                user_id = st.text_input("사용자 ID를 입력하세요 (비회원 가능)", max_chars=20)
            
            responses = []
            for q in questions:
                ans = st.radio(q, options, horizontal=True)
                responses.append(int(ans[0]))
                
            submit_button = st.form_submit_button(label="설문 제출")
            
            if submit_button:
                if user_id.strip() == "":
                    st.error("사용자 ID를 입력해 주세요!")
                else:
                    # DB 저장
                    insert_survey_data(
                        user_id, 
                        responses[0], responses[1], responses[2], responses[3], responses[4],
                        responses[5], responses[6], responses[7], responses[8], responses[9]
                    )
                    st.success(f"{user_id}님, 설문이 성공적으로 제출되었습니다. 감사합니다!")

    # ---------------------------
    # 탭 2: 설문결과 시각화
    # ---------------------------
    with tab2:
        st.subheader("설문 결과 통계 및 시각화")
        
        df = fetch_survey_data()
        
        if df.empty:
            st.info("아직 제출된 설문 데이터가 없습니다.")
        else:
            st.write(f"**총 응답자 수:** {len(df)}명")
            st.divider()
            
            for i, q in enumerate(questions):
                col_name = f'q{i+1}'
                
                st.markdown(f"**{q}**")
                
                avg_score = df[col_name].mean()
                
                counts = df[col_name].value_counts().reindex([1, 2, 3, 4, 5], fill_value=0)
                counts.index = ["1점", "2점", "3점", "4점", "5점"]
                
                st.bar_chart(counts)
                
                st.caption(f"이 문항의 평균 점수: **{avg_score:.2f} / 5.0**")
                st.divider()
                
