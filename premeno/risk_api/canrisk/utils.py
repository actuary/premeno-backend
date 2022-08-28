from typing import Any, Optional


def extract_cancer_rates(boadicea: dict) -> dict:
    pedigree_results = boadicea["pedigree_result"][0]  # only inputting one family

    def extract(rates_list: list[dict]) -> list[Any]:
        return list(map(lambda rate: rate["breast cancer risk"]["decimal"], rates_list))

    return {
        "age": list(map(lambda rate: rate["age"], pedigree_results["baseline_cancer_risks"])),
        "baseline": extract(pedigree_results["baseline_cancer_risks"]),
        "individual": extract(pedigree_results["cancer_risks"]),
    }


def interpolate_rate(ages: list[int], rates: list[float], target_age: int) -> float:
    """Interpolates rate based on given age. Raise error if not in range"""
    if len(ages) == 0 or len(ages) != len(rates):
        raise ValueError("Results dictionary error!")

    if target_age < ages[0] or target_age > ages[-1]:
        raise ValueError("Target age not within predicted age range")

    idx = 0
    for i, age in enumerate(ages):
        if target_age >= age:
            idx = i
        else:
            break

    if target_age == ages[idx]:
        return rates[idx]

    return rates[idx] + ((target_age - ages[idx]) / (ages[idx + 1] - ages[idx])) * (
        rates[idx + 1] - rates[idx]
    )


def header_line(name: str, value: Optional[Any]) -> str:
    if value is not None:
        return f"##{name}={str(value)}"
    else:
        return f"##{name}"
