import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import networkx as nx
from pathlib import Path

COLORS = {
    "apriori": "#E76F51",
    "fp_growth": "#2878B5",
    "apriori_filtered": "#F4A261",
    "fp_growth_filtered": "#56A3A6",
}

PLOT_STYLE = "whitegrid"
OUTPUT_DIR = Path("results") / "figures"

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
    rule_metrics_data = []

    for result in results:
        for algorithm in ["apriori", "fp_growth"]:
            filtered_rules = result.get(f"{algorithm}_filtered_rules", [])

            for rule in filtered_rules:
                rule_metrics_data.append({
                    "min_support": result["min_support"],
                    "algorithm": algorithm,
                    "antecedent": rule["antecedent"],
                    "consequent": rule["consequent"],
                    "support": rule["support"],
                    "confidence": rule["confidence"],
                    "lift": rule["lift"]
                })

    return rule_metrics_data


def configure_plot(title, xlabel, ylabel, figsize=(8, 5)):
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
    ax.errorbar(df["min_support"], df["apriori_avg_time"], yerr=df["apriori_std"], label="Apriori", color=COLORS["apriori"], marker='o', linewidth=2, capsize=4)
    ax.errorbar(df["min_support"], df["fp_growth_avg_time"], yerr=df["fp_growth_std"], label="FP-Growth", color=COLORS["fp_growth"], marker='s', linewidth=2, capsize=4)

    plt.legend()
    finish_plot(fig, "execution_time.png")

    
def plot_frequent_itemsets(data):
    if not data:
        print("No frequent itemset data available.")
        return
    df = pd.DataFrame(data)
    
    fig, ax = configure_plot("Frequent Itemsets Comparison", "Minimum Support", "Number of Frequent Itemsets")

    ax.plot(df["min_support"], df["apriori_frequent_itemsets"], label="Apriori", color=COLORS["apriori"], marker='o', linewidth=2)
    plt.plot(df["min_support"], df["fp_growth_frequent_itemsets"], label="FP-Growth", color=COLORS["fp_growth"], marker='s', linewidth=2)

    plt.legend()
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
    df = pd.DataFrame(data)

    fig, ax = configure_plot("Confidence vs Lift of Association Rules", "Confidence", "Lift")
    sns.scatterplot(data=df, x="confidence", y="lift", hue="algorithm", style="algorithm", size="support", sizes=(30, 200), 
        palette={
            "apriori": COLORS["apriori"],
            "fp_growth": COLORS["fp_growth"]
        }, alpha=0.75, ax=ax)
    ax.axhline(y=1, color="black", linestyle="--", label="Lift = 1")

    ax.legend()
    finish_plot(fig, "confidence_vs_lift.png")

def plot_technique_network(data):
    # import networkx as nx
    if not data:
        print("No technique association data available.")
        return
    df = pd.DataFrame(data)
    G = nx.DiGraph()

    for rule in data:
        antecedents = rule["antecedent"]
        consequents = rule["consequent"]
        lift = rule["lift"]

        if isinstance(antecedents, str):
            antecedents = [antecedents]

        if isinstance(consequents, str):
            consequents = [consequents]

        for antecent_tech in antecedents:
            for consequent_tech in consequents:

                if antecent_tech == consequent_tech:
                    continue

                if G.has_edge(antecent_tech, consequent_tech):
                    edge = G[antecent_tech][consequent_tech]

                    edge["total_lift"] += lift
                    edge["rule_count"] += 1

                    edge["weight"] = (edge["total_lift"] / edge["rule_count"])

                else:
                    G.add_edge(antecent_tech, consequent_tech, weight=lift, total_lift=lift, rule_count=1)

    if G.number_of_nodes() == 0:
        print("No techniques available.")
        return

    fig, ax = plt.subplots(figsize=(10, 7))

    # Calculate node positions.
    node_count = G.number_of_nodes()
    pos = nx.spring_layout(G, seed=42, iterations=150, k=2.5 / np.sqrt(node_count), scale=2.5)

    # Node sizes reflect the number of connections.
    node_sizes = [700 + G.degree(node) * 180 for node in G.nodes()]

    # Edge widths reflect average lift.
    edge_widths = [max(0.8, min(3, G[u][v]["weight"])) for u, v in G.edges()]

    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="#87CEEB", edgecolors="#2878B5", linewidths=1.2, alpha=0.9, ax=ax)
    nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color="gray", alpha=0.4, arrows=True, arrowsize=14, connectionstyle="arc3,rad=0.08", min_source_margin=12, min_target_margin=12, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold", ax=ax)

    # Display edge labels only for reasonably sized networks
    if G.number_of_edges() <= 25:
        edge_labels = {(u, v): f"{G[u][v]['weight']:.2f}" for u, v in G.edges()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7, font_color="darkred", ax=ax)

    ax.set_title("MITRE ATT&CK Technique Association Network", fontsize=12, fontweight="bold", pad=12)
    ax.axis("off")
    finish_plot(fig, "technique_network.png")



def visualize_results(results): 
    execution_time_data = prepare_execution_time_data(results)
    itemset_data = prepare_itemset_data(results)
    rule_data = prepare_rule_data(results)
    rule_metrics_data = prepare_rule_metrics_data(results)

    plot_execution_time(execution_time_data)
    plot_frequent_itemsets(itemset_data)
    plot_association_rules(rule_data)
    plot_confidence_vs_lift(rule_metrics_data)
    plot_technique_network(rule_metrics_data)

