import streamlit as st

# 1. 기본 설정 및 디자인
st.set_page_config(page_title="사내 카페 현황", page_icon="☕", layout="centered")

# 상수 설정
TOTAL_CAPACITY = 200

# 데이터 유지 (실제 운영 시 구글 시트 연동 권장)
if 'current_count' not in st.session_state:
    st.session_state.current_count = 0

# --- 관리자 기능 (사이드바 또는 상단 비밀번호 입력) ---
with st.sidebar:
    st.header("⚙️ 관리자 설정")
    admin_pw = st.text_input("관리자 인증 코드를 입력하세요", type="password")
    
    # 관리자 인증 성공 시
    if admin_pw == "1234":  # 원하는 비밀번호로 수정하세요
        st.success("인증되었습니다.")
        st.subheader("매니저 컨트롤러")
        
        # 1. 숫자를 직접 입력하는 방식 (기존 클릭 방식 대체)
        new_count = st.number_input(
            "현재까지 제공된 총 잔수", 
            min_value=0, 
            max_value=TOTAL_CAPACITY, 
            value=st.session_state.current_count,
            step=1
        )
        
        if st.button("현황 업데이트 반영"):
            st.session_state.current_count = new_count
            st.toast("현황이 실시간으로 반영되었습니다!")
            st.rerun()
            
        if st.button("새로고침 (0으로 초기화)"):
            st.session_state.current_count = 0
            st.rerun()
    else:
        st.info("관리자만 수량을 변경할 수 있습니다.")

# --- 직원용 메인 화면 ---
st.title("☕ 오늘 우리 카페는?")
st.write("실시간 제공 현황을 확인하고 방문해 주세요!")

# 잔여 수량 계산
remaining = TOTAL_CAPACITY - st.session_state.current_count

# 시각적 지표 (직원용 표현 사용)
st.divider()

col1, col2 = st.columns(2)

with col1:
    if remaining > 50:
        st.metric(label="지금 방문하시면", value="여유 있음")
    elif remaining > 0:
        st.metric(label="지금 방문하시면", value="곧 마감")
    else:
        st.metric(label="지금 방문하시면", value="준비 수량 소진")

with col2:
    st.metric(label="남은 잔여 수량", value=f"{remaining} / {TOTAL_CAPACITY} 잔")

# 프로그레스 바 (얼마나 남았는지 시각화)
# 직원들에게는 '소진율' 개념으로 부드럽게 표시
fill_rate = st.session_state.current_count / TOTAL_CAPACITY
st.progress(fill_rate)

# 상태별 메시지 (판매 대신 '준비', '제공' 표현 사용)
if remaining <= 0:
    st.error("📢 금일 준비된 200잔의 음료 서비스가 모두 종료되었습니다. 내일 다시 만나요!")
    st.balloons() # 마감 시 풍선 효과 (선택 사항)
elif remaining <= 20:
    st.warning(f"⚠️ 현재 이용 가능 수량이 {remaining}잔 남았습니다. 곧 마감될 예정입니다!")
else:
    st.info(f"✨ 즐거운 휴식 되세요! 현재 {remaining}잔의 서비스 여유가 있습니다.")

# 자동 새로고침 안내 (직원들을 위한 친절한 설명)
st.caption("※ 페이지를 새로고침(F5)하면 최신 현황을 확인할 수 있습니다.")
