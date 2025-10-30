import os
import requests
from typing import Dict, Any, List
from dataclasses import dataclass
import json

@dataclass
class MarketAnalysis:
    market_size: float
    competition_level: str
    growth_potential: float
    investment_score: float
    key_trends: List[str]
    risks: List[str]
    opportunities: List[str]

class MarketAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('MARKETPLACE_API_KEY')
        self.base_url = os.getenv('MARKET_DATA_API_URL', 'https://api.marketdata.com')
    
    def analyze_market(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze market conditions for a business"""
        
        industry = business_data.get('industry', 'General')
        location = business_data.get('location', 'US')
        business_type = business_data.get('type', 'B2B')
        
        # Get market data from external APIs
        market_data = self._fetch_market_data(industry, location)
        
        # Analyze competition
        competition_analysis = self._analyze_competition(industry, business_type)
        
        # Calculate investment score
        investment_score = self._calculate_investment_score(
            market_data, competition_analysis, business_data
        )
        
        # Generate market analysis
        analysis = {
            'industry': industry,
            'market_size': market_data.get('market_size', 0),
            'growth_rate': market_data.get('growth_rate', 0),
            'competition_level': competition_analysis['level'],
            'barriers_to_entry': competition_analysis['barriers'],
            'investment_score': investment_score,
            'market_trends': self._get_market_trends(industry),
            'risks': self._identify_risks(industry, business_data),
            'opportunities': self._identify_opportunities(industry, market_data),
            'customer_segments': self._get_customer_segments(industry, business_type),
            'revenue_potential': self._estimate_revenue_potential(market_data, business_type)
        }
        
        return analysis
    
    def _fetch_market_data(self, industry: str, location: str) -> Dict[str, Any]:
        """Fetch market data from external APIs"""
        
        # In a real implementation, this would call actual market data APIs
        # For now, return mock data based on industry
        
        industry_data = {
            'SaaS': {
                'market_size': 195000000000,  # $195B
                'growth_rate': 18.2,
                'cagr': 21.1
            },
            'E-commerce': {
                'market_size': 6500000000000,  # $6.5T
                'growth_rate': 14.7,
                'cagr': 16.8
            },
            'Mobile Apps': {
                'market_size': 133000000000,  # $133B
                'growth_rate': 15.3,
                'cagr': 17.2
            },
            'Fintech': {
                'market_size': 116000000000,  # $116B
                'growth_rate': 23.5,
                'cagr': 25.8
            },
            'AI/ML': {
                'market_size': 190000000000,  # $190B
                'growth_rate': 38.1,
                'cagr': 42.3
            }
        }
        
        default_data = {
            'market_size': 50000000000,  # $50B
            'growth_rate': 10.0,
            'cagr': 12.0
        }
        
        return industry_data.get(industry, default_data)
    
    def _analyze_competition(self, industry: str, business_type: str) -> Dict[str, str]:
        """Analyze competition level in the market"""
        
        competition_levels = {
            'SaaS': {'level': 'High', 'barriers': 'Medium'},
            'E-commerce': {'level': 'Very High', 'barriers': 'Low'},
            'Mobile Apps': {'level': 'Very High', 'barriers': 'Low'},
            'Fintech': {'level': 'High', 'barriers': 'Very High'},
            'AI/ML': {'level': 'Medium', 'barriers': 'Very High'},
            'Marketplace': {'level': 'High', 'barriers': 'High'}
        }
        
        return competition_levels.get(industry, {'level': 'Medium', 'barriers': 'Medium'})
    
    def _calculate_investment_score(self, market_data: Dict, competition: Dict, business_data: Dict) -> float:
        """Calculate investment score based on market conditions"""
        
        # Market size score (0-30 points)
        market_size = market_data.get('market_size', 0)
        if market_size > 100000000000:  # > $100B
            market_score = 30
        elif market_size > 50000000000:  # > $50B
            market_score = 25
        elif market_size > 10000000000:  # > $10B
            market_score = 20
        else:
            market_score = 15
        
        # Growth score (0-25 points)
        growth_rate = market_data.get('growth_rate', 0)
        if growth_rate > 25:
            growth_score = 25
        elif growth_rate > 15:
            growth_score = 20
        elif growth_rate > 10:
            growth_score = 15
        else:
            growth_score = 10
        
        # Competition score (0-20 points) - lower competition is better
        competition_level = competition['level']
        if competition_level == 'Low':
            comp_score = 20
        elif competition_level == 'Medium':
            comp_score = 15
        elif competition_level == 'High':
            comp_score = 10
        else:  # Very High
            comp_score = 5
        
        # Barriers score (0-15 points) - higher barriers are better for protection
        barriers = competition['barriers']
        if barriers == 'Very High':
            barrier_score = 15
        elif barriers == 'High':
            barrier_score = 12
        elif barriers == 'Medium':
            barrier_score = 8
        else:  # Low
            barrier_score = 5
        
        # Business quality score (0-10 points)
        years_operated = business_data.get('years_operated', 0)
        if years_operated > 5:
            quality_score = 10
        elif years_operated > 2:
            quality_score = 7
        elif years_operated > 1:
            quality_score = 5
        else:
            quality_score = 2
        
        total_score = market_score + growth_score + comp_score + barrier_score + quality_score
        return min(100, total_score)
    
    def _get_market_trends(self, industry: str) -> List[str]:
        """Get relevant market trends for the industry"""
        
        trends = {
            'SaaS': [
                'Shift to subscription-based models',
                'AI/ML integration in business tools',
                'Remote work driving SaaS adoption',
                'API-first architecture becoming standard'
            ],
            'E-commerce': [
                'Mobile commerce growth',
                'Social commerce emergence',
                'Sustainability focus in shopping',
                'Personalization and AI recommendations'
            ],
            'Mobile Apps': [
                'Super app model expansion',
                'Cross-platform development trends',
                'Privacy-first app development',
                'Voice and AR integration'
            ],
            'Fintech': [
                'Digital banking acceleration',
                'Cryptocurrency mainstream adoption',
                'Open banking and API ecosystems',
                'Buy now, pay later services growth'
            ],
            'AI/ML': [
                'Generative AI explosion',
                'Edge AI computing growth',
                'AutoML democratization',
                'AI ethics and governance focus'
            ]
        }
        
        return trends.get(industry, ['Digital transformation acceleration', 'Cloud adoption growth'])
    
    def _identify_risks(self, industry: str, business_data: Dict) -> List[str]:
        """Identify potential risks for the business"""
        
        common_risks = [
            'Market saturation risk',
            'Technology disruption',
            'Regulatory changes',
            'Economic downturn impact'
        ]
        
        industry_risks = {
            'SaaS': ['Customer churn risk', 'Competition from big tech', 'Data security concerns'],
            'E-commerce': ['Supply chain disruptions', 'Platform dependency risk', 'Return fraud'],
            'Mobile Apps': ['App store policy changes', 'Privacy regulations', 'Market fragmentation'],
            'Fintech': ['Regulatory compliance', 'Cybersecurity threats', 'Credit risk exposure'],
            'AI/ML': ['Data privacy regulations', 'Bias and fairness issues', 'Model interpretability']
        }
        
        return common_risks + industry_risks.get(industry, [])
    
    def _identify_opportunities(self, industry: str, market_data: Dict) -> List[str]:
        """Identify market opportunities"""
        
        base_opportunities = [
            'Digital transformation acceleration',
            'Remote work normalization',
            'Cloud migration ongoing'
        ]
        
        growth_rate = market_data.get('growth_rate', 0)
        if growth_rate > 20:
            base_opportunities.append('High-growth market segment')
        
        return base_opportunities
    
    def _get_customer_segments(self, industry: str, business_type: str) -> List[str]:
        """Get target customer segments"""
        
        if business_type == 'B2B':
            return ['Small businesses', 'Mid-market companies', 'Enterprise clients']
        elif business_type == 'B2C':
            return ['Millennials', 'Gen Z consumers', 'High-income demographics']
        else:
            return ['Mixed market segments']
    
    def _estimate_revenue_potential(self, market_data: Dict, business_type: str) -> str:
        """Estimate revenue potential"""
        
        market_size = market_data.get('market_size', 0)
        growth_rate = market_data.get('growth_rate', 0)
        
        if market_size > 100000000000 and growth_rate > 15:
            return 'Very High - Large and fast-growing market'
        elif market_size > 50000000000 and growth_rate > 10:
            return 'High - Substantial market opportunity'
        elif market_size > 10000000000:
            return 'Medium - Reasonable market potential'
        else:
            return 'Low - Limited market size'
    
    def batch_analyze(self, businesses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze multiple businesses"""
        analyses = []
        for business in businesses:
            try:
                analysis = self.analyze_market(business)
                analysis['business_id'] = business.get('id')
                analysis['business_name'] = business.get('name')
                analyses.append(analysis)
            except Exception as e:
                print(f"Error analyzing business {business.get('name')}: {e}")
                continue
        
        return analyses

if __name__ == "__main__":
    # Example usage
    agent = MarketAgent()
    
    sample_business = {
        'name': 'SaaS Company',
        'industry': 'SaaS',
        'location': 'US',
        'type': 'B2B',
        'years_operated': 3
    }
    
    analysis = agent.analyze_market(sample_business)
    print("Market Analysis:")
    print(f"Industry: {analysis['industry']}")
    print(f"Market Size: ${analysis['market_size']:,.0f}")
    print(f"Investment Score: {analysis['investment_score']}/100")
    print(f"Competition Level: {analysis['competition_level']}")
    print("Market Trends:")
    for trend in analysis['market_trends']:
        print(f"  - {trend}")