
import sqlite3
import re
import streamlit as st

from database import create_database

DB_NAME = "hospital.db"

st.set_page_config(
    page_title="Natural Language to SQL",
    page_icon="🗃️",
    layout="centered"
)

st.title("Natural Language to SQL")
st.write(
    "Ask questions about fictional hospital admission data. "
    "The app translates supported questions into SQL."
)

# Create the database and sample records.
create_database()


def translate_question(question):
    """Translate supported natural-language questions into SQL."""

    q = question.lower().strip()

    if "how many admissions" in q:
        return """
            SELECT COUNT(*) AS total_admissions
            FROM admissions
        """

    if "average length of stay" in q:
        return """
            SELECT ROUND(AVG(length_of_stay), 2)
                   AS average_days
            FROM admissions
        """

    if "readmission rate" in q:
        return """
            SELECT ROUND(AVG(readmitted) * 100, 2)
                   AS readmission_rate_percent
            FROM admissions
        """

    match = re.search(r"\btop\s+(\d+)\s+hospitals\b", q)

    if match and "most admissions" in q:
        limit = int(match.group(1))

        if not 1 <= limit <= 10:
            raise ValueError(
                "Please choose between 1 and 10 hospitals."
            )

        return f"""
            SELECT hospital, COUNT(*) AS admissions
            FROM admissions
            GROUP BY hospital
            ORDER BY admissions DESC, hospital ASC
            LIMIT {limit}
        """

    raise ValueError(
        "I don't recognize that question yet. "
        "Please try one of the example questions below."
    )


st.subheader("Ask a question")

question = st.text_input(
    "Your question",
    placeholder="How many admissions are there?"
)

st.caption(
    "Examples: How many admissions are there? | "
    "What is the average length of stay? | "
    "What is the readmission rate? | "
    "Top 3 hospitals with most admissions"
)

if st.button("Generate SQL and Run", type="primary"):
    if not question.strip():
        st.warning("Please enter a question first.")

    else:
        try:
            sql = translate_question(question)

            st.subheader("Generated SQL")
            st.code(sql, language="sql")

            # Open the database in read-only mode.
            with sqlite3.connect(
                f"file:{DB_NAME}?mode=ro",
                uri=True
            ) as conn:
                cursor = conn.execute(sql)
                rows = cursor.fetchall()
                columns = [
                    description[0]
                    for description in cursor.description
                ]

            st.subheader("Query Results")

            if rows:
                st.dataframe(
                    [dict(zip(columns, row)) for row in rows],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("The query returned no results.")

        except ValueError as error:
            st.error(str(error))

        except sqlite3.Error:
            st.error(
                "The database query failed. "
                "Please check the database and try again."
            )

st.divider()
st.caption(
    "Educational prototype using synthetic data. "
    "This version uses predefined rules, not an LLM."
)
