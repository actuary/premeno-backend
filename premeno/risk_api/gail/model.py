import math

from premeno.risk_api.gail.factors import GailFactors
from premeno.risk_api.gail.parameters import (
    BETAS,
    COMPETING_HAZARDS,
    INCIDENCE_RATES,
    UNATTRIBUTABLE_RISK,
)
from premeno.risk_api.gail.race import RACES_TO_RACE_CATEGORY


def age_factor(at_age: float) -> int:
    # Note: In BCRAT code, they for some reason split this out
    # rather than having an age cat
    PIVOT_AGE = 50
    return 1 if at_age > PIVOT_AGE else 0


class GailModel:
    """Produces relative and absolute risks given gail factors"""

    def __init__(self, factors: GailFactors):
        self.factors = factors

    def _calculate_interval_length(
        self, interval: int, interval_endpoints: tuple[int, int], age_end: float
    ) -> float:
        """Gets length of given interval - e.g. [27.5, 28] = 0.5, etc."""
        number_intervals = interval_endpoints[1] - interval_endpoints[0] + 1
        if number_intervals > 1 and interval == interval_endpoints[0]:
            return 1 - (self.factors.age - math.floor(self.factors.age))

        elif number_intervals > 1 and interval == interval_endpoints[1]:
            size = age_end - math.floor(age_end)
            return size if size != 0 else 1

        elif number_intervals == 1:
            return age_end - self.factors.age
        else:
            return 1

    def _get_incidence_rate(self, interval: int) -> float:
        AGE_BAND_WIDTH = 5
        idx = (interval - 1) // AGE_BAND_WIDTH
        return INCIDENCE_RATES[self.factors.race][idx]

    def _get_competing_hazard(self, interval: int) -> float:
        AGE_BAND_WIDTH = 5
        idx = (interval - 1) // AGE_BAND_WIDTH
        return COMPETING_HAZARDS[self.factors.race][idx]

    def _calculate_hazard(self, interval: int, unattrib_risk: float) -> float:
        incidence_rate = self._get_incidence_rate(interval)
        competing_hazard = self._get_competing_hazard(interval)

        return incidence_rate * unattrib_risk + competing_hazard

    def _calculate_abs_risk_in_interval(
        self,
        interval: int,
        interval_length: float,
        unattrib_risk: float,
        hazard: float,
        cumulative_hazard: float,
    ) -> float:
        incidence_rate = self._get_incidence_rate(interval)

        return (
            (unattrib_risk * incidence_rate / hazard)
            * math.exp(-cumulative_hazard)
            * (1 - math.exp(-hazard * interval_length))
        )

    def relative_risk(self, at_age: float) -> float:
        """Calculates the relative risk of the given Gail factors"""
        beta = BETAS[RACES_TO_RACE_CATEGORY[self.factors.race]]

        hazard = (
            self.factors.number_of_biopsies * beta[0]
            + self.factors.age_at_menarche * beta[1]
            + self.factors.age_at_first_child * beta[2]
            + self.factors.number_of_relatives * beta[3]
            + self.factors.number_of_biopsies * age_factor(at_age) * beta[4]
            + (
                self.factors.age_at_first_child
                * self.factors.number_of_relatives
                * beta[5]
            )
            + math.log(self.factors.relative_risk_factor)
        )

        return math.exp(hazard)

    def _unattrib_relative_risk(self, at_age) -> float:
        unattrib_risks = UNATTRIBUTABLE_RISK[RACES_TO_RACE_CATEGORY[self.factors.race]]
        rel_risk = self.relative_risk(at_age)
        return unattrib_risks[age_factor(at_age)] * rel_risk

    def predict(self, years: float) -> float:
        """
        Gets the probability (absolute risk) of breast cancer
        incidence of the
        given years from the starting age
        """
        START_AGE = 20

        age_end = self.factors.age + years
        interval_rng = (
            math.floor(self.factors.age) - START_AGE + 1,
            math.ceil(age_end) - START_AGE,
        )

        total_absolute_risk = 0.0
        total_hazard = 0.0
        for interval in range(interval_rng[0], interval_rng[1] + 1):
            interval_length = self._calculate_interval_length(
                interval, interval_rng, age_end
            )
            current_age = START_AGE + interval
            unattrib_risk = self._unattrib_relative_risk(current_age)

            hazard_in_interval = self._calculate_hazard(interval, unattrib_risk)

            total_absolute_risk += self._calculate_abs_risk_in_interval(
                interval,
                interval_length,
                unattrib_risk,
                hazard_in_interval,
                total_hazard,
            )

            total_hazard += hazard_in_interval * interval_length

        return total_absolute_risk
