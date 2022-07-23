import math
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Union


class Race(Enum):
    """Race of participant"""

    WHITE = 1
    AFRICAN_AMERICAN = 2
    HISPANIC_AMERICAN_US = 3
    WHITE_OTHER = 4
    HISPANIC_AMERICAN_FOREIGN = 5
    CHINESE = 6
    JAPANESE = 7
    FILIPINO = 8
    HAWAIIAN = 9
    PACIFIC_ISLANDER = 10
    ASIAN_OTHER = 11


"""
    These are the background rates of breast cancer for each age_group
    (5 year bands from 20 to 90)
"""
_incidence_rates = {
    # SEER BrCa incidence rates non-hispanic white women, SEER white 1983:87
    Race.WHITE: [
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
    Race.AFRICAN_AMERICAN: [
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
    Race.HISPANIC_AMERICAN_US: [
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
    Race.WHITE_OTHER: [
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
    Race.HISPANIC_AMERICAN_FOREIGN: [
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
    Race.CHINESE: [
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
    Race.JAPANESE: [
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
    Race.FILIPINO: [
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
    Race.HAWAIIAN: [
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
    Race.PACIFIC_ISLANDER: [
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
    Race.ASIAN_OTHER: [
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


"""
    These are the background rates of other risks for each age_group
    (5 year bands from 20 to 90)
"""
_competing_hazards = {
    # nchs competing mortality for non-hispanic white women, NCHS white 1985:87
    Race.WHITE: [
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
    # NCHS african american 1996-00
    Race.AFRICAN_AMERICAN: [
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
    Race.HISPANIC_AMERICAN_US: [
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
    Race.WHITE_OTHER: [
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
    Race.HISPANIC_AMERICAN_FOREIGN: [
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
    Race.CHINESE: [
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
    Race.JAPANESE: [
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
    Race.FILIPINO: [
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
    Race.HAWAIIAN: [
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
    Race.PACIFIC_ISLANDER: [
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
    Race.ASIAN_OTHER: [
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


class RaceCategory(Enum):
    WHITE = 1
    AFRICAN_AMERICAN = 2
    HISPANIC = 3
    WHITE_OTHER = 4
    HISPANIC_OTHER = 5
    ASIAN = 6


_races = {
    Race.WHITE: RaceCategory.WHITE,
    Race.AFRICAN_AMERICAN: RaceCategory.AFRICAN_AMERICAN,
    Race.HISPANIC_AMERICAN_US: RaceCategory.HISPANIC,
    Race.WHITE_OTHER: RaceCategory.WHITE_OTHER,
    Race.HISPANIC_AMERICAN_FOREIGN: RaceCategory.HISPANIC_OTHER,
    Race.CHINESE: RaceCategory.ASIAN,
    Race.JAPANESE: RaceCategory.ASIAN,
    Race.FILIPINO: RaceCategory.ASIAN,
    Race.HAWAIIAN: RaceCategory.ASIAN,
    Race.PACIFIC_ISLANDER: RaceCategory.ASIAN,
    Race.ASIAN_OTHER: RaceCategory.ASIAN,
}


"""
    These are the Cox model hazard rates for each risk factor,
    depends race category of participant
"""
_betas = {
    RaceCategory.WHITE: [
        0.5292641686,
        0.0940103059,
        0.2186262218,
        0.9583027845,
        -0.2880424830,
        -0.1908113865,
    ],
    RaceCategory.AFRICAN_AMERICAN: [
        0.1822121131,
        0.2672530336,
        0.0,
        0.4757242578,
        -0.1119411682,
        0.0,
    ],
    RaceCategory.HISPANIC: [
        0.0970783641,
        0.0,
        0.2318368334,
        0.166685441,
        0.0,
        0.0,
    ],
    RaceCategory.HISPANIC_OTHER: [
        0.4798624017,
        0.2593922322,
        0.4669246218,
        0.9076679727,
        0.0,
        0.0,
    ],
    RaceCategory.WHITE_OTHER: [
        0.5292641686,
        0.0940103059,
        0.2186262218,
        0.9583027845,
        -0.2880424830,
        -0.1908113865,
    ],
    RaceCategory.ASIAN: [
        0.55263612260619,
        0.07499257592975,
        0.27638268294593,
        0.79185633720481,
        0.0,
        0.0,
    ],
}


_unattributable_risk = {
    # F(t) = 1-Attributable Risk
    RaceCategory.WHITE: [0.5788413, 0.5788413],
    RaceCategory.AFRICAN_AMERICAN: [0.72949880, 0.74397137],
    RaceCategory.HISPANIC: [0.749294788397, 0.778215491668],
    RaceCategory.WHITE_OTHER: [0.5788413, 0.5788413],
    RaceCategory.HISPANIC_OTHER: [0.428864989813, 0.450352338746],
    RaceCategory.ASIAN: [0.47519806426735, 0.50316401683903],
}


class RecodingError(Exception):
    """Raised when we fail to recode a risk factor to the cox model levels"""


@dataclass
class GailFactors:
    """Holds the categorised risk factors after encoding for the Cox model"""

    age: float
    no_of_biopsies: int
    age_at_menarche: int
    age_at_first_child: int
    no_of_relatives: int
    relative_risk_factor: float
    race: Race


_HISPANICS = [Race.HISPANIC_AMERICAN_US, Race.HISPANIC_AMERICAN_FOREIGN]
_ASIANS = [
    Race.CHINESE,
    Race.JAPANESE,
    Race.FILIPINO,
    Race.HAWAIIAN,
    Race.PACIFIC_ISLANDER,
    Race.ASIAN_OTHER,
]

_UNKNOWN_RESPONSE = 99  # BCRAT/Gail uses this as a default response
_MIN_AGE = 20
_MAX_AGE = 90


class ValidationError(Exception):
    """Raised when we fail to validate a json api call"""


def validate_json(json: dict) -> bool:
    required_fields = [
        "biopsy",
        "number_of_biopsies",
        "hyperplasia",
        "age_at_menarche",
        "age_at_first_child",
        "no_children",
        "family_history",
        "ethnic_group",
    ]

    return all(map(lambda fld: fld in json, required_fields))


def gail_from_json(json: dict) -> GailFactors:
    """Validates past in dictionary (API data) and returns Gail Factors"""

    json = json.copy()
    if not validate_json(json):
        raise ValidationError("JSON error, fields missing.")

    for key in json:
        if json[key] == "":
            json[key] = _UNKNOWN_RESPONSE

    age = (
        datetime.now(timezone.utc)
        - datetime.strptime(json["date_of_birth"], "%Y-%m-%dT%H:%M:%S.%f%z")
    ) / timedelta(days=365.2425)

    if json["biopsy"] == "n":
        no_of_biopsies = 0
        hyperplasia = _UNKNOWN_RESPONSE
    else:
        no_of_biopsies = int(json["number_of_biopsies"])
        hyperplasia = int(json["hyperplasia"])

    age_menarche = int(json["age_at_menarche"])

    no_children = bool(json["no_children"])
    if no_children:
        age_at_first_child = _UNKNOWN_RESPONSE
    else:
        age_at_first_child = int(json["age_at_first_child"])

    no_of_relatives = int(json["family_history"])

    ethnic_group_to_race = {"white": 1, "african_american": 2}

    if json["ethnic_group"] in ethnic_group_to_race:
        race = ethnic_group_to_race[json["ethnic_group"]]
    else:
        race = _UNKNOWN_RESPONSE

    return recode_data_for_gail(
        age,
        no_of_biopsies,
        hyperplasia,
        age_menarche,
        age_at_first_child,
        no_of_relatives,
        race,
    )


def recode_data_for_gail(
    age: float,
    no_of_biopsies: int,
    hyperplasia: int,
    age_at_menarche: int,
    age_at_first_child: int,
    no_of_relatives: int,
    race: int,
) -> GailFactors:
    """Recodes each risk factor into their levels for the Cox model"""

    recoded_race = recode_race(race)
    return GailFactors(
        recode_age(age),
        recode_no_of_biopsies(no_of_biopsies, hyperplasia, recoded_race),
        recode_age_at_menarche(age_at_menarche, age, recoded_race),
        recode_age_at_first_child(
            age_at_first_child, age, age_at_menarche, recoded_race
        ),
        recode_no_of_relatives(no_of_relatives, recoded_race),
        relative_risk_factor(no_of_biopsies, hyperplasia, recoded_race),
        recoded_race,
    )


def recode_race(race: int) -> Race:
    """Ensures valid race factor"""

    if race not in range(1, 12):
        raise RecodingError("Failed to recode race")
    return Race(race)


def recode_age(age: float) -> float:
    """Validates age of individual for Cox model"""
    if age < _MIN_AGE or age >= _MAX_AGE:
        raise RecodingError("Failed to recode age start")
    return age


def recode_age_end(age: float, age_end: float) -> float:
    """Validates projected age of individual"""
    if age_end > _MAX_AGE or age >= age_end:
        raise RecodingError("Failed to recode age end")

    return age_end


def invalid_biopsy_choice(no_biopsies: int, hyperplasia: int) -> bool:
    """
    Returns false if bad selection of number of
    biopsies/hyperplasia biopsies
    """
    return (
        0 < no_biopsies < _UNKNOWN_RESPONSE
        and hyperplasia not in (0, 1, _UNKNOWN_RESPONSE)
    ) or (no_biopsies in (0, _UNKNOWN_RESPONSE) and hyperplasia != _UNKNOWN_RESPONSE)


def recode_no_of_biopsies(no_of_biopsies: int, hyperplasia: int, race: Race) -> int:
    """Recodes number of biopsies from 0 to 2"""
    if race in _HISPANICS and no_of_biopsies in (0, _UNKNOWN_RESPONSE):
        return 0

    elif invalid_biopsy_choice(no_of_biopsies, hyperplasia):
        raise RecodingError("Failed to recode number of biopsies")

    elif no_of_biopsies in (0, _UNKNOWN_RESPONSE):
        return 0

    elif no_of_biopsies == 1:
        return 1

    elif race in _HISPANICS and 2 <= no_of_biopsies < _UNKNOWN_RESPONSE:
        # hispanic RR model from San Fran Bay Area Breast Cancer Study (SFBCS):
        #         (1) groups N_Biop ge 2 with N_Biop eq 1
        return 1

    elif 2 <= no_of_biopsies < _UNKNOWN_RESPONSE:
        return 2
    else:
        raise RecodingError("Failed to recode number of biopsies")


def recode_age_at_menarche(age_at_menarche: int, age: float, race: Race) -> int:
    """Recodes age_at_menarche from 0 to 2"""
    if race == Race.HISPANIC_AMERICAN_US:
        # hispanic RR model from San Fran Bay Area Breast Cancer Study (SFBCS):
        #         (2) eliminates  AgeMen from model for US Born hispanic women
        return 0

    elif age < age_at_menarche < _UNKNOWN_RESPONSE:
        raise RecodingError("Failed to recode age at menarche")

    elif age_at_menarche < 0:
        raise RecodingError("Failed to recode age at menarche")

    elif age_at_menarche < 12 and race == Race.AFRICAN_AMERICAN:
        # african-american RR model from CARE study:
        #         (2) groups AgeMen=2 with AgeMen=1;
        return 1

    elif age_at_menarche < 12:
        return 2

    elif age_at_menarche < 14:
        return 1

    elif 14 <= age_at_menarche <= age:
        return 0

    elif age_at_menarche == _UNKNOWN_RESPONSE:
        return 0
    else:
        raise RecodingError("Failed to recode age at menarche")


def recode_age_at_first_child(
    age_at_first_child: int, age: float, age_at_menarche: int, race: Race
) -> int:
    """Recodes age at first child from 0 to 3"""

    UNKNOWN_RESPONSE_1st = 98

    if race == Race.AFRICAN_AMERICAN:
        # african-american RR model from CARE study:
        #       (1) eliminates Age1st from model;
        return 0

    elif age_at_first_child < age_at_menarche < _UNKNOWN_RESPONSE:
        raise RecodingError("Failed to recode age at first child")

    elif age < age_at_first_child < UNKNOWN_RESPONSE_1st:
        raise RecodingError("Failed to recode age at first child")

    elif age_at_first_child < 20:
        return 0

    elif age_at_first_child < 25:
        return 1

    elif age_at_first_child < 30 and race in _HISPANICS:
        # hispanic RR model from San Fran Bay Area Breast Cancer Study (SFBCS):
        #         (3) group Age1st=25-29 with Age1st=20-24 and code as 1
        return 1

    elif age_at_first_child < 30:
        return 2

    elif age_at_first_child < UNKNOWN_RESPONSE_1st and race in _HISPANICS:
        # hispanic RR model from San Fran Bay Area Breast Cancer Study (SFBCS):
        #         (3) for   Age1st=30+, 98 (nulliparous)       code as 2
        return 2

    elif age_at_first_child < UNKNOWN_RESPONSE_1st:
        return 3

    elif age_at_first_child == UNKNOWN_RESPONSE_1st:
        return 2

    elif age_at_first_child == _UNKNOWN_RESPONSE:
        return 0

    else:
        raise RecodingError("Failed to recode age at first child")


def recode_no_of_relatives(no_of_relatives: int, race: Race) -> int:
    """Recodes the number of relatives from 0 to 2"""
    if no_of_relatives == 0:
        return 0

    elif no_of_relatives == 1:
        return 1

    elif race in _HISPANICS + _ASIANS and no_of_relatives < _UNKNOWN_RESPONSE:
        # for asian-americans cat 2 is pooled with cat 1
        # hispanic RR model from San Fran Bay Area Breast Cancer Study (SFBCS):
        #         (4) groups N_Rels=2 with N_Rels=1;
        return 1

    elif no_of_relatives < _UNKNOWN_RESPONSE:
        return 2

    elif no_of_relatives == _UNKNOWN_RESPONSE:
        return 0

    else:
        raise RecodingError("Failed to recode number of relatives")


def relative_risk_factor(no_of_biopsies: int, hyperplasia: int, race: Race) -> float:
    """Returns the hyperplasia relative risk multiplicative factor"""

    no_of_biopsies_fac = recode_no_of_biopsies(no_of_biopsies, hyperplasia, race)
    if no_of_biopsies_fac == 0 or hyperplasia == _UNKNOWN_RESPONSE:
        return 1.00
    elif hyperplasia == 0:
        return 0.93
    elif hyperplasia == 1:
        return 1.82

    else:
        raise RecodingError("Failed to recode relative risk factor")


def bucket(value: int, buckets: Mapping[float, Union[int, None]]) -> Union[int, None]:
    """Buckets value into bucket with greatest key less than or
    equal to value. Buckets must be specified in order
    """
    keys = list(buckets.keys())

    if keys[0] > value:
        return None

    # find smallest key that it maps to
    for i in range(len(keys) - 1):
        print(keys[i], value, keys[i + 1], "oi")
        if keys[i] <= value < keys[i + 1]:
            print(keys[i])
            print(buckets)
            return buckets[keys[i]]

    return buckets[keys[len(keys) - 1]]


class GailModel:
    """Produces relative and absolute risks given gail factors"""

    def __init__(self, factors: GailFactors):
        self.factors = factors

    def _calculate_interval_length(
        self, interval: int, interval_endpoints: tuple[int, int], age_end: float
    ) -> float:
        number_intervals = interval_endpoints[1] - interval_endpoints[0] + 1
        if number_intervals > 1 and interval == interval_endpoints[0]:
            return 1 - (self.factors.age - math.floor(self.factors.age))

        elif number_intervals > 1 and interval == interval_endpoints[1]:
            z1 = 1 if age_end > math.floor(age_end) else 0
            z2 = 1 if age_end == math.floor(age_end) else 0
            return (age_end - math.floor(age_end)) * z1 + z2

        elif number_intervals == 1:
            return age_end - self.factors.age
        else:
            return 1

    def _get_incidence_rate(self, interval: int) -> float:
        BAND_WIDTH = 5
        idx = (interval - 1) // BAND_WIDTH
        return _incidence_rates[self.factors.race][idx]

    def _get_competing_hazard(self, interval: int) -> float:
        BAND_WIDTH = 5
        idx = (interval - 1) // BAND_WIDTH
        return _competing_hazards[self.factors.race][idx]

    def _lambda_j(self, interval: int, unattrib_risk: float) -> float:
        incidence_rate = self._get_incidence_rate(interval)
        competing_hazard = self._get_competing_hazard(interval)

        return incidence_rate * unattrib_risk + competing_hazard

    def _pi_j(
        self,
        interval: int,
        interval_length: float,
        unattrib_risk: float,
        lambdaj: float,
        cumulative_lambda: float,
    ) -> float:
        incidence_rate = self._get_incidence_rate(interval)

        return (
            (unattrib_risk * incidence_rate / lambdaj)
            * math.exp(-cumulative_lambda)
            * (1 - math.exp(-lambdaj * interval_length))
        )

    def relative_risk(self) -> tuple[float, float]:
        """Calculates the relative risk of the given Gail factors"""
        beta = _betas[_races[self.factors.race]]

        lp1 = (
            self.factors.no_of_biopsies * beta[0]
            + self.factors.age_at_menarche * beta[1]
            + self.factors.age_at_first_child * beta[2]
            + self.factors.no_of_relatives * beta[3]
            + (self.factors.age_at_first_child * self.factors.no_of_relatives * beta[5])
            + math.log(self.factors.relative_risk_factor)
        )
        lp2 = lp1 + self.factors.no_of_biopsies * beta[4]

        return (math.exp(lp1), math.exp(lp2))

    def predict(self, years: float) -> float:
        """
        Gets the probability (absolute risk) of breast cancer
        incidence of the
        given years from the starting age
        """
        START_AGE = 20
        PROJ_YEARS = 70  # project from 20 to 90
        PROJ_AGE = START_AGE + PROJ_YEARS
        PIVOT_AGE = 50  # Gail's model differentiates between <50 and above

        age_end = recode_age_end(self.factors.age, self.factors.age + years)
        interval_rng = (
            math.floor(self.factors.age) - START_AGE + 1,
            math.ceil(age_end) - START_AGE,
        )

        unattrib_risks = _unattributable_risk[_races[self.factors.race]]

        rel_risks = self.relative_risk()
        one_ar_rr1 = unattrib_risks[0] * rel_risks[0]
        one_ar_rr2 = unattrib_risks[1] * rel_risks[1]

        one_ar_rr = [
            one_ar_rr1 if i < PIVOT_AGE else one_ar_rr2
            for i in range(START_AGE, PROJ_AGE + 1)
        ]

        abs_risk = 0.0
        cum_lambda = 0.0
        for interval in range(interval_rng[0], interval_rng[1] + 1):
            interval_length = self._calculate_interval_length(
                interval, interval_rng, age_end
            )

            unattrib_risk = one_ar_rr[interval - 1]

            lambdaj = self._lambda_j(interval, unattrib_risk)
            pi_j = self._pi_j(
                interval, interval_length, unattrib_risk, lambdaj, cum_lambda
            )

            abs_risk += pi_j
            cum_lambda += lambdaj * interval_length

        return abs_risk
