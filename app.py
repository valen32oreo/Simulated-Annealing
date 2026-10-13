import math
import random
import time
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

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
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Container Spacing & Layout Responsif */
    .block-container {
        padding-top: 3.5rem !important;
        padding-bottom: 2rem;
        padding-left: 1.25rem;
        padding-right: 1.25rem;
    }

    /* Header Banner Responsif */
    .header-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        display: flex;
        gap: 16px;
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
        font-size: 11px;
        font-weight: 700;
        color: #2563eb;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin: 0;
    }

    .header-title {
        font-size: 22px !important;
        font-weight: 800 !important;
        line-height: 1.3 !important;
        color: #0f172a !important;
        margin: 0 !important;
        letter-spacing: -0.02em !important;
    }

    .header-title i {
        color: #2563eb;
        font-style: normal;
    }

    .header-subtitle {
        font-size: 13px;
        line-height: 1.5;
        color: #64748b;
        margin: 2px 0 0 0;
    }

    /* Metric Cards Grid Responsif */
    .metrics-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin-bottom: 20px;
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 14px 16px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
    }

    .metric-label {
        font-size: 11px;
        color: #64748b;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .metric-value {
        font-size: 24px;
        color: #0f172a;
        font-weight: 800;
        margin-top: 4px;
        line-height: 1.1;
    }

    .metric-value-red { color: #dc2626; }
    .metric-value-green { color: #16a34a; }
    .metric-value-blue { color: #2563eb; }

    /* Direction Status Cards */
    .phase-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
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

    .phase-badge {
        font-size: 12px;
        font-weight: 800;
        color: #2563eb;
        background: #eff6ff;
        padding: 2px 8px;
        border-radius: 6px;
        border: 1px solid #bfdbfe;
    }

    /* Media Queries untuk Mobile */
    @media (max-width: 768px) {
        .block-container {
            padding-top: 5rem !important;
            padding-left: 0.75rem;
            padding-right: 0.75rem;
        }

        .header-card {
            flex-direction: column;
            padding: 14px 16px;
            gap: 10px;
        }

        .accent-bar {
            width: 100%;
            height: 3px;
        }

        .header-title {
            font-size: 18px !important;
        }

        .header-subtitle {
            font-size: 12px;
        }

        .metrics-container {
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
        }

        .metric-card {
            padding: 10px 12px;
        }

        .metric-label {
            font-size: 10px;
        }

        .metric-value {
            font-size: 18px;
        }
    }

    @media (max-width: 480px) {
        .metrics-container {
            grid-template-columns: repeat(2, 1fr);
            gap: 6px;
        }

        .metric-card {
            padding: 8px 10px;
        }

        .metric-value {
            font-size: 16px;
        }
    }

    /* Sidebar Styling Responsif */
    div[data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }

    .sidebar-title {
        font-size: 15px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 4px;
    }

    .sidebar-desc {
        font-size: 12px;
        color: #64748b;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid #e2e8f0;
    }

    .sidebar-tag {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #2563eb;
        margin-top: 16px;
        margin-bottom: 8px;
    }

    .stButton>button {
        border-radius: 8px;
        font-weight: 700;
        font-size: 14px;
        padding: 10px 16px;
        background: #2563eb;
        border: none;
        color: #ffffff;
    }

    .stButton>button:hover {
        background: #1d4ed8;
    }

    </style>
""",
    unsafe_allow_html=True,
)


# FUNGSI RENDER VISUALISASI CANVAS PERSIMPANGAN RESPONSIF
def render_traffic_animation(green_times, demands):
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{
                box-sizing: border-box;
            }}
            body {{
                margin: 0;
                padding: 0;
                background: #090d16;
                font-family: 'Inter', system-ui, -apple-system, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                color: #f8fafc;
                overflow: hidden;
            }}
            #canvas-container {{
                position: relative;
                width: 100%;
                max-width: 680px;
                height: 400px;
                background: #090d16;
                border-radius: 10px;
                overflow: hidden;
                border: 1px solid #1e293b;
            }}
            canvas {{
                width: 100%;
                height: 100%;
                display: block;
            }}
            .info-panel {{
                position: absolute;
                top: 10px;
                left: 10px;
                right: 10px;
                background: rgba(15, 23, 42, 0.92);
                border: 1px solid #334155;
                padding: 6px 12px;
                border-radius: 8px;
                font-size: 11px;
                font-weight: 600;
                display: flex;
                justify-content: space-between;
                align-items: center;
                z-index: 10;
                flex-wrap: wrap;
                gap: 6px;
            }}
            .status-badge {{
                display: inline-block;
                width: 8px;
                height: 8px;
                border-radius: 50%;
                margin-right: 4px;
            }}
            .lane-hud {{
                position: absolute;
                background: rgba(15, 23, 42, 0.88);
                border: 1px solid #334155;
                color: #f8fafc;
                padding: 3px 6px;
                border-radius: 5px;
                font-size: 10px;
                font-weight: 700;
                pointer-events: none;
                z-index: 5;
            }}
            #hud-north {{ top: 46px; right: 10px; border-left: 3px solid #ef4444; }}
            #hud-south {{ bottom: 10px; left: 10px; border-left: 3px solid #3b82f6; }}
            #hud-east  {{ bottom: 10px; right: 10px; border-left: 3px solid #f59e0b; }}
            #hud-west  {{ top: 46px; left: 10px; border-left: 3px solid #10b981; }}

            @media (max-width: 480px) {{
                #canvas-container {{
                    height: 340px;
                }}
                .info-panel {{
                    font-size: 10px;
                    padding: 4px 8px;
                }}
                .lane-hud {{
                    font-size: 9px;
                    padding: 2px 4px;
                }}
                #hud-north {{ top: 42px; right: 6px; }}
                #hud-west  {{ top: 42px; left: 6px; }}
                #hud-south {{ bottom: 6px; left: 6px; }}
                #hud-east  {{ bottom: 6px; right: 6px; }}
            }}
        </style>
    </head>
    <body>
        <div id="canvas-container">
            <div class="info-panel">
                <span><span class="status-badge" id="badge-color" style="background:#10b981;"></span><span id="active-text">Lajur Aktif: Utara</span></span>
                <span id="timer-text" style="color:#38bdf8;">Sisa Hijau: --s</span>
                <span id="queue-text" style="color:#94a3b8;">Antrean: 0 kend</span>
            </div>

            <div class="lane-hud" id="hud-north">Utara: {green_times[0]}s ({demands[0]} kend/m)</div>
            <div class="lane-hud" id="hud-south">Selatan: {green_times[1]}s ({demands[1]} kend/m)</div>
            <div class="lane-hud" id="hud-east">Timur: {green_times[2]}s ({demands[2]} kend/m)</div>
            <div class="lane-hud" id="hud-west">Barat: {green_times[3]}s ({demands[3]} kend/m)</div>

            <canvas id="trafficCanvas" width="680" height="400"></canvas>
        </div>

        <script>
            const canvas = document.getElementById('trafficCanvas');
            const ctx = canvas.getContext('2d');
            
            const greenTimes = {green_times}; // [Utara, Selatan, Timur, Barat]
            const demands = {demands};       // [Utara, Selatan, Timur, Barat]
            const yellowTime = 4;

            const W = 680, H = 400;
            const roadW = 90;
            const cx = W / 2, cy = H / 2;

            let currentPhase = 0; // 0: Utara, 1: Selatan, 2: Timur, 3: Barat
            let phaseState = 'GREEN';
            let timer = greenTimes[0];
            let cars = [];

            class Car {{
                constructor(dir) {{
                    this.dir = dir; 
                    this.speed = 2.4;
                    this.stopped = false;
                    this.w = (dir === 0 || dir === 1) ? 14 : 24;
                    this.h = (dir === 0 || dir === 1) ? 24 : 14;

                    if (dir === 0) {{ this.x = cx - 22; this.y = -30; }}
                    else if (dir === 1) {{ this.x = cx + 22; this.y = H + 30; }}
                    else if (dir === 2) {{ this.x = W + 30; this.y = cy - 22; }}
                    else if (dir === 3) {{ this.x = -30; this.y = cy + 22; }}
                }}

                move() {{
                    let stopY_North = cy - roadW/2 - 16;
                    let stopY_South = cy + roadW/2 + 16;
                    let stopX_East  = cx + roadW/2 + 16;
                    let stopX_West  = cx - roadW/2 - 16;

                    let isGreen = (currentPhase === this.dir && phaseState === 'GREEN');

                    this.stopped = false;
                    if (!isGreen) {{
                        if (this.dir === 0 && this.y < stopY_North && this.y + this.speed >= stopY_North) this.stopped = true;
                        if (this.dir === 1 && this.y > stopY_South && this.y - this.speed <= stopY_South) this.stopped = true;
                        if (this.dir === 2 && this.x > stopX_East  && this.x - this.speed <= stopX_East)  this.stopped = true;
                        if (this.dir === 3 && this.x < stopX_West  && this.x + this.speed >= stopX_West)  this.stopped = true;
                    }}

                    cars.forEach(other => {{
                        if (other !== this && other.dir === this.dir && other.stopped) {{
                            if (this.dir === 0 && this.y < other.y && other.y - this.y < 30) this.stopped = true;
                            if (this.dir === 1 && this.y > other.y && this.y - other.y < 30) this.stopped = true;
                            if (this.dir === 2 && this.x > other.x && this.x - other.x < 30) this.stopped = true;
                            if (this.dir === 3 && this.x < other.x && other.x - this.x < 30) this.stopped = true;
                        }}
                    }});

                    if (!this.stopped) {{
                        if (this.dir === 0) this.y += this.speed;
                        if (this.dir === 1) this.y -= this.speed;
                        if (this.dir === 2) this.x -= this.speed;
                        if (this.dir === 3) this.x += this.speed;
                    }}
                }}

                draw() {{
                    ctx.save();
                    ctx.translate(this.x, this.y);
                    
                    ctx.fillStyle = this.dir === 0 ? '#ef4444' : this.dir === 1 ? '#3b82f6' : this.dir === 2 ? '#f59e0b' : '#10b981';
                    ctx.beginPath();
                    ctx.roundRect(-this.w/2, -this.h/2, this.w, this.h, 3);
                    ctx.fill();

                    ctx.fillStyle = '#0f172a';
                    if (this.dir === 0) ctx.fillRect(-this.w/2 + 2, 2, this.w - 4, 4);
                    if (this.dir === 1) ctx.fillRect(-this.w/2 + 2, -6, this.w - 4, 4);
                    if (this.dir === 2) ctx.fillRect(-6, -this.h/2 + 2, 4, this.h - 4);
                    if (this.dir === 3) ctx.fillRect(2, -this.h/2 + 2, 4, this.h - 4);

                    ctx.restore();
                }}
            }}

            setInterval(() => {{
                for (let i = 0; i < 4; i++) {{
                    if (Math.random() < (demands[i] / 110)) {{
                        cars.push(new Car(i));
                    }}
                }}
            }}, 650);

            setInterval(() => {{
                timer--;
                if (timer <= 0) {{
                    if (phaseState === 'GREEN') {{
                        phaseState = 'YELLOW';
                        timer = yellowTime;
                    }} else {{
                        phaseState = 'GREEN';
                        currentPhase = (currentPhase + 1) % 4;
                        timer = greenTimes[currentPhase];
                    }}
                }}
                
                const dirs = ["Utara", "Selatan", "Timur", "Barat"];
                document.getElementById('active-text').innerText = `Aktif: ${{dirs[currentPhase]}} (${{phaseState}})`;
                document.getElementById('timer-text').innerText = `Sisa: ${{timer}}s`;
                document.getElementById('badge-color').style.background = phaseState === 'GREEN' ? '#10b981' : '#f59e0b';
                
                let queued = cars.filter(c => c.stopped).length;
                document.getElementById('queue-text').innerText = `Antrean: ${{queued}} kend`;
            }}, 1000);

            function drawZebra(x, y, w, h, vertical) {{
                ctx.fillStyle = '#475569';
                let count = 5;
                for(let i = 0; i < count; i++) {{
                    if(vertical) ctx.fillRect(x + (i * (w/count)), y, w/(count*2), h);
                    else ctx.fillRect(x, y + (i * (h/count)), w, h/(count*2));
                }}
            }}

            function drawTrafficLightPost(x, y, color) {{
                ctx.fillStyle = '#0f172a';
                ctx.fillRect(x - 8, y - 8, 16, 16);
                ctx.strokeStyle = '#334155';
                ctx.lineWidth = 1;
                ctx.strokeRect(x - 8, y - 8, 16, 16);

                ctx.fillStyle = color;
                ctx.beginPath();
                ctx.arc(x, y, 5, 0, Math.PI * 2);
                ctx.fill();
            }}

            function animate() {{
                ctx.clearRect(0, 0, W, H);

                ctx.fillStyle = '#0f172a';
                ctx.fillRect(0, 0, W, H);

                ctx.fillStyle = '#1e293b';
                ctx.fillRect(cx - roadW/2, 0, roadW, H);
                ctx.fillRect(0, cy - roadW/2, W, roadW);

                drawZebra(cx - roadW/2, cy - roadW/2 - 16, roadW, 12, true);
                drawZebra(cx - roadW/2, cy + roadW/2 + 4, roadW, 12, true);
                drawZebra(cx - roadW/2 - 16, cy - roadW/2, 12, roadW, false);
                drawZebra(cx + roadW/2 + 4, cy - roadW/2, 12, roadW, false);

                ctx.strokeStyle = '#475569';
                ctx.lineWidth = 2;
                ctx.setLineDash([8, 8]);
                ctx.beginPath();
                ctx.moveTo(cx, 0); ctx.lineTo(cx, cy - roadW/2 - 16);
                ctx.moveTo(cx, cy + roadW/2 + 16); ctx.lineTo(cx, H);
                ctx.moveTo(0, cy); ctx.lineTo(cx - roadW/2 - 16, cy);
                ctx.moveTo(cx + roadW/2 + 16, cy); ctx.lineTo(W, cy);
                ctx.stroke();

                const lights = [0,1,2,3].map(i => {{
                    if (i === currentPhase) return phaseState === 'GREEN' ? '#10b981' : '#f59e0b';
                    return '#ef4444';
                }});

                drawTrafficLightPost(cx - roadW/2 - 14, cy - roadW/2 - 14, lights[0]);
                drawTrafficLightPost(cx + roadW/2 + 14, cy + roadW/2 + 14, lights[1]);
                drawTrafficLightPost(cx + roadW/2 + 14, cy - roadW/2 - 14, lights[2]);
                drawTrafficLightPost(cx - roadW/2 - 14, cy + roadW/2 + 14, lights[3]);

                cars.forEach((car, index) => {{
                    car.move();
                    car.draw();
                    if (car.x < -50 || car.x > W + 50 || car.y < -50 || car.y > H + 50) {{
                        cars.splice(index, 1);
                    }}
                }});

                requestAnimationFrame(animate);
            }}

            animate();
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=410)


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
                <p class="header-eyebrow">Kelompok 1 • Kompleksitas Algoritma</p>
                <h1 class="header-title">
                    Pengaturan Lampu Lalu Lintas Adaptif dengan <i>Simulated Annealing</i>
                </h1>
                <p class="header-subtitle">
                    Optimasi alokasi waktu hijau untuk meminimalkan rata-rata waktu tunggu kendaraan di persimpangan 4 lajur.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # SIDEBAR CONTROL PANEL
    st.sidebar.markdown(
        """
        <div class="sidebar-title">Panel Kontrol Simulasi</div>
        <div class="sidebar-desc">Pengaturan skenario kepadatan & parameter algoritma</div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown('<div class="sidebar-tag">01. Skenario Lalu Lintas</div>', unsafe_allow_html=True)
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

    st.sidebar.markdown('<div class="sidebar-tag">02. Parameter Algoritma</div>', unsafe_allow_html=True)
    t_0 = st.sidebar.slider("Suhu Awal (T₀)", 50.0, 300.0, 100.0, step=10.0, help="Suhu tinggi memperluas eksplorasi acak di awal pencarian.")
    alpha = st.sidebar.slider("Laju Pendinginan (α)", 0.80, 0.99, 0.92, step=0.01, help="Mengontrol kecepatan transisi menuju pencarian lokal.")

    st.sidebar.markdown('<div class="sidebar-tag">03. Landasan Teori</div>', unsafe_allow_html=True)
    with st.sidebar.expander("Landasan Teori Algoritma"):
        st.markdown("""
        *Simulated Annealing (SA)* mensimulasikan proses pendinginan logam untuk menemukan solusi optimal global:

        - **State ($S$)**: Alokasi waktu sinyal hijau 4 lajur.
        - **Cost / Fungsi Biaya ($E$)**: Rata-rata waktu tunggu kendaraan (detik).
        - **Suhu ($T$)**: Mengontrol eksploitasi vs eksplorasi untuk menghindari *local optima*.
        - **Pendinginan (α)**: Mengontrol transisi pencarian ($P = e^{-\\Delta E / T}$).
        """)

    # BASELINE COMPUTATION
    fixed_state = [25, 25, 25, 25]
    baseline_delay = calculate_delay(fixed_state, demands)

    # SESSION STATE INITIALIZATION FOR SYNCHRONIZATION
    if "best_state" not in st.session_state or st.session_state.get("last_scenario") != scenario:
        st.session_state.best_state = list(fixed_state)
        st.session_state.best_delay = baseline_delay
        st.session_state.is_optimized = False
        st.session_state.last_scenario = scenario

    # METRIC CARDS PLACEHOLDER
    p_kpis = st.empty()

    st.markdown("<br>", unsafe_allow_html=True)

    # LAYOUT UTAMA: GRAFIK & ALOKASI
    col_left, col_right = st.columns([1.5, 1])

    with col_left:
        st.markdown("##### 📈 Konvergensi Optimasi Waktu Tunggu")
        p_chart = st.empty()

    with col_right:
        st.markdown("##### ⏱️ Alokasi Sinyal Hijau Optimal")
        p_alloc = st.empty()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("##### 🚦 Visualisasi Animasi Persimpangan Real-Time")
    p_anim = st.empty()

    # RENDER METRIC CARDS
    def render_kpis(b_delay, s_delay="--", eff_val="--", temp_val=t_0, is_running=False):
        sa_class = "metric-value-green" if is_running or st.session_state.is_optimized else ""
        eff_str = f"+{eff_val}%" if is_running or st.session_state.is_optimized else "-- %"
        s_delay_str = f"{s_delay} <span style='font-size:13px;'>s</span>" if (is_running or st.session_state.is_optimized) else "-- s"

        p_kpis.markdown(
            f"""
            <div class="metrics-container">
                <div class="metric-card">
                    <div class="metric-label">Sistem Statis</div>
                    <div class="metric-value metric-value-red">{b_delay} <span style="font-size:13px;">s</span></div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Hasil Optimal SA</div>
                    <div class="metric-value {sa_class}">{s_delay_str}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Efisiensi</div>
                    <div class="metric-value metric-value-green">{eff_str}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Suhu Sistem (T)</div>
                    <div class="metric-value metric-value-blue">{temp_val:.1f}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # INITIAL CHART PLACEHOLDER
    fig_init = go.Figure()
    fig_init.add_trace(
        go.Scatter(
            x=[0],
            y=[baseline_delay],
            mode="lines+markers",
            name="Lampu Statis (Baseline)",
            line=dict(color="#dc2626", width=2, dash="dash"),
        )
    )
    fig_init.update_layout(
        height=310,
        margin=dict(l=15, r=15, t=15, b=15),
        xaxis_title="Iterasi (Langkah Optimasi)",
        yaxis_title="Rata-rata Waktu Tunggu (Detik)",
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    p_chart.plotly_chart(fig_init, use_container_width=True, config={'displayModeBar': False})

    # TOMBOL EKSEKUSI
    if st.button("Jalankan Optimasi Simulated Annealing", type="primary", use_container_width=True):
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

            eff = round(((baseline_delay - best_delay) / baseline_delay) * 100, 1)
            render_kpis(baseline_delay, s_delay=best_delay, eff_val=eff, temp_val=T, is_running=True)

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
                    line=dict(color="#16a34a", width=3),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=history["x"],
                    y=[baseline_delay] * len(history["x"]),
                    mode="lines",
                    name="Lampu Statis (Baseline)",
                    line=dict(color="#dc2626", width=2, dash="dash"),
                )
            )

            fig.update_layout(
                height=310,
                margin=dict(l=15, r=15, t=15, b=15),
                xaxis_title="Iterasi (Langkah Optimasi)",
                yaxis_title="Rata-rata Waktu Tunggu (Detik)",
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
                hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            )
            p_chart.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            phases = [
                ("Lajur Utara", demands[0], best_state[0]),
                ("Lajur Selatan", demands[1], best_state[1]),
                ("Lajur Timur", demands[2], best_state[2]),
                ("Lajur Barat", demands[3], best_state[3]),
            ]
            with p_alloc.container():
                for label, dem, val in phases:
                    st.markdown(
                        f"""
                        <div class="phase-card">
                            <div class="phase-title">
                                <span>{label} <small style="color:#64748b; font-weight:normal;">({dem} kend/mnt)</small></span>
                                <span class="phase-badge">{val} detik</span>
                            </div>
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )
                    st.progress(val / 100)

            time.sleep(0.01)

        # SIMPAN STATE TERBAIK KE SESSION STATE
        st.session_state.best_state = list(best_state)
        st.session_state.best_delay = best_delay
        st.session_state.is_optimized = True

    # RENDER METRIK & ALOKASI DARI SESSION STATE (SINKRON 100%)
    if st.session_state.is_optimized:
        eff_final = round(((baseline_delay - st.session_state.best_delay) / baseline_delay) * 100, 1)
        render_kpis(baseline_delay, s_delay=st.session_state.best_delay, eff_val=eff_final, temp_val=0.5, is_running=False)

        phases_final = [
            ("Lajur Utara", demands[0], st.session_state.best_state[0]),
            ("Lajur Selatan", demands[1], st.session_state.best_state[1]),
            ("Lajur Timur", demands[2], st.session_state.best_state[2]),
            ("Lajur Barat", demands[3], st.session_state.best_state[3]),
        ]
        with p_alloc.container():
            for label, dem, val in phases_final:
                st.markdown(
                    f"""
                    <div class="phase-card">
                        <div class="phase-title">
                            <span>{label} <small style="color:#64748b; font-weight:normal;">({dem} kend/mnt)</small></span>
                            <span class="phase-badge">{val} detik</span>
                        </div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
                st.progress(val / 100)

        with p_anim.container():
            render_traffic_animation(st.session_state.best_state, demands)
    else:
        render_kpis(baseline_delay)
        phases_init = [
            ("Lajur Utara", demands[0], fixed_state[0]),
            ("Lajur Selatan", demands[1], fixed_state[1]),
            ("Lajur Timur", demands[2], fixed_state[2]),
            ("Lajur Barat", demands[3], fixed_state[3]),
        ]
        with p_alloc.container():
            for label, dem, val in phases_init:
                st.markdown(
                    f"""
                    <div class="phase-card">
                        <div class="phase-title">
                            <span>{label} <small style="color:#64748b; font-weight:normal;">({dem} kend/mnt)</small></span>
                            <span class="phase-badge">{val} detik</span>
                        </div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
                st.progress(val / 100)

        with p_anim.container():
            render_traffic_animation(fixed_state, demands)


if __name__ == "__main__":
    main()