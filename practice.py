"""Parse and validate incoming race-car telemetry packets."""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from typing import Any


class TelemetryValidationError(ValueError):
    """Raised when a telemetry packet contains invalid data."""


class Gear(Enum):
    """Valid transmission states reported by the vehicle."""

    REVERSE = -1
    NEUTRAL = 0
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    FIFTH = 5
    SIXTH = 6


@dataclass(frozen=True)
class TelemetryPacket:
    """A validated snapshot of vehicle telemetry."""

    car_number: int
    timestamp_seconds: float
    speed_mph: float
    engine_rpm: int
    throttle_percent: float
    brake_percent: float
    gear: Gear

    def __post_init__(self) -> None:
        """Run validation after the dataclass has been created."""

        if self.car_number <= 0:
            raise TelemetryValidationError("Car number must be positive.")

        if self.timestamp_seconds < 0:
            raise TelemetryValidationError("Timestamp cannot be negative.")

        if not 0 <= self.speed_mph <= 250:
            raise TelemetryValidationError(
                f"Speed must be between 0 and 250 mph, received {self.speed_mph}."
            )

        if not 0 <= self.engine_rpm <= 12_000:
            raise TelemetryValidationError(
                f"Engine RPM is outside the expected range: {self.engine_rpm}."
            )

        for field_name, value in (
            ("throttle_percent", self.throttle_percent),
            ("brake_percent", self.brake_percent),
        ):
            if not 0 <= value <= 100:
                raise TelemetryValidationError(
                    f"{field_name} must be between 0 and 100."
                )

    @property
    def is_braking(self) -> bool:
        """Return whether the driver is applying meaningful brake pressure."""

        return self.brake_percent >= 5.0

    @property
    def is_full_throttle(self) -> bool:
        """Treat values above 98 percent as full throttle."""

        return self.throttle_percent >= 98.0

    @classmethod
    def from_json(cls, raw_packet: str) -> "TelemetryPacket":
        """Create a telemetry packet from a JSON string."""

        try:
            data: dict[str, Any] = json.loads(raw_packet)
        except json.JSONDecodeError as exc:
            raise TelemetryValidationError("Packet is not valid JSON.") from exc

        required_fields = {
            "car_number",
            "timestamp_seconds",
            "speed_mph",
            "engine_rpm",
            "throttle_percent",
            "brake_percent",
            "gear",
        }

        missing_fields = required_fields - data.keys()

        if missing_fields:
            missing = ", ".join(sorted(missing_fields))
            raise TelemetryValidationError(f"Missing fields: {missing}")

        try:
            return cls(
                car_number=int(data["car_number"]),
                timestamp_seconds=float(data["timestamp_seconds"]),
                speed_mph=float(data["speed_mph"]),
                engine_rpm=int(data["engine_rpm"]),
                throttle_percent=float(data["throttle_percent"]),
                brake_percent=float(data["brake_percent"]),
                gear=Gear(int(data["gear"])),
            )
        except (TypeError, ValueError) as exc:
            raise TelemetryValidationError(
                "One or more telemetry fields have an invalid type or value."
            ) from exc


def main() -> None:
    """Run a basic parsing example."""

    raw_packet = """
    {
        "car_number": 12,
        "timestamp_seconds": 51.42,
        "speed_mph": 181.6,
        "engine_rpm": 8340,
        "throttle_percent": 100,
        "brake_percent": 0,
        "gear": 5
    }
    """

    try:
        packet = TelemetryPacket.from_json(raw_packet)
    except TelemetryValidationError as exc:
        print(f"Packet rejected: {exc}")
        return

    print(packet)
    print(f"Full throttle: {packet.is_full_throttle}")
    print(f"Braking: {packet.is_braking}")


if __name__ == "__main__":
    main()