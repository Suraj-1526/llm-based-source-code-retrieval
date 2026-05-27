from flask import Flask, request, jsonify
from flask_cors import CORS
from embedding_model import get_embeddings
from vector_db import get_vector_store, get_retriever
from llm import get_llm
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

retriever = None
vector_store = None

def initialize_services():
    """Initialize retriever and vector store on first request"""
    global retriever, vector_store
    if retriever is None:
        try:
            vector_store = get_vector_store()
            retriever = get_retriever()
        except Exception as e:
            print(f"Error initializing services: {e}")
            raise

@app.before_request
def before_request():
    """Initialize services before each request"""
    try:
        initialize_services()
    except Exception as e:
        return jsonify({'error': 'Service initialization failed', 'details': str(e)}), 500

@app.route('/api/search', methods=['POST'])
def search_code():
    """
    Search for code files based on natural language query
    Request: {'query': 'string'}
    Response: {'success': bool, 'results': [...], 'count': int}
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        if len(query) < 2:
            return jsonify({'error': 'Query must be at least 2 characters'}), 400
        
        # Perform vector search
        results = retriever.invoke(query)
        
        # Format results for frontend
        formatted_results = []
        for i, doc in enumerate(results):
            result = {
                'id': i,
                'filename': doc.metadata.get('filename', 'Unknown'),
                'description': doc.page_content[:300] + ('...' if len(doc.page_content) > 300 else ''),
                'full_description': doc.page_content,
                'relevance_score': 0.95
            }
            formatted_results.append(result)
        
        return jsonify({
            'success': True,
            'results': formatted_results,
            'count': len(formatted_results),
            'query': query
        }), 200
        
    except Exception as e:
        print(f"Search error: {e}")
        return jsonify({
            'success': False,
            'error': 'Search failed',
            'details': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'Backend is running'
    }), 200

@app.route('/api/status', methods=['GET'])
def status():
    """Get detailed backend status"""
    return jsonify({
        'backend': 'online',
        'vector_database': 'initialized' if vector_store else 'not initialized',
        'retriever': 'ready' if retriever else 'not ready'
    }), 200

if __name__ == '__main__':
    print("Starting Code Search Backend...")
    print("Server: http://localhost:5000")
    print("Endpoints: /api/health, /api/search, /api/status")
    
    app.run(debug=True, port=5000, host='0.0.0.0')