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

    /* Container Spacing & Layout */
    .block-container {
        padding-top: 3.5rem !important;
        padding-bottom: 2rem;
        padding-left: 1.25rem;
        padding-right: 1.25rem;
    }

    /* Banner Gambar */
    div[data-testid="stImage"] {
        width: 100% !important;
        margin-bottom: 20px !important;
    }

    div[data-testid="stImage"] > img {
        width: 100% !important;
        height: auto !important;
        max-height: 220px !important; /* Mencegah gambar terlalu tinggi di layar ultra-wide */
        object-fit: cover !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
        display: block !important;
    }

    /* Penyesuaian Layar Tablet (Tablet Portrait & Landscape) */
    @media (max-width: 1024px) {
        div[data-testid="stImage"] > img {
            max-height: 180px !important;
            border-radius: 10px !important;
        }
    }

    /* Penyesuaian Layar Mobile (Smartphone) */
    @media (max-width: 768px) {
        div[data-testid="stImage"] {
            margin-bottom: 12px !important;
        }
        
        div[data-testid="stImage"] > img {
            max-height: 120px !important;
            border-radius: 8px !important;
            object-fit: contain !important; /* Memastikan seluruh isi banner tetap terlihat penuh di HP */
            background-color: #72aefd; /* Background penyelarasan warna banner */
        }
    }

    /* Metric Cards Grid */
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

    /* Media Queries untuk Mobile Optimization */
    @media (max-width: 768px) {
        .block-container {
            padding-top: 4rem !important;
            padding-left: 0.6rem !important;
            padding-right: 0.6rem !important;
        }

        .header-card {
            flex-direction: column;
            padding: 14px 16px;
            gap: 8px;
        }

        .accent-bar {
            width: 100%;
            height: 3px;
        }

        .header-title {
            font-size: 17px !important;
        }

        .header-subtitle {
            font-size: 11.5px;
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

    /* Sidebar Styling */
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


# FUNGSI RENDER VISUALISASI CANVAS
def render_traffic_animation(green_times, demands):
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <style>
        
            * {{ box-sizing: border-box; }}

            html, body {{
                margin: 0; padding: 0;
                width: 100%; height: 100%;
                background: #090d16;
                font-family: 'Inter', system-ui, -apple-system, sans-serif;
                overflow: hidden;
            }}

            #canvas-container {{
                position: relative;
                width: 100%; height: 100%;
                background: #090d16; border-radius: 10px;
                overflow: hidden; border: 1px solid #1e293b;
            }}

            canvas {{
                width: 100%; height: 100%;
                display: block;
            }}
            
            .info-panel {{
                position: absolute; top: 8px; left: 8px; right: 8px;
                background: rgba(15, 23, 42, 0.92);
                border: 1px solid #334155; padding: 6px 12px;
                border-radius: 6px; font-size: 11px; font-weight: 700;
                display: flex; justify-content: space-between; align-items: center;
                z-index: 20; box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                color: #f8fafc;
            }}

            .status-badge {{
                display: inline-block; width: 8px; height: 8px;
                border-radius: 50%; margin-right: 6px;
            }}

            .lane-hud {{
                position: absolute;
                background: rgba(15, 23, 42, 0.88);
                border: 1px solid #334155; color: #f8fafc;
                padding: 3px 6px; border-radius: 5px;
                font-size: 10px; font-weight: 700;
                pointer-events: none; z-index: 10;
                white-space: nowrap;
            }}

            #hud-north {{ top: 46px; right: 8px; border-left: 3px solid #38bdf8; }}
            #hud-south {{ bottom: 8px; left: 8px; border-left: 3px solid #38bdf8; }}
            #hud-east  {{ bottom: 8px; right: 8px; border-left: 3px solid #38bdf8; }}
            #hud-west  {{ top: 46px; left: 8px; border-left: 3px solid #38bdf8; }}

            @media (max-width: 480px) {{
                .info-panel {{ font-size: 9.5px; padding: 4px 8px; }}
                .lane-hud {{ font-size: 8.5px; padding: 2px 4px; }}
                #hud-north {{ top: 38px; }}
                #hud-west  {{ top: 38px; }}
            }}

        </style>
    </head>
    <body>
        <div id="canvas-container">
            <div class="info-panel">
                <span><span class="status-badge" id="badge-color" style="background:#10b981;"></span><span id="active-text">Sinyal Aktif: Utara</span></span>
                <span id="timer-text" style="color:#38bdf8;">Sisa: --s</span>
                <span id="queue-text" style="color:#94a3b8;">Antrean: 0</span>
            </div>

            <div class="lane-hud" id="hud-north">Utara: {green_times[0]}s ({demands[0]} kend/menit)</div>
            <div class="lane-hud" id="hud-south">Selatan: {green_times[1]}s ({demands[1]} kend/menit)</div>
            <div class="lane-hud" id="hud-east">Timur: {green_times[2]}s ({demands[2]} kend/menit)</div>
            <div class="lane-hud" id="hud-west">Barat: {green_times[3]}s ({demands[3]} kend/menit)</div>

            <canvas id="trafficCanvas"></canvas>
        </div>

        <script>
            const canvas = document.getElementById('trafficCanvas');
            const ctx = canvas.getContext('2d');
            const container = document.getElementById('canvas-container');

            const greenTimes = {green_times};
            const demands = {demands};
            const yellowTime = 4;

            let W = 680, H = 360;
            let roadW = 80;
            let cx = W / 2, cy = H / 2;

            function updateCanvasSize() {{
                W = container.clientWidth;
                H = container.clientHeight;
                canvas.width = W;
                canvas.height = H;
                roadW = Math.min(80, W * 0.18);
                cx = W / 2;
                cy = H / 2 + (W < 480 ? 12 : 10);
            }}

            window.addEventListener('resize', updateCanvasSize);
            updateCanvasSize();

            let currentPhase = 0;
            let phaseState = 'GREEN';
            let timer = greenTimes[0];
            let cars = [];

            const carColors = ['#e2e8f0', '#cbd5e1', '#94a3b8', '#64748b', '#38bdf8'];

            class Car {{
                constructor(dir) {{
                    this.dir = dir; 
                    this.speed = 2.2;
                    this.stopped = false;
                    this.color = carColors[Math.floor(Math.random() * carColors.length)];
                    this.w = (dir === 0 || dir === 1) ? 12 : 22;
                    this.h = (dir === 0 || dir === 1) ? 22 : 12;

                    if (dir === 0) {{ this.x = cx - roadW*0.25; this.y = 40; }}
                    else if (dir === 1) {{ this.x = cx + roadW*0.25; this.y = H + 30; }}
                    else if (dir === 2) {{ this.x = W + 30; this.y = cy - roadW*0.25; }}
                    else if (dir === 3) {{ this.x = -30; this.y = cy + roadW*0.25; }}
                }}

                move() {{
                    let stopY_North = cy - roadW/2 - 14;
                    let stopY_South = cy + roadW/2 + 14;
                    let stopX_East  = cx + roadW/2 + 14;
                    let stopX_West  = cx - roadW/2 - 14;

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
                            if (this.dir === 0 && this.y < other.y && other.y - this.y < 28) this.stopped = true;
                            if (this.dir === 1 && this.y > other.y && this.y - other.y < 28) this.stopped = true;
                            if (this.dir === 2 && this.x > other.x && this.x - other.x < 28) this.stopped = true;
                            if (this.dir === 3 && this.x < other.x && other.x - this.x < 28) this.stopped = true;
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
                    
                    ctx.fillStyle = this.color;
                    ctx.beginPath();
                    ctx.roundRect(-this.w/2, -this.h/2, this.w, this.h, 2);
                    ctx.fill();

                    ctx.fillStyle = '#0f172a';
                    if (this.dir === 0) ctx.fillRect(-this.w/2 + 2, 2, this.w - 4, 3);
                    if (this.dir === 1) ctx.fillRect(-this.w/2 + 2, -5, this.w - 4, 3);
                    if (this.dir === 2) ctx.fillRect(-5, -this.h/2 + 2, 3, this.h - 4);
                    if (this.dir === 3) ctx.fillRect(2, -this.h/2 + 2, 3, this.h - 4);

                    if (this.stopped) {{
                        ctx.fillStyle = '#ef4444';
                        if (this.dir === 0) {{ ctx.fillRect(-this.w/2, -this.h/2, 2, 2); ctx.fillRect(this.w/2 - 2, -this.h/2, 2, 2); }}
                        if (this.dir === 1) {{ ctx.fillRect(-this.w/2, this.h/2 - 2, 2, 2); ctx.fillRect(this.w/2 - 2, this.h/2 - 2, 2, 2); }}
                        if (this.dir === 2) {{ ctx.fillRect(this.w/2 - 2, -this.h/2, 2, 2); ctx.fillRect(this.w/2 - 2, this.h/2 - 2, 2, 2); }}
                        if (this.dir === 3) {{ ctx.fillRect(-this.w/2, -this.h/2, 2, 2); ctx.fillRect(-this.w/2, this.h/2 - 2, 2, 2); }}
                    }}

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
                ctx.fillStyle = '#334155';
                let count = 4;
                for(let i = 0; i < count; i++) {{
                    if(vertical) ctx.fillRect(x + (i * (w/count)), y, w/(count*2), h);
                    else ctx.fillRect(x, y + (i * (h/count)), w, h/(count*2));
                }}
            }}

            function drawTrafficLightPost(x, y, color) {{
                ctx.fillStyle = '#020617';
                ctx.fillRect(x - 7, y - 7, 14, 14);
                ctx.strokeStyle = '#475569';
                ctx.lineWidth = 1;
                ctx.strokeRect(x - 7, y - 7, 14, 14);

                ctx.fillStyle = color;
                ctx.beginPath();
                ctx.arc(x, y, 4.5, 0, Math.PI * 2);
                ctx.fill();
            }}

            function animate() {{
                ctx.clearRect(0, 0, W, H);

                ctx.fillStyle = '#090d16';
                ctx.fillRect(0, 0, W, H);

                ctx.fillStyle = '#1e293b';
                ctx.fillRect(cx - roadW/2, 40, roadW, H - 40);
                ctx.fillRect(0, cy - roadW/2, W, roadW);

                drawZebra(cx - roadW/2, cy - roadW/2 - 14, roadW, 10, true);
                drawZebra(cx - roadW/2, cy + roadW/2 + 4, roadW, 10, true);
                drawZebra(cx - roadW/2 - 14, cy - roadW/2, 10, roadW, false);
                drawZebra(cx + roadW/2 + 4, cy - roadW/2, 10, roadW, false);

                ctx.strokeStyle = '#475569';
                ctx.lineWidth = 1.5;
                ctx.setLineDash([6, 6]);
                ctx.beginPath();
                ctx.moveTo(cx, 40); ctx.lineTo(cx, cy - roadW/2 - 14);
                ctx.moveTo(cx, cy + roadW/2 + 14); ctx.lineTo(cx, H);
                ctx.moveTo(0, cy); ctx.lineTo(cx - roadW/2 - 14, cy);
                ctx.moveTo(cx + roadW/2 + 14, cy); ctx.lineTo(W, cy);
                ctx.stroke();

                const lights = [0,1,2,3].map(i => {{
                    if (i === currentPhase) return phaseState === 'GREEN' ? '#10b981' : '#f59e0b';
                    return '#ef4444';
                }});

                drawTrafficLightPost(cx - roadW/2 - 12, cy - roadW/2 - 12, lights[0]);
                drawTrafficLightPost(cx + roadW/2 + 12, cy + roadW/2 + 12, lights[1]);
                drawTrafficLightPost(cx + roadW/2 + 12, cy - roadW/2 - 12, lights[2]);
                drawTrafficLightPost(cx - roadW/2 - 12, cy + roadW/2 + 12, lights[3]);

                cars.forEach((car, index) => {{
                    car.move();
                    car.draw();
                    if (car.x < -40 || car.x > W + 40 || car.y < 20 || car.y > H + 40) {{
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
    components.html(html_code, height=360)


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
    st.image("assets/Traffic_Banner.webp", use_container_width=True)

    # SIDEBAR CONTROL PANEL
    st.sidebar.markdown(
        """
        <div class="sidebar-title">Panel Kontrol Simulasi</div>
        <div class="sidebar-desc">Pengaturan skenario kepadatan & parameter algoritma</div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown('<div class="sidebar-tag">Skenario Lalu Lintas</div>', unsafe_allow_html=True)
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

    st.sidebar.markdown('<div class="sidebar-tag">Parameter Algoritma</div>', unsafe_allow_html=True)
    t_0 = st.sidebar.slider("Suhu Awal (T₀)", 50.0, 300.0, 100.0, step=10.0, help="Suhu tinggi memperluas eksplorasi acak di awal pencarian.")
    alpha = st.sidebar.slider("Laju Pendinginan (α)", 0.80, 0.99, 0.92, step=0.01, help="Mengontrol kecepatan transisi menuju pencarian lokal.")

    st.sidebar.markdown('<div class="sidebar-tag">Landasan Teori</div>', unsafe_allow_html=True)
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

    # RENDER METRIK & ALOKASI DARI SESSION STATE
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