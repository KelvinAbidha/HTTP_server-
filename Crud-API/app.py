from flask import Flask, request, jsonify, g
import time

app = Flask(__name__)

# In-memory database with initial state
items = {
    1: {'id': 1, 'name': 'Laptop', 'price': 1200},
    2: {'id': 2, 'name': 'Mouse', 'price': 25},
    3: {'id': 3, 'name': 'Keyboard', 'price': 45}
}
next_id = 4

# Middleware: Request Timing
@app.before_request
def start_timer():
    g.start = time.time()

@app.after_request
def log_request(response):
    if hasattr(g, 'start'):
        duration = time.time() - g.start
        print(f"Completed {request.method} {request.path} in {duration:.4f}s")
    return response

# Helper: Standardized Error Response
def abort_error(status_code, message):
    response = jsonify({'error': message})
    response.status_code = status_code
    return response

# Root Endpoint: API Index
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "API is running",
        "available_routes": [
            "/items",
            "/items/<id>"
        ]
    })

# Route: Retrieve all items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(list(items.values()))

# Route: Retrieve single item by ID
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = items.get(item_id)
    if not item:
        return abort_error(404, "Item not found")
    return jsonify(item)

# Server Entry Point
if __name__ == '__main__':
    print("Starting Flask Server on port 5000...")
    app.run(port=5000, debug=True)