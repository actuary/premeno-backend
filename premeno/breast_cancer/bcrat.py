import math
from enum import Enum
from typing import Optional

### set up lambda1*, lambda2, beta & F(t] with known constants used in the nci brca risk disk
## lambda1_Star, BrCa composite incidences
# SEER BrCa incidence rates (current] non-hispanic white women, SEER white 1983:87
# SEER BrCa incidence rates for 1 other (native american) women, SEER white 1992:96
# "white_avg": [0.00001220, 0.00007410, 0.00022970, 0.00056490, 0.00116450, 0.00195250, 0.00261540,
#               0.00302790, 0.00367570, 0.00420290, 0.00473080, 0.00494250, 0.00479760, 0.00401060],
# SEER BrCa indicdence rates (under study) for non-hispanic white women, SEER white 1995:2003
# "white_n": [0.0000120469, 0.0000746893, 0.0002437767, 0.0005878291, 0.0012069622, 0.0019762053, 0.0026200977,
#             0.0033401788, 0.0039743676, 0.0044875763, 0.0048945499, 0.0051610641, 0.0048268456, 0.0040407389],

incidence_rates = {
    # SEER BrCa incidence rates (current) non-hispanic white women, SEER white 1983:87
    1: [
        0.00001000,
        0.00007600,
        0.00026600,
        0.00066100,
        0.00126500,
        0.00186600,
        0.00221100,
        0.00272100,
        0.00334800,
        0.00392300,
        0.00417800,
        0.00443900,
        0.00442100,
        0.00410900,
    ],
    # SEER black 1994-98
    2: [
        0.00002696,
        0.00011295,
        0.00031094,
        0.00067639,
        0.00119444,
        0.00187394,
        0.00241504,
        0.00291112,
        0.00310127,
        0.00366560,
        0.00393132,
        0.00408951,
        0.00396793,
        0.00363712,
    ],
    # SEER Ca Hisp 1995-2004
    3: [
        0.0000166,
        0.0000741,
        0.0002740,
        0.0006099,
        0.0012225,
        0.0019027,
        0.0023142,
        0.0028357,
        0.0031144,
        0.0030794,
        0.0033344,
        0.0035082,
        0.0025308,
        0.0020414,
    ],
    # SEER white 1983:87
    4: [
        0.00001000,
        0.00007600,
        0.00026600,
        0.00066100,
        0.00126500,
        0.00186600,
        0.00221100,
        0.00272100,
        0.00334800,
        0.00392300,
        0.00417800,
        0.00443900,
        0.00442100,
        0.00410900,
    ],
    # SEER Ca Hisp 1995-2004
    5: [
        0.0000102,
        0.0000531,
        0.0001578,
        0.0003602,
        0.0007617,
        0.0011599,
        0.0014111,
        0.0017245,
        0.0020619,
        0.0023603,
        0.0025575,
        0.0028227,
        0.0028295,
        0.0025868,
    ],
    # seer18 chinese  1998:02
    6: [
        0.000004059636,
        0.000045944465,
        0.000188279352,
        0.000492930493,
        0.000913603501,
        0.001471537353,
        0.001421275482,
        0.001970946494,
        0.001674745804,
        0.001821581075,
        0.001834477198,
        0.001919911972,
        0.002233371071,
        0.002247315779,
    ],
    # seer18 japanese 1998:02
    7: [
        0.000000000001,
        0.000099483924,
        0.000287041681,
        0.000545285759,
        0.001152211095,
        0.001859245108,
        0.002606291272,
        0.003221751682,
        0.004006961859,
        0.003521715275,
        0.003593038294,
        0.003589303081,
        0.003538507159,
        0.002051572909,
    ],
    # seer18 filipino 1998:02
    8: [
        0.000007500161,
        0.000081073945,
        0.000227492565,
        0.000549786433,
        0.001129400541,
        0.001813873795,
        0.002223665639,
        0.002680309266,
        0.002891219230,
        0.002534421279,
        0.002457159409,
        0.002286616920,
        0.001814802825,
        0.001750879130,
    ],
    # seer18 hawaiian 1998:02
    9: [
        0.000045080582,
        0.000098570724,
        0.000339970860,
        0.000852591429,
        0.001668562761,
        0.002552703284,
        0.003321774046,
        0.005373001776,
        0.005237808549,
        0.005581732512,
        0.005677419355,
        0.006513409962,
        0.003889457523,
        0.002949061662,
    ],
    # seer18 otr pac isl 1998:02
    10: [
        0.000000000001,
        0.000071525212,
        0.000288799028,
        0.000602250698,
        0.000755579402,
        0.000766406354,
        0.001893124938,
        0.002365580107,
        0.002843933070,
        0.002920921732,
        0.002330395655,
        0.002036291235,
        0.001482683983,
        0.001012248203,
    ],
    # seer18 otr asian 1998:02
    11: [
        0.000012355409,
        0.000059526456,
        0.000184320831,
        0.000454677273,
        0.000791265338,
        0.001048462801,
        0.001372467817,
        0.001495473711,
        0.001646746198,
        0.001478363563,
        0.001216010125,
        0.001067663700,
        0.001376104012,
        0.000661576644,
    ],
}

#
# nchs competing mortality for "avg" non-hispanic white women and "avg" other (native american] women, NCHS white 1992:96
# "white_avg": [0.00044120, 0.00052540, 0.00067460, 0.00090920, 0.00125340, 0.00195700, 0.00329840,
#               0.00546220, 0.00910350, 0.01418540, 0.02259350, 0.03611460, 0.06136260, 0.14206630],
# nchs competing mortality (under study] for non-hispanic white women, NCHS white 1995:2003
# "white_n": [0.0004000377, 0.0004280396, 0.0005656742, 0.0008474486, 0.0012752947, 0.0018601059, 0.0028780622,
#            0.0046903348, 0.0078835252, 0.0127434461, 0.0208586233, 0.0335901145, 0.0575791439,
#            0.1377327125],

competing_hazards = {
    # nchs competing mortality (current] for non-hispanic white women, NCHS white 1985:87
    1: [
        0.00049300,
        0.00053100,
        0.00062500,
        0.00082500,
        0.00130700,
        0.00218100,
        0.00365500,
        0.00585200,
        0.00943900,
        0.01502800,
        0.02383900,
        0.03883200,
        0.06682800,
        0.14490800,
    ],
    # NCHS black 1996-00
    2: [
        0.00074354,
        0.00101698,
        0.00145937,
        0.00215933,
        0.00315077,
        0.00448779,
        0.00632281,
        0.00963037,
        0.01471818,
        0.02116304,
        0.03266035,
        0.04564087,
        0.06835185,
        0.13271262,
    ],
    # SEER Ca Hisp 1995-2004
    3: [
        0.0003561,
        0.0004038,
        0.0005281,
        0.0008875,
        0.0013987,
        0.0020769,
        0.0030912,
        0.0046960,
        0.0076050,
        0.0120555,
        0.0193805,
        0.0288386,
        0.0429634,
        0.0740349,
    ],
    # NCHS white 1985:87
    4: [
        0.00049300,
        0.00053100,
        0.00062500,
        0.00082500,
        0.00130700,
        0.00218100,
        0.00365500,
        0.00585200,
        0.00943900,
        0.01502800,
        0.02383900,
        0.03883200,
        0.06682800,
        0.14490800,
    ],
    # SEER Ca Hisp 1995-2004
    5: [
        0.0003129,
        0.0002908,
        0.0003515,
        0.0004943,
        0.0007807,
        0.0012840,
        0.0020325,
        0.0034533,
        0.0058674,
        0.0096888,
        0.0154429,
        0.0254675,
        0.0448037,
        0.1125678,
    ],
    # NCHS mortality chinese  1998:02
    6: [
        0.000210649076,
        0.000192644865,
        0.000244435215,
        0.000317895949,
        0.000473261994,
        0.000800271380,
        0.001217480226,
        0.002099836508,
        0.003436889186,
        0.006097405623,
        0.010664526765,
        0.020148678452,
        0.037990796590,
        0.098333900733,
    ],
    # NCHS mortality japanese 1998:02
    7: [
        0.000173593803,
        0.000295805882,
        0.000228322534,
        0.000363242389,
        0.000590633044,
        0.001086079485,
        0.001859999966,
        0.003216600974,
        0.004719402141,
        0.008535331402,
        0.012433511681,
        0.020230197885,
        0.037725498348,
        0.106149118663,
    ],
    # NCHS mortality filipino 1998:02
    8: [
        0.000229120979,
        0.000262988494,
        0.000314844090,
        0.000394471908,
        0.000647622610,
        0.001170202327,
        0.001809380379,
        0.002614170568,
        0.004483330681,
        0.007393665092,
        0.012233059675,
        0.021127058106,
        0.037936954809,
        0.085138518334,
    ],
    # NCHS mortality hawaiian 1998:02
    9: [
        0.000563507269,
        0.000369640217,
        0.001019912579,
        0.001234013911,
        0.002098344078,
        0.002982934175,
        0.005402445702,
        0.009591474245,
        0.016315472607,
        0.020152229069,
        0.027354838710,
        0.050446998723,
        0.072262026612,
        0.145844504021,
    ],
    # NCHS mortality otr pac isl 1998:02
    10: [
        0.000465500812,
        0.000600466920,
        0.000851057138,
        0.001478265376,
        0.001931486788,
        0.003866623959,
        0.004924932309,
        0.008177071806,
        0.008638202890,
        0.018974658371,
        0.029257567105,
        0.038408980974,
        0.052869579345,
        0.074745721133,
    ],
    # NCHS mortality otr asian 1998:02
    11: [
        0.000212632332,
        0.000242170741,
        0.000301552711,
        0.000369053354,
        0.000543002943,
        0.000893862331,
        0.001515172239,
        0.002574669551,
        0.004324370426,
        0.007419621918,
        0.013251765130,
        0.022291427490,
        0.041746550635,
        0.087485802065,
    ],
}

unattributable_risk = {
    ## F(t) = 1-Attributable Risk
    "white": [0.5788413, 0.5788413],
    "black": [0.72949880, 0.74397137],
    "hispanic": [0.749294788397, 0.778215491668],
    "other_white": [0.5788413, 0.5788413],
    "other_hispanic": [0.428864989813, 0.450352338746],
    "asian": [0.47519806426735, 0.50316401683903],
}


class RecodingError(Exception):
    pass


class Subject:
    _betas = {
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
            0.0,
            0.2318368334,
            0.166685441,
            0.0,
            0.0,
        ],
        "other_hispanic": [
            0.4798624017,
            0.2593922322,
            0.4669246218,
            0.9076679727,
            0.0,
            0.0,
        ],
        "other_white": [
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

    _races = {
        1: "white",
        2: "black",
        3: "hispanic",
        4: "other_white",
        5: "other_hispanic",
        6: "asian",
        7: "asian",
        8: "asian",
        9: "asian",
        10: "asian",
        11: "asian",
    }

    HISPANICS = [3, 5]
    ASIANS = [6, 7, 8, 9, 10, 11]
    UNKNOWN_RESPONSE = 99
    MIN_AGE = 20
    MAX_AGE = 90

    # def __init__(self, json):
    #     self.age_start = self.recode_age_start(json["age_start"])
    #     self.age_end = self.recode_age_end(json["age_end"])
    #     self.no_of_biopsies_cat = self.recode_no_of_biopsies(json["no_of_biopsies"], json["hyperplasia"])
    #     self.hyperplasia_cat = self.recode_hyperplasia(json["hyperplasia"])
    #     self.age_menarche_cat = self.recode_age_menarche(json["age_menarche"])
    #     self.age_at_first_child_cat = self.recode_age_at_first_child(json["age_at_first_child"])
    #     self.no_of_relatives_cat = self.recode_no_of_relatives(json["no_of_relatives"])
    #     self.race_cat = self.recode_race(json["race"])

    @classmethod
    def fromJson(cls, json: dict):
        return Subject(
            float(json["age_start"]),
            float(json["age_end"]),
            int(json["no_of_biopsies"]),
            int(json["hyperplasia"]),
            int(json["age_menarche"]),
            int(json["age_at_first_child"]),
            int(json["no_of_relatives"]),
            int(json["race"]),
        )

    def __init__(
        self,
        age_start: float,
        age_end: float,
        no_of_biopsies: int,
        hyperplasia: int,
        age_menarche: int,
        age_at_first_child: int,
        no_of_relatives: int,
        race: int,
    ):
        self._age_start = age_start
        self._age_end = age_end
        self._no_of_biopsies = no_of_biopsies
        self._hyperplasia = hyperplasia
        self._age_menarche = age_menarche
        self._age_at_first_child = age_at_first_child
        self._no_of_relatives = no_of_relatives
        self._race = race

    @property
    def age_start(self) -> Optional[float]:
        if (
            self._age_start < self.MIN_AGE
            or self._age_start >= self.MAX_AGE
            or self._age_start >= self._age_end
        ):
            return None
        return self._age_start

    @property
    def age_end(self) -> Optional[float]:
        if self._age_end > self.MAX_AGE or self._age_start >= self._age_end:
            return None
        return self._age_end

    @property
    def no_of_biopsies_cat(self) -> Optional[int]:
        no_of_biopsies_cat = None

        if self._invalid_biopsy_choice(self._no_of_biopsies, self._hyperplasia):
            no_of_biopsies_cat = None

        elif no_of_biopsies_cat == None and self._no_of_biopsies in (
            0,
            self.UNKNOWN_RESPONSE,
        ):
            no_of_biopsies_cat = 0

        elif no_of_biopsies_cat == None and self._no_of_biopsies == 1:
            no_of_biopsies_cat = 1

        elif (
            no_of_biopsies_cat == None
            and 2 <= self._no_of_biopsies < self.UNKNOWN_RESPONSE
        ):
            no_of_biopsies_cat = 2

        if self._race in self.HISPANICS:
            if self._no_of_biopsies in (0, self.UNKNOWN_RESPONSE):
                no_of_biopsies_cat = 0

            if (no_of_biopsies_cat or -1) >= 2:
                no_of_biopsies_cat = 1

        return no_of_biopsies_cat

    @property
    def age_at_menarche_cat(self) -> Optional[int]:
        age_menarche_cat = None

        if self._age_menarche < 0:
            age_menarche_cat = None

        elif self._age_menarche < 12:
            age_menarche_cat = 2

        elif self._age_menarche < 14:
            age_menarche_cat = 1

        elif 14 <= self._age_menarche <= self._age_start:
            age_menarche_cat = 0

        elif self._age_menarche == self.UNKNOWN_RESPONSE:
            age_menarche_cat = 0

        if self._age_start < self._age_menarche < self.UNKNOWN_RESPONSE:
            age_menarche_cat = None

        if self._race == 2 and age_menarche_cat == 2:
            age_menarche_cat = 1

        if self._race == 3:
            age_menarche_cat = 0

        return age_menarche_cat

    @property
    def age_at_first_child_cat(self) -> Optional[int]:
        age_at_first_child_cat = None
        UNKNOWN_RESPONSE_1st = 98

        if self._age_at_first_child < 20:
            age_at_first_child_cat = 0

        elif self._age_at_first_child < 25:
            age_at_first_child_cat = 1

        elif self._age_at_first_child < 30:
            age_at_first_child_cat = 2

        elif self._age_at_first_child < UNKNOWN_RESPONSE_1st:
            age_at_first_child_cat = 3

        elif self._age_at_first_child == UNKNOWN_RESPONSE_1st:
            age_at_first_child_cat = 2

        elif self._age_at_first_child == self.UNKNOWN_RESPONSE:
            age_at_first_child_cat = 0

        if self._age_at_first_child < self._age_menarche < self.UNKNOWN_RESPONSE:
            age_at_first_child_cat = None

        if self._age_start < self._age_at_first_child < UNKNOWN_RESPONSE_1st:
            age_at_first_child_cat = None

        if self._race == 2:
            age_at_first_child_cat = 0

        if (
            self._race in self.HISPANICS
            and self._age_at_first_child != UNKNOWN_RESPONSE_1st
            and age_at_first_child_cat == 2
        ):
            age_at_first_child_cat = 1

        if self._race in self.HISPANICS and age_at_first_child_cat == 3:
            age_at_first_child_cat = 2

        return age_at_first_child_cat

    @property
    def no_of_relatives_cat(self) -> Optional[int]:
        no_of_relatives_cat = None

        if self._no_of_relatives == 0:
            no_of_relatives_cat = 0

        elif self._no_of_relatives == 1:
            no_of_relatives_cat = 1

        elif self._no_of_relatives < self.UNKNOWN_RESPONSE:
            no_of_relatives_cat = 2

        elif self._no_of_relatives == self.UNKNOWN_RESPONSE:
            no_of_relatives_cat = 0

        if self._race in self.HISPANICS + self.ASIANS and no_of_relatives_cat == 2:
            no_of_relatives_cat = 1

        return no_of_relatives_cat

    @property
    def race(self) -> Optional[int]:
        if self._race not in range(1, 12):
            return None
        return self._race

    @property
    def relative_risk_factor(self):
        relative_risk_factor = None

        if self.no_of_biopsies_cat is not None and self.no_of_biopsies_cat == 0:
            relative_risk_factor = 1.00

        if (self.no_of_biopsies_cat or 0) > 0:
            if self._hyperplasia == 0:
                relative_risk_factor = 0.93
            elif self._hyperplasia == 1:
                relative_risk_factor = 1.82
            elif self._hyperplasia == self.UNKNOWN_RESPONSE:
                relative_risk_factor = 1.00

        if self._invalid_biopsy_choice(self._no_of_biopsies, self._hyperplasia):
            relative_risk_factor = None

        return relative_risk_factor

    def _invalid_biopsy_choice(self, no_biopsies, hyperplasia) -> bool:
        return (
            (
                0 < no_biopsies < self.UNKNOWN_RESPONSE
                and hyperplasia not in (0, 1, self.UNKNOWN_RESPONSE)
            )
            or no_biopsies in (0, self.UNKNOWN_RESPONSE)
            and hyperplasia != self.UNKNOWN_RESPONSE
        )

    def is_valid(self) -> bool:
        return (
            self.age_start is not None
            and self.age_end is not None
            and self.no_of_biopsies_cat is not None
            and self.age_at_menarche_cat is not None
            and self.age_at_first_child_cat is not None
            and self.no_of_relatives_cat is not None
            and self.race is not None
        )

    def relative_risk(self) -> Optional[float]:
        if not self.is_valid():
            return None

        beta = self._betas[self._races[self.race]]  # type: ignore

        lp1 = (
            self.no_of_biopsies_cat * beta[0]  # type: ignore
            + self.age_at_menarche_cat * beta[1]  # type: ignore
            + self.age_at_first_child_cat * beta[2]  # type: ignore
            + self.no_of_relatives_cat * beta[3]  # type: ignore
            + self.age_at_first_child_cat  # type: ignore
            * self.no_of_relatives_cat  # type: ignore
            * beta[5]  # type: ignore
            + math.log(self.relative_risk_factor)  # type: ignore
        )  # type: ignore

        lp2 = lp1 + self.no_of_biopsies_cat * beta[4]  # type: ignore

        return (math.exp(lp1), math.exp(lp2))  # type: ignore

    def absolute_risk(self) -> Optional[float]:
        if not self.is_valid():
            return None

        rrstar1, rrstar2 = self.relative_risk()

        start_interval = math.floor(self.age_start) - 20 + 1
        end_interval = math.ceil(self.age_end) - 20

        number_intervals = end_interval - start_interval + 1
        abs_risk = 0
        cumulative_lambda = 0
        one_ar1, one_ar2 = unattributable_risk[self._races[self.race]]  # type: ignore
        one_ar_rr1 = one_ar1 * rrstar1
        one_ar_rr2 = one_ar2 * rrstar2

        one_ar_rr = [one_ar_rr1 if i < 30 else one_ar_rr2 for i in range(70)]
        lambda1 = incidence_rates[self.race]
        lambda2 = competing_hazards[self.race]

        for j in range(number_intervals):
            j_interval = start_interval + j - 1
            interval_length = 1
            if number_intervals > 1 and j == 0:
                interval_length = 1 - (self.age_start - math.floor(self.age_start))
            elif number_intervals > 1 and j == number_intervals - 1:
                z1 = 1 if self.age_end > math.floor(self.age_end) else 0
                z2 = 1 if self.age_end == math.floor(self.age_end) else 0
                interval_length = (self.age_end - math.floor(self.age_end)) * z1 + z2
            elif number_intervals == 1:
                interval_length = self.age_end - self.age_start

            lambdaj = (
                lambda1[j_interval // 5] * one_ar_rr[j_interval]
                + lambda2[j_interval // 5]
            )
            PI_j = (
                (one_ar_rr[j_interval] * lambda1[j_interval // 5] / lambdaj)
                * math.exp(-cumulative_lambda)
            ) * (1 - math.exp(-lambdaj * interval_length))
            abs_risk += PI_j
            cumulative_lambda += lambdaj * interval_length

        return abs_risk


relative_risks = {
    "age_at_menopause": {
        0: [0.95, 1.71],  # <55 years
        1: [1.31, 2.04],  # 55-64 years
        2: [1.35, 2.19],  # 65+ years
    },
    "bmi": {
        0: [1.49, 2.32],  # <25 kg/m2
        1: [1.25, 1.92],  # 25-29 kg/m2
        2: [1.14, 1.71],  # 30+ kg/m2
    },
    "family_history": {
        0: [1.31, 2.02],  # No
        1: [1.35, 2.11],  # Yes
    },
    "ethnic_group": {
        0: [1.32, 2.08],  # White
        1: [1.39, 2.13],  # Other
    },
    "education": {
        0: [1.28, 2.05],  # <13 years
        1: [1.35, 2.03],  # 13+ years
    },
    "height": {
        0: [1.32, 2.10],  # <165 cm
        1: [1.34, 2.03],  # 165+ cm
    },
    "age_at_menarche": {
        0: [1.27, 2.03],  # <13 years
        1: [1.35, 2.07],  # 13+ years
    },
    "parity": {
        0: [1.42, 2.23],  # Nulliparous
        1: [1.28, 2.04],  # Parous
    },
    "age_at_first_child": {
        0: [1.31, 2.02],  # <25 years
        1: [1.32, 2.03],  # 25+ years
    },
    "oral_contraceptive": {
        0: [1.28, 2.11],  # Never used
        1: [1.34, 2.01],  # Ever used
    },
    "alcohol": {
        0: [1.3, 2.04],  # <10 g/week
        1: [1.3, 2.11],  # 10+ g/week
    },
    "smoking": {
        0: [1.32, 2.08],  # Never
        1: [1.32, 2.04],  # Ever
    },
}


class MhtType(Enum):
    OESTROGEN_ONLY = 0
    OESTROGEN_PROGESTAGEN = 1


class SubjectMHT:
    def __init__(self, json):
        self.raw_data = json
        self.age_at_menopause_cat = self.recode_age_at_menopause(
            json["age_at_menopause"]
        )
        self.bmi_cat = self.recode_bmi(json["height"], json["weight"])
        self.no_of_relatives_cat = self.recode_no_of_relatives(json["no_of_relatives"])
        self.ethnic_group_cat = self.recode_ethnic_group(json["ethnic_group"])
        self.education_cat = self.recode_education(json["education"])
        self.height_cat = self.recode_height(json["height"])
        self.age_at_menarche = self.recode_age_at_menarche(json["age_at_menarche"])
        self.age_at_first_child_cat = self.recode_age_at_first_child(
            json["age_at_first_child"]
        )
        self.oral_contraceptive_cat = self.recode_oral_contraceptive(
            json["oral_contraceptive"]
        )
        self.alcohol_cat = self.recode_alcohol(json["units_per_week"])
        self.smoking_cat = self.recode_smoking(json["smoker_status"])

    def recode_age_at_menopause(self, age):
        if age < 55:
            return 0
        elif age < 65:
            return 1
        elif age < 90:
            return 2
        else:
            print("ERROR")
            return -1

    def recode_bmi(self, height, weight):
        bmi = weight / (height**2)

        if bmi < 25:
            return 0
        elif bmi < 35:
            return 1
        else:
            return 2

    def recode_ethnic_group(self, ethnic_group: str) -> int:
        return 0 if ethnic_group == "white" else 1

    def recode_no_of_relatives(self, no_of_relatives: int) -> int:
        return 0 if no_of_relatives == 0 else 1

    def recode_education(self, yrs_of_education: int) -> int:
        return 0 if yrs_of_education < 13 else 1

    def recode_height(self, height: int) -> int:
        return 0 if height < 165 else 1

    def recode_age_at_menarche(self, age_at_menarche: int) -> int:
        return 0 if age_at_menarche < 13 else 1

    def recode_age_at_first_child(self, age_at_first_child: int) -> int:
        return 0 if age_at_first_child < 25 else 1

    def recode_oral_contraceptive(self, oral_contraceptive: bool) -> int:
        return 0 if not oral_contraceptive else 1

    def recode_alcohol(self, units_per_week: int) -> int:
        return 0 if units_per_week < 10 else 1

    def recode_smoking(self, smoking: bool) -> int:
        return 0 if not smoking else 1

    def relative_risk(self, type_of_mht: MhtType) -> float:
        if type_of_mht == MhtType.OESTROGEN_ONLY:
            return 1.3
        elif type_of_mht == MhtType.OESTROGEN_PROGESTAGEN:
            return 2


if __name__ == "__main__":
    subject = Subject(27, 90, 99, 99, 13, 22, 99, 8)
    print(subject.relative_risk())
    print(subject.absolute_risk())
