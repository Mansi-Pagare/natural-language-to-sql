# Natural Language to SQL

A small Python project that converts simple questions about hospital admissions into SQL queries and displays the results.

## What it does

- Counts hospital admissions
- Calculates the average length of stay
- Calculates the readmission rate
- Lists hospitals with the most admissions
- Displays the SQL query and its results

## Tools Used

- Python
- SQLite
- Streamlit

## Getting Started

Clone the repository and navigate to the project folder.

Install the dependency:

```bash
pip install streamlit
```

Create the sample database:

```bash
python database.py
```

Run the application:

```bash
streamlit run app.py
```

## Example Questions

- How many admissions are there?
- What is the average length of stay?
- What is the readmission rate?
- Top 3 hospitals with most admissions

## Notes

The project uses fictional hospital data and predefined question patterns. It is a learning project, and it currently supports only the questions listed above.

## Future Improvements

- Support more questions
- Add automated tests
- Explore LLM-based SQL generation
