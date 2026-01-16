import io
from typing import Optional

import matplotlib

matplotlib.use("Agg")

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from storage.user import get_daily_logs, get_user


def create_progress_graph(user_id: int, days: int = 7) -> Optional[io.BytesIO]:
    user = get_user(user_id)

    dates, water_data, calories_data, burned_calories_data = get_daily_logs(
        user_id, days
    )

    fig, ax1 = plt.subplots(figsize=(10, 6))
    fig.suptitle("📊 Общий прогресс", fontsize=16, fontweight="bold")

    ax1.plot(
        dates,
        calories_data,
        marker="o",
        linewidth=2,
        color="#E24A4A",
        label="Съедено (ккал)",
    )

    ax1.plot(
        dates,
        burned_calories_data,
        marker="s",
        linewidth=2,
        color="#4AE24A",
        label="Сожжено (ккал)",
    )

    balance_data = [c - b for c, b in zip(calories_data, burned_calories_data)]

    ax1.plot(
        dates,
        balance_data,
        marker="^",
        linewidth=2,
        color="#E2A84A",
        label="Баланс (ккал)",
    )

    if user.get("calorie_goal"):
        ax1.axhline(
            y=user["calorie_goal"],
            color="#E24A4A",
            linestyle="--",
            alpha=0.5,
            label=f"Цель: {user['calorie_goal']:.0f} ккал",
        )

    ax1.set_ylabel("Калории (ккал)", fontsize=12, color="#E24A4A")
    ax1.tick_params(axis="y", labelcolor="#E24A4A")
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()

    ax2.plot(
        dates,
        water_data,
        marker="o",
        linewidth=2,
        linestyle="-",
        color="#4A90E2",
        label="Вода (мл)",
    )

    if user.get("water_goal"):
        ax2.axhline(
            y=user["water_goal"],
            color="#4A90E2",
            linestyle="--",
            alpha=0.5,
            label=f"Цель: {user['water_goal']:.0f} мл",
        )

    ax2.set_ylabel("Вода (мл)", fontsize=12, color="#4A90E2")
    ax2.tick_params(axis="y", labelcolor="#4A90E2")

    ax1.set_xlabel("Дата", fontsize=12)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha="right")

    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()

    ax1.legend(
        lines_1 + lines_2,
        labels_1 + labels_2,
        loc="upper left",
        bbox_to_anchor=(0, 1.15),
        ncol=2,
        fontsize=9,
    )

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)

    return buf
