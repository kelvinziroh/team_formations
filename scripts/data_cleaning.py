# Import modules
import numpy as np
import pandas as pd
import re


def extract_cohort(input_string):
    # Define the regex pattern
    pattern = re.compile(
        r"\d+|alumni|completed|pathway|aice|just started|not (?:yet(?: enrolled)?|sure)|i haven't been allocated one yet|software engineering|i don't know|front end web development|i am new",
        re.IGNORECASE,
    )

    # match the regex pattern in the string
    match = re.search(pattern, input_string)

    if match:
        if (
            (match.group().lower() == "alumni")
            or (match.group().lower() == "completed")
            or (match.group().lower() == "not yet")
            or (match.group().lower() == "not sure")
            or (match.group().lower() == "just started")
            or (match.group().lower() == "i haven't been allocated one yet")
            or (match.group().lower() == "pathway")
            or (match.group().lower() == "aice")
            or (match.group().lower() == "software engineering")
            or (match.group().lower() == "i don't know")
            or (match.group().lower() == "front end web development")
            or (match.group().lower() == "i am new")
        ):
            return 0
        elif match.group().lower() == "not yet enrolled":  # Very specific
            return np.NaN
        else:
            return int(match.group())
    else:
        return np.NaN


def clean_data(file_path):
    """Clean the dataset"""
    # Import the data from the .csv file
    df = pd.read_csv(file_path)  # "../data/dh_responses.csv"

    # Rename the columns
    df = df.rename(
        columns={
            "What course are you pursuing?": "course",
            "Which cohort do you belong to?": "cohort",
            "On a scale of  1 to 5 (1 being very unlikley and 5 being very likely), How likely are you to see this through to the end?": "cc_index",
        }
    )

    # Filter out the required columns
    df = df[["gender", "course", "cohort", "cc_index"]]

    # lower the case of text in gender and course columns
    df["gender"] = df["gender"].str.lower()
    df["course"] = df["course"].str.lower()

    # Extract the cohort
    df["cohort"] = df["cohort"].astype(str).str.strip().apply(extract_cohort)

    # Adjust da and ds cohorts greater than (latest cohorts)
    # latest ds cohort: 3
    # latest da cohort: 8
    df.loc[(df["course"] == "data science") & (df["cohort"] > 3), "cohort"] = 3
    df.loc[(df["course"] == "data analytics") & (df["cohort"] > 8), "cohort"] = 8

    # Add affiliation column to the dataframe
    df["alx_affiliated"] = df["cohort"].apply(
        lambda x: "Affiliated" if pd.notnull(x) else "Not affiliated"
    )

    return df


def persist_data(dataframe, file_path):
    """Export the dataframe to a .csv file"""
    dataframe.to_csv(file_path, index=False)


def main():
    # Original file path
    orig_file_path = "../data/dh_responses.csv"
    cleaned_file_path = "../data/cleaned_dh_responses.csv"

    # Clean the data
    clean_df = clean_data(orig_file_path)

    # export data
    persist_data(clean_df, cleaned_file_path)


if __name__ == "__main__":
    main()
