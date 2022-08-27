from datetime import date

import premeno.risk_api.canrisk.pedigree as p


class TestPedigreeEntry:
    TEST_PEDIGREE = p.PedigreeEntry("me", True, "me", p.Sex.Female, 56, 1965)

    def test_diagnoses_default_str(self) -> None:
        assert str(p.Diagnoses()) == "0\t0\t0\t0\t0\t"

    def test_diagnoses_populated_str(self) -> None:
        assert str(p.Diagnoses(56, 57, 58, 59, 60)) == "56\t57\t58\t59\t60\t"
        assert str(p.Diagnoses(60, 59, 58, 57, 56)) == "60\t59\t58\t57\t56\t"

    def test_pathology_default_str(self) -> None:
        assert str(p.Pathology()) == "0:0:0:0:0"

    def test_pathology_populated_str(self) -> None:
        assert str(p.Pathology(1, 1, 1, 1, 1)) == "1:1:1:1:1"
        assert str(p.Pathology(0, 0, 0, 1, 1)) == "0:0:0:1:1"

    def test_genetest_default_str(self) -> None:
        assert str(p.GeneTest()) == "0:0"

    def test_genetest_populated_str(self) -> None:
        assert str(p.GeneTest(p.GeneTestType.Direct, p.GeneTestResult.Positive)) == "T:P"

    def test_genetests_default_str(self) -> None:
        assert str(p.GeneTests()) == "0:0\t0:0\t0:0\t0:0\t0:0\t0:0\t0:0\t0:0\t0:0\t"

    def test_genetests_populated_str(self) -> None:
        atm = p.GeneTest(p.GeneTestType.Direct, p.GeneTestResult.Positive)
        assert str(p.GeneTests(atm=atm)) == "0:0\t0:0\t0:0\tT:P\t0:0\t0:0\t0:0\t0:0\t0:0\t"

    def test_pedigree_entry_dead(self) -> None:
        pedigree = p.PedigreeEntry("me", True, "me", p.Sex.Female, 56, 1965, age_on_death=56)
        assert pedigree.dead

        pedigree = p.PedigreeEntry("me", True, "me", p.Sex.Female, 56, 1965, age_on_death=0)
        assert not pedigree.dead

    def test_pedigree_husband(self) -> None:
        pedigree = self.TEST_PEDIGREE
        assert pedigree.husband() == p.PedigreeEntry("husb", False, "NA", p.Sex.Male, 0, 0)

    def test_pedigree_father(self) -> None:
        pedigree = self.TEST_PEDIGREE
        assert pedigree.father() == p.PedigreeEntry("dad", False, "dad", p.Sex.Male, 0, 0)

    def test_pedigree_mother(self) -> None:
        pedigree = self.TEST_PEDIGREE
        assert pedigree.mother(None) == p.PedigreeEntry("mum", False, "mum", p.Sex.Female, 0, 0)
        assert pedigree.mother(56) == p.PedigreeEntry(
            "mum",
            False,
            "mum",
            p.Sex.Female,
            56,
            date.today().year - 56,
            diagnoses=p.Diagnoses(breast_cancer_1st_age=56),
        )

    def test_pedigree_sister_with_cancer(self) -> None:
        pedigree = self.TEST_PEDIGREE
        assert pedigree.sister_with_cancer(0, 56) == p.PedigreeEntry(
            "sis0",
            False,
            "NA",
            p.Sex.Female,
            56,
            1965,
            diagnoses=p.Diagnoses(breast_cancer_1st_age=56),
        )

    def test_pedigree_sisters(self) -> None:
        pedigree = self.TEST_PEDIGREE
        assert pedigree.calculate_sisters([56]) == [
            p.PedigreeEntry(
                "sis0",
                False,
                "NA",
                p.Sex.Female,
                56,
                1965,
                diagnoses=p.Diagnoses(breast_cancer_1st_age=56),
            )
        ]

    def test_pedigree_child(self) -> None:
        pedigree = self.TEST_PEDIGREE
        assert pedigree.child(23, 0) == p.PedigreeEntry(
            "ch0", False, "NA", p.Sex.Male, 34, 1988, father_id="husb", mother_id="me"
        )

    def test_pedigree_children(self) -> None:
        pedigree = self.TEST_PEDIGREE
        assert pedigree.children(23, 0) == []
        assert pedigree.children(23, 1) == [
            p.PedigreeEntry(
                "ch0",
                False,
                "NA",
                p.Sex.Male,
                34,
                1988,
                father_id="husb",
                mother_id="me",
            )
        ]

    def test_header(self) -> None:
        assert p.PedigreeEntry.header() == (
            "FamID\tName\tTarget\tIndivID\tFathID\tMothID\tSex\tMZtwin\t"
            "Dead\tAge\tYob\tBC1\tBC2\tOC\tPRO\tPAN\tAshkn\tBRCA1\tBRCA2\t"
            "PALB2\tATM\tCHEK2\tBARD1\tRAD51D\tRAD51C\tBRIP1\tER:PR:HER2:CK14:CK56"
        )

    def test_pedigree_string(self) -> None:
        pedigree = self.TEST_PEDIGREE
        assert str(pedigree) == (
            "fam\tme\t1\tme\t0\t0\tF\t0\t0\t56\t1965\t0\t0\t0\t0\t0\t0\t"
            "0:0\t0:0\t0:0\t0:0\t0:0\t0:0\t0:0\t0:0\t0:0\t0:0:0:0:0"
        )
