import random
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import main as main

# Compute accuracy
def compute_accuracy(selected_items, optimal_items):
    if not selected_items or not optimal_items:
        return 0

    min_score = min(item.score for item in selected_items + optimal_items)
    selected_score = sum(item.score - min_score for item in selected_items)
    optimal_score = sum(item.score - min_score for item in optimal_items)

    accuracy = selected_score / optimal_score if optimal_score > 0 else 0
    return min(accuracy, 1.0)

# Get optimal items
def get_optimal_items(ListOfItems, K, d, floorList, ceilList):
    sorted_items = sorted(ListOfItems, key=lambda x: x.score, reverse=True)

    category_count = [0] * d
    optimal_items = []

    for item in sorted_items:
        i = item.category

        if category_count[i] < ceilList[i]:
            optimal_items.append(item)
            category_count[i] += 1

        if len(optimal_items) == K:
            break

    return optimal_items


def GetTestScoresDatasetResult():

    file_path = "test_scores.csv"
    df = pd.read_csv(file_path)

    df = df[['school_setting', 'gender', 'posttest']].dropna()

    df['school_setting'] = df['school_setting'].astype('category').cat.codes
    df['gender'] = df['gender'].astype('category').cat.codes

    df['category'] = df['school_setting'] * 10 + df['gender']  # Unique combination

    unique_categories = sorted(df['category'].unique())
    category_mapping = {cat: i for i, cat in enumerate(unique_categories)}

    df['category'] = df['category'].map(category_mapping)

    ListOfItems = [main.Item(i, int(row['posttest']), int(row['category'])) for i, row in df.iterrows()]

    N = len(ListOfItems)
    K = 10
    d = len(df['category'].unique())

    floorList = [2] * d
    ceilList = [3] * d
    numItemsList = [sum(df['category'] == i) for i in range(d)]

    GetResults(ListOfItems, K, N, d, floorList, ceilList, numItemsList)


def GetResults(ListOfItems, K, N, d, floorList, ceilList, numItemsList):
    warmup_factors = [1, 4, 16]
    results = {factor: [] for factor in warmup_factors}

    for _ in range(500):
        random.shuffle(ListOfItems)
        for factor in warmup_factors:
            walking_distance = [0]
            selected_items = main.SecretaryAlgorithm(
                ListOfItems, K, N, d, floorList, ceilList, numItemsList, warmup_factor=factor, walking_distance=walking_distance
            )
            optimal_items = get_optimal_items(ListOfItems, K, d, floorList, ceilList)
            accuracy = compute_accuracy(selected_items, optimal_items)
            results[factor].append((walking_distance, accuracy))

    # Visualization
    sns.set(style="whitegrid")

    fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

    colors = ["black", "purple", "orange"]

    for ax, factor, color in zip(axes, warmup_factors, colors):
        walking_distances, accuracies = zip(*results[factor])

        walking_distances = np.array(walking_distances)
        accuracies = np.array(accuracies)

        sns.regplot(x=walking_distances, y=accuracies, ax=ax, scatter=True, color=color,
                    scatter_kws={"s": 40, "alpha": 0.8},
                    line_kws={"color": color},
                    ci=90)

        ax.set_title(f"({chr(97 + axes.tolist().index(ax))}) {1}/{factor} warm-up", fontsize=12, fontweight="bold")
        ax.set_xlabel("Walking distance", fontsize=11)
        ax.set_xlim(0, N)

    axes[0].set_ylabel("Overall accuracy", fontsize=11)
    axes[0].set_ylim(0, 1)

    plt.tight_layout()
    plt.show()

def GetSyntheticDatasetResult():
    random.seed(42)
    N = 400  # Fix total dataset size
    K = 4  # Fix number of selected items
    d = 2  # Number of categories

    ListOfItems = []
    category_sizes = N // d  # Ensure equal items per category

    for category in range(d):
        for i in range(category_sizes):
            ListOfItems.append(main.Item(len(ListOfItems), random.randint(1, 1000), category))  # Assign exact categories

    # Experiment with different warm-up factors and plot results
    floorList = [2, 2]
    ceilList = [2, 2]
    numItemsList = [200, 200]
    GetResults(ListOfItems, K, N, d, floorList, ceilList, numItemsList)



GetTestScoresDatasetResult()
GetSyntheticDatasetResult()