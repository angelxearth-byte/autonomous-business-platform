from prefect import flow, task
from typing import List, Dict, Any
import asyncio
from ai_scorer import AIScorer
from market_agent import MarketAgent

@task
def analyze_business_opportunities(market_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Analyze business opportunities from market data"""
    agent = MarketAgent()
    opportunities = []
    
    for business in market_data:
        try:
            # Get market analysis
            analysis = agent.analyze_market(business)
            
            opportunity = {
                'business_id': business.get('id'),
                'business_name': business.get('name'),
                'market_analysis': analysis,
                'investment_potential': analysis.get('investment_score', 0)
            }
            opportunities.append(opportunity)
            
        except Exception as e:
            print(f"Error analyzing business {business.get('name')}: {e}")
            continue
    
    return opportunities

@task
def score_businesses(businesses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Score businesses using AI"""
    scorer = AIScorer()
    scored_businesses = []
    
    for business in businesses:
        try:
            score = scorer.score_business(business)
            
            scored_business = {
                'business_id': business.get('id'),
                'business_name': business.get('name'),
                'overall_score': score.overall_score,
                'revenue_score': score.revenue_score,
                'growth_score': score.growth_score,
                'market_score': score.market_score,
                'risk_score': score.risk_score,
                'reasoning': score.reasoning
            }
            scored_businesses.append(scored_business)
            
        except Exception as e:
            print(f"Error scoring business {business.get('name')}: {e}")
            continue
    
    return scored_businesses

@task
def generate_listings(scored_businesses: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Generate listing content for scored businesses"""
    listings = []
    
    for business in scored_businesses:
        if business['overall_score'] >= 70:  # Only generate for high-scoring businesses
            listing = {
                'business_id': business['business_id'],
                'title': f"{business['business_name']} - {business['overall_score']}/100 Investment Score",
                'description': generate_listing_description(business),
                'investment_summary': generate_investment_summary(business)
            }
            listings.append(listing)
    
    return listings

@task
def deploy_listings(listings: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Deploy listings to marketplace"""
    deployment_results = []
    
    for listing in listings:
        try:
            # Simulate deployment to marketplace
            result = {
                'listing_id': listing['business_id'],
                'status': 'deployed',
                'marketplace_url': f"https://marketplace.com/listing/{listing['business_id']}",
                'deployed_at': '2025-10-30T12:00:00Z'
            }
            deployment_results.append(result)
            
        except Exception as e:
            print(f"Error deploying listing {listing['business_id']}: {e}")
            result = {
                'listing_id': listing['business_id'],
                'status': 'failed',
                'error': str(e)
            }
            deployment_results.append(result)
    
    return deployment_results

def generate_listing_description(business: Dict[str, Any]) -> str:
    """Generate a compelling listing description"""
    description = f"""
    {business['business_name']} presents an exceptional investment opportunity with a {business['overall_score']}/100 investment score.
    
    Key Highlights:
    • Revenue Score: {business['revenue_score']}/100 - Demonstrates strong revenue generation
    • Growth Score: {business['growth_score']}/100 - Shows excellent growth trajectory
    • Market Score: {business['market_score']}/100 - Large addressable market
    • Risk Score: {business['risk_score']}/100 - Manageable risk profile
    
    Investment Thesis:
    """
    
    for reason in business['reasoning']:
        description += f"• {reason}\n"
    
    description += """
    
    This business is positioned for continued growth and represents a compelling investment opportunity for strategic investors seeking exposure to this market segment.
    """
    
    return description.strip()

def generate_investment_summary(business: Dict[str, Any]) -> str:
    """Generate investment summary"""
    return f"""
    Investment Score: {business['overall_score']}/100
    Risk-Adjusted Return: High
    Market Opportunity: {business['market_score']}/100
    Growth Potential: {business['growth_score']}/100
    Revenue Quality: {business['revenue_score']}/100
    
    Recommendation: {'STRONG BUY' if business['overall_score'] >= 85 else 'BUY' if business['overall_score'] >= 70 else 'HOLD'}
    """.strip()

@flow
def full_pipeline(market_data: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Main pipeline for processing business opportunities"""
    
    # Sample data if none provided
    if market_data is None:
        market_data = [
            {
                'id': '1',
                'name': 'Tech Startup A',
                'monthly_revenue': 50000,
                'monthly_profit': 25000,
                'growth_rate': 30,
                'market_size': 100000000,
                'industry': 'SaaS',
                'years_operated': 2
            },
            {
                'id': '2',
                'name': 'E-commerce Business B',
                'monthly_revenue': 25000,
                'monthly_profit': 12000,
                'growth_rate': 20,
                'market_size': 50000000,
                'industry': 'E-commerce',
                'years_operated': 4
            }
        ]
    
    print("Starting business analysis pipeline...")
    
    # Step 1: Analyze market opportunities
    print("Analyzing business opportunities...")
    opportunities = analyze_business_opportunities(market_data)
    
    # Step 2: Score businesses
    print("Scoring businesses...")
    scored_businesses = score_businesses(market_data)
    
    # Step 3: Generate listings
    print("Generating listings...")
    listings = generate_listings(scored_businesses)
    
    # Step 4: Deploy listings
    print("Deploying listings...")
    deployment_results = deploy_listings(listings)
    
    # Compile results
    results = {
        'total_businesses_processed': len(market_data),
        'high_quality_opportunities': len([b for b in scored_businesses if b['overall_score'] >= 70]),
        'listings_generated': len(listings),
        'successful_deployments': len([r for r in deployment_results if r['status'] == 'deployed']),
        'scored_businesses': scored_businesses,
        'deployment_results': deployment_results
    }
    
    print(f"Pipeline completed. Processed {results['total_businesses_processed']} businesses.")
    print(f"Generated {results['listings_generated']} high-quality listings.")
    print(f"Successfully deployed {results['successful_deployments']} listings.")
    
    return results

if __name__ == "__main__":
    # Run the pipeline
    result = full_pipeline()
    print("Pipeline result:", result)