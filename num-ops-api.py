from flask import Flask, request, jsonify
from flask_cors import CORS
import operator

app = Flask(__name__)
CORS(app)

# Dictionary mapping operation strings to their corresponding functions
operations = {
    'add': operator.add,
    'subtract': operator.sub,
    'multiply': operator.mul,
    'divide': operator.truediv,
    'power': operator.pow
}

@app.route('/api/operate', methods=['POST'])
def operate():
    data = request.json

    if not data or 'operation' not in data or 'numbers' not in data:
        return jsonify({"error": "Invalid input. Please provide 'operation' and 'numbers'."}), 400

    operation = data['operation']
    numbers = data['numbers']

    if operation not in operations:
        return jsonify({"error": f"Invalid operation. Supported operations are: {', '.join(operations.keys())}"}), 400

    if not isinstance(numbers, list) or len(numbers) < 2:
        return jsonify({"error": "Please provide at least two numbers for the operation."}), 400

    try:
        numbers = [float(num) for num in numbers]
    except ValueError:
        return jsonify({"error": "Invalid numbers provided. Please ensure all inputs are numeric."}), 400

    try:
        if operation == 'divide' and 0 in numbers[1:]:
            return jsonify({"error": "Division by zero is not allowed."}), 400

        result = numbers[0]
        for num in numbers[1:]:
            result = operations[operation](result, num)

        return jsonify({
            "operation": operation,
            "numbers": numbers,
            "result": result
        }), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found. Please check the API endpoint."}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed. Please use POST for this endpoint."}), 405

if __name__ == '__main__':
    app.run(debug=True, port=5002)  # Note: Using port 5002 to avoid conflict with num-stats-api