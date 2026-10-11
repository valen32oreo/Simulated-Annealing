import math
import random
import matplotlib.pyplot as plt


class TrafficSignalOptimizerSA:

    def __init__(
        self,
        queues,
        arrival_rates,
        discharge_rate=0.5,
        g_min=10,
        g_max=90,
        yellow_time=4,
    ):
        self.queues = queues
        self.arrival_rates = arrival_rates
        self.discharge_rate = discharge_rate
        self.g_min = g_min
        self.g_max = g_max
        self.yellow_time = yellow_time
        self.num_phases = len(queues)

    def calculate_cost(self, state):
        total_cycle_time = sum(state) + (self.num_phases * self.yellow_time)
        total_delay_penalty = 0

        for i in range(self.num_phases):
            green = state[i]
            q_initial = self.queues[i]
            arrival_rate = self.arrival_rates[i]

            total_vehicles = q_initial + (arrival_rate * total_cycle_time)
            served_vehicles = green * self.discharge_rate
            remaining_queue = max(0.0, total_vehicles - served_vehicles)

            total_delay_penalty += (remaining_queue**2) + (
                remaining_queue * 10
            )

        return total_delay_penalty

    def get_neighbor(self, current_state):
        neighbor = list(current_state)
        idx1, idx2 = random.sample(range(self.num_phases), 2)
        delta = random.choice([-5, -3, -2, 2, 3, 5])

        neighbor[idx1] = max(
            self.g_min, min(self.g_max, neighbor[idx1] + delta)
        )
        neighbor[idx2] = max(
            self.g_min, min(self.g_max, neighbor[idx2] - delta)
        )

        return neighbor

    def optimize(self, t_initial=100.0, t_min=0.01, alpha=0.92, max_iter=40):
        current_state = [
            random.randint(self.g_min, 40) for _ in range(self.num_phases)
        ]
        current_cost = self.calculate_cost(current_state)

        best_state = list(current_state)
        best_cost = current_cost

        t = t_initial
        step = 0

        # Struktur data untuk menyimpan histori per iterasi
        history_steps = []
        history_current_cost = []
        history_best_cost = []
        history_temp = []

        print("=== Memulai Optimasi Simulated Annealing ===")
        print(f"Solusi Awal  : {current_state} | Cost Awal: {current_cost:.2f}")
        print("-" * 55)

        while t > t_min:
            for _ in range(max_iter):
                neighbor_state = self.get_neighbor(current_state)
                neighbor_cost = self.calculate_cost(neighbor_state)

                delta_e = neighbor_cost - current_cost

                if delta_e < 0:
                    accept = True
                else:
                    probability = math.exp(-delta_e / t)
                    accept = random.random() < probability

                if accept:
                    current_state = neighbor_state
                    current_cost = neighbor_cost

                    if current_cost < best_cost:
                        best_state = list(current_state)
                        best_cost = current_cost

            # Rekam statistik di akhir tiap tingkat suhu
            history_steps.append(step)
            history_current_cost.append(current_cost)
            history_best_cost.append(best_cost)
            history_temp.append(t)

            t *= alpha
            step += 1

            if step % 10 == 0 or t <= t_min:
                print(
                    f"Iterasi {step:3d} | Suhu: {t:6.2f} | Best State: {best_state} | Best Cost: {best_cost:.2f}"
                )

        print("-" * 55)
        print("=== Optimasi Selesai ===")

        history_data = {
            "steps": history_steps,
            "current_cost": history_current_cost,
            "best_cost": history_best_cost,
            "temp": history_temp,
        }

        return best_state, best_cost, history_data


def plot_convergence(history, fixed_cost=None):
    """Visualisasi Grafik Konvergensi Cost vs Iterasi & Penurunan Suhu"""
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # Sumbu Y Kiri: Cost / Delay Penalty
    color = "tab:blue"
    ax1.set_xlabel("Iterasi Penurunan Suhu", fontsize=11, fontweight="bold")
    ax1.set_ylabel(
        "Cost (Penalti Waktu Tunggu)",
        color=color,
        fontsize=11,
        fontweight="bold",
    )

    (line1,) = ax1.plot(
        history["steps"],
        history["current_cost"],
        label="Current Cost (Fluktuasi Eksplorasi)",
        color="skyblue",
        linestyle="--",
        alpha=0.7,
    )
    (line2,) = ax1.plot(
        history["steps"],
        history["best_cost"],
        label="Best Cost (Solusi Terbaik SA)",
        color="blue",
        linewidth=2.5,
    )

    lines = [line1, line2]

    if fixed_cost is not None:
        line_baseline = ax1.axhline(
            y=fixed_cost,
            color="red",
            linestyle=":",
            linewidth=2,
            label=f"Lampu Statis / Baseline ({fixed_cost:.1f})",
        )
        lines.append(line_baseline)

    ax1.tick_params(axis="y", labelcolor=color)
    ax1.grid(True, linestyle="--", alpha=0.5)

    # Sumbu Y Kanan: Suhu (T)
    ax2 = ax1.twinx()
    color = "tab:orange"
    ax2.set_ylabel(
        "Suhu / Temperature (T)", color=color, fontsize=11, fontweight="bold"
    )
    (line3,) = ax2.plot(
        history["steps"],
        history["temp"],
        label="Suhu (T)",
        color=color,
        linestyle="-.",
        linewidth=1.8,
    )
    ax2.tick_params(axis="y", labelcolor=color)

    lines.append(line3)

    # Menampilkan Legend Gabungan
    labels = [l.get_label() for l in lines]
    ax1.legend(
        lines,
        labels,
        loc="center right",
        frameon=True,
        facecolor="white",
        framealpha=0.9,
    )

    plt.title(
        "Grafik Konvergensi Simulated Annealing pada Lampu Lalu Lintas Adaptif",
        fontsize=12,
        fontweight="bold",
        pad=15,
    )
    plt.tight_layout()
    plt.show()


# =====================================================================
# MAIN PROGRAM
# =====================================================================
if __name__ == "__main__":
    sensor_queues = [45, 10, 50, 12]
    sensor_arrivals = [0.35, 0.08, 0.40, 0.10]

    optimizer = TrafficSignalOptimizerSA(
        queues=sensor_queues,
        arrival_rates=sensor_arrivals,
        g_min=10,
        g_max=90,
    )

    # Jalankan Optimasi
    optimal_green_times, optimal_cost, history = optimizer.optimize(
        t_initial=100.0, t_min=0.01, alpha=0.92, max_iter=40
    )

    fixed_timing = [30, 30, 30, 30]
    fixed_cost = optimizer.calculate_cost(fixed_timing)

    # Tampilkan Grafik
    plot_convergence(history, fixed_cost=fixed_cost)