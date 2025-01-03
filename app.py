from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from dotenv import load_dotenv
from src.experts import SportsExpert, FoodExpert, AIExpert, SudoStarExpert
from src.core.expert_selector import ExpertSelector
from config.config import EXPERT_CONFIG, APP_CONFIG

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Global variables
openai_api_key = None
expert_system = None

def init_app():
    """Initialize the application and its dependencies"""
    global openai_api_key, expert_system
    
    try:
        # Load environment variables
        load_dotenv()
        
        # Get OpenAI API key
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            logger.warning("OPENAI_API_KEY environment variable is not set")
            return False
            
        # Initialize expert system only if needed
        if expert_system is None:
            expert_system = {
                'sports': SportsExpert(EXPERT_CONFIG['sports']),
                'food': FoodExpert(EXPERT_CONFIG['food']),
                'ai': AIExpert(EXPERT_CONFIG['ai']),
                'sudostar': SudoStarExpert(EXPERT_CONFIG['sudostar']),
                'selector': ExpertSelector()
            }
            
            logger.info("Expert system initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error initializing application: {str(e)}")
        return False

@app.route('/')
def home():
    is_initialized = init_app()
    return jsonify({
        'status': 'online',
        'initialized': is_initialized,
        'version': '1.0.0',
        'config': {
            'openai_api': 'configured' if openai_api_key else 'missing',
            'expert_system': 'running' if expert_system else 'error'
        }
    })

@app.route('/health')
def health():
    is_initialized = init_app()
    
    response = {
        'status': 'healthy' if is_initialized else 'unhealthy',
        'services': {
            'api': 'running',
            'openai_api': 'configured' if openai_api_key else 'missing',
            'expert_system': 'running' if expert_system else 'error'
        }
    }
    
    if not is_initialized:
        response['error'] = 'System not properly initialized'
    
    return jsonify(response), 200 if is_initialized else 503

@app.route('/ask', methods=['POST'])
async def ask():
    if not init_app():
        return jsonify({
            'status': 'error',
            'error': 'System not properly initialized',
            'code': 'INIT_ERROR'
        }), 503

    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({
                'status': 'error',
                'error': 'Question is required',
                'code': 'MISSING_QUESTION'
            }), 400

        question = data['question']
        logger.info(f"Received question: {question}")
        
        # Select expert and get response
        expert_type, direct_response = await expert_system['selector'].select_expert(question)
        logger.info(f"Selected expert: {expert_type}")
        
        response = None
        if expert_type and expert_type in expert_system:
            response = await expert_system[expert_type].get_response(question)
        else:
            response = direct_response

        if not response:
            return jsonify({
                'status': 'error',
                'error': 'Could not generate response',
                'code': 'NO_RESPONSE'
            }), 500

        logger.info(f"Generated response for {expert_type} expert")
        return jsonify({
            'status': 'success',
            'data': {
                'answer': response,
                'expert_type': expert_type or 'general'
            }
        })

    except Exception as e:
        logger.error(f"Error in /ask endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'code': 'INTERNAL_ERROR'
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port) 