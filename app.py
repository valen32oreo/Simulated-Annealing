import math
import random
import time
import plotly.graph_objects as go
import streamlit as st

# KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Traffic Optimizer - Simulated Annealing",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Layout Container Utama */
    .block-container {
        padding-top: 3.8rem !important;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    /* Custom Header Banner */
    .header-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: clamp(16px, 3vw, 24px);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        display: flex;
        gap: clamp(12px, 2vw, 18px);
        align-items: stretch;
        margin-bottom: 20px;
    }

    .accent-bar {
        width: 4px;
        background: #2563eb;
        border-radius: 9999px;
        flex-shrink: 0;
    }

    .header-content {
        display: flex;
        flex-direction: column;
        gap: 4px;
        width: 100%;
    }

    .header-eyebrow {
        font-size: clamp(11px, 1.2vw, 12px);
        font-weight: 600;
        color: #64748b;
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 0;
    }

    .eyebrow-bold {
        font-weight: 700;
        color: #2563eb;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    .eyebrow-divider { color: #cbd5e1; }

    .header-title {
        font-size: clamp(18px, 2.4vw, 24px) !important;
        font-weight: 800 !important;
        line-height: 1.3 !important;
        color: #0f172a !important;
        margin: 0 !important;
        letter-spacing: -0.02em !important;
    }

    .header-title i {
        color: #2563eb;
        font-style: italic;
        font-weight: 700;
    }

    .header-subtitle {
        font-size: clamp(12px, 1.2vw, 13.5px);
        line-height: 1.45;
        color: #64748b;
        margin: 2px 0 0 0;
    }

    /* CSS Grid untuk Metric Cards */
    .metrics-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin-bottom: 20px;
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 14px 10px;
        text-align: center;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
        transition: all 0.2s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px -2px rgba(0, 0, 0, 0.06);
        border-color: #cbd5e1;
    }

    .metric-icon {
        font-size: 18px;
        margin-bottom: 4px;
    }

    .metric-label {
        font-size: 10.5px;
        color: #64748b;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        line-height: 1.2;
    }

    .metric-value {
        font-size: clamp(19px, 2vw, 24px);
        color: #0f172a;
        font-weight: 800;
        margin-top: 4px;
        line-height: 1.1;
    }

    .metric-value-red { color: #ef4444; }
    .metric-value-green { color: #10b981; }
    .metric-value-blue { color: #2563eb; }

    /* Phase Direction Cards */
    .phase-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 8px;
    }

    .phase-title {
        font-weight: 700;
        font-size: 13px;
        color: #1e293b;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .phase-time {
        font-size: 13px;
        font-weight: 800;
        color: #2563eb;
        background: #eff6ff;
        padding: 2px 8px;
        border-radius: 6px;
        border: 1px solid #bfdbfe;
    }

    /* Custom Mobile Overlay Styling */
    @media (max-width: 768px) {
        .block-container {
            padding-top: 1rem;
            padding-left: 0.75rem;
            padding-right: 0.75rem;
        }

        .metrics-container {
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }

        .metric-value { font-size: 18px; }
    }

    /* SIDEBAR PROFESIONAL STYLING */
    div[data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }

    .sidebar-header {
        margin-bottom: 20px;
        padding-top: 0px;
        padding-bottom: 12px;
        border-bottom: 1px solid #e2e8f0;
    }

    .sidebar-header-title {
        font-size: 16px;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.01em;
    }

    .sidebar-header-sub {
        font-size: 12px;
        color: #64748b;
        margin-top: 2px;
    }

    .sidebar-section-tag {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #2563eb;
        margin-top: 18px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Custom Styling Expander Sidebar */
    div[data-testid="stExpander"] {
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        background-color: #ffffff !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
    }

    .stButton>button {
        border-radius: 10px;
        font-weight: 700;
        font-size: 14.5px;
        padding: 10px 18px;
        background: #2563eb;
        border: none;
        color: #ffffff;
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        background: #1d4ed8;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# FUNGSI HITUNG RATA-RATA WAKTU TUNGGU
def calculate_delay(state, demands):
    discharge_rate = 0.55
    yellow_time = 4
    total_cycle = sum(state) + (len(state) * yellow_time)

    total_delay = 0
    total_vehicles = 0

    for i in range(len(state)):
        arrival_rate = demands[i] / 60.0
        green = state[i]

        arr = arrival_rate * total_cycle
        served = green * discharge_rate
        rem = max(0.0, arr - served)

        # Estimasi delay realistis (sisa antrean + waktu merah)
        red_time = total_cycle - green
        delay_fase = (rem * red_time) + (arr * (red_time / 2))

        total_delay += delay_fase
        total_vehicles += max(1.0, arr)

    avg_delay = total_delay / total_vehicles
    return round(avg_delay, 1)


# MAIN APP
def main():

    # HEADER BANNER
    st.markdown(
        """
        <div class="header-card">
            <div class="accent-bar"></div>
            <div class="header-content">
                <p class="header-eyebrow">
                    <span class="eyebrow-bold">Kelompok 1</span>
                    <span class="eyebrow-divider">•</span>
                    <span>Kompleksitas Algoritma</span>
                </p>
                <h1 class="header-title">
                    Pengaturan Lampu Lalu Lintas Adaptif dengan Algoritma <i>Simulated Annealing</i>
                </h1>
                <p class="header-subtitle">
                    Optimasi alokasi waktu lampu lalu lintas untuk meminimalkan waktu tunggu kendaraan di persimpangan.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # SIDEBAR CONTROL PANEL (DESIGN REFINED)
    st.sidebar.markdown(
        """
        <div class="sidebar-header">
            <div class="sidebar-header-title">Panel Kontrol Simulasi</div>
            <div class="sidebar-header-sub">Atur variabel skenario & parameter optimasi</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Seksi 1: Skenario Lalu Lintas
    st.sidebar.markdown(
        '<div class="sidebar-section-tag">01. Skenario Lalu Lintas</div>',
        unsafe_allow_html=True,
    )
    scenario = st.sidebar.selectbox(
        "Pilih Skenario Kepadatan:",
        [
            "Utara Sangat Padat (Jam Sibuk)",
            "Lalu Lintas Merata",
            "Simpang Tidak Seimbang",
            "Input Manual (Custom)",
        ],
        label_visibility="collapsed",
    )

    if scenario == "Utara Sangat Padat (Jam Sibuk)":
        demands = [50, 15, 30, 10]
    elif scenario == "Lalu Lintas Merata":
        demands = [35, 35, 35, 35]
    elif scenario == "Simpang Tidak Seimbang":
        demands = [60, 10, 45, 15]
    else:
        st.sidebar.markdown("<small style='color:#64748b;'>Volume kendaraan per menit:</small>", unsafe_allow_html=True)
        u = st.sidebar.slider("Utara", 5, 100, 40)
        s = st.sidebar.slider("Selatan", 5, 100, 20)
        t = st.sidebar.slider("Timur", 5, 100, 30)
        b = st.sidebar.slider("Barat", 5, 100, 15)
        demands = [u, s, t, b]

    # Seksi 2: Parameter Simulated Annealing
    st.sidebar.markdown(
        '<div class="sidebar-section-tag" style="margin-top:24px;">02. Parameter Algoritma</div>',
        unsafe_allow_html=True,
    )
    t_0 = st.sidebar.slider("Suhu Awal (T₀)", 50.0, 300.0, 100.0, step=10.0, help="Suhu tinggi memperluas eksplorasi acak di awal pencarian.")
    alpha = st.sidebar.slider(
        "Laju Pendinginan (α)", 0.80, 0.99, 0.92, step=0.01, help="Mengontrol kecepatan transisi menuju penentuan hasil terbaik."
    )

    # Seksi 3: Landasan Teori
    st.sidebar.markdown(
        '<div class="sidebar-section-tag" style="margin-top:24px;">03. Referensi Teori</div>',
        unsafe_allow_html=True,
    )
    with st.sidebar.expander("Landasan Teori Algoritma"):
        st.markdown("""
        *Simulated Annealing (SA)* mensimulasikan proses pendinginan logam untuk menemukan solusi optimal global:

        - **State ($S$)**: Alokasi waktu sinyal hijau 4 lajur.
        - **Cost / Fungsi Biaya ($E$)**: Rata-rata waktu tunggu kendaraan (detik) yang ingin diminimalkan.
        - **Suhu ($T$)**: Mengontrol keberanian eksplorasi untuk melompat dari jebakan *local optima*.
        - **Pendinginan (α)**: Mengontrol transisi dari mode penjelajahan bebas menuju penguncian solusi terbaik ($P = e^{-\\Delta E / T}$).
        """)

    # BASELINE COMPUTATION
    fixed_state = [25, 25, 25, 25]
    baseline_delay = calculate_delay(fixed_state, demands)

    # METRIC CARDS PLACEHOLDER
    p_kpis = st.empty()

    st.markdown("<br>", unsafe_allow_html=True)

    # LAYOUT UTAMA: GRAFIK & ALOKASI
    col_left, col_right = st.columns([1.6, 1])

    with col_left:
        st.markdown("##### 📈 Grafik Konvergensi Optimasi Waktu Tunggu")
        p_chart = st.empty()

    with col_right:
        st.markdown("##### ⏱️ Alokasi Sinyal Hijau Optimal")
        p_alloc = st.empty()

    st.markdown("<br>", unsafe_allow_html=True)

    # RENDER METRIC CARDS
    def render_kpis(
        b_delay, s_delay="--", eff_val="--", temp_val=t_0, is_running=False
    ):
        sa_class = "metric-value-green" if is_running else ""
        eff_str = f"+{eff_val}%" if is_running else "-- %"
        s_delay_str = (
            f"{s_delay} <span style='font-size:13px;'>s</span>"
            if (is_running or s_delay != "--")
            else "-- s"
        )

        p_kpis.markdown(
            f"""
            <div class="metrics-container">
                <div class="metric-card">
                    <div class="metric-icon">🔴</div>
                    <div class="metric-label">Sistem Statis</div>
                    <div class="metric-value metric-value-red">{b_delay} <span style="font-size:13px;">s</span></div>
                </div>
                <div class="metric-card">
                    <div class="metric-icon">🟢</div>
                    <div class="metric-label">Hasil Optimal SA</div>
                    <div class="metric-value {sa_class}">{s_delay_str}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-icon">⚡</div>
                    <div class="metric-label">Efisiensi</div>
                    <div class="metric-value metric-value-green">{eff_str}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-icon">🔥</div>
                    <div class="metric-label">Suhu Sistem (T)</div>
                    <div class="metric-value metric-value-blue">{temp_val:.1f}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Initial Render
    render_kpis(baseline_delay)

    # INITIAL CHART PLACEHOLDER
    fig_init = go.Figure()
    fig_init.add_trace(
        go.Scatter(
            x=[0],
            y=[baseline_delay],
            mode="lines+markers",
            name="Lampu Statis (Baseline)",
            line=dict(color="#ef4444", width=2, dash="dash"),
        )
    )
    fig_init.update_layout(
        height=320,
        margin=dict(l=15, r=15, t=15, b=15),
        xaxis_title="Iterasi (Langkah Optimasi)",
        yaxis_title="Rata-rata Waktu Tunggu (Detik)",
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        hovermode="x unified",
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
        ),
    )
    p_chart.plotly_chart(fig_init, use_container_width=True, config={'displayModeBar': False})

    # INITIAL ALLOCATION PLACEHOLDER
    directions = [
        ("⬆️ Lajur Utara", demands[0], fixed_state[0]),
        ("⬇️ Lajur Selatan", demands[1], fixed_state[1]),
        ("➡️ Lajur Timur", demands[2], fixed_state[2]),
        ("⬅️ Lajur Barat", demands[3], fixed_state[3]),
    ]
    with p_alloc.container():
        for label, dem, val in directions:
            st.markdown(
                f"""
                <div class="phase-card">
                    <div class="phase-title">
                        <span>{label} <small style="color:#64748b; font-weight:normal;">({dem} kend/mnt)</small></span>
                        <span class="phase-time">{val} detik</span>
                    </div>
                </div>
            """,
                unsafe_allow_html=True,
            )
            st.progress(val / 100)

    # TOMBOL EKSEKUSI
    if st.button(
        "🚀 Jalankan Optimasi Simulated Annealing",
        type="primary",
        use_container_width=True,
    ):
        current_state = list(fixed_state)
        current_delay = baseline_delay
        best_state = list(current_state)
        best_delay = current_delay

        T = t_0
        T_min = 0.5
        step = 0

        history = {"x": [0], "current": [current_delay], "best": [best_delay]}

        while T > T_min:
            for _ in range(8):
                step += 1

                neighbor = list(current_state)
                i, j = random.sample(range(4), 2)
                delta = random.choice([2, 3, 4, 5])

                if neighbor[i] - delta >= 10 and neighbor[j] + delta <= 60:
                    neighbor[i] -= delta
                    neighbor[j] += delta

                neighbor_delay = calculate_delay(neighbor, demands)
                diff = neighbor_delay - current_delay

                if diff < 0 or random.random() < math.exp(-diff / T):
                    current_state = neighbor
                    current_delay = neighbor_delay
                    if current_delay < best_delay:
                        best_state = list(current_state)
                        best_delay = current_delay

                history["x"].append(step)
                history["current"].append(current_delay)
                history["best"].append(best_delay)

            T *= alpha

            # UPDATE KPIS REALTIME
            eff = round(((baseline_delay - best_delay) / baseline_delay) * 100, 1)
            render_kpis(
                baseline_delay,
                s_delay=best_delay,
                eff_val=eff,
                temp_val=T,
                is_running=True,
            )

            # UPDATE CHART REALTIME
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=history["x"],
                    y=history["current"],
                    mode="lines",
                    name="Eksplorasi Suhu SA",
                    line=dict(color="#94a3b8", width=1.5),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=history["x"],
                    y=history["best"],
                    mode="lines",
                    name="Hasil Optimal (Best)",
                    line=dict(color="#10b981", width=3),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=history["x"],
                    y=[baseline_delay] * len(history["x"]),
                    mode="lines",
                    name="Lampu Statis (Baseline)",
                    line=dict(color="#ef4444", width=2, dash="dash"),
                )
            )

            fig.update_layout(
                height=320,
                margin=dict(l=15, r=15, t=15, b=15),
                xaxis_title="Iterasi (Langkah Optimasi)",
                yaxis_title="Rata-rata Waktu Tunggu (Detik)",
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
                hovermode="x unified",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                ),
            )
            p_chart.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            # UPDATE ALOKASI HIJAU REALTIME
            phases = [
                ("⬆️ Lajur Utara", demands[0], best_state[0]),
                ("⬇️ Lajur Selatan", demands[1], best_state[1]),
                ("➡️ Lajur Timur", demands[2], best_state[2]),
                ("⬅️ Lajur Barat", demands[3], best_state[3]),
            ]
            with p_alloc.container():
                for label, dem, val in phases:
                    st.markdown(
                        f"""
                        <div class="phase-card">
                            <div class="phase-title">
                                <span>{label} <small style="color:#64748b; font-weight:normal;">({dem} kend/mnt)</small></span>
                                <span class="phase-time">{val} detik</span>
                            </div>
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )
                    st.progress(val / 100)

            time.sleep(0.01)


if __name__ == "__main__":
    main()