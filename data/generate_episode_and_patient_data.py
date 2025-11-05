import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# --- CONFIG ---
N_PATIENTS = 3000
N_EPISODES = 10000
FY_START = datetime(2024, 4, 1)
FY_END = datetime(2025, 3, 31)
random.seed(42)
np.random.seed(42)

# --- LOAD HRG CODES FROM NHS TARIFF EXCEL ---
tariff_path = "25-26NHSPS-prices-pay-award.xlsx"
try:
    tariff = pd.read_excel(tariff_path, sheet_name=None)
    for name, df in tariff.items():
        if any('HRG' in str(c).upper() for c in df.columns):
            tariff_df = df
            break
    hrg_col = [c for c in tariff_df.columns if 'HRG' in str(c).upper()][0]
    HRG_CODES = list(tariff_df[hrg_col].dropna().unique())
    print(f"Loaded {len(HRG_CODES)} HRG codes from tariff Excel")
except Exception as e:
    print("⚠️  Could not read HRG codes from tariff Excel:", e)
    HRG_CODES = [f"HRG{str(i).zfill(3)}" for i in range(1, 301)]

# --- HELPERS ---
def random_date():
    delta = FY_END - FY_START
    start_offset = random.randint(0, delta.days)
    los = random.randint(1, 14)
    start = FY_START + timedelta(days=start_offset)
    end = start + timedelta(days=los)
    return start.date(), end.date(), los

def weighted_choice(options, weights):
    return random.choices(options, weights=weights, k=1)[0]

# --- DEMOGRAPHICS ---
SEXES = ["M", "F"]
SEX_WEIGHTS = [0.48, 0.52]

ETHNIC_CODES = [
    "A","B","C","D","E","F","G","H","J","K","L","M","N","P","R","S","Z"
]
ETHNIC_WEIGHTS = [
    0.70,0.05,0.02,0.02,0.04,0.02,0.02,0.01,
    0.02,0.01,0.02,0.03,0.02,0.01,0.01,0.01,0.01
]

GP_PRACTICES = [f"A83{str(i).zfill(2)}" for i in range(1, 21)]
PROVIDERS = ["R0A", "RTE", "R1H", "RBD", "RWF", "RQ8"]

ICD10 = ["I21.9","J18.9","K35.8","C50.9","S82.1","N39.0","M16.0","E11.9","I50.9","O80.0"]
ICD10_WEIGHTS = [0.15,0.12,0.10,0.06,0.08,0.06,0.10,0.07,0.10,0.06]
OPCS4 = ["K49.1","J09.1","J10.3","H33.1","W44.3","H54.2","W47.2","Z37.0","I34.2","H50.1"]

# --- GENERATE PATIENTS ---
patients = []
for i in range(1, N_PATIENTS + 1):
    sex = weighted_choice(SEXES, SEX_WEIGHTS)
    ethnic = weighted_choice(ETHNIC_CODES, ETHNIC_WEIGHTS)
    age = int(np.clip(np.random.normal(58, 22), 0, 95))
    gp = random.choice(GP_PRACTICES)
    patients.append([f"PAT{i:05d}", sex, age, ethnic, gp])

patients_df = pd.DataFrame(patients, columns=[
    "PATIENT_ID","SEX","AGE_AT_REFERENCE","ETHNIC_CATEGORY","GP_PRACTICE_CODE"
])
patients_df.to_csv("bronze_patients.csv", index=False)
print("✅ Created bronze_patients.csv")

# --- GENERATE EPISODES ---
episodes = []
for i in range(1, N_EPISODES + 1):
    patient = random.choice(patients_df["PATIENT_ID"].values)
    spell = f"SPL{random.randint(1, N_EPISODES//2):05d}"
    provider = weighted_choice(PROVIDERS, [0.25,0.2,0.2,0.15,0.1,0.1])
    admission, discharge, los = random_date()
    method = weighted_choice(["Emergency","Elective"], [0.65,0.35])
    specialty = random.choice(range(100, 800, 10))
    tfc = specialty
    diag = weighted_choice(ICD10, ICD10_WEIGHTS)
    proc = random.choice(OPCS4)
    hrg = random.choice(HRG_CODES)
    seq = random.randint(1, 3)
    episodes.append([
        f"EPI{i:05d}", spell, patient, provider, admission, discharge, method,
        specialty, tfc, diag, proc, hrg, None, los, seq
    ])

episodes_df = pd.DataFrame(episodes, columns=[
    "EPISODE_ID","SPELL_ID","PATIENT_ID","PROVIDER_CODE","ADMISSION_DATE","DISCHARGE_DATE",
    "ADMISSION_METHOD","MAIN_SPECIALTY_CODE","TREATMENT_FUNCTION_CODE",
    "DIAGNOSIS_PRIMARY","PROCEDURE_PRIMARY","HRG_CODE","TARIFF_PRICE",
    "LOS","EPISODE_SEQUENCE_NUMBER"
])
episodes_df.to_csv("bronze_episodes.csv", index=False)
print("✅ Created bronze_episodes.csv")
print("🎉 All done!")
