"""Create visualizations for Apriori and FP-Growth evaluation results"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from pathlib import Path
from matplotlib.lines import Line2D


COLORS = {
    "apriori": "#E76F51",
    "fp_growth": "#2878B5",
    "apriori_filtered": "#F4A261",
    "fp_growth_filtered": "#56A3A6",
    "shared": "#8E44AD"
}

PLOT_STYLE = "whitegrid"
OUTPUT_DIR = Path("results") / "figures"


# DATA PREPARATION

def prepare_execution_time_data(results):
    """Extract execution-time statistics for both algorithms"""
    execution_time_data = [
        {"min_support": result["min_support"],
        "apriori_avg_time": result["apriori"]['average_time'],
        "apriori_std": result["apriori"]['std_deviation'],
        "fp_growth_avg_time": result["fp_growth"]['average_time'],
        "fp_growth_std": result["fp_growth"]['std_deviation']}
        for result in results
        if result.get("apriori") and result.get("fp_growth")
    ]
    
    return execution_time_data

def prepare_itemset_data(results):
    """Extract frequent-itemset counts and algorithm agreement"""
    itemset_data = [
        {"min_support": result["min_support"],
        "apriori_frequent_itemsets": result["apriori"]['number_of_itemsets'],
        "fp_growth_frequent_itemsets": result["fp_growth"]['number_of_itemsets'],
        "itemsets_agree": result["itemsets_agree"]}
        for result in results
        if result.get("apriori") and result.get("fp_growth")
    ]
    return itemset_data

def prepare_rule_data(results):
    """Extract generated and confidence-filtered rule counts"""
    rule_data = [
        {"min_support": result["min_support"],
        "apriori_rules": len(result["apriori_rules"]),
        "fp_growth_rules": len(result["fp_growth_rules"]),
        "apriori_filtered_rules": len(result["apriori_filtered_rules"]),
        "fp_growth_filtered_rules": len(result["fp_growth_filtered_rules"])}
        for result in results
    ]
    return rule_data

def prepare_rule_metrics_data(results):
    """Extract support, confidence and lift for filtered association rules"""
    rule_metrics_data = [
        {"min_support": result["min_support"],
            "antecedent": rule["antecedent"],
            "consequent": rule["consequent"],
            "support": rule["support"],
            "confidence": rule["confidence"],
            "lift": rule["lift"]}
        for result in results
        for algorithm in ["apriori", "fp_growth"]
        for rule in result[f"{algorithm}_filtered_rules"]
    ]
    return rule_metrics_data


#FORMATTING AND DUPLICATE HANDLING

def get_itemset_values(items):
    """Convert an itemset into a list of technique IDs"""
    if isinstance(items, str):
        return [items]

    return list(items)

def format_itemset(items):
    """Format an itemset using sorted MITRE technique IDs"""
    techniques = get_itemset_values(items)
    return ", ".join(sorted(techniques))


def format_rule(antecedent, consequent):
    """Format an association rule using MITRE technique IDs"""
    antecedent_label = format_itemset(antecedent)
    consequent_label = format_itemset(consequent)
    return f"{antecedent_label} -> {consequent_label}"

def remove_duplicate_rules(data):
    """Remove duplicate rules while retaining separate support thresholds"""
    df = pd.DataFrame(data).copy()

    if df.empty:
        return df

    df["antecedent_key"] = df["antecedent"].apply(lambda items: tuple(sorted(get_itemset_values(items))))
    df["consequent_key"] = df["consequent"].apply(lambda items: tuple(sorted(get_itemset_values(items))))

    return df.drop_duplicates(subset=["min_support", "antecedent_key", "consequent_key"])


# PLOT SETTINGS

def configure_plot(title, xlabel, ylabel, figsize=(8, 5)):
    """Create a consistently styled plot"""
    sns.set_theme(style=PLOT_STYLE)
    fig, ax = plt.subplots(figsize=figsize)

    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)

    ax.grid(True, alpha=0.3)
    ax.set_axisbelow(True)

    return fig, ax


def finish_plot(fig, filename):
    """Save, display and close a visualization"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / filename

    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Visualization saved: {output_path}")

    plt.show()
    plt.close(fig)


# VISUALIZATION

def plot_execution_time(data):
    """Compare the execution times of Apriori and FP-Growth"""
    if not data:
        print("No execution time data available.")
        return
    
    df = pd.DataFrame(data)

    fig, ax = configure_plot("Execution Time Comparison: Apriori vs FP-Growth", "Minimum Support", "Average Execution Time (seconds)")
    ax.errorbar(df["min_support"], df["apriori_avg_time"], yerr=df["apriori_std"], label="Apriori", color=COLORS["apriori"], marker='o', linewidth=2)
    ax.errorbar(df["min_support"], df["fp_growth_avg_time"], yerr=df["fp_growth_std"], label="FP-Growth", color=COLORS["fp_growth"], marker='s', linewidth=2)

    ax.set_xticks(df["min_support"])
    ax.legend()
    finish_plot(fig, "execution_time.png")

    
def plot_frequent_itemsets(data):
    """Compare the number of frequent itemsets discovered by each algorithm"""
    if not data:
        print("No frequent itemset data available.")
        return
    df = pd.DataFrame(data)
    
    fig, ax = configure_plot("Frequent Itemsets Comparison", "Minimum Support", "Number of Frequent Itemsets")
    apriori_values = df["apriori_frequent_itemsets"].to_numpy()
    fp_growth_values = df["fp_growth_frequent_itemsets"].to_numpy()

    # Show one shared line only when the actual itemsets agree at every threshold.
    if df["itemsets_agree"].all():
        ax.plot(df["min_support"], apriori_values, label="Shared Result", color=COLORS["shared"], marker='o', linewidth=2.5)
    else:
        ax.plot(df["min_support"], apriori_values, label="Apriori", color=COLORS["apriori"], marker='o', linewidth=2)
        ax.plot(df["min_support"], fp_growth_values, label="FP-Growth", color=COLORS["fp_growth"], marker='s', linewidth=2)

    ax.set_xticks(df["min_support"])
    ax.legend()
    finish_plot(fig, "frequent_itemsets.png")


def plot_association_rules(data):   
    """Compare generated and confidence-filtered association-rule counts"""
    if not data:
        print("No association rule data available.")
        return
        
    df = pd.DataFrame(data)
    x = np.arange(len(df))
    width = 0.2

    fig, ax = configure_plot("Association Rules Comparison", "Minimum Support", "Number of Association Rules")

    bars = [(df["apriori_rules"], -1.5, COLORS["apriori"], "Apriori (All Rules)"),
        (df["fp_growth_rules"], -0.5, COLORS["fp_growth"], "FP-Growth (All Rules)"),
        (df["apriori_filtered_rules"], 0.5, COLORS["apriori_filtered"], "Apriori (Filtered)"),
        (df["fp_growth_filtered_rules"], 1.5,COLORS["fp_growth_filtered"], "FP-Growth (Filtered)")]
                                                
    for values, offset, color, label in bars:
        ax.bar(x + offset * width, values, width, color=color, label=label, alpha=0.9)

    ax.set_xticks(x)
    ax.set_xticklabels(df["min_support"].astype(str))
    ax.legend(fontsize=9)
    finish_plot(fig, "association_rules.png")


def plot_confidence_vs_lift(data):
    """Visualize confidence and lift for unique filtered association rules"""
    if not data:
        print("No association rule metrics available.")
        return

    df = remove_duplicate_rules(data)
    # Keep one point per unique rule across all support thresholds.
    df = df.drop_duplicates(subset=["antecedent_key", "consequent_key"])

    fig, ax = configure_plot("Confidence vs Lift of Filtered Association Rules", "Confidence", "Lift")
    sns.scatterplot(data=df, x="confidence", y="lift", size="support", sizes=(30, 200), color=COLORS["shared"], alpha=0.75, legend="brief", ax=ax)
    ax.axhline(y=1, color="black", linestyle="--", label="Lift = 1")

    ax.legend(title="Support", loc="upper right")
    finish_plot(fig, "confidence_vs_lift.png")


def plot_top_association_rules(data, technique_names=None):
    """Plot the ten highest-lift rules from distinct itemset combinations"""
    if not data:
        print("No association rules available.")
        return

    df = remove_duplicate_rules(data)

    # Construct readable rule labels using MITRE IDs only
    df["rule_label"] = df.apply(lambda row: format_rule(row["antecedent"], row["consequent"]), axis=1)
    
    # Keep the highest-lift rule for each unique itemset combination.
    df["combined_itemset"] = df.apply(lambda row: row["antecedent"] | row["consequent"], axis=1)

    # Select the 10 strongest distinct combinations
    df = (df.sort_values("lift", ascending=False)
            .drop_duplicates(subset="combined_itemset")
            .head(10)
            .sort_values("lift"))

    if df.empty:
        return

    fig, ax = configure_plot("Top 10 Distinct Association Rules by Lift", "Confidence", "Association Rule", figsize=(12, 6))
    bars = ax.barh(df["rule_label"], df["confidence"], color=COLORS["shared"], alpha=0.9)

    # Display lift and support alongside each rule
    for bar, (_, rule) in zip(bars, df.iterrows()):
        ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height() / 2,
            (f"Lift: {rule['lift']:.2f} | Support: {rule['support']:.3f}"), va="center",fontsize=8)

    ax.set_xlim(0, 1.5)
    ax.tick_params(axis="y", labelsize=9)

    ax.legend(handles=[Line2D([0], [0], color=COLORS["shared"], lw=6, label="Shared Results")],loc="upper right")
    finish_plot(fig, "top_association_rules.png")

    # Print technique names corresponding to the displayed MITRE IDs
    if technique_names:
        print("\n========== TECHNIQUE REFERENCE ==========")

        used_techniques = {technique
            for _, rule in df.iterrows()
            for technique in (get_itemset_values(rule["antecedent"])+ get_itemset_values(rule["consequent"]))
        }

        for technique in sorted(used_techniques):
            print(f"{technique}: {technique_names.get(technique, 'Unknown technique')}")


def visualize_results(results, technique_names=None): 
    """Prepare experimental results and generate all five visualizations"""
    execution_time_data = prepare_execution_time_data(results)
    itemset_data = prepare_itemset_data(results)
    rule_data = prepare_rule_data(results)
    rule_metrics_data = prepare_rule_metrics_data(results)

    plot_execution_time(execution_time_data)
    plot_frequent_itemsets(itemset_data)
    plot_association_rules(rule_data)
    plot_confidence_vs_lift(rule_metrics_data)
    plot_top_association_rules(rule_metrics_data, technique_names)

