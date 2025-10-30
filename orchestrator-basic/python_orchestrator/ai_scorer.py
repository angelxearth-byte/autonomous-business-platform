import os
import requests
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class BusinessScore:
    overall_score: float
    revenue_score: float
    growth_score: float
    market_score: float
    risk_score: float
    reasoning: List[str]

class AIScorer:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('AI_MODEL_API_KEY')
        self.base_url = "https://api.openai.com/v1"
        
    def score_business(self, business_data: Dict[str, Any]) -> BusinessScore:
        """Score a business based on various metrics"""
        
        # Extract key metrics
        monthly_revenue = business_data.get('monthly_revenue', 0)
        monthly_profit = business_data.get('monthly_profit', 0)
        growth_rate = business_data.get('growth_rate', 0)
        market_size = business_data.get('market_size', 0)
        industry = business_data.get('industry', 'Unknown')
        years_operated = business_data.get('years_operated', 0)
        
        # Calculate base scores
        revenue_score = self._score_revenue(monthly_revenue, monthly_profit)
        growth_score = self._score_growth(growth_rate)
        market_score = self._score_market(market_size, industry)
        risk_score = self._score_risk(years_operated, business_data)
        
        # Calculate overall score (weighted average)
        overall_score = (
            revenue_score * 0.3 +
            growth_score * 0.25 +
            market_score * 0.25 +
            risk_score * 0.2
        )
        
        # Generate reasoning
        reasoning = self._generate_reasoning(
            business_data, revenue_score, growth_score, 
            market_score, risk_score
        )
        
        return BusinessScore(
            overall_score=overall_score,
            revenue_score=revenue_score,
            growth_score=growth_score,
            market_score=market_score,
            risk_score=risk_score,
            reasoning=reasoning
        )
    
    def _score_revenue(self, revenue: float, profit: float) -> float:
        """Score based on revenue and profitability"""
        if revenue < 1000:
            return 20
        elif revenue < 5000:
            return 40
        elif revenue < 15000:
            return 60
        elif revenue < 50000:
            return 80
        else:
            return 95
    
    def _score_growth(self, growth_rate: float) -> float:
        """Score based on growth rate"""
        if growth_rate < 0:
            return 10
        elif growth_rate < 5:
            return 30
        elif growth_rate < 15:
            return 60
        elif growth_rate < 30:
            return 80
        else:
            return 95
    
    def _score_market(self, market_size: float, industry: str) -> float:
        """Score based on market size and industry"""
        industry_multipliers = {
            'SaaS': 1.2,
            'E-commerce': 1.1,
            'Marketplace': 1.15,
            'Mobile App': 1.0,
            'Web App': 1.0,
            'Service': 0.9
        }
        
        multiplier = industry_multipliers.get(industry, 1.0)
        
        if market_size < 100000:
            return 30 * multiplier
        elif market_size < 1000000:
            return 50 * multiplier
        elif market_size < 10000000:
            return 70 * multiplier
        else:
            return 90 * multiplier
    
    def _score_risk(self, years_operated: int, business_data: Dict) -> float:
        """Score based on business risk factors"""
        # Base score from years operated
        if years_operated < 1:
            base_score = 30
        elif years_operated < 3:
            base_score = 50
        elif years_operated < 5:
            base_score = 70
        else:
            base_score = 85
        
        # Adjust for risk factors
        risk_factors = business_data.get('risk_factors', [])
        for factor in risk_factors:
            if factor.lower() in ['单一客户依赖', '高度竞争', '监管风险']:
                base_score -= 10
        
        return max(0, min(100, base_score))
    
    def _generate_reasoning(self, business_data: Dict, revenue_score: float, 
                          growth_score: float, market_score: float, risk_score: float) -> List[str]:
        """Generate human-readable reasoning for the scores"""
        reasoning = []
        
        if revenue_score >= 80:
            reasoning.append("Strong revenue generation with healthy profitability")
        elif revenue_score >= 60:
            reasoning.append("Moderate revenue with decent profit margins")
        else:
            reasoning.append("Revenue needs improvement for better investment appeal")
        
        if growth_score >= 80:
            reasoning.append("Excellent growth trajectory indicating market opportunity")
        elif growth_score >= 60:
            reasoning.append("Steady growth with potential for acceleration")
        else:
            reasoning.append("Growth is limited, may need strategic improvements")
        
        if market_score >= 80:
            reasoning.append("Large addressable market with favorable industry dynamics")
        elif market_score >= 60:
            reasoning.append("Decent market size with reasonable competition")
        else:
            reasoning.append("Market opportunity may be limited")
        
        if risk_score >= 80:
            reasoning.append("Low risk profile with proven track record")
        elif risk_score >= 60:
            reasoning.append("Moderate risk with some established operations")
        else:
            reasoning.append("Higher risk factors require careful evaluation")
        
        return reasoning
    
    def batch_score(self, businesses: List[Dict[str, Any]]) -> List[BusinessScore]:
        """Score multiple businesses in batch"""
        scores = []
        for business in businesses:
            try:
                score = self.score_business(business)
                scores.append(score)
            except Exception as e:
                print(f"Error scoring business: {e}")
                # Return neutral score for failed businesses
                scores.append(BusinessScore(50, 50, 50, 50, 50, ["Scoring failed"]))
        
        return scores

if __name__ == "__main__":
    # Example usage
    scorer = AIScorer()
    
    sample_business = {
        'name': 'Example SaaS Company',
        'monthly_revenue': 25000,
        'monthly_profit': 15000,
        'growth_rate': 25,
        'market_size': 50000000,
        'industry': 'SaaS',
        'years_operated': 3,
        'risk_factors': []
    }
    
    score = scorer.score_business(sample_business)
    print(f"Overall Score: {score.overall_score}")
    print(f"Revenue Score: {score.revenue_score}")
    print(f"Growth Score: {score.growth_score}")
    print(f"Market Score: {score.market_score}")
    print(f"Risk Score: {score.risk_score}")
    print("Reasoning:")
    for reason in score.reasoning:
        print(f"  - {reason}")