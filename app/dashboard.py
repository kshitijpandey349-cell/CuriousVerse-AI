"""Initial CURIOUSVERSE local dashboard."""
import streamlit as st
from app.config import settings
from app.database import add_topic, initialize_database, list_topics

st.set_page_config(page_title=settings.app_name, page_icon="🎬", layout="wide")
initialize_database()
st.title("🎬 CURIOUSVERSE AI STUDIO")
st.caption("Your local workspace for original educational YouTube videos.")

with st.sidebar:
    st.header("Studio settings")
    st.write("Timezone:", settings.timezone)
    st.write("Default upload privacy:", settings.youtube_default_privacy)
    st.info("Public publishing is disabled by default. Review every video before release.")

col1, col2 = st.columns(2)
col1.metric("Daily target", "1 Short + 1 long video")
col2.metric("Current milestone", "Project foundation")

st.subheader("Topic research queue")
with st.form("add_topic", clear_on_submit=True):
    title = st.text_input("Video topic", placeholder="Why does the Moon look larger near the horizon?")
    category = st.selectbox("Category", ["science", "space", "technology", "history", "everyday mysteries"])
    notes = st.text_area("Notes (optional)")
    submitted = st.form_submit_button("Add topic")
    if submitted:
        try:
            add_topic(title, category, notes)
            st.success("Topic saved.")
        except ValueError as error:
            st.error(str(error))

topics = list_topics()
if topics:
    st.dataframe(
        [{"ID": r["id"], "Topic": r["title"], "Category": r["category"],
          "Status": r["status"], "Created": r["created_at"]} for r in topics],
        use_container_width=True, hide_index=True,
    )
else:
    st.info("No topics yet. Add your first topic above.")

st.divider()
st.warning(
    "Foundation milestone only: automated research, script generation, narration, "
    "video rendering, quality gates, YouTube OAuth uploads and scheduling remain to be built."
)