"""
Simple Ticket Tracker API
Flask-based REST API for managing tickets stored in a JSON file.
"""

from flask import Flask, jsonify, request, send_from_directory
import json
import os
import uuid
from datetime import datetime

app = Flask(__name__, static_folder='.')

DATA_FILE = 'tickets_data.json'


def load_tickets():
    """Load tickets from JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_tickets(tickets):
    """Save tickets to JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(tickets, f, indent=2)


# Serve static HTML files
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')


@app.route('/index.html')
def serve_index_html():
    return send_from_directory('.', 'index.html')


@app.route('/board.html')
def serve_board():
    return send_from_directory('.', 'board.html')


# API Routes
@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    """Get all tickets."""
    tickets = load_tickets()
    return jsonify(tickets)


@app.route('/api/tickets/<ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    """Get a specific ticket by ID."""
    tickets = load_tickets()
    ticket = next((t for t in tickets if t['id'] == ticket_id), None)
    if ticket:
        return jsonify(ticket)
    return jsonify({'error': 'Ticket not found'}), 404


@app.route('/api/tickets', methods=['POST'])
def create_ticket():
    """Create a new ticket."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['title', 'description', 'due_date']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    tickets = load_tickets()
    
    new_ticket = {
        'id': str(uuid.uuid4()),
        'title': data['title'],
        'description': data['description'],
        'due_date': data['due_date'],
        'status': data.get('status', 'todo'),
        'created_at': datetime.now().isoformat()
    }
    
    tickets.append(new_ticket)
    save_tickets(tickets)
    
    return jsonify(new_ticket), 201


@app.route('/api/tickets/<ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    """Update an existing ticket."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    tickets = load_tickets()
    ticket_index = next((i for i, t in enumerate(tickets) if t['id'] == ticket_id), None)
    
    if ticket_index is None:
        return jsonify({'error': 'Ticket not found'}), 404
    
    # Update allowed fields
    allowed_fields = ['title', 'description', 'due_date', 'status']
    for field in allowed_fields:
        if field in data:
            tickets[ticket_index][field] = data[field]
    
    tickets[ticket_index]['updated_at'] = datetime.now().isoformat()
    save_tickets(tickets)
    
    return jsonify(tickets[ticket_index])


@app.route('/api/tickets/<ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    """Delete a ticket."""
    tickets = load_tickets()
    ticket_index = next((i for i, t in enumerate(tickets) if t['id'] == ticket_id), None)
    
    if ticket_index is None:
        return jsonify({'error': 'Ticket not found'}), 404
    
    deleted_ticket = tickets.pop(ticket_index)
    save_tickets(tickets)
    
    return jsonify({'message': 'Ticket deleted', 'ticket': deleted_ticket})


if __name__ == '__main__':
    # Initialize empty tickets file if it doesn't exist
    if not os.path.exists(DATA_FILE):
        save_tickets([])
    
    app.run(host='0.0.0.0', port=80, debug=False)
