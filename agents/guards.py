# agents/guards.py
class RiskDeadlineException(Exception):
    """Raised when quantitative safety checks cross strict latency limits."""
    pass

class RiskCircuitBreaker:
    """
    Active hardware-simulated fail-safe designed to monitor execution risk parameters
    and prevent catastrophic portfolio drop-offs.
    """
    def __init__(self, hard_deadline_ms: float = 5.0):
        self.hard_deadline_ms = hard_deadline_ms
        self.breaker_status = "CLOSED"  # CLOSED (Safe), OPEN (Emergency Liquidation)

    def evaluate_execution_timing(self, elapsed_ms: float):
        if elapsed_ms > self.hard_deadline_ms:
            self.breaker_status = "OPEN"
            raise RiskDeadlineException(
                f"CRITICAL COMPUTE LATENCY FAULT: Risk engine took {elapsed_ms:.2f}ms (Limit: {self.hard_deadline_ms}ms)."
            )
