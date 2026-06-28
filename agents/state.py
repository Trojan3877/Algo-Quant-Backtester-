# agents/state.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class PortfolioState(BaseModel):
    """
    The immutable ledger data contract governing the Algo-Quant engine.
    Enforces rigid data boundaries on pricing matrices and current equity allocations.
    """
    timestamp_frame: str
    current_cash: float
    asset_allocations: Dict[str, float] = Field(default_factory=dict)
    total_portfolio_value: float
    
    # Mathematical Quant Performance Indicators
    sharpe_ratio: float = 0.0
    max_drawdown_pct: float = 0.0
    risk_score: float = 0.0
    
    # LLM Risk Analyst Inference Output Space
    llm_market_sentiment: Optional[str] = None
    llm_strategy_adjustments: Optional[str] = None
    override_active: bool = False
    
    # Engine Observability Tracking
    calculation_latency_ms: float = 0.0
    execution_trace: List[str] = Field(default_factory=list)

    def append_trace(self, log_msg: str) -> "PortfolioState":
        return self.model_copy(update={"execution_trace": list(self.execution_trace) + [log_msg]})
