from io import BytesIO
import textwrap

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


st.set_page_config(page_title="Lab 10 | Framing the Data Story", page_icon="📊", layout="wide")

NAME = "Nur Aidina binti Mohd Nasir"
STUDENT_ID = "22005974"
SOURCE = f"Data: fictional lab practice values (2026) | Chart: {NAME}"
AUDIENCES = ["Students", "Workshop instructor", "Department manager"]

ORIGINAL = pd.DataFrame({
    "Skill": ["Data storytelling", "Python", "Chart selection", "Color and labels", "Data cleaning"],
    "Average rating": [2.4, 3.0, 3.2, 3.7, 4.1],
})


def lowest_skills(data):
    """Find the lowest value, including any ties."""
    low = float(data["Average rating"].min())
    names = data.loc[data["Average rating"].eq(low), "Skill"].tolist()
    return low, names


def describe_skills(names):
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} and {names[1]}"
    return ", ".join(names[:-1]) + f", and {names[-1]}"


def story_text(data, audience):
    """Match the title, purpose and takeaway to the audience and current ratings."""
    low, names = lowest_skills(data)
    focus = describe_skills(names)
    plural = len(names) > 1
    if audience == "Students":
        purpose = "Choose which skill to practise in the next workshop."
        title = ("Skills with the lowest average self-rating" if plural
                 else f"{focus} has the lowest average self-rating")
        takeaway = f"Practise {focus.lower()} in the next workshop ({low:.1f}/5)."
    elif audience == "Workshop instructor":
        purpose = "Choose which topic should receive more teaching time."
        title = ("Plan teaching around the lowest-rated skills" if plural
                 else f"Prioritise {focus.lower()} in the next workshop")
        takeaway = f"Give {focus.lower()} focused teaching support ({low:.1f}/5)."
    else:
        purpose = "Decide how to prioritise workshop support and resources."
        title = ("Multiple skill gaps share the same lowest rating" if plural
                 else f"Workshop support is most needed for {focus.lower()}")
        takeaway = f"Prioritise support for {focus.lower()} ({low:.1f}/5)."
    return purpose, title, takeaway


def make_chart(data, title, emphasis, explanation):
    """Create a readable horizontal bar chart using one method of emphasis."""
    display = data.copy()
    if emphasis == "Position (lowest first)":
        display = display.sort_values("Average rating", kind="stable")

    low, names = lowest_skills(display)
    is_low = display["Average rating"].eq(low).tolist()
    if emphasis == "Contrasting colour":
        bar_colours = ["#E47738" if flag else "#5279A8" for flag in is_low]
    else:
        bar_colours = ["#5279A8"] * len(display)

    fig, ax = plt.subplots(figsize=(10, 5.5), facecolor="white")
    bars = ax.barh(display["Skill"], display["Average rating"],
                   color=bar_colours, height=0.63)
    ax.invert_yaxis()
    ax.set_xlim(0, 5.15)
    ax.set_xticks([0, 1, 2, 3, 4, 5])
    ax.set_xlabel("Average self-rating (1 = beginner, 5 = confident)", labelpad=9)
    ax.set_title("\n".join(textwrap.wrap(title, 57)),
                 loc="left", pad=16, fontsize=14, fontweight="bold")
    ax.grid(axis="x", linewidth=0.7, color="#DEE4EA")
    ax.set_axisbelow(True)
    for edge in ("top", "right", "left"):
        ax.spines[edge].set_visible(False)
    ax.tick_params(axis="both", length=0, labelsize=10)

    # Direct numeric labels eliminate the need for a colour legend.
    for bar, value in zip(bars, display["Average rating"]):
        x = float(value)
        y = bar.get_y() + bar.get_height() / 2
        if x > 4.5:
            ax.text(x - 0.10, y, f"{x:.1f}", ha="right", va="center",
                    fontsize=10, color="white", fontweight="bold")
        else:
            ax.text(x + 0.08, y, f"{x:.1f}", ha="left", va="center", fontsize=10)

    if emphasis == "Text annotation":
        first_index = is_low.index(True)
        ax.annotate("Lowest average" + (" (tie)" if len(names) > 1 else ""),
                    xy=(low, first_index), xycoords="data",
                    xytext=(4.8, first_index + 0.75 if first_index < len(display) - 1 else first_index - 0.75),
                    textcoords="data", ha="right", fontsize=9, color="#B45520",
                    bbox={"boxstyle": "round,pad=0.3", "fc": "#FFF2E8", "ec": "#EAC8AF"},
                    arrowprops={"arrowstyle": "->", "color": "#B45520"})

    fig.subplots_adjust(left=0.25, right=0.96, top=0.81, bottom=0.28)
    fig.text(0.06, 0.145, "\n".join(textwrap.wrap(explanation, width=119)),
             fontsize=9.2, color="#3F4752", va="top")
    fig.text(0.06, 0.05, SOURCE, fontsize=8, color="#626D79")
    return fig


def sample_peer_review(focus, low):
    return {
        "Reviewer": "Liyana (simulated peer-review example)",
        "Explanation of axes": (
            "The left side lists the data visualisation skills. The horizontal scale shows "
            "average self-ratings, where 1 means beginner and 5 means confident. Longer bars mean higher ratings."
        ),
        "Meaning of highlight": (
            f"The emphasis points to {focus.lower()}, the lowest-rated skill at {low:.1f} out of 5."
        ),
        "Message remembered": (
            f"The next workshop should spend more time on {focus.lower()} because it has the lowest average rating."
        ),
        "Point understood": "The chart makes the skill needing the most support easy to identify.",
        "Point unclear": (
            "At first, it was not obvious whether the averages represented students' confidence "
            "or their actual performance in a skills test."
        ),
        "Revision illustrated": (
            "Revised the horizontal-axis label to explain the 1–5 self-rating scale and added a "
            "sentence clarifying that the values are self-ratings, not tested proficiency."
        ),
    }


REFLECTION = (
    "Visual emphasis helps the audience notice one important finding instead of looking at every "
    "value equally. In this lab, I used fictional average self-ratings for five data visualisation "
    "skills to tell a workshop-planning story. The horizontal bars make the skill names readable, "
    "while the zero baseline keeps their lengths proportional. A contrasting colour can draw "
    "attention to the lowest average without making the other values difficult to compare. "
    "Explanatory text is important because the chart alone does not tell readers what decision "
    "to make. For students, the takeaway focuses on what to practise. For a workshop instructor, "
    "it focuses on what to teach first. I also changed the fictional Python rating from 3.0 "
    "to 2.1 and updated the title and emphasis to match the new finding. One possible point of "
    "confusion is whether the scores measure confidence or actual ability. I addressed this "
    "by explaining the scale and stating that the values are self-ratings, not test results. "
    "Keeping the graphic simple, using direct labels, and placing the explanation near the "
    "chart make the intended message easier to understand and remember."
)


st.sidebar.header("Student information")
st.sidebar.write(f"**Name:** {NAME}")
st.sidebar.write(f"**Student ID:** {STUDENT_ID}")
st.sidebar.write("**Course:** TFB3133: Data Visualization")
st.sidebar.write("**Assignment:** Lab 10 – Framing the Data Story")
st.sidebar.divider()
st.sidebar.subheader("Customize the data story")
audience = st.sidebar.selectbox("Audience", AUDIENCES, index=1)
changed_skill = st.sidebar.selectbox("Skill to adjust", ORIGINAL["Skill"].tolist(), index=1)
old_rating = float(ORIGINAL.loc[ORIGINAL["Skill"].eq(changed_skill), "Average rating"].iloc[0])
default_rating = 2.1 if changed_skill == "Python" else old_rating
new_rating = st.sidebar.slider(
    "Adjusted average rating", min_value=1.0, max_value=5.0,
    value=default_rating, step=0.1, key=f"rating_{changed_skill}",
)
emphasis = st.sidebar.radio(
    "Visual emphasis",
    ["Contrasting colour", "Position (lowest first)", "Text annotation"],
)

data = ORIGINAL.copy()
data.loc[data["Skill"].eq(changed_skill), "Average rating"] = float(new_rating)
low, lowest_names = lowest_skills(data)
original_low, original_names = lowest_skills(ORIGINAL)
focus = describe_skills(lowest_names)
purpose, title, takeaway = story_text(data, audience)
student_purpose, original_title, original_takeaway = story_text(ORIGINAL, "Students")
peer = sample_peer_review(focus, low)
explanation = (
    f"{focus} has the lowest fictional average rating ({low:.1f}/5). "
    "These are self-reported confidence ratings, not results from a practical skills test."
)

st.title("Lab 10: Framing the Data Story")
st.caption("TFB3133 | Audience-focused visualisation")

# Lesson 3, Task 1: Reframe the same story for different readers.
st.subheader("1. Reframe the story")
c1, c2 = st.columns(2)
with c1:
    st.markdown(f"**Audience:** {audience}")
    st.markdown(f"**Audience decision:** {purpose}")
with c2:
    st.markdown(f"**Chart message:** {title}")
    st.markdown(f"**Key takeaway:** {takeaway}")
st.write(
    "**Why the framing changed:** The original student version tells learners which skill to "
    "practise. The workshop-instructor version emphasises teaching time, while the department-manager "
    "version emphasises support and resource planning. The data remain the same when only the audience changes."
)
with st.expander("Compare the original student-focused version"):
    st.write(f"**Audience:** Students | **Decision:** {student_purpose}")
    st.write(f"**Original title:** {original_title}")
    st.write(f"**Original takeaway:** {original_takeaway}")

# Lesson 3, Task 2: Update one value, revise the label, and test visual emphasis.
st.subheader("2. Improve the chart")
m1, m2, m3 = st.columns(3)
m1.metric("Skills", len(data))
m2.metric("Lowest average", f"{low:.1f} / 5")
m3.metric("Adjusted skill", changed_skill, f"{new_rating - old_rating:+.1f} rating points")
st.write(
    f"**Rating experiment:** {changed_skill} changed from {old_rating:.1f} to {new_rating:.1f}. "
    f"Originally, {describe_skills(original_names)} was lowest ({original_low:.1f}/5); "
    f"the current lowest-rated skill is {focus} ({low:.1f}/5)."
)

fig = make_chart(data, title, emphasis, explanation)
st.pyplot(fig, use_container_width=True)
buffer = BytesIO()
fig.savefig(buffer, format="png", dpi=180, facecolor="white")
plt.close(fig)
st.download_button(
    "Download final chart (PNG)", buffer.getvalue(),
    file_name="Lab10_Final_Chart_22005974.png", mime="image/png",
)
st.caption("The category axis names five skills; the horizontal bars show fictional average ratings. Source and author are printed on the chart.")

st.markdown("**Design improvements demonstrated**")
st.write(
    "The revised axis label spells out the 1–5 scale, and the note below the chart distinguishes "
    "self-ratings from skill-test results. The unnecessary top, right, and left chart borders were "
    "removed. The direct value labels make a separate legend unnecessary. The sidebar lets you "
    "compare contrasting colour, position, and text annotation as alternative emphasis methods."
)

with st.expander("Five questions for explaining the graphic (Lesson 1)"):
    st.markdown(
        "1. **Axes:** Skill names are categorical; bar lengths show average ratings on a 1–5 scale.\n"
        "2. **Encodings:** Longer bars mean higher average ratings; the chosen emphasis identifies the lowest.\n"
        "3. **Level of detail:** The figures are fictional skill averages, not individual responses.\n"
        f"4. **What to notice:** {focus} is lowest at {low:.1f}/5.\n"
        f"5. **Takeaway:** {takeaway}"
    )

with st.expander("View the five rating values"):
    st.dataframe(data, hide_index=True, use_container_width=True)

# Lesson 3, Task 3: Completed, clearly labelled sample evaluation.
st.subheader("3. Audience understanding: example peer review")
st.caption(peer["Reviewer"])
st.write("**What the reader said about the axes:**", peer["Explanation of axes"])
st.write("**Meaning of the visual emphasis:**", peer["Meaning of highlight"])
st.write("**Takeaway remembered:**", peer["Message remembered"])
r1, r2 = st.columns(2)
with r1:
    st.markdown("**Point understood**")
    st.write(peer["Point understood"])
with r2:
    st.markdown("**Point that was unclear**")
    st.write(peer["Point unclear"])
st.markdown("**Revision illustrated after the sample feedback**")
st.write(peer["Revision illustrated"])

# Lesson 3, Task 4: Written summary and 150–200 word reflection.
st.subheader("4. Short report and reflection")
report_lines = [
    "LAB 10: FRAMING THE DATA STORY | SHORT REPORT",
    f"Name: {NAME} | Student ID: {STUDENT_ID}",
    "",
    f"Audience: {audience}",
    f"Purpose: {purpose}",
    f"Chart title: {title}",
    f"Key takeaway: {takeaway}",
    "Reframing: Students need a practice priority; instructors need a teaching priority; "
    "managers need a resource-planning priority.",
    f"Original lowest rating: {describe_skills(original_names)} ({original_low:.1f}/5)",
    f"Modified rating: {changed_skill}, {old_rating:.1f} -> {new_rating:.1f}/5",
    f"Current lowest rating: {focus} ({low:.1f}/5)",
    f"Visual emphasis: {emphasis}",
    f"Explanatory note: {explanation}",
    "Removed visual detail: Unnecessary plot borders and the need for a separate legend.",
    "",
    "PEER REVIEW SCENARIO (SIMULATED EXAMPLE; LIYANA)",
    f"Axes: {peer['Explanation of axes']}",
    f"Highlighted value: {peer['Meaning of highlight']}",
    f"Remembered message: {peer['Message remembered']}",
    f"Understood: {peer['Point understood']}",
    f"Unclear: {peer['Point unclear']}",
    f"Revision illustrated: {peer['Revision illustrated']}",
    "",
    f"REFLECTION ({len(REFLECTION.split())} words)",
    REFLECTION,
    "",
    f"Source: {SOURCE}",
]
report_text = "\n".join(report_lines)
st.write(
    "The chart prioritises the lowest average rather than treating every value as equally important. "
    "The takeaway, title and explanatory note remain consistent when the audience or data changes."
)
st.markdown(f"**Reflection ({len(REFLECTION.split())} words)**")
st.write(REFLECTION)
st.download_button(
    "Download short report and reflection (TXT)",
    data=report_text.encode("utf-8"),
    file_name="Lab10_Report_22005974.txt",
    mime="text/plain",
)
st.caption(SOURCE)
