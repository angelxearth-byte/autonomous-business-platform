const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Import modules
const scorer = require('./scorer');
const marketAgent = require('./marketAgent');
const codegen = require('./codegen');
const deploy = require('./deploy');

// Routes
app.get('/', (req, res) => {
    res.json({
        message: 'Autonomous Business Selling Machine - Node.js Orchestrator',
        version: '1.0.0',
        status: 'running'
    });
});

app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        uptime: process.uptime()
    });
});

// Market research endpoint
app.get('/api/research', async (req, res) => {
    try {
        const query = req.query.query || 'business automation';
        const results = await marketAgent.researchMarket(query);
        
        res.json({
            success: true,
            query: query,
            results: results,
            count: results.length
        });
    } catch (error) {
        console.error('Research error:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Scoring endpoint
app.post('/api/score', async (req, res) => {
    try {
        const business = req.body;
        const score = await scorer.scoreBusiness(business);
        
        res.json({
            success: true,
            business: business.name || business.id,
            score: score
        });
    } catch (error) {
        console.error('Scoring error:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Batch scoring endpoint
app.post('/api/batch-score', async (req, res) => {
    try {
        const businesses = req.body.businesses || [];
        const results = await scorer.batchScore(businesses);
        
        res.json({
            success: true,
            count: businesses.length,
            results: results
        });
    } catch (error) {
        console.error('Batch scoring error:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Code generation endpoint
app.post('/api/generate', async (req, res) => {
    try {
        const { title, description, type = 'webapp' } = req.body;
        const result = await codegen.generateBusiness({ title, description, type });
        
        res.json({
            success: true,
            title: title,
            repository: result.repository,
            demo_url: result.demo_url
        });
    } catch (error) {
        console.error('Code generation error:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Deployment endpoint
app.post('/api/deploy', async (req, res) => {
    try {
        const { repository_url } = req.body;
        const result = await deploy.deployRepository(repository_url);
        
        res.json({
            success: true,
            repository_url: repository_url,
            deployment: result
        });
    } catch (error) {
        console.error('Deployment error:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Full pipeline endpoint
app.post('/api/pipeline', async (req, res) => {
    try {
        const { query, min_score = 70 } = req.body;
        
        // Step 1: Research market
        console.log('Step 1: Researching market...');
        const candidates = await marketAgent.researchMarket(query);
        
        // Step 2: Score businesses
        console.log('Step 2: Scoring businesses...');
        const scored = await scorer.batchScore(candidates);
        
        // Step 3: Filter high-quality opportunities
        const highQuality = scored.filter(b => b.score >= min_score);
        
        // Step 4: Generate and deploy for top candidates
        const deployments = [];
        for (const business of highQuality.slice(0, 3)) { // Limit to top 3
            try {
                // Generate code
                const generation = await codegen.generateBusiness({
                    title: business.title || `${business.name} Solution`,
                    description: business.summary,
                    type: 'saas'
                });
                
                // Deploy
                const deployment = await deploy.deployRepository(generation.repository);
                
                deployments.push({
                    business: business,
                    generation: generation,
                    deployment: deployment
                });
            } catch (error) {
                console.error(`Failed to process ${business.name}:`, error);
            }
        }
        
        res.json({
            success: true,
            query: query,
            total_candidates: candidates.length,
            high_quality_count: highQuality.length,
            processed_count: deployments.length,
            deployments: deployments
        });
        
    } catch (error) {
        console.error('Pipeline error:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Analytics endpoint
app.get('/api/analytics', (req, res) => {
    // Mock analytics data
    res.json({
        success: true,
        analytics: {
            total_requests: Math.floor(Math.random() * 1000),
            successful_deployments: Math.floor(Math.random() * 50),
            average_score: Math.random() * 100,
            top_industries: ['SaaS', 'E-commerce', 'Mobile Apps', 'Fintech'],
            daily_active_users: Math.floor(Math.random() * 100)
        }
    });
});

// Error handling middleware
app.use((error, req, res, next) => {
    console.error('Unhandled error:', error);
    res.status(500).json({
        success: false,
        error: 'Internal server error',
        message: error.message
    });
});

// 404 handler
app.use('*', (req, res) => {
    res.status(404).json({
        success: false,
        error: 'Endpoint not found',
        available_endpoints: [
            'GET /',
            'GET /health',
            'GET /api/research',
            'POST /api/score',
            'POST /api/batch-score',
            'POST /api/generate',
            'POST /api/deploy',
            'POST /api/pipeline',
            'GET /api/analytics'
        ]
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`🚀 Autonomous Business Selling Machine running on port ${PORT}`);
    console.log(`📊 Health check: http://localhost:${PORT}/health`);
    console.log(`🔍 API docs: http://localhost:${PORT}/`);
});

module.exports = app;