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


def header_line(name: str, value: Optional[Any]) -> str:
    if value is not None:
        return f"##{name}={str(value)}"
    else:
        return f"##{name}"
