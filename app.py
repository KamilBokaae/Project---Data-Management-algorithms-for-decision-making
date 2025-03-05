import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import time
from main import process_file
from main import validate_inputs


st.set_page_config(layout="wide")  # Use wide layout

# Sidebar: Algorithm Selection
st.sidebar.header("Step 1: Select Algorithm")
algorithm_type = st.sidebar.radio("Choose an Algorithm", ("Static Problem", "Online Problem"))

# Collapsible Inputs Section
with st.sidebar.expander("Advanced Inputs (Expand for options)", expanded=False):
    # Number of Items to Pick (K)
    K = st.number_input("Number of Items to Pick (K)", min_value=1, value=3)

    # Number of Categories (d)
    d = st.number_input("Number of Categories (d)", min_value=1, value=2)

    # Show additional inputs **only for the Online Problem**
    N = None
    numItemsList = None

    # Floor and Ceil Constraints
    st.subheader("Step 2: Set Constraints")
    floorList = {}
    ceilList = {}

    for i in range(d):
        floorList[i] = st.number_input(f"Min items from Category {i}", min_value=0, max_value=K, value=1)
        ceilList[i] = ceilList[i] = st.number_input(f"Max items from Category {i}", min_value=1, max_value=max(1, K),  value=min(2, K))


    if algorithm_type == "Online Problem":
        # Total number of items (N)
        N = st.number_input("Total Number of Items (N)", min_value=1, value=12)

        # Items per category (numItemsList)
        numItemsList = []
        st.subheader("Step 3: Set Number of Items Per Category")

        for i in range(d):
            num_i = st.number_input(f"Items in Category {i} ", min_value=0, value=N // d)
            numItemsList.append(num_i)

# File Upload Section
step_number = "Step 4" if algorithm_type == "Online Problem" else "Step 3"
st.sidebar.subheader(f"{step_number}: Upload Your Excel File")

uploaded_file = st.sidebar.file_uploader("Upload an Excel file (.xlsx)", type=["xlsx"])

# Run Algorithm Button (Green)
st.sidebar.markdown("""
    <style>
        .stButton>button {
            background-color: #4CAF50 !important;
            color: white !important;
            font-size: 18px !important;
            padding: 12px !important;
            border-radius: 8px !important;
            transition: 0.3s !important;
        }
        .stButton>button:hover {
            background-color: #3e8e41 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Run Algorithm Button
if uploaded_file and st.sidebar.button("Run Algorithm"):
    # Save file temporarily
    file_path = f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    try:
        # Load dataset before processing
        df = pd.read_excel(file_path, engine="openpyxl")

        required_columns = {"ID", "Score", "Category Number"}

        algorithm_choice = "static" if algorithm_type == "Static Problem" else "online"
        floorList = list(floorList.values())
        ceilList = list(ceilList.values())

        if algorithm_type == "Static Problem":
            df = df.sort_values(by="Score", ascending=False)

        if not validate_inputs(K, d, floorList, ceilList, df, algorithm_choice,
                N=N if algorithm_type == "Online Problem" else None,
                numItemsList=numItemsList if algorithm_type == "Online Problem" else None):

            raise ValueError(f"Validating Error!")

        else:
            start_time = time.time()

            # Run Algorithm
            selected_df = process_file(
                file_path, K, d, floorList, ceilList, algorithm_choice,
                N=N if algorithm_type == "Online Problem" else None,
                numItemsList=numItemsList if algorithm_type == "Online Problem" else None
            )
            end_time = time.time()
            runtime_sec = end_time - start_time
            runtime_ms = runtime_sec * 1000

            os.remove(file_path)

            st.subheader("Visual Representation of Items Before Selection")

            # Define Category Colors
            category_colors = ["blue", "red", "green", "purple", "orange", "pink", "cyan", "yellow", "brown", "gray",
                               "gold", "navy", "lime", "teal", "magenta", "olive", "indigo", "maroon", "turquoise",
                               "lavender"]

            # If number of categories exceeds the number of colors, disable coloring
            use_colors = d <= len(category_colors)

            # Extract data
            item_ids = df["ID"].tolist()
            scores = df["Score"].tolist()
            categories = df["Category Number"].tolist()
            if use_colors:
                fig, ax = plt.subplots(figsize=(10, 2), facecolor="none")
                ax.set_xlim(-1, len(item_ids))
                ax.set_ylim(-1, 2)
                ax.set_facecolor("none")

                for idx, (id_, score, category) in enumerate(zip(item_ids, scores, categories)):
                    color = category_colors[category % len(category_colors)]
                    circle = plt.Circle((idx, 0), 0.4, color=color, ec="black", lw=1, zorder=2)
                    ax.add_patch(circle)
                    ax.text(idx, 0, id_, ha="center", va="center", fontsize=14, color="white", fontweight="bold", zorder=3)
                    ax.text(idx, 0.8, str(score), ha="center", va="center", fontsize=14, color="white", fontweight="bold",
                            zorder=4)

                ax.set_xticks([])
                ax.set_yticks([])
                ax.set_frame_on(False)
                st.pyplot(fig)

            st.success("✅ Algorithm executed successfully!")
            st.subheader("🎯 Selected Items:")
            st.dataframe(selected_df)

            # **Visual Representation of Selected Items (Aligned in a Single Row)**
            st.subheader("Selected Items as Painted Balls")

            # Extract selected data correctly
            selected_item_ids = selected_df["ID"].tolist()
            selected_scores = selected_df["Score"].tolist()
            selected_categories = selected_df["Category Number"].tolist()

            if use_colors:
                fig_selected, ax_selected = plt.subplots(figsize=(10, 2), facecolor="none")
                ax_selected.set_xlim(-1, len(item_ids))  # Match upper row width
                ax_selected.set_ylim(-1, 2)
                ax_selected.set_facecolor("none")

                for idx, (id_, score, category) in enumerate(zip(item_ids, scores, categories)):
                    if id_ in selected_item_ids:  # Ensure only selected items are highlighted
                        color = category_colors[category % len(category_colors)]

                        # Draw the ball
                        circle = plt.Circle((idx, 0), 0.4, color=color, ec="black", lw=1, zorder=2)
                        ax_selected.add_patch(circle)

                        # Draw item ID inside the ball
                        ax_selected.text(idx, 0, id_, ha="center", va="center", fontsize=14, color="white",
                                         fontweight="bold", zorder=3)

                        # Draw score above the ball
                        ax_selected.text(idx, 0.8, str(score), ha="center", va="center", fontsize=14, color="white",
                                         fontweight="bold", zorder=4)

                ax_selected.set_xticks([])
                ax_selected.set_yticks([])
                ax_selected.set_frame_on(False)
                st.pyplot(fig_selected)

            st.write(f"**Algorithm executed in {runtime_ms:.3f} ms.**")

            # Download Option
            csv = selected_df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Results", data=csv, file_name="selected_items.csv", mime="text/csv")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")