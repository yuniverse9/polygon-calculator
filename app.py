import math
import pandas as pd
import streamlit as st

st.set_page_config(page_title="외접 정다각형 계산기", page_icon="📐", layout="centered")
st.title("📐 원 외접 정다각형 길이 계산기")
st.caption("원의 지름 d와 정n각형의 n을 입력하면, 외접(=내접원 지름이 d) 기준으로 한 변과 가장 긴 대각선 길이를 계산합니다.")

def side_outscribed(n: int, d: float) -> float:
    return d * math.tan(math.pi / n)

def longest_diagonal_outscribed(n: int, d: float) -> float:
    r = d / 2
    R = r / math.cos(math.pi / n)
    if n % 2 == 0:
        return 2 * R
    else:
        return 2 * R * math.cos(math.pi / (2 * n))

# 입력 UI
col1, col2, col3 = st.columns([2,1,1])
with col1:
    d = st.number_input("원의 지름 d", min_value=0.0, value=10.0, step=1.0, format="%.6f")
with col2:
    n = st.number_input("정n각형의 n", min_value=3, value=6, step=1)
with col3:
    decimals = st.number_input("표시 소수 자릿수", min_value=0, max_value=10, value=6, step=1)

st.divider()

if d <= 0:
    st.warning("지름 d는 0보다 커야 합니다.")
elif n < 3:
    st.warning("n은 3 이상이어야 합니다.")
else:
    s = side_outscribed(n, d)
    Dmax = longest_diagonal_outscribed(n, d)

    # 결과 테이블
    df = pd.DataFrame(
        [[f"정{n}각형", s, Dmax]],
        columns=["도형", "한 변 길이", "가장 긴 대각선"]
    )
    disp = df.copy()
    disp["한 변 길이"] = disp["한 변 길이"].map(lambda x: f"{x:.{decimals}f}")
    disp["가장 긴 대각선"] = disp["가장 긴 대각선"].map(lambda x: f"{x:.{decimals}f}")

    st.subheader("결과")
    st.dataframe(disp, use_container_width=True)

    # 수식 보여주기
    st.subheader("계산식")
    st.markdown(
        f"""
        **한 변 (s)**  
        \\[
        s = d \\cdot \\tan\\left(\\frac{{\\pi}}{{n}}\\right)
        = {d} \\times \\tan\\left(\\frac{{\\pi}}{{{n}}}\\right)
        = {s:.{decimals}f}
        \\]

        **가장 긴 대각선 (Dmax)**  
        {"짝수" if n%2==0 else "홀수"} n 이므로,
        \\[
        D_{{max}} =
        {"2R, \\quad R = \\dfrac{r}{\\cos(\\pi/n)}" if n%2==0 else "2R\\cos\\left(\\dfrac{\\pi}{2n}\\right), \\quad R = \\dfrac{r}{\\cos(\\pi/n)}"}
        \\]
        여기서 \\(r = d/2 = {d/2}\\)

        → Dmax = {Dmax:.{decimals}f}
        """
    )

    # CSV 다운로드
    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "CSV 다운로드",
        data=csv,
        file_name=f"외접_정{n}각형_길이.csv",
        mime="text/csv",
    )

