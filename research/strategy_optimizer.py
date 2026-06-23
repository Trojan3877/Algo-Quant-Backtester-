import os
from openai import OpenAI

class StrategyOptimizer:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"

    def optimize_strategy(self, strategy_metadata: dict, backtest_results: dict) -> dict:
        """
        Evaluates quantitative backtest performance matrices and returns a 
        structured optimization profile with parameter adjustments.
        """
        system_prompt = (
            "You are an L6 Principal Quantitative Researcher and Financial Engineer. "
            "Analyze the backtest performance metrics of the given technical strategy. "
            "Identify statistical weaknesses and return a structured JSON object detailing "
            "exact quantitative hyperparameter adjustments to maximize the Sharpe ratio."
        )
        
        user_content = f"STRATEGY DESIGN:\n{strategy_metadata}\n\nBACKTEST RESULTS:\n{backtest_results}"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                temperature=0.1, # Extremely low temperature for rigorous mathematical reasoning
                response_format={ "type": "json_object" }
            )
            return response.choices[0].message.content
        except Exception as e:
            return {"error": f"Quantitative Optimization Failure: {str(e)}"}
