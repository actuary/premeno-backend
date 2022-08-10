from enum import Enum
from dataclasses import dataclass
from typing import List


class Sex(Enum):
    Male = "M"
    Female = "F"


@dataclass
class Diagnoses:
    breast_cancer_1st_age: int = 0
    breast_cancer_2nd_age: int = 0
    ovarian_cancer_age: int = 0
    prostate_cancer_age: int = 0
    pancreatic_cancer_age: int = 0

    def __str__(self) -> str:
        return (f"{self.breast_cancer_1st_age}\t"
                f"{self.breast_cancer_2nd_age}\t"
                f"{self.ovarian_cancer_age}\t"
                f"{self.prostate_cancer_age}\t"
                f"{self.pancreatic_cancer_age}\t")


class ReceptorStatus(Enum):
    Unknown = "0"
    Positive = "P"
    Negative = "N"


@dataclass
class Pathology:
    oestrogen_receptor: int = 0
    progesterone_recepter: int = 0
    her2: int = 0
    cytokeratin14: int = 0
    cytokeratin56: int = 0

    def __str__(self) -> str:
        return (f"{self.oestrogen_receptor}:"
                f"{self.progesterone_recepter}:"
                f"{self.her2}:"
                f"{self.cytokeratin14}:"
                f"{self.cytokeratin56}")


class GeneTestResult(Enum):
    Untested = "0"
    Positive = "P"
    Negative = "N"


class GeneTestType(Enum):
    Untested = "0"
    MutationSearch = "S"
    Direct = "T"

class GeneTest:
    test_type: GeneTestType = GeneTestType.Untested
    result: GeneTestResult = GeneTestResult.Untested

    def __str__(self) -> str:
        return f"{self.test_type.value}:{self.result.value}"


@dataclass
class GeneTests:
    brca1: GeneTest = GeneTest() 
    brca2: GeneTest = GeneTest() 
    palb2: GeneTest = GeneTest() 
    atm: GeneTest = GeneTest() 
    chek2: GeneTest = GeneTest() 
    bard1: GeneTest = GeneTest() 
    rad51d: GeneTest = GeneTest() 
    rad51c: GeneTest = GeneTest() 
    brip1: GeneTest = GeneTest() 

    def __str__(self) -> str:
        return (f"{self.brca1}\t"
                f"{self.brca2}\t"
                f"{self.palb2}\t"
                f"{self.atm}\t"
                f"{self.chek2}\t"
                f"{self.bard1}\t"
                f"{self.rad51d}\t"
                f"{self.rad51c}\t"
                f"{self.brip1}\t")


@dataclass
class PedigreeEntry:
    fam_id: str
    individ_id: str
    is_target: bool

    name: str
    sex: Sex
    age: int
    year_of_birth: int

    father_id: str = "0"
    mother_id: str = "0"

    age_on_death: int = 0

    mz_twin: int = 0 # monoziotic twin - not used in our model
    ashkenazi: int = 0 # also ignore this

    diagnoses: Diagnoses = Diagnoses()
    pathology: Pathology = Pathology()
    gene_tests: GeneTests = GeneTests()

    @property
    def dead(self) -> int:
        return 0 if self.age_on_death == 0 else 1
    
    def husband(self) -> "PedigreeEntry":
        return PedigreeEntry(self.fam_id, 
                             f"husb", 
                             False, 
                             "NA", 
                             Sex.Male, 
                             age=0,
                             year_of_birth=0
                             )
    
    def sister_with_cancer(self, sister_no: int, age_at_diagnosis: int) -> "PedigreeEntry":
        """ Returns a sister entry with cancer at given age. Sets her age
            to age at diagnosis. This understates the risk we are only
            giving her one cancer, and by saying she is at the age of diagnosis 
            we're removing any possible information about her surviving beyond 
            this without a contralateral diagnosis. Of course, this second diagnosis 
            would increase the risk of cancer for the woman in question so this 
            is understating the risk, but we're hoping by not too much.
        """
        return PedigreeEntry(self.fam_id, 
                             f"sis{sister_no}", 
                             False, 
                             "NA", 
                             Sex.Female, 
                             age=age_at_diagnosis,
                             year_of_birth=self.year_of_birth + (self.age - age_at_diagnosis),
                             father_id=self.father_id,
                             mother_id=self.mother_id,
                             diagnoses=Diagnoses(age_at_diagnosis)
                             )

    def child(self, age_at_first_live_birth: int, child_no: int) -> "PedigreeEntry":
        return PedigreeEntry(
                fam_id=self.fam_id, 
                individ_id=f"ch{child_no}",
                is_target=False,
                name="NA",
                sex=Sex.Male,
                age=self.age - age_at_first_live_birth - child_no + 1,
                year_of_birth=self.year_of_birth + age_at_first_live_birth + child_no,
                father_id="husb",
                mother_id=self.individ_id
                )

    def children(self, age_at_first_live_birth: int, no_of_children: int) -> List["PedigreeEntry"]:
        return [self.child(age_at_first_live_birth, child_no) for child_no in range(no_of_children)]

    def __str__(self) -> str:
        return (f"{self.fam_id}\t"
                f"{self.name}\t"
                f"{1 if self.is_target else 0}\t"
                f"{self.individ_id}\t"
                f"{self.father_id}\t"
                f"{self.mother_id}\t"
                f"{self.sex.value}\t"
                f"{self.mz_twin}\t"
                f"{self.dead}\t"
                f"{self.age}\t"
                f"{self.year_of_birth}\t"
                f"{self.diagnoses}"
                f"{self.ashkenazi}\t"
                f"{self.gene_tests}"
                f"{self.pathology}")

    @classmethod
    def header(cls) -> str:
        return ("FamID\tName\tTarget\tIndivID\tFathID\tMothID\tSex\tMZtwin\t"
                "Dead\tAge\tYob\tBC1\tBC2\tOC\tPRO\tPAN\tAshkn\tBRCA1\tBRCA2\t"
                "PALB2\tATM\tCHEK2\tBARD1\tRAD51D\tRAD51C\tBRIP1\tER:PR:HER2:CK14:CK56")
