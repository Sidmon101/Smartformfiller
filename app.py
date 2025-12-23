import streamlit as st
from datetime import datetime

from langgraph_flow import build_graph
from agent_graph import init_state
from schemas import FORM_TYPES

st.set_page_config(page_title="Smart Form Filler", layout="wide")

# ======================================================
# Session defaults
# ======================================================
if "history" not in st.session_state:
    st.session_state.history = []

if "mode" not in st.session_state:
    st.session_state.mode = "FILLING"  # FILLING | SUMMARY | VIEW_HISTORY

if "active_history_item" not in st.session_state:
    st.session_state.active_history_item = None

# ======================================================
# Sidebar — Completed Forms
# ======================================================
st.sidebar.markdown("## 📂 Completed Forms")

if not st.session_state.history:
    st.sidebar.caption("No completed forms yet")
else:
    for idx, item in enumerate(st.session_state.history):
        if st.sidebar.button(
            item["title"],
            key=f"history_{idx}",
            use_container_width=True
        ):
            st.session_state.active_history_item = item
            st.session_state.mode = "VIEW_HISTORY"

# ======================================================
# CENTERED MAIN LAYOUT
# ======================================================
left_spacer, main_col, right_spacer = st.columns([2, 6, 2])

with main_col:

    # ======================================================
    # Main Header
    # ======================================================
    st.markdown(
        "<h1 style='margin-bottom:0.25rem;'>🧠 Smart Form Filler</h1>",
        unsafe_allow_html=True
    )

    # ======================================================
    # Form type selector (compact, top-left)
    # ======================================================
    col_form_type, _ = st.columns([3, 6])
    with col_form_type:
        form_type = st.selectbox(
            "Form type",
            FORM_TYPES,
            label_visibility="collapsed"
        )

    # ======================================================
    # Graph init
    # ======================================================
    if "graph" not in st.session_state:
        st.session_state.graph = build_graph()

    # ======================================================
    # VIEW HISTORY MODE
    # ======================================================
    if st.session_state.mode == "VIEW_HISTORY":
        item = st.session_state.active_history_item

        st.markdown("## 📄 Form Summary")
        st.caption(item["title"])

        for k, v in item["data"].items():
            st.markdown(f"**{k.replace('_', ' ').title()}**: {v}")

        if st.button("⬅ Back"):
            st.session_state.mode = "FILLING"
            st.session_state.active_history_item = None

        st.stop()

    # ======================================================
    # Initialize / reset form state
    # ======================================================
    if (
        "state" not in st.session_state
        or st.session_state.state["form_type"] != form_type
    ):
        st.session_state.state = init_state(form_type)
        st.session_state.mode = "FILLING"

        # Ask first question immediately
        st.session_state.state = st.session_state.graph.invoke(
            st.session_state.state
        )

    state = st.session_state.state

    # ======================================================
    # SUMMARY MODE
    # ======================================================
    if state["status"] == "COMPLETE" or st.session_state.mode == "SUMMARY":
        st.session_state.mode = "SUMMARY"

        st.markdown("## 📄 Form Summary")

        for k, v in state["form_data"].items():
            st.markdown(f"**{k.replace('_', ' ').title()}**: {v}")

        if "pending_save" not in st.session_state:
            st.session_state.pending_save = False

        if not st.session_state.pending_save:
            if st.button("✅ Save Form"):
                st.session_state.pending_save = True
                st.rerun()
        else:
            default_name = f"{form_type} – {datetime.now().strftime('%Y-%m-%d')}"

            custom_name = st.text_input(
                "Form name",
                value=default_name,
                placeholder="Enter a custom name for this form"
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("💾 Save & Start New Form", use_container_width=True):
                    st.session_state.history.insert(0, {
                        "title": custom_name.strip() or default_name,
                        "form_type": form_type,
                        "data": state["form_data"]
                    })

                    st.session_state.pending_save = False
                    st.session_state.mode = "FILLING"
                    st.session_state.state = init_state(form_type)

                    st.session_state.state = st.session_state.graph.invoke(
                        st.session_state.state
                    )
                    st.rerun()

            with col2:
                if st.button("❌ Cancel", use_container_width=True):
                    st.session_state.pending_save = False
                    st.rerun()

        st.stop()

    # ======================================================
    # FILLING MODE — Question
    # ======================================================
    question = None
    for msg in reversed(state["messages"]):
        if msg["role"] == "assistant":
            question = msg["content"]
            break

    if question:
        st.markdown(
            f"""
            <div style="
                font-size: 1.4rem;
                font-weight: 600;
                margin-top: 2rem;
                margin-bottom: 0.75rem;
            ">
                {question}
            </div>
            """,
            unsafe_allow_html=True
        )

    # ======================================================
    # Answer input and Submit button (compact)
    # ======================================================
    if "answer_input" not in st.session_state:
        st.session_state.answer_input = ""

    answer = st.text_input(
        "",
        key="answer_input",
        placeholder="Type your answer here..."
    )

    # Submit button in a small column so it doesn't stretch
    col_submit, _ = st.columns([2, 6])
    with col_submit:
        if st.button("Submit"):
            if answer.strip():
                state["last_user_input"] = answer
                st.session_state.state = st.session_state.graph.invoke(state)
                st.session_state.state["last_user_input"] = None
                st.rerun()
