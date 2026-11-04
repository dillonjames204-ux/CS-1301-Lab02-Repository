# This creates the page for displaying data visualizations.

import json
import os
import pandas as pd
import altair as alt
import streamlit as st

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
with open("data.json") as f:
    data = json.load(f)

df = pd.DataFrame(data["data_points"])

st.header(data["chart_title"])
st.dataframe(df)

# STATIC CHART (bar)
st.subheader("Static Chart: Weight per Lift")

bar = alt.Chart(df).mark_bar().encode(
    x=alt.X("label:N", title="Lift", sort=None),
    y=alt.Y("weight:Q", title="Weight (lbs)"),
    color=alt.Color("muscle_group:N", title="Muscle Group"),
).properties(title="Weight per Lift")

st.altair_chart(bar)

# DYNAMIC CHART (scatter + radio + session state)
st.subheader("Dynamic Chart: Weight vs. Reps")

groups = ["All"] + sorted(df["muscle_group"].unique())

if "group_choice" not in st.session_state:
    st.session_state["group_choice"] = "All"

st.radio("Choose a muscle group:", groups, key="group_choice")

if st.session_state["group_choice"] == "All":
    filtered = df
else:
    filtered = df[df["muscle_group"] == st.session_state["group_choice"]]

scatter = alt.Chart(filtered).mark_circle(size=120).encode(
    x=alt.X("reps:Q", title="Reps"),
    y=alt.Y("weight:Q", title="Weight (lbs)"),
    color=alt.Color("muscle_group:N", title="Muscle Group"),
    tooltip=["label:N", "weight:Q", "reps:Q"],
).properties(title="Weight vs. Reps")

st.altair_chart(scatter)

# EXTRA CREDIT: mean and median weight that update with the radio button
mean_w = filtered["weight"].mean()
median_w = filtered["weight"].median()

if "shown_w" not in st.session_state:
    st.session_state["shown_w"] = {
        "group": st.session_state["group_choice"],
        "mean": mean_w,
        "median": median_w,
    }
    st.session_state["previous_w"] = None

if st.session_state["shown_w"]["group"] != st.session_state["group_choice"]:
    st.session_state["previous_w"] = st.session_state["shown_w"]
    st.session_state["shown_w"] = {
        "group": st.session_state["group_choice"],
        "mean": mean_w,
        "median": median_w,
    }

previous_w = st.session_state["previous_w"]
if previous_w is None:
    mean_w_delta = None
    median_w_delta = None
else:
    mean_w_delta = round(mean_w - previous_w["mean"], 2)
    median_w_delta = round(median_w - previous_w["median"], 2)

c1, c2 = st.columns(2)
c1.metric("Mean weight (lbs)", round(mean_w, 2), delta=mean_w_delta)
c2.metric("Median weight (lbs)", round(median_w, 2), delta=median_w_delta)


# PART 2: GRAPHS FROM data.csv
st.header("Campus Food Survey Results")

if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:
    csv_df = pd.read_csv("data.csv")
    # Everything in a CSV can come in as text, so make sure ratings are numbers.
    csv_df["value"] = pd.to_numeric(csv_df["value"])

    st.dataframe(csv_df)

    # STATIC CHART (bar)
    st.subheader("Static Chart: Average Rating by Dining Spot")

    avg_df = csv_df.groupby("category", as_index=False)["value"].mean()

    avg_bar = alt.Chart(avg_df).mark_bar().encode(
        x=alt.X("category:N", title="Dining Spot", sort=None),
        y=alt.Y("value:Q", title="Average Rating (1-5)"),
        color=alt.Color("category:N", title="Dining Spot"),
    ).properties(title="Average Rating by Campus Dining Spot")

    st.altair_chart(avg_bar)

    # DYNAMIC CHART (pie + slider + session state)
    st.subheader("Dynamic Chart: Share of Responses by Dining Spot")

    if "min_rating" not in st.session_state:
        st.session_state["min_rating"] = 1

    st.slider("Only count ratings of at least:", 1, 5, key="min_rating")

    rated_df = csv_df[csv_df["value"] >= st.session_state["min_rating"]]

    if rated_df.empty:
        st.info("No responses have a rating that high yet. Try a lower number.")
    else:
        counts_df = rated_df.groupby("category").size().reset_index(name="count")

        pie = alt.Chart(counts_df).mark_arc().encode(
            theta=alt.Theta("count:Q", title="Responses"),
            color=alt.Color("category:N", title="Dining Spot"),
            tooltip=["category:N", "count:Q"],
        ).properties(title="Responses by Dining Spot")

        st.altair_chart(pie)

        # EXTRA CREDIT: mean and median that update with the slider
        mean_now = rated_df["value"].mean()
        median_now = rated_df["value"].median()

        if "shown" not in st.session_state:
            st.session_state["shown"] = {
                "min": st.session_state["min_rating"],
                "mean": mean_now,
                "median": median_now,
            }
            st.session_state["previous"] = None

        if st.session_state["shown"]["min"] != st.session_state["min_rating"]:
            st.session_state["previous"] = st.session_state["shown"]
            st.session_state["shown"] = {
                "min": st.session_state["min_rating"],
                "mean": mean_now,
                "median": median_now,
            }

        previous = st.session_state["previous"]
        if previous is None:
            mean_delta = None
            median_delta = None
        else:
            mean_delta = round(mean_now - previous["mean"], 2)
            median_delta = round(median_now - previous["median"], 2)

        col1, col2 = st.columns(2)
        col1.metric("Mean rating", round(mean_now, 2), delta=mean_delta)
        col2.metric("Median rating", round(median_now, 2), delta=median_delta)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet. Fill out the Survey page first.")