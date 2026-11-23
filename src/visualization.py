import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import networkx as nx

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
    execution_time_data = [
        {"min_support": result ["min_support"],
        "apriori_avg_time": result ["apriori"]['average_time'],
        "apriori_std": result ["apriori"]['std_deviation'],
        "fp_growth_avg_time": result ["fp_growth"]['average_time'],
        "fp_growth_std": result ["fp_growth"]['std_deviation']}
        for result in results
        if result.get("apriori") and result.get("fp_growth")
    ]
    
    return execution_time_data

def prepare_itemset_data(results):
    itemset_data = [
        {"min_support": result["min_support"],
        "apriori_frequent_itemsets": result ["apriori"]['number_of_itemsets'],
        "fp_growth_frequent_itemsets": result ["fp_growth"]['number_of_itemsets']}
        for result in results
        if result.get("apriori") and result.get("fp_growth")
    ]
    return itemset_data

def prepare_rule_data(results):
    rule_data = [
        {"min_support": result["min_support"],
        "apriori_rules": len(result ["apriori_rules"]),
        "fp_growth_rules": len(result ["fp_growth_rules"]),
        "apriori_filtered_rules": len(result ["apriori_filtered_rules"]),
        "fp_growth_filtered_rules": len(result ["fp_growth_filtered_rules"])}
        for result in results
    ]
    return rule_data

def prepare_rule_metrics_data(results):
    rule_metrics_data = [
        {"min_support": result["min_support"],
            "algorithm": algorithm,
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
    if isinstance(items, str):
        return [items]

    return list(items)


def format_technique(technique_id, technique_names=None):
    if technique_names is None:
        return str(technique_id)

    technique_name = technique_names.get(str(technique_id), str(technique_id))
    return f"{technique_name} ({technique_id})"


def format_itemset(items, technique_names=None):
    techniques = get_itemset_values(items)
    formatted_techniques = [format_technique(technique, technique_names) for technique in techniques]
    return ", ".join(sorted(formatted_techniques))


def format_rule(antecedent, consequent, technique_names=None):
    antecedent_label = format_itemset(antecedent, technique_names)
    consequent_label = format_itemset(consequent, technique_names)
    return f"{antecedent_label} → {consequent_label}"

def remove_duplicate_rules(data):
    df = pd.DataFrame(data).copy()

    if df.empty:
        return df

    df["antecedent_key"] = df["antecedent"].apply(lambda items: tuple(sorted(get_itemset_values(items))))
    df["consequent_key"] = df["consequent"].apply(lambda items: tuple(sorted(get_itemset_values(items))))

    return df.drop_duplicates(subset=["min_support", "antecedent_key", "consequent_key"])


# PLOT SETTINGS

def configure_plot(title, xlabel, ylabel, figsize=(8, 5)):
    sns.set_theme(style=PLOT_STYLE)
    fig, ax = plt.subplots(figsize=figsize)

    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)

    ax.grid(True, alpha=0.3)
    ax.set_axisbelow(True)

    return fig, ax


def finish_plot(fig, filename):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / filename

    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Visualization saved: {output_path}")

    plt.show()
    plt.close(fig)


def plot_execution_time(data):
    if not data:
        print("No execution time data available.")
        return
    
    df = pd.DataFrame(data)

    fig, ax = configure_plot("Execution Time Comparison: Apriori vs FP-Growth", "Minimum Support", "Average Execution Time (seconds)")
    ax.errorbar(df["min_support"], df["apriori_avg_time"], yerr=df["apriori_std"], label="Apriori", color=COLORS["apriori"], marker='o', linewidth=2)
    ax.errorbar(df["min_support"], df["fp_growth_avg_time"], yerr=df["fp_growth_std"], label="FP-Growth", color=COLORS["fp_growth"], marker='s', linewidth=2)

    ax.legend()
    finish_plot(fig, "execution_time.png")

    
def plot_frequent_itemsets(data):
    if not data:
        print("No frequent itemset data available.")
        return
    df = pd.DataFrame(data)
    
    fig, ax = configure_plot("Frequent Itemsets Comparison", "Minimum Support", "Number of Frequent Itemsets")
    apriori_values = df["apriori_frequent_itemsets"].to_numpy()
    fp_growth_values = df["fp_growth_frequent_itemsets"].to_numpy()

    if np.array_equal(apriori_values, fp_growth_values):
        ax.plot(df["min_support"], apriori_values, label="Shared Result", color=COLORS["shared"], marker='o', linewidth=2.5)
    else:
        ax.plot(df["min_support"], apriori_values, label="Apriori", color=COLORS["apriori"], marker='o', linewidth=2)
        ax.plot(df["min_support"], fp_growth_values, label="FP-Growth", color=COLORS["fp_growth"], marker='s', linewidth=2)

    ax.legend()
    finish_plot(fig, "frequent_itemsets.png")


def plot_association_rules(data):   
    if not data:
        print("No association rule data available.")
        return
        
    df = pd.DataFrame(data)
    x = np.arange(len(df))
    width = 0.2

    fig, ax = configure_plot("Association Rules Comparison", "Minimum Support", "Number of Association Rules", figsize=(11, 6))

    bars = [(df["apriori_rules"], -1.5, COLORS["apriori"], "Apriori Total"),
        (df["fp_growth_rules"], -0.5, COLORS["fp_growth"], "FP-Growth Total"),
        (df["apriori_filtered_rules"], 0.5, COLORS["apriori_filtered"], "Apriori Filtered"),
        (df["fp_growth_filtered_rules"], 1.5,COLORS["fp_growth_filtered"], "FP-Growth Filtered")]
                                                
    for values, offset, color, label in bars:
        ax.bar(x + offset * width, values, width, color=color, label=label, alpha=0.9)

    ax.set_xticks(x)
    ax.set_xticklabels(df["min_support"].astype(str))

    ax.legend(fontsize=9)
    finish_plot(fig, "association_rules.png")


def plot_confidence_vs_lift(data):
    if not data:
        print("No association rule metrics available.")
        return

    df = remove_duplicate_rules(data)

    fig, ax = configure_plot("Confidence vs Lift of Association Rules", "Confidence", "Lift")
    sns.scatterplot(data=df, x="confidence", y="lift", size="support", sizes=(30, 200), color=COLORS["shared"], alpha=0.75, legend="brief", ax=ax)
    ax.axhline(y=1, color="black", linestyle="--", label="Lift = 1")

    ax.legend()
    finish_plot(fig, "confidence_vs_lift.png")


def plot_top_association_rules(data, technique_names=None):
    if not data:
        print("No association rules available.")
        return

    df = remove_duplicate_rules(data)

    # Construct readable rule labels.
    df["rule_label"] = df.apply(lambda row: format_rule(row["antecedent"], row["consequent"], technique_names),axis=1)

    # Remove repeated occurrences of the same rule and retian those with highest lift
    df = (df.sort_values("lift", ascending=False)
            .drop_duplicates(subset="rule_label")
            .nlargest(10, "lift")
            .sort_values("lift"))

    if df.empty:
        return

    fig, ax = plt.subplots(figsize=(12, 5))
    plt.subplots_adjust(left=0.50, right=0.98)
    bars = ax.barh(df["rule_label"], df["confidence"], color=COLORS["shared"], alpha=0.9)

    # Display all three association metrics.
    for bar, (_, rule) in zip(bars, df.iterrows()):
        ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height() / 2,
            (f"Lift: {rule['lift']:.2f} | Support: {rule['support']:.3f}"), va="center",fontsize=8)

    ax.set_title("Top Association Rules", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Confidence")
    ax.set_ylabel("Association Rule")
    ax.set_xlim(0,min(1.0, max(0.1, df["confidence"].max() * 1.65)))
    ax.tick_params(axis="y", labelsize=7)

    ax.grid(axis="x", alpha=0.3)
    ax.set_axisbelow(True)
    ax.legend(handles=[Line2D([0], [0], color=COLORS["shared"], lw=6, label="Shared Results")],loc="lower right")

    finish_plot(fig, "top_association_rules.png")


def plot_technique_network(data, technique_names):
    if not data:
        print("No technique association data available.")
        return
    df = remove_duplicate_rules(data)

    # Keep only rules with one technique on each side.
    df = df[df["antecedent"].apply(lambda items: len(get_itemset_values(items)) == 1)
        & df["consequent"].apply(lambda items: len(get_itemset_values(items)) == 1)
    ].copy()

    if df.empty:
        print("No one-to-one technique associations available.")
        return

    df["source"] = df["antecedent"].apply(lambda items: get_itemset_values(items)[0])
    df["target"] = df["consequent"].apply(lambda items: get_itemset_values(items)[0])
    df = df[df["source"] != df["target"]]

    # Keep the strongest association for each directed connection.
    df = (
        df.sort_values("lift", ascending=False)
        .drop_duplicates(subset=["source", "target"])
        .nlargest(15, "lift")
    )

    if df.empty:
        print("No valid technique associations available.")
        return

    G = nx.DiGraph()

    for _, rule in df.iterrows():
        G.add_edge(rule["source"], rule["target"], lift=rule["lift"])

    fig, ax = plt.subplots(figsize=(12, 8))

    # Calculate node positions.
    node_count = G.number_of_nodes()
    pos = nx.spring_layout(G, seed=42, iterations=150, k=0.8 / np.sqrt(node_count), scale=1.5)

    # Node sizes reflect the number of connections.
    node_sizes = [700 + G.degree(node) * 180 for node in G.nodes()]

    # Edge widths reflect average lift.
    edge_widths = [max(1.0, min(4.0, G[u][v]["lift"])) for u, v in G.edges()]

    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="#87CEEB", edgecolors=COLORS["fp_growth"], linewidths=1.2, alpha=0.9, ax=ax)
    nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color=COLORS["shared"], alpha=0.75, arrows=True, arrowsize=16, connectionstyle="arc3,rad=0.08", min_source_margin=12, min_target_margin=12, ax=ax)
    
    node_labels = {node: format_technique(node, technique_names) for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8, font_weight="bold", ax=ax)

    edge_labels = {(u, v): f"{G[u][v]['lift']:.2f}" for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7, font_color="darkred", ax=ax)

    legend_handles = [Line2D([0], [0], color=COLORS["shared"],lw=2, label="Shared Association")]
    ax.legend(handles=legend_handles, loc="upper right")

    ax.set_title("MITRE ATT&CK Technique Association Network", fontsize=12, fontweight="bold", pad=12)
    ax.text(0.5, -0.04, "Arrow = Association Direction | " "Edge Width = Lift | " "Node Size = Connectivity",transform=ax.transAxes,ha="center",fontsize=9)
    ax.axis("off")
    finish_plot(fig, "technique_network.png")



def visualize_results(results, technique_names=None): 
    execution_time_data = prepare_execution_time_data(results)
    itemset_data = prepare_itemset_data(results)
    rule_data = prepare_rule_data(results)
    rule_metrics_data = prepare_rule_metrics_data(results)

    plot_execution_time(execution_time_data)
    plot_frequent_itemsets(itemset_data)
    plot_association_rules(rule_data)
    plot_confidence_vs_lift(rule_metrics_data)
    plot_top_association_rules(rule_metrics_data, technique_names)
    plot_technique_network(rule_metrics_data, technique_names)

