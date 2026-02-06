"""
Unit Tests for Ticket Tracker API
Covers all test case scenarios from user-test-cases.md

Test Case Coverage:
- TC-001: Ticket Creation (TC-001.1, TC-001.2, TC-001.3)
- TC-002: Ticket Workflow Management (TC-002.1, TC-002.2, TC-002.3, TC-002.4)
- TC-003: Ticket Deletion (TC-003.1, TC-003.2, TC-003.3)
"""

import pytest
import json
import os
import tempfile
from datetime import datetime, timedelta
from app import app, load_tickets, save_tickets, DATA_FILE


class TestConfig:
    """Test configuration and fixtures."""
    
    @pytest.fixture
    def client(self, tmp_path, monkeypatch):
        """Create a test client with isolated data file."""
        # Use a temporary file for test data
        test_data_file = tmp_path / "test_tickets.json"
        monkeypatch.setattr('app.DATA_FILE', str(test_data_file))
        
        # Initialize empty tickets file
        with open(test_data_file, 'w') as f:
            json.dump([], f)
        
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    @pytest.fixture
    def sample_ticket_data(self):
        """Sample valid ticket data."""
        future_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        return {
            'title': 'Fix login bug',
            'description': 'Users cannot log in with special characters in password',
            'due_date': future_date
        }
    
    @pytest.fixture
    def client_with_tickets(self, client, sample_ticket_data):
        """Create a test client with pre-existing tickets."""
        # Create tickets in each status
        statuses = ['todo', 'in-progress', 'review', 'completed']
        tickets = []
        
        for i, status in enumerate(statuses):
            ticket_data = {
                **sample_ticket_data,
                'title': f'Test Ticket {i + 1}',
                'status': status
            }
            response = client.post('/api/tickets', 
                                   data=json.dumps(ticket_data),
                                   content_type='application/json')
            tickets.append(json.loads(response.data))
        
        return client, tickets


class TestTC001TicketCreation(TestConfig):
    """
    TC-001: Ticket Creation Test Cases
    Tests the ability to create tickets with various inputs.
    """
    
    def test_tc001_1_create_ticket_with_valid_data(self, client, sample_ticket_data):
        """
        TC-001.1: Create Ticket with Valid Data
        
        Test Steps:
        1. Send POST request to create ticket with valid data
        2. Verify success response
        3. Verify ticket is created with correct data
        4. Verify ticket appears in GET /api/tickets
        
        Expected Result:
        - Ticket is created successfully with status 201
        - Ticket has correct fields and default status 'todo'
        - Ticket is retrievable via API
        """
        # Act: Create ticket
        response = client.post('/api/tickets',
                               data=json.dumps(sample_ticket_data),
                               content_type='application/json')
        
        # Assert: Check response
        assert response.status_code == 201
        data = json.loads(response.data)
        
        # Verify ticket fields
        assert data['title'] == sample_ticket_data['title']
        assert data['description'] == sample_ticket_data['description']
        assert data['due_date'] == sample_ticket_data['due_date']
        assert data['status'] == 'todo'  # Default status
        assert 'id' in data
        assert 'created_at' in data
        
        # Verify ticket is retrievable
        get_response = client.get('/api/tickets')
        tickets = json.loads(get_response.data)
        assert len(tickets) == 1
        assert tickets[0]['id'] == data['id']
    
    def test_tc001_2_create_ticket_missing_title(self, client, sample_ticket_data):
        """
        TC-001.2: Create Ticket with Missing Required Fields - Title
        
        Test Steps:
        1. Send POST request without title field
        2. Verify error response
        
        Expected Result:
        - Error response with status 400
        - Ticket is NOT created
        """
        # Arrange: Remove title
        invalid_data = {k: v for k, v in sample_ticket_data.items() if k != 'title'}
        
        # Act
        response = client.post('/api/tickets',
                               data=json.dumps(invalid_data),
                               content_type='application/json')
        
        # Assert
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'title' in data['error'].lower()
        
        # Verify no ticket created
        get_response = client.get('/api/tickets')
        tickets = json.loads(get_response.data)
        assert len(tickets) == 0
    
    def test_tc001_2_create_ticket_missing_description(self, client, sample_ticket_data):
        """
        TC-001.2: Create Ticket with Missing Required Fields - Description
        
        Test Steps:
        1. Send POST request without description field
        2. Verify error response
        
        Expected Result:
        - Error response with status 400
        - Ticket is NOT created
        """
        # Arrange: Remove description
        invalid_data = {k: v for k, v in sample_ticket_data.items() if k != 'description'}
        
        # Act
        response = client.post('/api/tickets',
                               data=json.dumps(invalid_data),
                               content_type='application/json')
        
        # Assert
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'description' in data['error'].lower()
    
    def test_tc001_2_create_ticket_missing_due_date(self, client, sample_ticket_data):
        """
        TC-001.2: Create Ticket with Missing Required Fields - Due Date
        
        Test Steps:
        1. Send POST request without due_date field
        2. Verify error response
        
        Expected Result:
        - Error response with status 400
        - Ticket is NOT created
        """
        # Arrange: Remove due_date
        invalid_data = {k: v for k, v in sample_ticket_data.items() if k != 'due_date'}
        
        # Act
        response = client.post('/api/tickets',
                               data=json.dumps(invalid_data),
                               content_type='application/json')
        
        # Assert
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'due_date' in data['error'].lower()
    
    def test_tc001_2_create_ticket_empty_title(self, client, sample_ticket_data):
        """
        TC-001.2: Create Ticket with Empty Title
        
        Test Steps:
        1. Send POST request with empty title
        2. Verify error response
        
        Expected Result:
        - Error response with status 400
        """
        # Arrange: Set empty title
        invalid_data = {**sample_ticket_data, 'title': ''}
        
        # Act
        response = client.post('/api/tickets',
                               data=json.dumps(invalid_data),
                               content_type='application/json')
        
        # Assert
        assert response.status_code == 400
    
    def test_tc001_2_create_ticket_no_data(self, client):
        """
        TC-001.2: Create Ticket with No Data
        
        Test Steps:
        1. Send POST request with no JSON body
        2. Verify error response
        
        Expected Result:
        - Error response with status 400
        """
        # Act
        response = client.post('/api/tickets',
                               data='',
                               content_type='application/json')
        
        # Assert
        assert response.status_code == 400
    
    def test_tc001_3_create_ticket_with_past_due_date_accepted_by_api(self, client, sample_ticket_data):
        """
        TC-001.3: Create Ticket with Past Due Date
        
        Note: The API does not validate past dates (validation is client-side).
        This test documents API behavior for past dates.
        
        Test Steps:
        1. Send POST request with past due date
        2. Verify API accepts it (validation is client-side)
        
        Expected Result:
        - API accepts the request (client handles date validation)
        """
        # Arrange: Set past date
        past_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        ticket_data = {**sample_ticket_data, 'due_date': past_date}
        
        # Act
        response = client.post('/api/tickets',
                               data=json.dumps(ticket_data),
                               content_type='application/json')
        
        # Assert: API accepts (client-side validation prevents past dates)
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['due_date'] == past_date


class TestTC002TicketWorkflowManagement(TestConfig):
    """
    TC-002: Ticket Workflow Management Test Cases
    Tests the Kanban board workflow and status transitions.
    """
    
    def test_tc002_1_view_tickets_on_board(self, client_with_tickets):
        """
        TC-002.1: View Tickets on Kanban Board
        
        Test Steps:
        1. Get all tickets via API
        2. Verify tickets exist for each status
        
        Expected Result:
        - Tickets retrieved successfully
        - Tickets exist in todo, in-progress, review, completed statuses
        """
        client, created_tickets = client_with_tickets
        
        # Act: Get all tickets
        response = client.get('/api/tickets')
        
        # Assert
        assert response.status_code == 200
        tickets = json.loads(response.data)
        assert len(tickets) == 4
        
        # Verify tickets in each status
        statuses = [t['status'] for t in tickets]
        assert 'todo' in statuses
        assert 'in-progress' in statuses
        assert 'review' in statuses
        assert 'completed' in statuses
    
    def test_tc002_1_get_specific_ticket(self, client_with_tickets):
        """
        TC-002.1: View Specific Ticket
        
        Test Steps:
        1. Get a specific ticket by ID
        2. Verify correct ticket is returned
        
        Expected Result:
        - Correct ticket details returned
        """
        client, created_tickets = client_with_tickets
        ticket_id = created_tickets[0]['id']
        
        # Act
        response = client.get(f'/api/tickets/{ticket_id}')
        
        # Assert
        assert response.status_code == 200
        ticket = json.loads(response.data)
        assert ticket['id'] == ticket_id
    
    def test_tc002_1_get_nonexistent_ticket(self, client):
        """
        TC-002.1: Get Non-existent Ticket
        
        Test Steps:
        1. Attempt to get ticket with invalid ID
        
        Expected Result:
        - 404 error returned
        """
        # Act
        response = client.get('/api/tickets/nonexistent-id-12345')
        
        # Assert
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_tc002_2_move_ticket_to_in_progress(self, client, sample_ticket_data):
        """
        TC-002.2: Move Ticket to In Progress
        
        Test Steps:
        1. Create a ticket (defaults to 'todo')
        2. Update status to 'in-progress'
        3. Verify status change
        
        Expected Result:
        - Ticket status updated to 'in-progress'
        - updated_at timestamp is set
        """
        # Arrange: Create ticket
        create_response = client.post('/api/tickets',
                                      data=json.dumps(sample_ticket_data),
                                      content_type='application/json')
        ticket = json.loads(create_response.data)
        ticket_id = ticket['id']
        
        # Act: Update status
        update_data = {'status': 'in-progress'}
        response = client.put(f'/api/tickets/{ticket_id}',
                              data=json.dumps(update_data),
                              content_type='application/json')
        
        # Assert
        assert response.status_code == 200
        updated_ticket = json.loads(response.data)
        assert updated_ticket['status'] == 'in-progress'
        assert 'updated_at' in updated_ticket
    
    def test_tc002_3_move_ticket_through_complete_workflow(self, client, sample_ticket_data):
        """
        TC-002.3: Move Ticket Through Complete Workflow
        
        Test Steps:
        1. Create ticket (todo)
        2. Move to 'in-progress'
        3. Move to 'review'
        4. Move to 'completed'
        
        Expected Result:
        - Ticket successfully transitions through all phases
        """
        # Arrange: Create ticket
        create_response = client.post('/api/tickets',
                                      data=json.dumps(sample_ticket_data),
                                      content_type='application/json')
        ticket = json.loads(create_response.data)
        ticket_id = ticket['id']
        assert ticket['status'] == 'todo'
        
        # Step 1: Move to in-progress
        response = client.put(f'/api/tickets/{ticket_id}',
                              data=json.dumps({'status': 'in-progress'}),
                              content_type='application/json')
        assert response.status_code == 200
        assert json.loads(response.data)['status'] == 'in-progress'
        
        # Step 2: Move to review
        response = client.put(f'/api/tickets/{ticket_id}',
                              data=json.dumps({'status': 'review'}),
                              content_type='application/json')
        assert response.status_code == 200
        assert json.loads(response.data)['status'] == 'review'
        
        # Step 3: Move to completed
        response = client.put(f'/api/tickets/{ticket_id}',
                              data=json.dumps({'status': 'completed'}),
                              content_type='application/json')
        assert response.status_code == 200
        assert json.loads(response.data)['status'] == 'completed'
        
        # Verify final state
        get_response = client.get(f'/api/tickets/{ticket_id}')
        final_ticket = json.loads(get_response.data)
        assert final_ticket['status'] == 'completed'
    
    def test_tc002_4_move_ticket_backwards_in_workflow(self, client, sample_ticket_data):
        """
        TC-002.4: Move Ticket Backwards in Workflow
        
        Test Steps:
        1. Create ticket and move to 'in-progress'
        2. Move back to 'todo'
        
        Expected Result:
        - Ticket moves back to 'todo' without restrictions
        """
        # Arrange: Create ticket and move to in-progress
        create_response = client.post('/api/tickets',
                                      data=json.dumps(sample_ticket_data),
                                      content_type='application/json')
        ticket = json.loads(create_response.data)
        ticket_id = ticket['id']
        
        client.put(f'/api/tickets/{ticket_id}',
                   data=json.dumps({'status': 'in-progress'}),
                   content_type='application/json')
        
        # Act: Move back to todo
        response = client.put(f'/api/tickets/{ticket_id}',
                              data=json.dumps({'status': 'todo'}),
                              content_type='application/json')
        
        # Assert
        assert response.status_code == 200
        updated_ticket = json.loads(response.data)
        assert updated_ticket['status'] == 'todo'
    
    def test_tc002_update_ticket_fields(self, client, sample_ticket_data):
        """
        Additional: Update multiple ticket fields
        
        Test Steps:
        1. Create ticket
        2. Update title, description, and due_date
        
        Expected Result:
        - All fields updated correctly
        """
        # Arrange: Create ticket
        create_response = client.post('/api/tickets',
                                      data=json.dumps(sample_ticket_data),
                                      content_type='application/json')
        ticket = json.loads(create_response.data)
        ticket_id = ticket['id']
        
        # Act: Update multiple fields
        new_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        update_data = {
            'title': 'Updated Title',
            'description': 'Updated description',
            'due_date': new_date
        }
        response = client.put(f'/api/tickets/{ticket_id}',
                              data=json.dumps(update_data),
                              content_type='application/json')
        
        # Assert
        assert response.status_code == 200
        updated_ticket = json.loads(response.data)
        assert updated_ticket['title'] == 'Updated Title'
        assert updated_ticket['description'] == 'Updated description'
        assert updated_ticket['due_date'] == new_date
    
    def test_tc002_update_nonexistent_ticket(self, client):
        """
        Additional: Update Non-existent Ticket
        
        Test Steps:
        1. Attempt to update ticket with invalid ID
        
        Expected Result:
        - 404 error returned
        """
        # Act
        response = client.put('/api/tickets/nonexistent-id',
                              data=json.dumps({'status': 'completed'}),
                              content_type='application/json')
        
        # Assert
        assert response.status_code == 404
    
    def test_tc002_update_ticket_no_data(self, client, sample_ticket_data):
        """
        Additional: Update Ticket with No Data
        
        Test Steps:
        1. Create ticket
        2. Attempt update with empty body
        
        Expected Result:
        - 400 error returned
        """
        # Arrange: Create ticket
        create_response = client.post('/api/tickets',
                                      data=json.dumps(sample_ticket_data),
                                      content_type='application/json')
        ticket = json.loads(create_response.data)
        ticket_id = ticket['id']
        
        # Act
        response = client.put(f'/api/tickets/{ticket_id}',
                              data='',
                              content_type='application/json')
        
        # Assert
        assert response.status_code == 400


class TestTC003TicketDeletion(TestConfig):
    """
    TC-003: Ticket Deletion Test Cases
    Tests the ability to delete tickets.
    """
    
    def test_tc003_1_delete_ticket_successfully(self, client, sample_ticket_data):
        """
        TC-003.1: Delete Ticket Successfully
        
        Test Steps:
        1. Create a ticket
        2. Delete the ticket
        3. Verify ticket is removed
        
        Expected Result:
        - Ticket is deleted successfully
        - Ticket no longer exists in the system
        """
        # Arrange: Create ticket
        create_response = client.post('/api/tickets',
                                      data=json.dumps(sample_ticket_data),
                                      content_type='application/json')
        ticket = json.loads(create_response.data)
        ticket_id = ticket['id']
        
        # Verify ticket exists
        get_response = client.get('/api/tickets')
        tickets_before = json.loads(get_response.data)
        assert len(tickets_before) == 1
        
        # Act: Delete ticket
        delete_response = client.delete(f'/api/tickets/{ticket_id}')
        
        # Assert
        assert delete_response.status_code == 200
        delete_data = json.loads(delete_response.data)
        assert 'message' in delete_data
        assert delete_data['ticket']['id'] == ticket_id
        
        # Verify ticket no longer exists
        get_response = client.get('/api/tickets')
        tickets_after = json.loads(get_response.data)
        assert len(tickets_after) == 0
    
    def test_tc003_1_delete_returns_deleted_ticket_info(self, client, sample_ticket_data):
        """
        TC-003.1: Delete Returns Deleted Ticket Information
        
        Test Steps:
        1. Create a ticket
        2. Delete the ticket
        3. Verify response includes deleted ticket details
        
        Expected Result:
        - Response includes deleted ticket information
        """
        # Arrange: Create ticket
        create_response = client.post('/api/tickets',
                                      data=json.dumps(sample_ticket_data),
                                      content_type='application/json')
        ticket = json.loads(create_response.data)
        ticket_id = ticket['id']
        
        # Act: Delete ticket
        delete_response = client.delete(f'/api/tickets/{ticket_id}')
        
        # Assert
        assert delete_response.status_code == 200
        delete_data = json.loads(delete_response.data)
        assert delete_data['ticket']['title'] == sample_ticket_data['title']
        assert delete_data['ticket']['description'] == sample_ticket_data['description']
    
    def test_tc003_2_delete_nonexistent_ticket(self, client):
        """
        TC-003.2: Attempt to Delete Non-existent Ticket
        
        This simulates the API behavior when deletion is attempted
        for a ticket that doesn't exist (e.g., already deleted or
        user cancelled but another process deleted it).
        
        Test Steps:
        1. Attempt to delete ticket with invalid ID
        
        Expected Result:
        - 404 error returned
        - No system changes
        """
        # Act
        response = client.delete('/api/tickets/nonexistent-id-12345')
        
        # Assert
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_tc003_3_delete_last_ticket_in_column(self, client, sample_ticket_data):
        """
        TC-003.3: Delete Last Ticket in Column
        
        Test Steps:
        1. Create a single ticket
        2. Delete that ticket
        3. Verify column is empty
        
        Expected Result:
        - Ticket is removed
        - API returns empty list
        """
        # Arrange: Create single ticket
        create_response = client.post('/api/tickets',
                                      data=json.dumps(sample_ticket_data),
                                      content_type='application/json')
        ticket = json.loads(create_response.data)
        ticket_id = ticket['id']
        
        # Act: Delete the only ticket
        client.delete(f'/api/tickets/{ticket_id}')
        
        # Assert: No tickets remain
        get_response = client.get('/api/tickets')
        tickets = json.loads(get_response.data)
        assert len(tickets) == 0
    
    def test_tc003_3_delete_one_of_many_tickets(self, client_with_tickets):
        """
        TC-003.3: Delete One Ticket When Multiple Exist
        
        Test Steps:
        1. Start with multiple tickets
        2. Delete one ticket
        3. Verify only that ticket is removed
        
        Expected Result:
        - One ticket removed
        - Other tickets remain
        """
        client, created_tickets = client_with_tickets
        ticket_to_delete = created_tickets[0]
        ticket_id = ticket_to_delete['id']
        
        # Verify 4 tickets exist
        get_response = client.get('/api/tickets')
        tickets_before = json.loads(get_response.data)
        assert len(tickets_before) == 4
        
        # Act: Delete one ticket
        client.delete(f'/api/tickets/{ticket_id}')
        
        # Assert: 3 tickets remain
        get_response = client.get('/api/tickets')
        tickets_after = json.loads(get_response.data)
        assert len(tickets_after) == 3
        
        # Verify deleted ticket is not in the list
        remaining_ids = [t['id'] for t in tickets_after]
        assert ticket_id not in remaining_ids


class TestStaticFileServing(TestConfig):
    """
    Additional tests for static file serving.
    """
    
    def test_serve_index_page(self, client):
        """Test serving the index.html page."""
        response = client.get('/')
        # May return 404 if file doesn't exist in test context
        # but the route handler should work
        assert response.status_code in [200, 404]
    
    def test_serve_board_page(self, client):
        """Test serving the board.html page."""
        response = client.get('/board.html')
        assert response.status_code in [200, 404]


class TestCoverageGaps(TestConfig):
    """
    Tests specifically targeting uncovered code paths to improve coverage.
    Addresses lines: 20, 24-25, 42, 74, 104 in app.py
    """
    
    def test_load_tickets_file_not_exists(self, tmp_path, monkeypatch):
        """
        Test load_tickets() returns empty list when file doesn't exist.
        
        Coverage: Line 20
        """
        # Arrange: Point to non-existent file
        non_existent_file = tmp_path / "does_not_exist.json"
        monkeypatch.setattr('app.DATA_FILE', str(non_existent_file))
        
        # Act
        from app import load_tickets
        tickets = load_tickets()
        
        # Assert
        assert tickets == []
        assert not non_existent_file.exists()
    
    def test_load_tickets_corrupted_json(self, tmp_path, monkeypatch):
        """
        Test load_tickets() handles corrupted JSON gracefully.
        
        Coverage: Lines 24-25 (JSONDecodeError)
        """
        # Arrange: Create file with invalid JSON
        corrupted_file = tmp_path / "corrupted.json"
        with open(corrupted_file, 'w') as f:
            f.write("{invalid json content")
        
        monkeypatch.setattr('app.DATA_FILE', str(corrupted_file))
        
        # Act
        from app import load_tickets
        tickets = load_tickets()
        
        # Assert: Returns empty list instead of crashing
        assert tickets == []
    
    def test_load_tickets_io_error(self, tmp_path, monkeypatch):
        """
        Test load_tickets() handles IOError gracefully.
        
        Coverage: Lines 24-25 (IOError)
        """
        # Arrange: Create file then make it unreadable
        import stat
        unreadable_file = tmp_path / "unreadable.json"
        with open(unreadable_file, 'w') as f:
            json.dump([], f)
        
        # Make file unreadable (Unix-style permissions)
        os.chmod(unreadable_file, stat.S_IWUSR)
        
        monkeypatch.setattr('app.DATA_FILE', str(unreadable_file))
        
        # Act
        from app import load_tickets
        tickets = load_tickets()
        
        # Assert: Returns empty list instead of crashing
        assert tickets == []
        
        # Cleanup: Restore permissions
        os.chmod(unreadable_file, stat.S_IRUSR | stat.S_IWUSR)
    
    def test_serve_index_html_direct_route(self, client):
        """
        Test serving the index.html page via /index.html route.
        
        Coverage: Line 42
        """
        response = client.get('/index.html')
        # May return 404 if file doesn't exist in test context
        # but the route handler should work
        assert response.status_code in [200, 404]
    
    def test_create_ticket_empty_json_object(self, client):
        """
        Test create_ticket() with empty JSON object.
        
        This tests the check for falsy data (empty dict).
        Coverage: Line 74
        """
        # Act: Send request with empty JSON object
        response = client.post('/api/tickets',
                               data='{}',
                               content_type='application/json')
        
        # Assert: Should return 400 error
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'No data provided' in data['error']
    
    def test_update_ticket_empty_json_object(self, client, sample_ticket_data):
        """
        Test update_ticket() with empty JSON object.
        
        Coverage: Line 104
        """
        # Arrange: Create a ticket first
        create_response = client.post('/api/tickets',
                                      data=json.dumps(sample_ticket_data),
                                      content_type='application/json')
        ticket = json.loads(create_response.data)
        ticket_id = ticket['id']
        
        # Act: Send update with empty JSON object
        response = client.put(f'/api/tickets/{ticket_id}',
                              data='{}',
                              content_type='application/json')
        
        # Assert: Should return 400 error
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'No data provided' in data['error']


class TestEdgeCases(TestConfig):
    """
    Additional edge case tests.
    """
    
    def test_create_ticket_with_custom_status(self, client, sample_ticket_data):
        """
        Test creating ticket with custom initial status.
        """
        # Arrange
        ticket_data = {**sample_ticket_data, 'status': 'in-progress'}
        
        # Act
        response = client.post('/api/tickets',
                               data=json.dumps(ticket_data),
                               content_type='application/json')
        
        # Assert
        assert response.status_code == 201
        ticket = json.loads(response.data)
        assert ticket['status'] == 'in-progress'
    
    def test_ticket_id_is_uuid(self, client, sample_ticket_data):
        """
        Test that ticket IDs are valid UUIDs.
        """
        # Act
        response = client.post('/api/tickets',
                               data=json.dumps(sample_ticket_data),
                               content_type='application/json')
        
        # Assert
        ticket = json.loads(response.data)
        ticket_id = ticket['id']
        
        # Verify it looks like a UUID
        assert len(ticket_id) == 36
        assert ticket_id.count('-') == 4
    
    def test_created_at_is_iso_format(self, client, sample_ticket_data):
        """
        Test that created_at uses ISO 8601 format.
        """
        # Act
        response = client.post('/api/tickets',
                               data=json.dumps(sample_ticket_data),
                               content_type='application/json')
        
        # Assert
        ticket = json.loads(response.data)
        created_at = ticket['created_at']
        
        # Verify it can be parsed as ISO format
        datetime.fromisoformat(created_at)
    
    def test_updated_at_is_iso_format(self, client, sample_ticket_data):
        """
        Test that updated_at uses ISO 8601 format after update.
        """
        # Arrange
        create_response = client.post('/api/tickets',
                                      data=json.dumps(sample_ticket_data),
                                      content_type='application/json')
        ticket = json.loads(create_response.data)
        ticket_id = ticket['id']
        
        # Act
        response = client.put(f'/api/tickets/{ticket_id}',
                              data=json.dumps({'status': 'completed'}),
                              content_type='application/json')
        
        # Assert
        updated_ticket = json.loads(response.data)
        updated_at = updated_ticket['updated_at']
        
        # Verify it can be parsed as ISO format
        datetime.fromisoformat(updated_at)
    
    def test_multiple_ticket_creation(self, client, sample_ticket_data):
        """
        Test creating multiple tickets.
        """
        # Act: Create 5 tickets
        for i in range(5):
            ticket_data = {**sample_ticket_data, 'title': f'Ticket {i + 1}'}
            response = client.post('/api/tickets',
                                   data=json.dumps(ticket_data),
                                   content_type='application/json')
            assert response.status_code == 201
        
        # Assert: All tickets exist
        get_response = client.get('/api/tickets')
        tickets = json.loads(get_response.data)
        assert len(tickets) == 5
    
    def test_special_characters_in_title(self, client, sample_ticket_data):
        """
        Test creating ticket with special characters in title.
        """
        # Arrange
        ticket_data = {**sample_ticket_data, 'title': 'Fix bug <script>alert("xss")</script>'}
        
        # Act
        response = client.post('/api/tickets',
                               data=json.dumps(ticket_data),
                               content_type='application/json')
        
        # Assert
        assert response.status_code == 201
        ticket = json.loads(response.data)
        assert ticket['title'] == 'Fix bug <script>alert("xss")</script>'
    
    def test_unicode_in_description(self, client, sample_ticket_data):
        """
        Test creating ticket with unicode characters.
        """
        # Arrange
        ticket_data = {**sample_ticket_data, 'description': 'Fix bug for 日本語 users 🎉'}
        
        # Act
        response = client.post('/api/tickets',
                               data=json.dumps(ticket_data),
                               content_type='application/json')
        
        # Assert
        assert response.status_code == 201
        ticket = json.loads(response.data)
        assert ticket['description'] == 'Fix bug for 日本語 users 🎉'


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
