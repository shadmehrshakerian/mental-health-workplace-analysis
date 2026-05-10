
import pandas as pd
import os
import re
import numpy as np

folder_path = r"C:\Users\shadm\Downloads\archive"

# Load files
df_2014 = pd.read_csv(os.path.join(folder_path, "survey_2014.csv"))
df_2016 = pd.read_csv(os.path.join(folder_path, "survey_2016.csv"))
df_2017 = pd.read_csv(os.path.join(folder_path, "survey_2017.csv"))
df_2018 = pd.read_csv(os.path.join(folder_path, "survey_2018.csv"))

df_2014["year"] = 2014
df_2016["year"] = 2016
df_2017["year"] = 2017
df_2018["year"] = 2018

# Strip HTML tags and special characters
def clean_columns(df):
    df.columns = [re.sub(r"<[^>]+>", "", col).strip().lower() for col in df.columns]
    df.columns = [col.replace("\xa0", " ") for col in df.columns]
    return df

df_2014 = clean_columns(df_2014)
df_2016 = clean_columns(df_2016)
df_2017 = clean_columns(df_2017)
df_2018 = clean_columns(df_2018)

# Column mappings
cols_2014 = {
    "are you self-employed?"                                                                                    : "self_employed",
    "have you sought treatment for a mental health condition?"                                                  : "sought_treatment",
    "does your employer provide mental health benefits?"                                                        : "employer_benefits",
    "do you feel that your employer takes mental health as seriously as physical health?"                       : "employer_takes_seriously",
    "do you think that discussing a mental health issue with your employer would have negative consequences?"   : "fear_negative_consequences",
    "if you have a mental health condition, do you feel that it interferes with your work?"                    : "work_interference",
    "do you work remotely (outside of an office) at least 50% of the time?"                                   : "remote_work",
    "gender"                                                                                                    : "gender",
    "age"                                                                                                       : "age",
    "country"                                                                                                   : "country",
    "year"                                                                                                      : "year"
}

cols_2016 = {
    "are you self-employed?"                                                                                    : "self_employed",
    "have you ever sought treatment for a mental health issue from a mental health professional?"               : "sought_treatment",
    "does your employer provide mental health benefits as part of healthcare coverage?"                         : "employer_benefits",
    "do you feel that your employer takes mental health as seriously as physical health?"                       : "employer_takes_seriously",
    "do you think that discussing a mental health disorder with your employer would have negative consequences?": "fear_negative_consequences",
    "do you believe your productivity is ever affected by a mental health issue?"                               : "productivity_affected",
    "do you currently have a mental health disorder?"                                                           : "has_mental_health_disorder",
    "do you work remotely?"                                                                                     : "remote_work",
    "what is your gender?"                                                                                      : "gender",
    "what is your age?"                                                                                         : "age",
    "what country do you live in?"                                                                              : "country",
    "is your primary role within your company related to tech/it?"                                             : "tech_role",
    "year"                                                                                                      : "year"
}

cols_2017_2018 = {
    "are you self-employed?"                                                                                    : "self_employed",
    "have you ever sought treatment for a mental health disorder from a mental health professional?"            : "sought_treatment",
    "does your employer provide mental health benefits as part of healthcare coverage?"                         : "employer_benefits",
    "do you believe your productivity is ever affected by a mental health issue?"                               : "productivity_affected",
    "do you currently have a mental health disorder?"                                                           : "has_mental_health_disorder",
    "what is your gender?"                                                                                      : "gender",
    "what is your age?"                                                                                         : "age",
    "what country do you live in?"                                                                              : "country",
    "is your primary role within your company related to tech/it?"                                             : "tech_role",
    "year"                                                                                                      : "year"
}

# Rename and select columns
df_2014_clean = df_2014.rename(columns=cols_2014)[list(cols_2014.values())]
df_2016_clean = df_2016.rename(columns=cols_2016)[list(cols_2016.values())]
df_2017_clean = df_2017.rename(columns=cols_2017_2018)[list(cols_2017_2018.values())]
df_2018_clean = df_2018.rename(columns=cols_2017_2018)[list(cols_2017_2018.values())]

# Combine into master dataset
master_df = pd.concat([df_2014_clean, df_2016_clean, df_2017_clean, df_2018_clean], ignore_index=True)

# Clean age
master_df["age"] = pd.to_numeric(master_df["age"], errors="coerce")
master_df.loc[~master_df["age"].between(16, 80), "age"] = np.nan

# Clean gender
def clean_gender(val):
    if pd.isnull(val): return np.nan
    val = str(val).strip().lower()
    if val in ["male", "m", "man", "cis male", "cis man", "make", "mal", "msle", "mail"]: return "Male"
    elif val in ["female", "f", "woman", "cis female", "cis woman", "femake", "femail"]: return "Female"
    else: return "Other"

master_df["gender"] = master_df["gender"].apply(clean_gender)

# Clean yes/no columns
def clean_yes_no(val):
    if pd.isnull(val): return np.nan
    val = str(val).strip().lower()
    if val in ["yes", "1", "1.0"]: return "Yes"
    elif val in ["no", "0", "0.0"]: return "No"
    else: return np.nan

master_df["sought_treatment"] = master_df["sought_treatment"].apply(clean_yes_no)
master_df["self_employed"] = master_df["self_employed"].apply(clean_yes_no)

# Clean employer benefits
def clean_benefits(val):
    if pd.isnull(val): return np.nan
    val = str(val).strip().lower()
    if val == "yes": return "Yes"
    elif val == "no": return "No"
    elif "don" in val and "know" in val: return "Dont Know"
    elif "not eligible" in val: return "Not Eligible"
    else: return np.nan

master_df["employer_benefits"] = master_df["employer_benefits"].apply(clean_benefits)

# Clean disorder status
def clean_disorder(val):
    if pd.isnull(val): return np.nan
    val = str(val).strip().lower()
    if val == "yes": return "Yes"
    elif val == "no": return "No"
    elif val in ["maybe", "possibly", "don't know"]: return "Uncertain"
    else: return np.nan

master_df["has_mental_health_disorder"] = master_df["has_mental_health_disorder"].apply(clean_disorder)

# Clean employer takes seriously
def clean_seriously(val):
    if pd.isnull(val): return np.nan
    val = str(val).strip().lower()
    if val == "yes": return "Yes"
    elif val == "no": return "No"
    elif "don" in val and "know" in val: return "Dont Know"
    else: return np.nan

master_df["employer_takes_seriously"] = master_df["employer_takes_seriously"].apply(clean_seriously)

# Create support level
master_df["support_level"] = "Low Support"
master_df.loc[
    (master_df["employer_benefits"] == "Yes") &
    (master_df["employer_takes_seriously"] == "Yes"),
    "support_level"
] = "High Support"
master_df.loc[
    (master_df["employer_benefits"] == "Yes") &
    (master_df["employer_takes_seriously"] != "Yes"),
    "support_level"
] = "Medium Support"

# Save final dataset
master_df.to_csv(r"C:\Users\shadm\Downloads\archive\master_mental_health_final.csv", index=False)
print("Done!")
