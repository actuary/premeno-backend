from gail.gail import GailFactors, GailModel, Race
from risk import (
    BreastCancer,
    CanRisk,
    MhtStatus,
    canrisk_file_from_json,
    extract_cancer_rates,
    gail_from_json,
)


def project_canrisk(data, years=None):
    mht_type = MhtStatus.Combined if data["mht"] == "e+p" else MhtStatus.Oestrogen

    canrisk_file_no_mht = canrisk_file_from_json(data, MhtStatus.Never)
    canrisk_file_with_mht = canrisk_file_from_json(data, mht_type)

    results_no_mht = extract_cancer_rates(api.boadicea(str(canrisk_file_no_mht)))
    results_with_mht = extract_cancer_rates(api.boadicea(str(canrisk_file_with_mht)))

    no_mht = results_no_mht["individual"]
    mht = results_with_mht["individual"]

    return {
        "age": results_no_mht["age"],
        "background_risk": no_mht,
        "relative_risk": [mht[i] / no_mht[i] for i in range(len(mht))],
    }


def project_gail(data, years):
    gail = BreastCancer(data)
    age = gail_from_json(data).age

    return {
        "age": [int(age) + i for i in range(1, years + 1)],
        "background_risk": [gail.background_risk(i) for i in range(1, years + 1)],
        "relative_risk": [gail.relative_risk(i) for i in range(1, years + 1)],
    }


def get_baseline(
    age=0,
    age_at_menarche=0,
    age_at_first_child=0,
    oral_contra=True,
    breast_biop=0,
    hyperplasia=0,
    mother=0,
    sister=0,
    height=0,
    weight=0,
    alcohol=0,
):

    return {
        "date_of_birth": f"{1972 + age}-08-06T00:00:00.000Z",
        "height": str(162 + height),
        "height_unit": "cm",
        "weight": str(70 + weight),
        "weight_unit": "kg",
        "ethnic_group": "white",
        "education": "primary",
        "alcohol": str(0 + alcohol),
        "smoking": "never",
        "mht": "e+p",
        "age_at_menarche": str(13 + age_at_menarche),
        "age_at_first_child": str(29 + age_at_first_child),
        "no_children": "false",
        "oral_contra": "y" if oral_contra else "n",
        "biopsy": "n" if breast_biop == 0 else "y",
        "number_of_biopsies": str(0 + breast_biop),
        "hyperplasia": str(0 + hyperplasia),
        "mother_has_cancer": str(mother),
        "number_of_sisters": str(sister),
        "sister_age_at_diagnosis_0": "56",
        "sister_age_at_diagnosis_1": "56",
        "sister_age_at_diagnosis_2": "56",
        "sister_age_at_diagnosis_3": "56",
        "sister_age_at_diagnosis_4": "56",
    }


def get_comparison(base_results, new_results):
    return {
        "canrisk": new_results["canrisk"] - base_results["canrisk"],
        "gail": new_results["gail"] - base_results["gail"],
    }


def run(data):
    canrisk = project_canrisk(data, 5)
    gail = project_gail(data, 5)

    return {
        "canrisk": canrisk["background_risk"][4],
        "gail": gail["background_risk"][4],
    }


def get_sensitivity_row(base_results, data):
    new_data = get_baseline(**data)

    results = run(new_data)
    diffs = get_comparison(base_results, results)

    return f"{round(diffs['gail']*100, 2)}%, {round(diffs['canrisk']*100, 2)}%"


def sensitivities_data():
    base_data = {
        "age": 0,
        "age_at_menarche": 0,
        "age_at_first_child": 0,
        "oral_contra": True,
        "breast_biop": 0,
        "hyperplasia": 0,
        "mother": 0,
        "sister": 0,
        "height": 0,
        "weight": 0,
        "alcohol": 0,
    }

    base_results = run(get_baseline(**base_data))

    adjustments = {
        "age": [-5, -10, 5, 10],
        "height": [20, -20],
        "weight": [20, -20],
        "alcohol": [10, 50],
        "age_at_menarche": [3, -3],
        "age_at_first_child": [10, -10, -29],
        "oral_contra": [True, False],
        "breast_biop": [1, 2],
        "hyperplasia": [1, 2],
    }

    for fac in adjustments:
        data = base_data.copy()
        print(fac)
        if fac == "hyperplasia":
            data[fac] = 1
            for adj in adjustments["breast_biop"]:
                data["breast_biop"] = base_data["breast_biop"] + adj
                print(get_sensitivity_row(base_results, data))
        elif fac == "breast_biop":
            data["hyperplasia"] = 0
            for adj in adjustments[fac]:
                data[fac] = base_data["breast_biop"] + adj
                print(get_sensitivity_row(base_results, data))
        elif fac == "oral_contra":
            for adj in adjustments[fac]:
                data[fac] = adj
                print(get_sensitivity_row(base_results, data))
        else:
            for adj in adjustments[fac]:
                data[fac] = base_data[fac] + adj
                print(get_sensitivity_row(base_results, data))


def get_table_row(woman):
    woman["mht"] = "e"
    canrisk_e = project_canrisk(woman, 5)
    gail_e = project_gail(woman, 5)
    woman["mht"] = "e+p"
    canrisk_enp = project_canrisk(woman, 5)
    gail_enp = project_gail(woman, 5)

    print(
        f"ModifiedGail,"
        f"{round(gail_e['background_risk'][4]*100, 2)}%,"
        f"{round(gail_e['background_risk'][4]*gail_e['relative_risk'][4]*100, 2)}%,"
        f"{round(gail_enp['background_risk'][4]*gail_enp['relative_risk'][4]*100, 2)}%,"
        f"{round(gail_e['relative_risk'][4], 2)},"
        f"{round(gail_enp['relative_risk'][4], 2)}"
    )
    print(
        f"CanRisk,"
        f"{round(canrisk_e['background_risk'][4]*100, 2)}%,"
        f"{round(canrisk_e['background_risk'][4]*canrisk_e['relative_risk'][4]*100, 2)}%,"
        f"{round(canrisk_enp['background_risk'][4]*canrisk_enp['relative_risk'][4]*100, 2)}%,"
        f"{round(canrisk_e['relative_risk'][4], 2)},"
        f"{round(canrisk_enp['relative_risk'][4], 2)}"
    )


def baseline_table_data():
    baseline_woman = get_baseline()
    get_table_row(baseline_woman)


def projection_overtime_data():
    woman = get_baseline()
    woman["mht"] = "e"
    canrisk_e = project_canrisk(woman, 30)
    gail_e = project_gail(woman, 30)
    woman["mht"] = "e+p"
    canrisk_enp = project_canrisk(woman, 30)
    gail_enp = project_gail(woman, 30)

    with open("/Users/vernon/Documents/proj_file.csv", "w+") as file:
        file.write("model,age,background,relative_e,relative_enp\n")

        for i in range(10):
            file.write(
                f"canrisk,"
                f"{canrisk_e['age'][i]},"
                f"{canrisk_e['background_risk'][i]},"
                f"{canrisk_e['relative_risk'][i] * canrisk_e['background_risk'][i]},"
                f"{canrisk_enp['relative_risk'][i] * canrisk_e['background_risk'][i]}\n"
            )

        for i in range(30):
            file.write(
                f"gail,"
                f"{gail_e['age'][i]},"
                f"{gail_e['background_risk'][i]},"
                f"{gail_e['relative_risk'][i] * gail_e['background_risk'][i]},"
                f"{gail_enp['relative_risk'][i] * gail_e['background_risk'][i]}\n"
            )


def main():
    # baseline_table_data()
    # sensitivities_data()
    projection_overtime_data()


if __name__ == "__main__":
    api = CanRisk(username="dv21", password="GQv4C5@UmyiYTwc")
    # main()
    gail = GailModel(GailFactors(24, 0, 0, 0, 0, 1, Race.WHITE))
    print(gail.predict(10))
