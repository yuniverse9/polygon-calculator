import math
import pandas as pd
import streamlit as st

st.set_page_config(page_title="외접 정다각형 계산기 (심플)", page_icon="📐", layout="centered")
st.title("📐 원 외접 정다각형 길이 계산기 (심플)")
st.caption("원의 지름 d와 정n각형의 n을 입력하면, 외접(=내접원 지름이 d) 기준으로 한 변과 가장 긴 대각선 길이를 계산합니다.")

def side_outscribed(n: int, d: float) -> float:
    """외접 정n각형의 한 변 길이: s = d * tan(pi/n)"""
    return d * math.tan(math.pi / n)

def longest_diagonal_outscribed(n: int, d: float) -> float:
    """
    외접 정n각형의 가장 긴 대각선.
    짝수 n: 맞은편 꼭짓점 연결 = 2R
    홀수 n: 최장 대각선 = 2R * cos(pi/(2n))
    (R = r / cos(pi/n),  r = d/2)
    """
    r = d / 2
    R = r / math.cos(math.pi / n)
    if n % 2 == 0:
        return 2 * R
    else:
        return 2 * R * math.cos(math.pi / (2 * n))

# 입력 UI (필수값만)
c1, c2, c3 = st.columns([2,1,1])
with c1:
    d = st.number_input("원의 지름 d", min_value=0.0, value=10.0, step=1.0, format="%.6f")
with c2:
    n = st.number_input("정n각형의 n", min_value=3, value=6, step=1)
with c3:
    decimals = st.number_input("표시 소수 자릿수", min_value=0, max_value=10, value=6, step=1)

st.divider()

# 계산 및 표시
if d <= 0:
    st.warning("지름 d는 0보다 커야 합니다.")
elif n < 3:
    st.warning("n은 3 이상이어야 합니다.")
else:
    s = side_outscribed(n, d)
    Dmax = longest_diagonal_outscribed(n, d)

    df = pd.DataFrame(
        [[f"정{n}각형", s, Dmax]],
        columns=["도형", "한 변 길이", "가장 긴 대각선"]
    )

    disp = df.copy()
    disp["한 변 길이"] = disp["한 변 길이"].map(lambda x: f"{x:.{decimals}f}")
    disp["가장 긴 대각선"] = disp["가장 긴 대각선"].map(lambda x: f"{x:.{decimals}f}")

    st.subheader("결과")
    st.dataframe(disp, use_container_width=True)

    # CSV 다운로드 (원시값)
    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "CSV 다운로드",
        data=csv,
        file_name=f"외접_정{n}각형_길이.csv",
        mime="text/csv",
    )

with st.expander("공식/설명 보기"):
    st.markdown(
r"""
- 전제: 원의 지름 \(d\) = 정\(n\)각형 **내접원 지름** (정\(n\)각형이 원에 외접)
- 반지름 \( r = d/2 \), 외접원 반지름 \( R = \dfrac{r}{\cos(\pi/n)} \)

**한 변**
\[
s = 2r\tan\left(\frac{\pi}{n}\right) = d\tan\left(\frac{\pi}{n}\right)
\]

**가장 긴 대각선**
\[
D_{\max} =
\begin{cases}
2R, & n \text{ 짝수} \\
2R\cos\left(\dfrac{\pi}{2n}\right), & n \text{ 홀수}
\end{cases}
\]
"""
    )
