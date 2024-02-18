# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations
from collections import abc
import numpy as np
from gaarf.base_query import BaseQuery
from gaarf.report import GaarfReport
from datetime import datetime, timedelta

from googleads_housekeeper.services.enums import PlacementTypeEnum, ExclusionLevelEnum


class Placements(BaseQuery):
    """Class for getting detail_placement meta information and performance."""

    _today = datetime.today()
    _start_date = _today - timedelta(days=7)
    _end_date = _today - timedelta(days=1)
    _placement_types = set([p.name for p in PlacementTypeEnum])
    _non_excludable_placements = ("youtube.com", "mail.google.com",
                                  "adsenseformobileapps.com")
    _non_supported_campaign_types = ("PERFORMANCE_MAX", )

    def __init__(
            self,
            placement_types: tuple[str, ...] | None = None,
            placement_level_granularity: str = "group_placement_view",
            start_date: str | None = _start_date.strftime("%Y-%m-%d"),
            end_date: str | None = _end_date.strftime("%Y-%m-%d"),
            clicks: int = 0,
            cost: int = 0,
            view_rate: float = 1.0,  #TODO: Unused. Check calling uses before removing
            impressions: int = 0,
            ctr: float = 1.0):
        """Constructor for the class.

        Args:
            placement_types: List of placement types that need to be fetched
                for exclusion.
            start_date: start_date of the period.
            end_date: start_date of the period.
            clicks: number of clicks for the period.
            impressions: number of impressions for the period.
            cost: cost for the period.
            view_rate: video view rate for the period.
            impressions: impressions for the period.
            ctr: average CTR for the period.
        """

        if placement_types:
            if isinstance(placement_types, str):
                placement_types = tuple(placement_types.split(","))
            if (wrong_types :=
                    set(placement_types).difference(self._placement_types)):
                raise ValueError("Wrong placement(s): ",
                                 ', '.join(wrong_types))
            self.placement_types = '","'.join(placement_types)
        else:
            self.placement_types = '","'.join(self._placement_types)

        if placement_level_granularity not in ("detail_placement_view",
                                               "group_placement_view"):
            raise ValueError(
                "Only 'detail_placement_view' or 'group_placement_view' can be specified!"
            )
        else:
            self.placement_level_granularity = placement_level_granularity

        self.validate_dates(start_date, end_date)
        self.start_date = start_date
        self.end_date = end_date
        self.non_excludable_placements = '","'.join(
            self._non_excludable_placements)
        self.non_supported_campaign_types = '","'.join(
            self._non_supported_campaign_types)

        self.parent_url = ("group_placement_target_url"
                         if self.placement_level_granularity
                         == "detail_placement_view" else
                         "target_url")
        self.query_text = f"""
        SELECT
            customer.descriptive_name AS account_name,
            customer.id AS customer_id,
            campaign.id AS campaign_id,
            campaign.name AS campaign_name,
            campaign.advertising_channel_type AS campaign_type,
            ad_group.id AS ad_group_id,
            ad_group.name AS ad_group_name,
            {self.placement_level_granularity}.{self.parent_url} AS base_url,
            {self.placement_level_granularity}.target_url AS url,
            {self.placement_level_granularity}.placement AS placement,
            {self.placement_level_granularity}.placement_type AS placement_type,
            {self.placement_level_granularity}.resource_name AS resource_name,
            {self.placement_level_granularity}.display_name AS name,
            {self.placement_level_granularity}.resource_name~0 AS criterion_id,
            metrics.clicks AS clicks,
            metrics.impressions AS impressions,
            metrics.cost_micros / 1e6 AS cost,
            metrics.conversions AS conversions,
            metrics.video_views AS video_views,
            metrics.interactions AS interactions,
            metrics.all_conversions AS all_conversions,
            metrics.view_through_conversions AS view_through_conversions,
            metrics.conversions_value AS conversions_value
        FROM {self.placement_level_granularity}
        WHERE segments.date >= "{self.start_date}"
            AND segments.date <= "{self.end_date}"
            AND {self.placement_level_granularity}.placement_type IN ("{self.placement_types}")
            AND {self.placement_level_granularity}.target_url NOT IN ("{self.non_excludable_placements}")
            AND campaign.advertising_channel_type NOT IN ("{self.non_supported_campaign_types}")
            AND metrics.clicks >= {clicks}
            AND metrics.impressions > {impressions}
            AND metrics.ctr < {ctr}
            AND metrics.cost_micros >= {int(cost*1e6)}
        """

    def validate_dates(self, start_date: str, end_date: str) -> None:
        if not self.is_valid_date(start_date):
            raise ValueError(f"Invalid start_date: {start_date}")

        if not self.is_valid_date(end_date):
            raise ValueError(f"Invalid end_date: {end_date}")

        if datetime.strptime(start_date, "%Y-%m-%d") > datetime.strptime(
                end_date, "%Y-%m-%d"):
            raise ValueError(
                f"start_date cannot be greater than end_date: {start_date} > {end_date}"
            )

    def is_valid_date(self, date_string: str) -> bool:
        date = datetime.strptime(date_string, "%Y-%m-%d")
        return True


class PlacementsConversionSplit(Placements):
    _today = datetime.today()
    _start_date = _today - timedelta(days=7)
    _end_date = _today - timedelta(days=1)
    _placement_types = set([p.name for p in PlacementTypeEnum])
    _non_excludable_placements = ("youtube.com", "mail.google.com",
                                  "adsenseformobileapps.com")

    def __init__(
        self,
        placement_types: tuple[str, ...] | None = None,
        placement_level_granularity: str = "group_placement_view",
        start_date: str = _start_date.strftime("%Y-%m-%d"),
        end_date: str = _end_date.strftime("%Y-%m-%d")
    ) -> None:
        super().__init__(placement_types, placement_level_granularity,
                         start_date, end_date)
        self.query_text = f"""
        SELECT
            campaign.advertising_channel_type AS campaign_type,
            ad_group.id AS ad_group_id,
            segments.conversion_action_name AS conversion_name,
            {self.placement_level_granularity}.placement AS placement,
            metrics.conversions AS conversions,
            metrics.all_conversions AS all_conversions
        FROM {self.placement_level_granularity}
        WHERE segments.date >= "{self.start_date}"
            AND segments.date <= "{self.end_date}"
            AND {self.placement_level_granularity}.placement_type IN ("{self.placement_types}")
            AND {self.placement_level_granularity}.target_url NOT IN ("{self.non_excludable_placements}")
            AND campaign.advertising_channel_type NOT IN ("{self.non_supported_campaign_types}")
        """


def aggregate_placements(
        placements: GaarfReport,
        exclusion_level: str | ExclusionLevelEnum,
        perform_relative_aggregations: bool = True) -> GaarfReport:
    if not isinstance(exclusion_level, ExclusionLevelEnum):
        exclusion_level = getattr(ExclusionLevelEnum, exclusion_level)
    base_groupby = [
        "placement", "placement_type", "name", "criterion_id", "url"
    ]
    aggregation_dict = dict.fromkeys([
        "clicks",
        "impressions",
        "cost",
        "conversions",
        "video_views",
        "interactions",
        "all_conversions",
        "view_through_conversions",
    ], "sum")
    relative_aggregations_dict = {
        "ctr": ["clicks", "impressions"],
        "avg_cpc": ["cost", "clicks"],
        "avg_cpm": ["cost", "impressions"],
        "avg_cpv": ["cost", "video_views"],
        "video_view_rate": ["video_views", "impressions"],
        "interaction_rate": ["interactions", "clicks"],
        "conversions_from_interactions_rate": ["conversions", "interactions"],
        "cost_per_conversion": ["cost", "conversions"],
        "cost_per_all_conversion": ["cost", "all_conversions"],
        "all_conversion_rate": ["all_conversions", "interactions"],
    }
    if "conversion_name" in placements.column_names:
        base_groupby = base_groupby + ["conversion_name"]
        aggregation_dict.update(
            dict.fromkeys(["conversions_", "all_conversions_"], "sum"))
        relative_aggregations_dict.update({
            "cost_per_conversion_": ["cost", "conversions_"],
            "cost_per_all_conversion_": ["cost", "all_conversions_"]
        })

    if exclusion_level == ExclusionLevelEnum.ACCOUNT:
        aggregation_groupby = ["account_name", "customer_id"]
    elif exclusion_level == ExclusionLevelEnum.CAMPAIGN:
        aggregation_groupby = [
            "account_name", "customer_id", "campaign_id", "campaign_name",
            "campaign_type"
        ]
    elif exclusion_level == ExclusionLevelEnum.AD_GROUP:
        aggregation_groupby = [
            "account_name", "customer_id", "campaign_id", "campaign_name",
            "campaign_type", "ad_group_id", "ad_group_name"
        ]
    groupby = [
        base for base in base_groupby + aggregation_groupby
        if base in placements.column_names
    ]
    aggregations = {
        key: value
        for key, value in aggregation_dict.items()
        if key in placements.column_names
    }
    aggregated_placements = placements.to_pandas().groupby(
        groupby, as_index=False).agg(aggregations)
    if perform_relative_aggregations:
        for key, [numerator,
                  denominator] in relative_aggregations_dict.items():
            if set([numerator,
                    denominator]).issubset(set(aggregated_placements.columns)):
                aggregated_placements[key] = aggregated_placements[
                    numerator] / aggregated_placements[denominator]
                if key == "avg_cpm":
                    aggregated_placements[
                        key] = aggregated_placements[key] * 1000
                if key == "ctr":
                    aggregated_placements[key] = round(
                        aggregated_placements[key], 4)
                else:
                    aggregated_placements[key] = round(
                        aggregated_placements[key], 2)
    aggregated_placements.replace([np.inf, -np.inf], 0, inplace=True)
    return GaarfReport.from_pandas(aggregated_placements)


def join_conversion_split(placements: GaarfReport,
                          placements_by_conversion_name: GaarfReport,
                          conversion_name: str) -> GaarfReport:
    placements_by_conversion_name = placements_by_conversion_name.to_pandas()
    final_report_values = []
    for row in placements:
        conversion_row = placements_by_conversion_name.loc[
            (placements_by_conversion_name.ad_group_id == row.ad_group_id)
            & (placements_by_conversion_name.placement == row.placement)]
        data = list(row.data)
        if not (conversions := sum(conversion_row["conversions"].values)):
            conversions = 0.0
        if not (all_conversions := sum(
                conversion_row["all_conversions"].values)):
            all_conversions = 0.0
        data.extend([conversion_name, conversions, all_conversions])
        final_report_values.append(data)
    columns = list(placements.column_names)
    columns.extend(["conversion_name", "conversions_", "all_conversions_"])
    return GaarfReport(results=final_report_values, column_names=columns)
