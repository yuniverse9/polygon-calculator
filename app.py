import math
import pandas as pd
import streamlit as st

st.set_page_config(page_title="외접 정다각형 계산기 (일반화)", page_icon="📐", layout="centered")
st.title("📐 원 외접 정다각형 길이 계산기 (일반화)")
st.caption("원의 지름 d를 입력하고 n(정n각형)을 선택하면, 외접(=내접원 지름이 d) 기준으로 한 변과 대각선을 계산합니다.")

def side_outscribed(n: int, d: float) -> float:
    return d * math.tan(math.pi / n)

def circumradius_from_inradius(n: int, r: float) -> float:
    return r / math.cos(math.pi / n)

def longest_diagonal_outscribed(n: int, d: float) -> float:
    r = d / 2
    R = circumradius_from_inradius(n, r)
    if n % 2 == 0:  # even
        return 2 * R
    else:           # odd
        return 2 * R * math.cos(math.pi / (2 * n))

def step_diagonal_outscribed(n: int, d: float, m: int) -> float:
    r = d / 2
    R = circumradius_from_inradius(n, r)
    return 2 * R * math.sin(m * math.pi / n)

# 입력 UI
c1, c2, c3 = st.columns([2,1,1])
with c1:
    d = st.number_input("원의 지름 d", min_value=0.0, value=10.0, step=1.0, format="%.6f")
with c2:
    n = st.number_input("정n각형의 n", min_value=3, value=6, step=1)
with c3:
    decimals = st.number_input("소수 자릿수", min_value=0, max_value=10, value=6, step=1)

# 빠른 선택 버튼 (정사각형/육각형/팔각형)
st.write("빠른 선택:")
b1, b2, b3 = st.columns(3)
with b1:
    if st.button("정사각형(n=4)"):
        n = 4
with b2:
    if st.button("정육각형(n=6)"):
        n = 6
with b3:
    if st.button("정팔각형(n=8)"):
        n = 8

st.divider()

if d <= 0:
    st.warning("지름 d는 0보다 커야 합니다.")
elif n < 3:
    st.warning("n은 3 이상이어야 합니다.")
else:
    # 기본 결과: 한 변 + 가장 긴 대각선
    s = side_outscribed(n, d)
    Dmax = longest_diagonal_outscribed(n, d)

    base = pd.DataFrame(
        [[f"정{n}각형", s, Dmax]],
        columns=["도형", "한 변 길이", "가장 긴 대각선"]
    )

    # m-스텝 대각선 선택
    st.subheader("m-스텝 대각선 (선택)")
    m_max = n // 2
    m = st.slider("m (1은 변, 최대는 대칭상 서로 다른 대각선의 끝)", 1, m_max, 1)
    Dm = step_diagonal_outscribed(n, d, m)

    diag_df = pd.DataFrame(
        [[f"m={m} 스텝 대각선", Dm]],
        columns=["종류", "길이"]
    )

    # 표시/반올림
    disp_base = base.copy()
    disp_base["한 변 길이"] = disp_base["한 변 길이"].map(lambda x: f"{x:.{decimals}f}")
    disp_base["가장 긴 대각선"] = disp_base["가장 긴 대각선"].map(lambda x: f"{x:.{decimals}f}")

    disp_diag = diag_df.copy()
    disp_diag["길이"] = disp_diag["길이"].map(lambda x: f"{x:.{decimals}f}")

    st.subheader("결과 (기본)")
    st.dataframe(disp_base, use_container_width=True)

    st.subheader("결과 (m-스텝 대각선)")
    st.dataframe(disp_diag, use_container_width=True)

    # CSV 다운로드 (원시값)
    out = base.copy()
    out_m = diag_df.copy()
    out_all = pd.concat([out, out_m], axis=1)
    csv = out_all.to_csv(index=False).encode("utf-8-sig")
    st.download_button("CSV 다운로드", data=csv, file_name=f"외접_정{n}각형_길이.csv", mime="text/csv")

with st.expander("공식/설명 보기"):
    st.markdown(
r"""
- **전제**: 원의 지름 \(d\) = 정\(n\)각형의 **내접원 지름** (정\(n\)각형이 원에 외접)
- 반지름 \( r = d/2 \), 외접원 반지름 \( R = \dfrac{r}{\cos(\pi/n)} \)

**한 변**  
\[
s = 2r\,\tan\left(\frac{\pi}{n}\right) = d\,\tan\left(\frac{\pi}{n}\right)
\]

**가장 긴 대각선**  
\[
D_{\max} = 
\begin{cases}
2R, & n \text{ 짝수} \\
2R\cos\left(\dfrac{\pi}{2n}\right), & n \text{ 홀수}
\end{cases}
\]

**m-스텝 대각선** (꼭짓점 간 m칸 건너뛰기)  
\[
D_m = 2R \sin\left(\frac{m\pi}{n}\right), \quad m=1,\dots,\left\lfloor \frac{n}{2}\right\rfloor
\]
- \(m=1\)이면 한 변과 동일.
- 짝수 \(n\)에서 \(m=\frac{n}{2}\)는 지름(= \(2R\)).

**특수값 예시**  
- 정사각형(\(n=4\)): \(s=d\), \(D_{\max}=d\sqrt{2}\)  
- 정육각형(\(n=6\)): \(s=\frac{d}{\sqrt{3}}\), \(D_{\max}=\frac{2d}{\sqrt{3}}\)  
- 정팔각형(\(n=8\)): \(s=d\tan(\pi/8)\), \(D_{\max}=\frac{d}{\cos(\pi/8)}\)
"""
    )