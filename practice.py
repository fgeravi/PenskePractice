"""Calculate rolling statistics from a stream of telemetry samples."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from statistics import fmean, pstdev


@dataclass(frozen=True)
class SpeedSample:
    """A single timestamped vehicle-speed measurement."""

    timestamp_seconds: float
    speed_mph: float


@dataclass(frozen=True)
class RollingSpeedSummary:
    """Statistics calculated from the current rolling window."""

    sample_count: int
    average_speed_mph: float
    minimum_speed_mph: float
    maximum_speed_mph: float
    standard_deviation: float


class RollingTelemetryAnalyzer:
    """Maintain a fixed-size window of recent telemetry samples."""

    def __init__(self, window_size: int = 20) -> None:
        if window_size < 2:
            raise ValueError("Window size must be at least 2.")

        self._samples: deque[SpeedSample] = deque(maxlen=window_size)

    def add_sample(self, sample: SpeedSample) -> None:
        """Validate and add a sample to the rolling window."""

        if sample.timestamp_seconds < 0:
            raise ValueError("Timestamp cannot be negative.")

        if not 0 <= sample.speed_mph <= 250:
            raise ValueError("Speed must be between 0 and 250 mph.")

        if self._samples:
            previous = self._samples[-1]

            if sample.timestamp_seconds <= previous.timestamp_seconds:
                raise ValueError(
                    "Samples must be added in increasing timestamp order."
                )

        self._samples.append(sample)

    def summarize(self) -> RollingSpeedSummary:
        """Calculate statistics for the current window."""

        if not self._samples:
            raise RuntimeError("Cannot summarize an empty telemetry window.")

        speeds = [sample.speed_mph for sample in self._samples]

        return RollingSpeedSummary(
            sample_count=len(speeds),
            average_speed_mph=fmean(speeds),
            minimum_speed_mph=min(speeds),
            maximum_speed_mph=max(speeds),
            standard_deviation=pstdev(speeds),
        )

    def detect_sudden_speed_drop(
        self,
        minimum_drop_mph: float = 20.0,
    ) -> bool:
        """Detect a large speed decrease between the latest two samples."""

        if len(self._samples) < 2:
            return False

        previous = self._samples[-2]
        current = self._samples[-1]
        speed_drop = previous.speed_mph - current.speed_mph

        return speed_drop >= minimum_drop_mph

    def calculate_acceleration_mph_per_second(self) -> float:
        """Calculate acceleration between the latest two samples."""

        if len(self._samples) < 2:
            raise RuntimeError("At least two samples are required.")

        previous = self._samples[-2]
        current = self._samples[-1]

        speed_change = current.speed_mph - previous.speed_mph
        time_change = current.timestamp_seconds - previous.timestamp_seconds

        return speed_change / time_change


def main() -> None:
    analyzer = RollingTelemetryAnalyzer(window_size=5)

    samples = [
        SpeedSample(0.0, 151.2),
        SpeedSample(0.5, 158.6),
        SpeedSample(1.0, 165.3),
        SpeedSample(1.5, 169.8),
        SpeedSample(2.0, 137.1),
    ]

    for sample in samples:
        analyzer.add_sample(sample)

        if analyzer.detect_sudden_speed_drop():
            print(
                f"Warning: sudden speed drop detected at "
                f"{sample.timestamp_seconds:.1f} seconds."
            )

    summary = analyzer.summarize()
    acceleration = analyzer.calculate_acceleration_mph_per_second()

    print(f"Samples analyzed: {summary.sample_count}")
    print(f"Average speed: {summary.average_speed_mph:.2f} mph")
    print(f"Speed variation: {summary.standard_deviation:.2f} mph")
    print(f"Latest acceleration: {acceleration:.2f} mph/s")


if __name__ == "__main__":
    main()