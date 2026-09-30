import matplotlib.pyplot as plt
import pandas as pd
import requests


def fetch_and_visualize_student_scores():
    api_url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(api_url, timeout=10)
    response.raise_for_status()
    raw_data = response.json()[:10]

    processed_records = []
    subjects = ["Cloud_Security", "Machine_Learning", "Algorithms"]

    for idx, item in enumerate(raw_data):
        user_id = f"Student_{item['userId']}_{idx+1}"
        scores = {
            "Student_ID": user_id,
            "Cloud_Security": 70 + (item["id"] * 3) % 28,
            "Machine_Learning": 65 + (item["id"] * 5) % 32,
            "Algorithms": 60 + (item["id"] * 7) % 35,
        }
        processed_records.append(scores)

    df = pd.DataFrame(processed_records)
    df["Average_Score"] = df[subjects].mean(axis=1)

    print("--- Processed Student Metrics ---")
    print(df[["Student_ID", *subjects, "Average_Score"]])
    cohort_mean = df["Average_Score"].mean()
    print(f"\nCohort Overall Average: {cohort_mean:.2f}")

    # Visualization
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(
        df["Student_ID"],
        df["Average_Score"],
        color="#2b5c8f",
        edgecolor="#1a365d",
        alpha=0.85,
    )

    ax.axhline(
        cohort_mean,
        color="#e53e3e",
        linestyle="--",
        linewidth=2,
        label=f"Cohort Mean ({cohort_mean:.1f})",
    )

    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height:.1f}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
        )

    ax.set_title(
        "Student Average Performance Across Security & ML Modules",
        fontsize=13,
        pad=15,
    )
    ax.set_xlabel("Student Identifier", fontsize=11)
    ax.set_ylabel("Average Score (%)", fontsize=11)
    ax.set_ylim(0, 110)
    ax.grid(axis="y", linestyle=":", alpha=0.6)
    ax.legend(loc="upper right")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig("student_performance_chart.png", dpi=300)
    print("\nChart saved as 'student_performance_chart.png'.")
    plt.show()


if __name__ == "__main__":
    fetch_and_visualize_student_scores()
