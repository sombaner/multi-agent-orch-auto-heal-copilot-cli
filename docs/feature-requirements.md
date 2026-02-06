# Feature Requirements Document

## Project: Ticket Tracker Platform

**Document Version:** 1.0  
**Created Date:** 2026-02-03  
**Source:** Teams conversation with Somnath

---

## Overview

This document outlines the feature requirements for the Ticket Tracker platform as discussed with Somnath. Each feature is tracked with its implementation status.

---

## Feature Requirements

### FR-001: Ticket Creation ✅ COMPLETED

| Attribute | Details |
|-----------|---------|
| **Priority** | High |
| **Status** | ✅ Completed |
| **Description** | Users should be able to come to the platform and create a ticket |

**Acceptance Criteria:**
- [x] User can access a ticket creation form
- [x] Form includes title, description, and due date fields
- [x] Ticket is saved with a unique identifier
- [x] User receives confirmation upon successful creation

**Implementation Notes:**
- Implemented in `src/index.html` (frontend form)
- API endpoint: `POST /api/tickets` in `src/app.py`
- Tickets stored in `tickets_data.json`

---

### FR-002: Ticket Workflow Management ✅ COMPLETED

| Attribute | Details |
|-----------|---------|
| **Priority** | High |
| **Status** | ✅ Completed |
| **Description** | Users should be able to move tickets across various phases until completion |

**Acceptance Criteria:**
- [x] Kanban board displays tickets in columns by status
- [x] Status options: To Do, In Progress, Review, Completed
- [x] User can change ticket status via dropdown
- [x] Board updates immediately after status change

**Implementation Notes:**
- Implemented in `src/board.html` (Kanban board UI)
- API endpoint: `PUT /api/tickets/:id` in `src/app.py`
- Status transitions supported: todo → in-progress → review → completed

---

### FR-003: Ticket Deletion ✅ COMPLETED

| Attribute | Details |
|-----------|---------|
| **Priority** | Medium |
| **Status** | ✅ Completed |
| **Description** | Users should be able to delete tickets if needed |

**Acceptance Criteria:**
- [x] Delete button available on each ticket card
- [x] Confirmation prompt before deletion
- [x] Ticket removed from board after deletion
- [x] API returns success message

**Implementation Notes:**
- Delete button implemented in `src/board.html`
- API endpoint: `DELETE /api/tickets/:id` in `src/app.py`
- Includes confirmation dialog to prevent accidental deletion

---

### FR-004: Ticket Search ❌ NOT IMPLEMENTED

| Attribute | Details |
|-----------|---------|
| **Priority** | Medium |
| **Status** | ❌ Not Implemented |
| **Description** | Users should be able to search for tickets |

**Acceptance Criteria:**
- [ ] Search input field available on the board page
- [ ] Search filters tickets by title and/or description
- [ ] Results update in real-time as user types
- [ ] Clear search option to reset view

**Implementation Notes:**
- Not yet implemented
- Suggested location: Add search bar to `src/board.html`
- Backend option: Add query parameter support to `GET /api/tickets`

---

### FR-005: About and FAQ Page ❌ NOT IMPLEMENTED

| Attribute | Details |
|-----------|---------|
| **Priority** | Low |
| **Status** | ❌ Not Implemented |
| **Description** | An "About" and FAQ page giving an overview of how to use the platform |

**Acceptance Criteria:**
- [ ] Dedicated About/FAQ page accessible from navigation
- [ ] Platform overview and purpose explained
- [ ] FAQ section with common questions and answers
- [ ] Instructions on how to use key features

**Implementation Notes:**
- Not yet implemented
- Suggested: Create `src/about.html` with navigation link
- Add route in `src/app.py` to serve the page

---

## Summary

| Feature | Status |
|---------|--------|
| FR-001: Ticket Creation | ✅ Completed |
| FR-002: Ticket Workflow Management | ✅ Completed |
| FR-003: Ticket Deletion | ✅ Completed |
| FR-004: Ticket Search | ❌ Not Implemented |
| FR-005: About and FAQ Page | ❌ Not Implemented |

**Completion Rate:** 3/5 features (60%)

---

## Next Steps

1. Implement ticket search functionality (FR-004)
2. Create About and FAQ page (FR-005)
3. Consider additional enhancements based on user feedback
