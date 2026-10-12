import math
import random
import time
import plotly.graph_objects as go
import streamlit as st

# --- KONFIGURASI HALAMAN ---
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

    /* Header Banner */
    .header-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: clamp(16px, 3vw, 28px);
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        display: flex;
        gap: clamp(12px, 2vw, 20px);
        align-items: stretch;
        margin-bottom: 20px;
    }

    /* Left Accent Bar Warna Biru */
    .accent-bar {
        width: 4px;
        background-color: #1d4ed8;
        border-radius: 9999px;
        flex-shrink: 0;
    }

    /* Wrapper Konten Teks */
    .header-content {
        display: flex;
        flex-direction: column;
        gap: 6px;
        width: 100%;
    }

    /* Eyebrow / Tag Atas */
    .header-eyebrow {
        font-size: clamp(11px, 1.2vw, 13px);
        font-weight: 500;
        color: #94a3b8;
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 0;
    }

    .eyebrow-bold {
        font-weight: 700;
        color: #1d4ed8;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    .eyebrow-divider {
        color: #cbd5e1;
        font-weight: 300;
    }

    /* Judul Utama */
    .header-title {
        font-size: clamp(18px, 2.5vw, 26px) !important;
        font-weight: 700 !important;
        line-height: 1.3 !important;
        color: #0f172a !important;
        margin: 0 !important;
        padding: 0 !important;
        letter-spacing: -0.01em !important;
    }

    /* Dynamic / Highlighted Text (Simulated Annealing) */
    .header-title i {
        color: #1d4ed8;
        font-style: italic;
        font-weight: 600;
    }

    /* Deskripsi Sub-header */
    .header-subtitle {
        font-size: clamp(12px, 1.3vw, 14px);
        line-height: 1.45;
        color: #64748b;
        margin: 2px 0 0 0;
    }

    /* CSS Grid untuk Metric Cards (4x1 di Desktop, 2x2 di Mobile) */
    .metrics-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin-bottom: 20px;
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px 12px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
        transition: all 0.2s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 12px -2px rgba(0, 0, 0, 0.06);
    }

    .metric-icon {
        font-size: 18px;
        margin-bottom: 4px;
    }

    .metric-label {
        font-size: 11px;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.4px;
        line-height: 1.2;
    }

    .metric-value {
        font-size: clamp(20px, 2.2vw, 26px);
        color: #0f172a;
        font-weight: 800;
        margin-top: 4px;
        line-height: 1.1;
    }

    .metric-value-red {
        color: #ef4444;
    }

    .metric-value-green {
        color: #10b981;
    }

    .metric-value-blue {
        color: #3b82f6;
    }

    /* Phase Direction Cards */
    .phase-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 12px 14px;
        margin-bottom: 10px;
    }

    .phase-title {
        font-weight: 700;
        font-size: 13.5px;
        color: #1e293b;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .phase-time {
        font-size: 14px;
        font-weight: 800;
        color: #2563eb;
        background: #eff6ff;
        padding: 2px 8px;
        border-radius: 6px;
        border: 1px solid #bfdbfe;
    }

    /* Penyesuaian Responsif Layar Kecil (Mobile / Smartphone) */
    @media (max-width: 768px) {
        .header-card {
            padding: 14px 16px;
            gap: 12px;
            border-radius: 10px;
        }

        .accent-bar {
            width: 3px;
        }

        .metrics-container {
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }

        .metric-card {
            padding: 12px 8px;
            border-radius: 10px;
        }

        .metric-icon {
            font-size: 16px;
            margin-bottom: 2px;
        }

        .metric-label {
            font-size: 10px;
        }

        .metric-value {
            font-size: 18px;
        }

        .phase-card {
            padding: 10px 12px;
            margin-bottom: 8px;
        }

        .phase-title {
            font-size: 12.5px;
        }

        .phase-time {
            font-size: 13px;
            padding: 2px 6px;
        }
    }

    /* Streamlit Components Overrides */
    div[data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }

    .stButton>button {
        border-radius: 12px;
        font-weight: 700;
        font-size: 15px;
        padding: 12px 20px;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
        transform: translateY(-1px);
    }

    </style>
""",
    unsafe_allow_html=True,
)


# --- FUNGSI HITUNG RATA-RATA WAKTU TUNGGU ---
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


# --- MAIN APP ---
def main():

    # HEADER BANNER
    st.markdown(
        """
        <div class="header-card">
            <div class="accent-bar"></div>
            <div class="header-content">
                <p class="header-eyebrow">
                    <span class="eyebrow-bold">Kelompok 1</span>
                    <span class="eyebrow-divider">|</span>
                    <span>Kompleksitas Algoritma</span>
                </p>
                <h1 class="header-title">
                    Pengaturan Lampu Lalu Lintas Adaptif dengan Algoritma <i>Simulated Annealing</i>
                </h1>
                <p class="header-subtitle">
                    Optimasi pengaturan waktu lampu lalu lintas untuk membantu mengurangi waktu tunggu kendaraan.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # SIDEBAR CONTROL PANEL
    st.sidebar.markdown("### Panel Kontrol Simulasi")

    st.sidebar.subheader("📋 Skenario Kepadatan Jalan")
    scenario = st.sidebar.selectbox(
        "Pilih Kondisi Lalu Lintas:",
        [
            "Utara Sangat Padat (Jam Sibuk)",
            "Lalu Lintas Merata",
            "Simpang Tidak Seimbang",
            "Input Manual (Custom)",
        ],
    )

    if scenario == "Utara Sangat Padat (Jam Sibuk)":
        demands = [50, 15, 30, 10]
    elif scenario == "Lalu Lintas Merata":
        demands = [35, 35, 35, 35]
    elif scenario == "Simpang Tidak Seimbang":
        demands = [60, 10, 45, 15]
    else:
        st.sidebar.markdown("**Atur Kendaraan/Menit:**")
        u = st.sidebar.slider("Utara", 5, 100, 40)
        s = st.sidebar.slider("Selatan", 5, 100, 20)
        t = st.sidebar.slider("Timur", 5, 100, 30)
        b = st.sidebar.slider("Barat", 5, 100, 15)
        demands = [u, s, t, b]

    st.sidebar.markdown("---")
    st.sidebar.subheader("🔥 Parameter Simulated Annealing")
    t_0 = st.sidebar.slider("Suhu Awal (T₀)", 50.0, 300.0, 100.0, step=10.0)
    alpha = st.sidebar.slider(
        "Laju Pendinginan (α)", 0.80, 0.99, 0.92, step=0.01
    )

    # Information Expander di Sidebar
    with st.sidebar.expander("Landasan Teori Algoritma"):
        st.markdown("""
        *Simulated Annealing (SA)* mensimulasikan proses pendinginan logam untuk menemukan solusi optimal global:

        - **State ($S$)**: Alokasi waktu sinyal hijau 4 lajur.
        - **Cost / Fungsi Biaya ($E$)**: Rata-rata waktu tunggu kendaraan (detik) yang ingin diminimalkan.
        - **Suhu ($T$)**: Mengontrol keberanian eksplorasi. Suhu tinggi memungkinkan algoritma melompat dari jebakan *local optima* (alokasi yang kelihatan bagus padahal belum maksimal).
        - **Pendinginan (α)**: Mengontrol transisi dari mode **penjelajahan bebas di awal** menjadi **penguncian solusi terbaik di akhir** ($P = e^{-\\Delta E / T}$).
        """)

    # BASELINE COMPUTATION
    fixed_state = [25, 25, 25, 25]
    baseline_delay = calculate_delay(fixed_state, demands)

    # METRIC CARDS PLACEHOLDER (RESPONSIF GRID)
    p_kpis = st.empty()

    st.markdown("<br>", unsafe_allow_html=True)

    # LAYOUT UTAMA: GRAFIK (KIRI) & ALOKASI DUA FASE (KANAN)
    col_left, col_right = st.columns([1.6, 1])

    with col_left:
        st.markdown("##### 📈 Grafik Konvergensi Optimasi Waktu Tunggu")
        p_chart = st.empty()

    with col_right:
        st.markdown("##### ⏱️ Alokasi Sinyal Hijau Optimal")
        p_alloc = st.empty()

    st.markdown("<br>", unsafe_allow_html=True)

    # RENDER TAMPILAN METRIC CARDS
    def render_kpis(
        b_delay, s_delay="--", eff_val="--", temp_val=t_0, is_running=False
    ):
        sa_class = "metric-value-green" if is_running else ""
        eff_str = f"+{eff_val}%" if is_running else "-- %"
        s_delay_str = (
            f"{s_delay} <span style='font-size:14px;'>s</span>"
            if (is_running or s_delay != "--")
            else "-- s"
        )

        p_kpis.markdown(
            f"""
            <div class="metrics-container">
                <div class="metric-card">
                    <div class="metric-icon">🔴</div>
                    <div class="metric-label">Sistem Statis</div>
                    <div class="metric-value metric-value-red">{b_delay} <span style="font-size:14px;">s</span></div>
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
            # Lakukan 8 pencarian per tingkat suhu agar algoritma konvergen secara optimal
            for _ in range(8):
                step += 1

                # Logika Neighbor Generation
                neighbor = list(current_state)
                i, j = random.sample(range(4), 2)
                delta = random.choice([2, 3, 4, 5])

                if neighbor[i] - delta >= 10 and neighbor[j] + delta <= 60:
                    neighbor[i] -= delta
                    neighbor[j] += delta

                neighbor_delay = calculate_delay(neighbor, demands)
                diff = neighbor_delay - current_delay

                # Logika Metropolis Criterion
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

            # UPDATE ALOKASI HIJAU REALTIME (Gunakan best_state)
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