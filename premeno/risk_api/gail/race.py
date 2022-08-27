from enum import Enum

from premeno.risk_api.questionnaire import EthnicGroup


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


class RaceCategory(Enum):
    """Category for parameter lookups """

    WHITE = 1
    AFRICAN_AMERICAN = 2
    HISPANIC = 3
    WHITE_OTHER = 4
    HISPANIC_OTHER = 5
    ASIAN = 6


""" Map questionnaire group to a Gail race """
ETHNIC_GROUP_TO_RACE = {
    EthnicGroup.WHITE: Race.WHITE,
    EthnicGroup.OTHER: Race.AFRICAN_AMERICAN
}


""" Some gail parameters are stored by category """
RACES_TO_RACE_CATEGORY = {
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

""" Can be different recodings depending on group (see factors.py) """
HISPANICS = [Race.HISPANIC_AMERICAN_US, Race.HISPANIC_AMERICAN_FOREIGN]


""" Can be different recodings depending on group (see factors.py) """
ASIANS = [
    Race.CHINESE,
    Race.JAPANESE,
    Race.FILIPINO,
    Race.HAWAIIAN,
    Race.PACIFIC_ISLANDER,
    Race.ASIAN_OTHER,
]
