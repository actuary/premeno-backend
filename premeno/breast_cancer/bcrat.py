import math
import pickle
from dataclasses import dataclass
from itertools import product
from typing import Optional

import numpy as np
import pandas as pd


@dataclass
class BCRAT:
    T1: Optional[float]
    T2: Optional[float]
    N_Biop: Optional[int]
    HypPlas: Optional[int]
    AgeMen: Optional[float]
    Age1st: Optional[float]
    N_Rels: Optional[int]
    Race: Optional[str]


def recode_N_Biop(N_Biop, HypPlas, Race):
    NB_Cat = None

    if (N_Biop == 0 or N_Biop == 99) and HypPlas != 99:
        return None

    if N_Biop > 0 and N_Biop < 99 and HypPlas not in (0, 1, 99):
        return None

    if NB_Cat is None and N_Biop in (0, 99):
        NB_Cat = 0

    if NB_Cat is None and N_Biop == 1:
        NB_Cat = 1

    if NB_Cat is None and 2 <= N_Biop < 99:
        NB_Cat = 2

    if NB_Cat is None:
        return None

    if Race in [3, 5] and NB_Cat and NB_Cat >= 2:
        NB_Cat = 1

    return NB_Cat


def recode_age_men(AgeMen, T1, Race):
    AM_Cat = None

    if (14 <= AgeMen <= T1) or AgeMen == 99:
        AM_Cat = 0

    elif 12 <= AgeMen < 14:
        AM_Cat = 1

    elif 0 < AgeMen < 12:
        AM_Cat = 2

    if Race == 2 and AM_Cat == 2:
        AM_Cat = 1

    if Race == 3:
        AM_Cat = 0

    return AM_Cat


def recode_age_1st(Age1st, AgeMen, T1, Race):
    AF_Cat = None

    if Age1st < 20 or Age1st == 99:
        AF_Cat = 0

    if 20 <= Age1st < 25:
        AF_Cat = 1

    if 25 <= Age1st < 30 or Age1st == 98:
        AF_Cat = 2

    if 30 <= Age1st < 98:
        AF_Cat = 3

    if AgeMen != 99 and Age1st < AgeMen:
        return None

    if T1 < Age1st < 98:
        return None

    if Race == 2:
        AF_Cat = 0

    if Race in (3, 5) and Age1st != 98 and AF_Cat == 2:
        AF_Cat = 1

    if Race in (3, 5) and AF_Cat == 3:
        AF_Cat = 2

    return AF_Cat


def recode_N_rel(N_Rels, Race):
    NR_Cat = None

    if N_Rels == 0 or N_Rels == 99:
        NR_Cat = 0

    if N_Rels == 1:
        NR_Cat = 1

    if 2 <= N_Rels < 99:
        NR_Cat = 2

    if 6 <= Race <= 11 and NR_Cat == 2:
        NR_Cat = 1

    if Race in (3, 5) and NR_Cat == 2:
        NR_Cat = 1

    return NR_Cat


def recode_race(Race):
    if Race not in range(1, 12):
        return None

    return Race


def get_RR_factor(HypPlas, NB_Cat):
    if NB_Cat is None:
        return None

    if NB_Cat == 0:
        return 1.00

    if NB_Cat > 0:
        if HypPlas == 0:
            return 0.93
        elif HypPlas == 1:
            return 1.82
        elif HypPlas == 99:
            return 1.00

    return None


def recode_age(age):
    if age < 20 or age > 90:
        return None
    return age


def recode_T1(T1, T2):
    if T1 < 20 or T1 >= 90 or T1 >= T2:
        return None
    return T1


def recode_T2(T1, T2):
    if T2 > 90 or T1 >= T2:
        return None
    return T2


def char_race(Race):
    CharRace = "??"

    race_to_char = {
        1: "Wh",
        2: "AA",
        3: "HU",
        4: "NA",
        5: "HF",
        6: "Ch",
        7: "Ja",
        8: "Fi",
        9: "Hw",
        10: "oP",
        11: "oA",
    }

    if Race in race_to_char.keys():
        CharRace = race_to_char[Race]

    return CharRace


@dataclass
class BCRAT_Factors:
    T1: Optional[int]
    T2: Optional[int]
    NB_Cat: Optional[int]
    AM_Cat: Optional[int]
    AF_Cat: Optional[int]
    NR_Cat: Optional[int]
    R_Hyp: Optional[float]
    HypPlas: Optional[float]
    Race: Optional[int]

    @property
    def is_valid(self) -> bool:
        return (
            self.T1 is not None
            and self.T2 is not None
            and self.NB_Cat is not None
            and self.AM_Cat is not None
            and self.AF_Cat is not None
            and self.NR_Cat is not None
            and self.R_Hyp is not None
            and self.HypPlas is not None
            and self.Race is not None
            and self.T2 > self.T1
        )

    @property
    def to_csv_row(self) -> str:
        return f"{self.T1},{self.T2},{self.NB_Cat},{self.AM_Cat},{self.AF_Cat},{self.NR_Cat},{self.R_Hyp},{self.HypPlas},{self.Race},{self.is_valid}\n"


def recode_HypPlas(HypPlas, NB_Cat):
    if NB_Cat is None or HypPlas is None:
        return None

    return HypPlas


def recode_check_v2(data):
    T1 = recode_T1(data.T1, data.T2)
    T2 = recode_T2(data.T1, data.T2)
    NB_Cat = recode_N_Biop(data.N_Biop, data.HypPlas, data.Race)
    AM_Cat = recode_age_men(data.AgeMen, data.T1, data.Race)
    AF_Cat = recode_age_1st(data.Age1st, data.AgeMen, data.T1, data.Race)
    NR_Cat = recode_N_rel(data.N_Rels, data.Race)
    HypPlas = recode_HypPlas(data.HypPlas, NB_Cat)
    R_Hyp = get_RR_factor(data.HypPlas, NB_Cat)
    Race = recode_race(data.Race)

    return BCRAT_Factors(T1, T2, NB_Cat, AM_Cat, AF_Cat, NR_Cat, R_Hyp, HypPlas, Race)


# Make sure my version of NB_Cat is correct
def recode_check(data, Raw_Ind=1):
    ### set error indicator to default value of 0 for each subject
    ## if mean not 0, implies ERROR in file
    Error_Ind = np.zeros(data.shape[0])
    ### test for consistency of T1 (initial age) and T2 (projection age)
    set_T1_missing = data.T1.values.copy().astype(float)

    set_T2_missing = data.T2.values.copy().astype(float)
    set_T1_missing[
        np.where((data.T1 < 20) | (data.T1 >= 90) | (data.T1 >= data.T2))
    ] = np.nan
    set_T2_missing[(data.T2.values > 90) | (data.T1.values >= data.T2.values)] = np.nan
    Error_Ind[np.isnan(set_T1_missing)] = 1
    Error_Ind[np.isnan(set_T2_missing)] = 1

    ### RR covariates are in raw/original format
    if Raw_Ind == 1:
        ### test for consistency of NumBiop (#biopsies) and Hyperplasia
        ## set NB_Cat to default value of -1
        NB_Cat = np.repeat(-1.0, data.shape[0])

        ## REQUIREMENT (A)
        NB_Cat[
            ((data.N_Biop == 0) | (data.N_Biop == 99)) & (data.HypPlas != 99)
        ] = np.nan

        Error_Ind[np.isnan(NB_Cat)] = 1

        ## REQUIREMENT (B)
        NB_Cat[
            ((data.N_Biop > 0) & (data.N_Biop < 99))
            & ((data.HypPlas != 0) & (data.HypPlas != 1) & (data.HypPlas != 99))
        ] = np.nan

        Error_Ind[np.isnan(NB_Cat)] = 1

        ### editing and recoding for N_Biop
        NB_Cat[(NB_Cat == -1) & ((data.N_Biop == 0) | (data.N_Biop == 99))] = 0

        NB_Cat[(NB_Cat == -1) & (data.N_Biop == 1)] = 1
        NB_Cat[(NB_Cat == -1) & ((data.N_Biop >= 2) | (data.N_Biop != 99))] = 2
        NB_Cat[NB_Cat == -1] = np.nan

        ### editing and recoding for AgeMen
        AM_Cat = np.repeat(np.nan, data.shape[0])
        AM_Cat[
            ((data.AgeMen >= 14) & (data.AgeMen <= data.T1)) | (data.AgeMen == 99)
        ] = 0
        AM_Cat[(data.AgeMen >= 12) & (data.AgeMen < 14)] = 1
        AM_Cat[(data.AgeMen > 0) & (data.AgeMen < 12)] = 2
        AM_Cat[(data.AgeMen > data.T1) & (data.AgeMen != 99)] = np.nan
        ## for African-Americans AgeMen code 2 (age <= 11) grouped with code 1(age == 12 or 13)
        AM_Cat[(data.Race == 2) & (AM_Cat == 2)] = 1

        ### editing and recoding for Age1st
        AF_Cat = np.repeat(np.nan, data.shape[0])
        AF_Cat[(data.Age1st < 20) | (data.Age1st == 99)] = 0
        AF_Cat[(data.Age1st >= 20) & (data.Age1st < 25)] = 1
        AF_Cat[((data.Age1st >= 25) & (data.Age1st < 30)) | (data.Age1st == 98)] = 2
        AF_Cat[(data.Age1st >= 30) & (data.Age1st < 98)] = 3
        AF_Cat[(data.Age1st < data.AgeMen) & (data.AgeMen != 99)] = np.nan
        AF_Cat[(data.Age1st > data.T1) & (data.Age1st < 98)] = np.nan
        ## for African-Americans Age1st is not a RR covariate and not in RR model, set to 0
        AF_Cat[data.Race == 2] = 0

        ### editing and recoding for N_Rels
        NR_Cat = np.repeat(np.nan, data.shape[0])
        NR_Cat[(data.N_Rels == 0) | (data.N_Rels == 99)] = 0
        NR_Cat[data.N_Rels == 1] = 1
        NR_Cat[(data.N_Rels >= 2) & (data.N_Rels < 99)] = 2
        ## for Asian-American NR_Cat=2 is pooled with NR_Cat=2
        NR_Cat[((data.Race >= 6) & (data.Race <= 11)) & (NR_Cat == 2)] = 1

    ### Raw_Ind=0 means RR covariates have already been re-coded to 0, 1, 2 or 3 (when necessary)
    ### edit/consistency checks for all relative four risk covariates not performed when Raw_Ind=0. (use this option at your own risk)
    if Raw_Ind == 0:
        NB_Cat = data.N_Biop
        AM_Cat = data.AgeMen
        AF_Cat = data.Age1st
        NR_Cat = data.N_Rels

    ### setting RR multiplicative factor for atypical hyperplasia
    R_Hyp = np.repeat(np.nan, data.shape[0])
    R_Hyp[NB_Cat == 0] = 1.00
    R_Hyp[(~np.isnan(NB_Cat) & (NB_Cat > 0)) & (data.HypPlas == 0)] = 0.93
    R_Hyp[(~np.isnan(NB_Cat) & (NB_Cat > 0)) & (data.HypPlas == 1)] = 1.82
    R_Hyp[(~np.isnan(NB_Cat) & (NB_Cat > 0)) & (data.HypPlas == 99)] = 1.00

    set_HyperP_missing = data.HypPlas.values.astype(float)
    set_R_Hyp_missing = R_Hyp.copy().astype(float)
    set_HyperP_missing[np.isnan(NB_Cat)] = np.nan
    set_R_Hyp_missing[np.isnan(NB_Cat)] = np.nan

    set_Race_missing = data.Race.values.astype(float)
    Race_range = np.array(range(1, 12))
    set_Race_missing[-data.Race.isin(Race_range)] = np.nan

    Error_Ind[
        (np.isnan(NB_Cat))
        | (np.isnan(AM_Cat))
        | (np.isnan(AF_Cat))
        | (np.isnan(NR_Cat))
        | (np.isnan(set_Race_missing))
    ] = 1

    ### african-american RR model from CARE study:(1) eliminates Age1st from model;(2) groups AgeMen=2 with AgeMen=1;
    ## setting AF_Cat=0 eliminates Age1st and its interaction from RR model;
    AF_Cat[data.Race == 2] = 0
    ## group AgeMen RR level 2 with 1;
    AM_Cat[(data.Race == 2) & (AM_Cat == 2)] = 1

    ### hispanic RR model from San Francisco Bay Area Breast Cancer Study (SFBCS):
    ###         (1) groups N_Biop ge 2 with N_Biop eq 1
    ###         (2) eliminates  AgeMen from model for US Born hispanic women
    ###         (3) group Age1st=25-29 with Age1st=20-24 and code as 1
    ###             for   Age1st=30+, 98 (nulliparous)       code as 2
    ###         (4) groups N_Rels=2 with N_Rels=1;
    NB_Cat[(data.Race.isin([3, 5])) & (data.N_Biop.isin([0, 99]))] = 0
    NB_Cat[(data.Race.isin([3, 5])) & (NB_Cat == 2)] = 1
    AM_Cat[data.Race == 3] = 0

    AF_Cat[(data.Race.isin([3, 5])) & (data.Age1st != 98) & (AF_Cat == 2)] = 1
    AF_Cat[(data.Race.isin([3, 5])) & (AF_Cat == 3)] = 2
    NR_Cat[(data.Race.isin([3, 5])) & (NR_Cat == 2)] = 1

    ### for asian-americans NR_Cat=2 is pooled with NR_Cat=1;
    NR_Cat[(data.Race >= 6) & (data.Race <= 11) & (NR_Cat == 2)] = 1

    CharRace = np.repeat("??", data.shape[0])
    CharRace[data.Race == 1] = "Wh"  # white SEER 1983:87 BrCa Rate
    CharRace[data.Race == 2] = "AA"  # african-american
    CharRace[data.Race == 3] = "HU"  # hispanic-american (US born)
    CharRace[data.Race == 4] = "NA"  # other (native american and unknown race)
    CharRace[data.Race == 5] = "HF"  # hispanic-american (foreign born)
    CharRace[data.Race == 6] = "Ch"  # chinese
    CharRace[data.Race == 7] = "Ja"  # japanese
    CharRace[data.Race == 8] = "Fi"  # filipino
    CharRace[data.Race == 9] = "Hw"  # hawaiian
    CharRace[data.Race == 10] = "oP"  # other pacific islander
    CharRace[data.Race == 11] = "oA"  # other asian

    recode_check = pd.DataFrame(
        {
            "Error_Ind": Error_Ind,
            "T1": set_T1_missing,
            "T2": set_T2_missing,
            "NB_Cat": NB_Cat,
            "AM_Cat": AM_Cat,
            "AF_Cat": AF_Cat,
            "NR_Cat": NR_Cat,
            "R_Hyp_A": R_Hyp,
            "HypPlas": set_HyperP_missing,
            "R_Hyp": set_R_Hyp_missing,
            "Race": set_Race_missing,
            "CharRace": CharRace,
        }
    )
    return recode_check


def convert_pd_to_namedtuples(data):
    return list(data.itertuples(name="Row", index=False))


def convert_row_to_BCRAT(row):
    return BCRAT(
        row.T1,
        row.T2,
        row.N_Biop,
        row.HypPlas,
        row.AgeMen,
        row.Age1st,
        row.N_Rels,
        row.Race,
    )


def relativeRisk(
    race, numberOfBiopies, ageFirstChild, ageMenarche, numberRelatives, rHyp
):
    betas = {
        "white": [
            0.5292641686,
            0.0940103059,
            0.2186262218,
            0.9583027845,
            -0.2880424830,
            -0.1908113865,
        ],
        "black": [0.1822121131, 0.2672530336, 0.0, 0.4757242578, -0.1119411682, 0.0],
        "hispanic": [
            0.0970783641,
            0.0000000000,
            0.2318368334,
            0.166685441,
            0.0000000000,
            0.0000000000,
        ],
        "other_hispanic": [
            0.4798624017,
            0.2593922322,
            0.4669246218,
            0.9076679727,
            0.0000000000,
            0.0000000000,
        ],
        "other": [
            0.5292641686,
            0.0940103059,
            0.2186262218,
            0.9583027845,
            -0.2880424830,
            -0.1908113865,
        ],
        "asian": [
            0.55263612260619,
            0.07499257592975,
            0.27638268294593,
            0.79185633720481,
            0.0,
            0.0,
        ],
    }

    beta = betas[race]
    lp1 = (
        numberOfBiopies * beta[0]
        + ageMenarche * beta[1]
        + ageFirstChild * beta[2]
        + numberRelatives * beta[3]
        + ageFirstChild * numberRelatives * beta[5]
        + math.log(rHyp)
    )
    lp2 = lp1 + numberOfBiopies * beta[4]

    return (math.exp(lp1), math.exp(lp2))


def compare_values(v1, v2):
    if v1.T1 != v2.T1:
        print("T1s differ: v1=" + str(v1.T1) + ", v2=" + str(v2.T1))
    if v1.T2 != v2.T2:
        print("T2s differ: v1=" + str(v1.T2) + ", v2=" + str(v2.T2))
    if v1.NB_Cat != v2.NB_Cat:
        print("NB_Cats differ: v1=" + str(v1.NB_Cat) + ", v2=" + str(v2.NB_Cat))
    if v1.AM_Cat != v2.AM_Cat:
        print("AM_Cats differ: v1=" + str(v1.AM_Cat) + ", v2=" + str(v2.AM_Cat))
    if v1.AF_Cat != v2.AF_Cat:
        print("AF_Cats differ: v1=" + str(v1.AF_Cat) + ", v2=" + str(v2.AF_Cat))
    if v1.NR_Cat != v2.NR_Cat:
        print("NR_Cats differ: v1=" + str(v1.NR_Cat) + ", v2=" + str(v2.NR_Cat))
    if v1.R_Hyp != v2.R_Hyp:
        print("R_Hyp differ: v1=" + str(v1.R_Hyp) + ", v2=" + str(v2.R_Hyp))
    if v1.Race != v2.Race:
        print("Race differ: v1=" + str(v1.Race) + ", v2=" + str(v2.Race))


def replace_in_file(to_read, to_save, to_replace, replacement):
    with open(to_read) as file_read:
        with open(to_save, "w") as file_write:
            file_write.write(file_read.read().replace(to_replace, replacement))


def coerce_to_float(val):
    if val == "None":
        return None
    else:
        return float(val)


def compare_row(v1, v2):
    if not v1[1].is_valid and v2[1].Error_Ind == 1:
        return False

    if str(v1[1].NB_Cat) != str(v2[1].NB_Cat):
        print(
            "NB_Cats differ: v1[1]="
            + str(v1[1].NB_Cat)
            + ", v2[1]="
            + str(v2[1].NB_Cat)
        )
    if str(v1[1].AM_Cat) != str(v2[1].AM_Cat):
        print(
            "AM_Cats differ: v1[1]="
            + str(v1[1].AM_Cat)
            + ", v2[1]="
            + str(v2[1].AM_Cat)
        )
    if str(v1[1].AF_Cat) != str(v2[1].AF_Cat):
        print(
            "AF_Cats differ: v1[1]="
            + str(v1[1].AF_Cat)
            + ", v2[1]="
            + str(v2[1].AF_Cat)
        )
    if str(v1[1].NR_Cat) != str(v2[1].NR_Cat):
        print(
            "NR_Cats differ: v1[1]="
            + str(v1[1].NR_Cat)
            + ", v2[1]="
            + str(v2[1].NR_Cat)
        )
    if coerce_to_float(v1[1].R_Hyp) != coerce_to_float(v2[1].R_Hyp):
        print("R_Hyp differ: v1[1]=" + str(v1[1].R_Hyp) + ", v2[1]=" + str(v2[1].R_Hyp))
    if v1[1].Race != v2[1].Race:
        print("Race differ: v1[1]=" + str(v1[1].Race) + ", v2[1]=" + str(v2[1].Race))
    return (
        v1[1].T1 != v2[1].T1
        or v1[1].T2 != v2[1].T2
        or v1[1].NB_Cat != v2[1].NB_Cat
        or v1[1].AM_Cat != v2[1].AM_Cat
        or v1[1].AF_Cat != v2[1].AF_Cat
        or v1[1].NR_Cat != v2[1].NR_Cat
        or coerce_to_float(v1[1].R_Hyp) != coerce_to_float(v2[1].R_Hyp)
        or v1[1].Race != v2[1].Race
    ) and not (v2[1].T1 == "None" and v2[1].T2 == "None")


def compare_files(file1, file2):
    py_file = pd.read_csv(file1)
    r_file = pd.read_csv(file2)

    for i, (py_row, r_row) in enumerate(zip(py_file.iterrows(), r_file.iterrows())):
        if compare_row(py_row, r_row):
            print(py_row, r_row)
            break


def compare_rows(before, after):
    T1 = (before.T1 is None and after.T1 is None) or (before.T1 == after.T1)
    T2 = (before.T2 is None and after.T2 is None) or (before.T2 == after.T2)
    NB_Cat = (before.NB_Cat is None and after.NB_Cat is None) or (
        before.NB_Cat == after.NB_Cat
    )
    AM_Cat = (before.AM_Cat is None and after.AM_Cat is None) or (
        before.AM_Cat == after.AM_Cat
    )
    AF_Cat = (before.AF_Cat is None and after.AF_Cat is None) or (
        before.AF_Cat == after.AF_Cat
    )
    NR_Cat = (before.NR_Cat is None and after.NR_Cat is None) or (
        before.NR_Cat == after.NR_Cat
    )
    R_Hyp = (before.R_Hyp is None and after.R_Hyp is None) or (
        before.R_Hyp == after.R_Hyp
    )
    HypPlas = (before.HypPlas is None and after.HypPlas is None) or (
        before.HypPlas == after.HypPlas
    )
    Race = (before.T1 is None and after.T1 is None) or (before.T1 == after.T1)

    return not (
        T1
        and T2
        and NB_Cat
        and AM_Cat
        and AF_Cat
        and NR_Cat
        and R_Hyp
        and HypPlas
        and Race
    )


def generate_all_combos():
    T1 = [19, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 98, 99]
    T2 = [19, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 98, 99]
    N_Biop = [0, 1, 2, 3, 99]
    HypPlas = [0, 1, 99]
    AgeMen = [0, 7, 8, 9, 11, 12, 13, 14, 99]
    Age1st = [19, 20, 22, 27, 32, 37]
    N_Rels = [0, 1, 2, 99]
    Race = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    (
        T1,
        T2,
        N_Biop,
        HypPlas,
        AgeMen,
        Age1st,
        N_Rels,
        Race,
    ) = pd.core.reshape.util.cartesian_product(
        [T1, T2, N_Biop, HypPlas, AgeMen, Age1st, N_Rels, Race]
    )

    return pd.DataFrame(
        dict(
            T2=T1,
            T1=T2,
            N_Biop=N_Biop,
            HypPlas=HypPlas,
            AgeMen=AgeMen,
            Age1st=Age1st,
            N_Rels=N_Rels,
            Race=Race,
        )
    )


import pickle
from collections import namedtuple


def save_object(obj, filename):
    with open(filename, "wb") as outp:
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    exampledata = pd.read_csv("./bcrat_data.csv")
    recoded_exampledata = recode_check(exampledata)
    all_combos = generate_all_combos()
    print("done")
    before = recode_check(all_combos)
    before = convert_pd_to_namedtuples(before.replace({np.nan: None}))
    Row = namedtuple(
        "Row",
        [
            "T1",
            "T2",
            "NB_Cat",
            "AM_Cat",
            "AF_Cat",
            "NR_Cat",
            "R_Hyp",
            "HypPlas",
            "Race",
            "Error_Ind",
        ],
    )

    before = [
        Row(
            row.T1,
            row.T2,
            row.NB_Cat,
            row.AM_Cat,
            row.AF_Cat,
            row.NR_Cat,
            row.R_Hyp,
            row.HypPlas,
            row.Race,
            row.Error_Ind,
        )
        for row in before
    ]
    print("done")
    after = [
        recode_check_v2(convert_row_to_BCRAT(row))
        for row in convert_pd_to_namedtuples(all_combos)
    ]
    print("done")
    save_object(before, "./before.pkl")
    save_object(after, "./after.pkl")

    # for brow, arow in zip(before, after):
    #     if compare_rows(brow, arow):
    #         print(brow)
    #         print(arow)
