"""IGN Sismología feed."""
from __future__ import annotations

from typing import Final

from georss_client.feed import GeoRssFeed

from .feed_entry import IgnSismologiaFeedEntry

URL: Final = "http://www.ign.es/ign/RssTools/sismologia.xml"


class IgnSismologiaFeed(GeoRssFeed):
    """IGN Sismología feed."""

    def __init__(
        self,
        home_coordinates: tuple[float, float],
        filter_radius: float | None = None,
        filter_minimum_magnitude: float | None = None,
    ):
        """Initialise this service."""
        super().__init__(home_coordinates, URL, filter_radius=filter_radius)
        self._filter_minimum_magnitude: float | None = filter_minimum_magnitude

    def __repr__(self):
        """Return string representation of this feed."""
        return "<{}(home={}, url={}, radius={}, magnitude={})>".format(
            self.__class__.__name__,
            self._home_coordinates,
            self._url,
            self._filter_radius,
            self._filter_minimum_magnitude,
        )

    def _new_entry(
        self, home_coordinates: tuple[float, float], rss_entry, global_data
    ) -> IgnSismologiaFeedEntry:
        """Generate a new entry."""
        return IgnSismologiaFeedEntry(home_coordinates, rss_entry)

    def _filter_entries(self, entries):
        """Filter the provided entries."""
        entries = super()._filter_entries(entries)
        if self._filter_minimum_magnitude:
            # Return only entries that have an actual magnitude value, and
            # the value is equal or above the defined threshold.
            return list(
                filter(
                    lambda entry: entry.magnitude
                    and entry.magnitude >= self._filter_minimum_magnitude,
                    entries,
                )
            )
        return entries
