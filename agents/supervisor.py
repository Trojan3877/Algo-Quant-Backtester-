# agents/supervisor.py
import time
from .state import PortfolioState
from .guards import RiskCircuitBreaker, RiskDeadlineException

class QuantSupervisorEngine:
    """
    The central Quant Orchestration Core. Manages mathematical asset allocations,
    coordinates data ingestion workers, and runs LLM strategy evaluations.
    """
    def __init__(self, use_llm_analyst: bool = True):
        self.breaker = RiskCircuitBreaker(hard_deadline_ms=5.0)
        self.use_llm_analyst = use_llm_analyst

    def process_backtest_tick(self, timestamp: str, cash: float, allocations: dict, value: float, drawdown: float) -> PortfolioState:
        state = PortfolioState(timestamp_frame=timestamp, current_cash=cash, asset_allocations=allocations, total_portfolio_value=value, max_drawdown_pct=drawdown)
        state = state.append_trace("Ingested raw historical pricing tick vector.")
        
        start_time = time.time()
        try:
            # 1. Evaluate Portfolio Exposure Boundaries (Worker 1)
            if state.max_drawdown_pct > 0.15:  # 15% Maximum Loss Limit Breach
                state = state.model_copy(update={"risk_score": 9.5}).append_trace("Worker 1: Critical drawdown breach identified.")
            
            # 2. Invoke Generative LLM Analyst Layer (Agent 2)
            if self.use_llm_analyst and state.risk_score > 7.0:
                state = self._invoke_llm_risk_analyst(state)

            # Check timing compliance constraints
            elapsed_ms = (time.time() - start_time) * 1000
            self.breaker.evaluate_execution_timing(elapsed_ms)
            
            return state.model_copy(update={"calculation_latency_ms": elapsed_ms})

        except RiskDeadlineException as rde:
            # Emergency Circuit Breaker Liquidation Path
            elapsed_ms = (time.time() - start_time) * 1000
            return state.model_copy(update={
                "override_active": True,
                "asset_allocations": {},  # Liquidate all open active asset vectors instantly
                "llm_strategy_adjustments": "EMERGENCY LIQUIDATION TO CASH ORDER EXECUTED.",
                "calculation_latency_ms": elapsed_ms
            }).append_trace(f"CIRCUIT BREAKER OPENED: {str(rde)}")

    def _invoke_llm_risk_analyst(self, state: PortfolioState) -> PortfolioState:
        """
        Simulates structured Claude 3.5 Sonnet agent prompt analysis.
        In production, replace with actual: client.beta.prompt_analyzer.messages.create()
        """
        mock_analysis = "High-volatility structural regime shift detected in asset tickers. Reduce leverage immediately."
        return state.model_copy(update={
            "llm_market_sentiment": "BEARISH_VOLATILE",
            "llm_strategy_adjustments": mock_analysis
        }).append_trace("LLM Analyst Agent: Structural safety corrections computed and returned.")
