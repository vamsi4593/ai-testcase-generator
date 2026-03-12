import streamlit as st
import pandas as pd
import math
from core import testcase_generator as Tg
from utils import export_csv as Exp

st.set_page_config(page_title="AI Test Case Generator", page_icon="🧪", layout="wide")

st.title("AI Test Case Generator")
st.caption("Generate structured functional and non-functional test cases using AI")

results_container = st.container()

requirement = st.sidebar.text_input("Enter Requirement")
test_type = st.sidebar.selectbox(
    "Select test type", ["functional", "non-functional", "both"]
)


# Generate testcases
if st.sidebar.button("Generate Test Cases"):

    if requirement.strip() == "":
        st.warning("Please enter a requirement")
    else:
        with st.spinner("Generating Test Cases..."):
            st.session_state.testcases = Tg.generate_testcase(requirement, test_type)
            st.session_state.page_num = 0  # reset pagination


# Display testcases if they exist
with results_container:
    if "testcases" in st.session_state:

        testcases = st.session_state.testcases

        total_cases = len(testcases)
        total_steps = sum(len(testcase.steps) for testcase in testcases)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Cases", total_cases)
        col2.metric("Total Steps", total_steps)
        col3.metric("Test Type", Tg.normalised_test_type(test_type))

        items_per_page = 2
        total_pages = math.ceil(total_cases / items_per_page)

        page = st.session_state.get("page_num", 0)

        start = page * items_per_page
        end = start + items_per_page

        current_cases = testcases[start:end]

        # Render testcases
        for testcase in current_cases:

            st.markdown(f"### {testcase.test_case_id} — {testcase.title}")

            rows = []
            for step in testcase.steps:
                rows.append(
                    {
                        "Step": step.step_number,
                        "Action": step.action,
                        "Expected Result": step.expected_result,
                    }
                )

            df = pd.DataFrame(rows)

            st.dataframe(df, hide_index=True, use_container_width=True)
            st.divider()

        # Pagination buttons
        col1, col2, col3 = st.columns([1, 1, 3])

        with col1:
            if st.button("Previous", disabled=page <= 0):
                st.session_state.page_num -= 1
                st.rerun()

        with col2:
            if st.button("Next", disabled=page >= total_pages - 1):
                st.session_state.page_num += 1
                st.rerun()

        st.caption(f"Page {page + 1} of {total_pages}")

        # download test cases as csv
        if st.button("Export TestCases To CSV"):
            st.session_state.show_export = True

        if st.session_state.get("show_export", False):

            with st.form("Give File Name:"):
                csv_file_name = st.text_input(
                    "Enter Filename:", value=Exp.default_file_name(requirement)
                )

                submit = st.form_submit_button("Generate CSV")

                if submit:
                    st.session_state.csv_file_name = csv_file_name
                    st.session_state.download_ready = True

            if st.session_state.get("download_ready", False):

                csv_data = Exp.build_csv_data(testcases)
                st.download_button(
                    label="Submit",
                    data=csv_data,
                    file_name=csv_file_name,
                    mime="text/csv",
                )
    else:
        st.info("Enter a requirement and click Generate Test Cases.")
