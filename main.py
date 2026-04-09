import streamlit as st

# 초기값 설정 (실제 운영 시에는 구글 시트 연동 권장)
if 'count' not in st.session_state:
    st.session_state.count = 0

TOTAL = 200
remaining = TOTAL - st.session_state.count

# --- 사용자 화면 (누구나 보는 화면) ---
st.title("☕ 사내 카페 실시간 현황")

# 상태에 따른 색상 및 메시지 설정
if remaining > 50:
    st.success(f"현재 주문 가능합니다! (남은 수량: {remaining}잔)")
elif remaining > 0:
    st.warning(f"마감이 임박했습니다! (남은 수량: {remaining}잔)")
else:
    st.error("오늘 준비된 200잔이 모두 마감되었습니다.")

# 시각적인 게이지 차트
st.progress(st.session_state.count / TOTAL)
st.metric("현재 판매량", f"{st.session_state.count} / {TOTAL}")

# --- 관리자 영역 (비밀번호 입력 시에만 등장) ---
st.divider()
admin_pw = st.sidebar.text_input("관리자 인증", type="password")

if admin_pw == "1234":  # 설정하실 비밀번호
    st.sidebar.subheader("매니저 전용 컨트롤러")
    if st.sidebar.button("1잔 판매 완료 (+1)"):
        st.session_state.count += 1
        st.rerun()
    if st.sidebar.button("초기화 (새로 시작)"):
        st.session_state.count = 0
        st.rerun()
