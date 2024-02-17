from typing import Any
from .const import Method
from .energyspecific import EnergySpecific


class Energy:
    """Class describing the Tesla Fleet API partner endpoints"""

    def __init__(self, parent):
        self._request = parent._request

    def specific(self, energy_site_id: int) -> EnergySpecific:
        """Create a specific energy site."""
        return EnergySpecific(self, energy_site_id)

    async def backup(
        self, energy_site_id: int, backup_reserve_percent: int
    ) -> dict[str, Any]:
        """Adjust the site's backup reserve."""
        return await self._request(
            Method.POST,
            f"api/1/energy_sites/{energy_site_id}/backup",
            json={"backup_reserve_percent": backup_reserve_percent},
        )

    async def backup_history(
        self,
        energy_site_id: int,
        kind: str,
        start_date: str,
        end_date: str,
        period: str,
        time_zone: str,
    ) -> dict[str, Any]:
        """Returns the backup (off-grid) event history of the site in duration of seconds."""
        return await self._request(
            Method.GET,
            f"api/1/energy_sites/{energy_site_id}/calendar_history",
            json={
                "kind": kind,
                "start_date": start_date,
                "end_date": end_date,
                "period": period,
                "time_zone": time_zone,
            },
        )

    async def charge_history(
        self,
        energy_site_id: int,
        kind: str,
        start_date: str,
        end_date: str,
        time_zone: str,
    ) -> dict[str, Any]:
        """Returns the charging history of a wall connector."""
        return await self._request(
            Method.GET,
            f"api/1/energy_sites/{energy_site_id}/telemetry_history",
            query={
                "kind": kind,
                "start_date": start_date,
                "end_date": end_date,
                "time_zone": time_zone,
            },
        )

    async def energy_history(
        self,
        energy_site_id: int,
        kind: str,
        start_date: str,
        end_date: str,
        period: str,
        time_zone: str,
    ) -> dict[str, Any]:
        """Returns the energy measurements of the site, aggregated to the requested period."""
        return await self._request(
            Method.GET,
            f"api/1/energy_sites/{energy_site_id}/calendar_history",
            query={
                "kind": kind,
                "start_date": start_date,
                "end_date": end_date,
                "period": period,
                "time_zone": time_zone,
            },
        )

    async def grid_import_export(
        self,
        energy_site_id: int,
        disallow_charge_from_grid_with_solar_installed: bool | None = None,
        customer_preferred_export_rule: str | None = None,
    ) -> dict[str, Any]:
        """Allow/disallow charging from the grid and exporting energy to the grid."""
        data = {}
        if disallow_charge_from_grid_with_solar_installed is not None:
            data[
                "disallow_charge_from_grid_with_solar_installed"
            ] = disallow_charge_from_grid_with_solar_installed
        if customer_preferred_export_rule is not None:
            data["customer_preferred_export_rule"] = customer_preferred_export_rule
        if not data:
            raise ValueError(
                "At least one of disallow_charge_from_grid_with_solar_installed or customer_preferred_export_rule must be set."
            )
        return await self._request(
            Method.POST,
            f"api/1/energy_sites/{energy_site_id}/grid_import_export",
            json=data,
        )

    async def live_status(self, energy_site_id: int) -> dict[str, Any]:
        """Returns the live status of the site (power, state of energy, grid status, storm mode)."""
        return await self._request(
            Method.GET,
            f"api/1/energy_sites/{energy_site_id}/live_status",
        )

    async def off_grid_vehicle_charging_reserve(
        self, energy_site_id: int, off_grid_vehicle_charging_reserve_percent: int
    ) -> dict[str, Any]:
        """Adjust the site's off-grid vehicle charging backup reserve."""
        return await self._request(
            Method.POST,
            f"api/1/energy_sites/{energy_site_id}/off_grid_vehicle_charging_reserve",
            json={
                "off_grid_vehicle_charging_reserve_percent": off_grid_vehicle_charging_reserve_percent
            },
        )

    async def operation(
        self, energy_site_id: int, default_real_mode: str
    ) -> dict[str, Any]:
        """Set the site's mode."""
        return await self._request(
            Method.POST,
            f"api/1/energy_sites/{energy_site_id}/operation",
            json={"default_real_mode": default_real_mode},
        )

    async def site_info(self, energy_site_id: int) -> dict[str, Any]:
        """Returns information about the site. Things like assets (has solar, etc), settings (backup reserve, etc), and features (storm_mode_capable, etc)."""
        return await self._request(
            Method.GET,
            f"api/1/energy_sites/{energy_site_id}/site_info",
        )

    async def storm_mode(self, energy_site_id: int, enabled: bool) -> dict[str, Any]:
        """Update storm watch participation."""
        return await self._request(
            Method.POST,
            f"api/1/energy_sites/{energy_site_id}/storm_mode",
            json={"enabled": enabled},
        )
