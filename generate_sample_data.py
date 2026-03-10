"""
Generate realistic sample data for CS Operations Dashboard.
Simulates a SaaS company's renewal, churn, and account data.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

# --- Configuration ---
NUM_ACCOUNTS = 250
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2026, 6, 30)

PRODUCTS = ["Sumo Logic Enterprise", "Sumo Logic Essentials", "Sumo Logic Flex", "Cloud SIEM", "Cloud SOAR"]
SEGMENTS = ["Enterprise", "Mid-Market", "SMB"]
INDUSTRIES = ["Technology", "Financial Services", "Healthcare", "Retail", "Manufacturing", "Media", "Government", "Education"]
REGIONS = ["North America", "EMEA", "APAC", "LATAM"]
CSM_NAMES = ["Sarah Chen", "Marcus Johnson", "Emily Rodriguez", "David Kim", "Rachel Foster",
             "James Thompson", "Lisa Wang", "Michael Brown", "Ana Garcia", "Chris Lee"]
TAE_NAMES = ["Tom Anderson", "Nina Patel", "Robert Wilson", "Maria Santos", "Alex Turner"]
HEALTH_SCORES = ["Healthy", "Needs Attention", "At Risk", "Critical"]
CHURN_REASONS = [
    "Budget Constraints", "Competitor Switch", "Product Fit", "Lack of Adoption",
    "Champion Left", "Merger/Acquisition", "Downsized", "Poor Support Experience",
    "Missing Features", "Contract Consolidation"
]

def generate_accounts():
    accounts = []
    for i in range(1, NUM_ACCOUNTS + 1):
        segment = np.random.choice(SEGMENTS, p=[0.3, 0.4, 0.3])
        if segment == "Enterprise":
            arr = np.random.lognormal(mean=11.5, sigma=0.5)
            arr = max(100000, min(arr, 2000000))
        elif segment == "Mid-Market":
            arr = np.random.lognormal(mean=10.5, sigma=0.4)
            arr = max(25000, min(arr, 200000))
        else:
            arr = np.random.lognormal(mean=9.5, sigma=0.5)
            arr = max(5000, min(arr, 50000))

        contract_start = START_DATE + timedelta(days=random.randint(0, 365))
        contract_months = np.random.choice([12, 24, 36], p=[0.4, 0.35, 0.25])
        renewal_date = contract_start + timedelta(days=int(contract_months) * 30)

        health = np.random.choice(HEALTH_SCORES, p=[0.45, 0.25, 0.20, 0.10])
        nps = {"Healthy": random.randint(7, 10), "Needs Attention": random.randint(5, 8),
               "At Risk": random.randint(3, 6), "Critical": random.randint(0, 4)}[health]

        usage_pct = {"Healthy": random.uniform(60, 100), "Needs Attention": random.uniform(35, 70),
                     "At Risk": random.uniform(15, 50), "Critical": random.uniform(0, 30)}[health]

        churn_prob = {"Healthy": random.uniform(0.02, 0.10), "Needs Attention": random.uniform(0.10, 0.30),
                      "At Risk": random.uniform(0.30, 0.60), "Critical": random.uniform(0.55, 0.90)}[health]

        is_churned = random.random() < churn_prob * 0.6
        churn_reason = random.choice(CHURN_REASONS) if is_churned else None
        churn_date = renewal_date - timedelta(days=random.randint(0, 30)) if is_churned else None
        status = "Churned" if is_churned else ("Active" if renewal_date > datetime(2026, 3, 1) else "Renewed")

        if status == "Renewed":
            expansion = np.random.choice([-0.15, -0.05, 0, 0.05, 0.10, 0.20], p=[0.05, 0.10, 0.25, 0.30, 0.20, 0.10])
            new_arr = arr * (1 + expansion)
        elif is_churned:
            new_arr = 0
        else:
            new_arr = arr

        accounts.append({
            "Account_ID": f"ACC-{i:04d}",
            "Account_Name": f"Account_{i:04d}",
            "Segment": segment,
            "Industry": random.choice(INDUSTRIES),
            "Region": np.random.choice(REGIONS, p=[0.45, 0.25, 0.20, 0.10]),
            "Product": random.choice(PRODUCTS),
            "CSM": random.choice(CSM_NAMES),
            "TAE": random.choice(TAE_NAMES),
            "ARR": round(arr, 2),
            "New_ARR": round(new_arr, 2),
            "Contract_Start": contract_start.strftime("%Y-%m-%d"),
            "Contract_Term_Months": contract_months,
            "Renewal_Date": renewal_date.strftime("%Y-%m-%d"),
            "Health_Score": health,
            "NPS_Score": nps,
            "License_Utilization_Pct": round(usage_pct, 1),
            "Last_Login_Days_Ago": {"Healthy": random.randint(0, 7), "Needs Attention": random.randint(5, 30),
                                     "At Risk": random.randint(20, 60), "Critical": random.randint(30, 120)}[health],
            "Support_Tickets_Open": {"Healthy": random.randint(0, 2), "Needs Attention": random.randint(1, 5),
                                      "At Risk": random.randint(2, 8), "Critical": random.randint(3, 15)}[health],
            "Escalations_Last_90d": {"Healthy": 0, "Needs Attention": random.randint(0, 1),
                                      "At Risk": random.randint(0, 3), "Critical": random.randint(1, 5)}[health],
            "Status": status,
            "Churn_Reason": churn_reason,
            "Churn_Date": churn_date.strftime("%Y-%m-%d") if churn_date else None,
            "Churn_Probability": round(churn_prob, 3),
            "Forecast_Category": np.random.choice(
                ["Commit", "Best Case", "Pipeline", "At Risk"],
                p={"Healthy": [0.7, 0.2, 0.05, 0.05], "Needs Attention": [0.3, 0.3, 0.2, 0.2],
                   "At Risk": [0.1, 0.15, 0.25, 0.5], "Critical": [0.05, 0.05, 0.1, 0.8]}[health]
            ),
            "PS_Hours_Purchased": random.choice([0, 0, 0, 20, 40, 80, 160]) if segment != "SMB" else 0,
            "PS_Hours_Used": 0,
            "Training_Completed": random.choice([True, False]),
            "Executive_Sponsor": random.choice([True, True, False]),
            "Multi_Year": contract_months > 12,
        })
        if accounts[-1]["PS_Hours_Purchased"] > 0:
            accounts[-1]["PS_Hours_Used"] = random.randint(0, accounts[-1]["PS_Hours_Purchased"])

    return pd.DataFrame(accounts)


def generate_monthly_metrics(accounts_df):
    """Generate monthly aggregated metrics for trending."""
    months = pd.date_range("2024-01-01", "2026-03-01", freq="MS")
    rows = []
    base_arr = accounts_df["ARR"].sum()
    cumulative_churn = 0

    for i, month in enumerate(months):
        month_str = month.strftime("%Y-%m")
        seasonal = 1 + 0.05 * np.sin(2 * np.pi * month.month / 12)
        growth = 1 + 0.003 * i
        noise = np.random.normal(1, 0.02)

        renewals_due = random.randint(8, 25)
        renewed = int(renewals_due * random.uniform(0.78, 0.95))
        churned_count = renewals_due - renewed
        churned_arr = churned_count * np.random.uniform(20000, 80000)
        cumulative_churn += churned_arr
        expansion = renewed * np.random.uniform(2000, 15000)
        contraction = random.randint(0, renewed // 3) * np.random.uniform(3000, 10000)
        new_logo_arr = random.randint(1, 5) * np.random.uniform(15000, 60000)

        current_arr = base_arr * growth * seasonal * noise - cumulative_churn + new_logo_arr * (i + 1) * 0.3

        rows.append({
            "Month": month_str,
            "Total_ARR": round(current_arr, 2),
            "Renewals_Due": renewals_due,
            "Renewals_Completed": renewed,
            "Gross_Renewal_Rate": round(renewed / renewals_due * 100, 1),
            "Churned_Accounts": churned_count,
            "Churned_ARR": round(churned_arr, 2),
            "Expansion_ARR": round(expansion, 2),
            "Contraction_ARR": round(contraction, 2),
            "New_Logo_ARR": round(new_logo_arr, 2),
            "Net_New_ARR": round(expansion - contraction + new_logo_arr - churned_arr, 2),
            "NRR_Pct": round((current_arr / (base_arr * growth)) * 100, 1),
            "GRR_Pct": round(100 - (churned_arr + contraction) / (base_arr * growth / len(months)) * 100, 1),
            "Avg_Health_Score": round(random.uniform(68, 82) + 0.2 * i * noise, 1),
            "CSAT_Score": round(random.uniform(4.0, 4.7), 2),
            "Avg_Time_To_Renew_Days": random.randint(15, 45),
            "PS_Revenue": round(random.uniform(30000, 120000), 2),
            "PS_Utilization_Pct": round(random.uniform(55, 85), 1),
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print("Generating account data...")
    accounts = generate_accounts()
    import os
    os.makedirs("data", exist_ok=True)
    accounts.to_csv("data/renewal_churn_data.csv", index=False)
    accounts.to_excel("data/renewal_churn_data.xlsx", index=False)
    print(f"  -> {len(accounts)} accounts generated")

    print("Generating monthly metrics...")
    metrics = generate_monthly_metrics(accounts)
    metrics.to_csv("data/monthly_metrics.csv", index=False)
    print(f"  -> {len(metrics)} months of metrics generated")

    print("\nSample data summary:")
    print(f"  Total ARR: ${accounts['ARR'].sum():,.0f}")
    print(f"  Churned: {len(accounts[accounts['Status'] == 'Churned'])}")
    print(f"  Active: {len(accounts[accounts['Status'] == 'Active'])}")
    print(f"  Renewed: {len(accounts[accounts['Status'] == 'Renewed'])}")
    print(f"\nFiles saved to /home/user/cs-ops-dashboard/data/")
