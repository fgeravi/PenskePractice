"""Process telemetry events using a producer-consumer pipeline."""

from __future__ import annotations

import logging
import random
import threading
import time
from dataclasses import dataclass
from queue import Queue
from typing import Final


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(threadName)s | %(levelname)s | %(message)s",
)

LOGGER = logging.getLogger(__name__)
STOP_SIGNAL: Final = object()


@dataclass(frozen=True)
class TelemetryEvent:
    """A telemetry event produced by a vehicle data source."""

    car_number: int
    sequence_number: int
    speed_mph: float
    engine_rpm: int


class TelemetryProducer(threading.Thread):
    """Generate telemetry events and place them in a shared queue."""

    def __init__(
        self,
        output_queue: Queue[TelemetryEvent | object],
        event_count: int,
        consumer_count: int,
    ) -> None:
        super().__init__(name="telemetry-producer")
        self._output_queue = output_queue
        self._event_count = event_count
        self._consumer_count = consumer_count

    def run(self) -> None:
        try:
            for sequence_number in range(1, self._event_count + 1):
                event = TelemetryEvent(
                    car_number=12,
                    sequence_number=sequence_number,
                    speed_mph=round(random.uniform(145, 190), 2),
                    engine_rpm=random.randint(7_000, 9_500),
                )

                # Queue.put blocks when the queue reaches its maximum
                # size, which prevents the producer from overwhelming
                # slower consumers.
                self._output_queue.put(event)
                LOGGER.info("Produced event %s", sequence_number)

                time.sleep(0.05)
        finally:
            # Each consumer needs its own stop signal because a queue
            # item can only be removed once.
            for _ in range(self._consumer_count):
                self._output_queue.put(STOP_SIGNAL)

            LOGGER.info("Producer finished")


class TelemetryConsumer(threading.Thread):
    """Read and process telemetry events from a shared queue."""

    def __init__(
        self,
        input_queue: Queue[TelemetryEvent | object],
        consumer_number: int,
    ) -> None:
        super().__init__(name=f"telemetry-consumer-{consumer_number}")
        self._input_queue = input_queue
        self.processed_count = 0

    def run(self) -> None:
        while True:
            item = self._input_queue.get()

            try:
                if item is STOP_SIGNAL:
                    LOGGER.info("Consumer received shutdown signal")
                    return

                if not isinstance(item, TelemetryEvent):
                    LOGGER.warning("Unexpected queue item: %r", item)
                    continue

                self._process_event(item)
                self.processed_count += 1
            except Exception:
                # One malformed event should not terminate the entire
                # telemetry processing thread.
                LOGGER.exception("Failed to process telemetry event")
            finally:
                self._input_queue.task_done()

    @staticmethod
    def _process_event(event: TelemetryEvent) -> None:
        """Apply basic alert logic to an incoming event."""

        if event.engine_rpm >= 9_200:
            LOGGER.warning(
                "High RPM for car %s: %s RPM",
                event.car_number,
                event.engine_rpm,
            )
        else:
            LOGGER.info(
                "Processed event %s at %.2f mph",
                event.sequence_number,
                event.speed_mph,
            )

        # Simulate a small amount of processing time.
        time.sleep(0.1)


def main() -> None:
    consumer_count = 3

    telemetry_queue: Queue[TelemetryEvent | object] = Queue(
        maxsize=10
    )

    consumers = [
        TelemetryConsumer(telemetry_queue, number)
        for number in range(1, consumer_count + 1)
    ]

    producer = TelemetryProducer(
        output_queue=telemetry_queue,
        event_count=20,
        consumer_count=consumer_count,
    )

    for consumer in consumers:
        consumer.start()

    producer.start()

    producer.join()
    telemetry_queue.join()

    for consumer in consumers:
        consumer.join()

    total_processed = sum(
        consumer.processed_count for consumer in consumers
    )

    LOGGER.info("Pipeline complete: %s events processed", total_processed)


if __name__ == "__main__":
    main()