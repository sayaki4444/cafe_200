import streamlit as st

# 초기 설정
TOTAL_CAPACITY = 200

# 데이터 불러오기 (실제로는 파일이나 DB 연결 권장)
if 'count' not in st.session_state:
    st.session_state.count = 0

st.title("☕ 사내 카페 실시간 현황")

# 현재 상태 계산
remaining = TOTAL_CAPACITY - st.session_state.count

# 대시보드 표시
col1, col2 = st.columns(2)
col1.metric("판매된 잔 수", f"{st.session_state.count}잔")
col2.metric("남은 잔 수", f"{remaining}잔", delta_color="inverse")

# 진행률 표시
progress = st.session_state.count / TOTAL_CAPACITY
st.progress(progress)

if st.session_state.count >= TOTAL_CAPACITY:
    st.error("🚫 오늘 준비된 수량이 모두 소진되었습니다. 내일 만나요!")
elif remaining <= 20:
    st.warning("⚠️ 마감 임박! 곧 200잔이 마감됩니다.")

# 관리 권한이 있는 경우에만 버튼 노출 (비밀번호 등으로 제한 가능)
if st.button("커피 1잔 판매 (+1)"):
    if st.session_state.count < TOTAL_CAPACITY:
        st.session_state.count += 1
        st.rerun()