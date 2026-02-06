# User Test Case Scenarios

## Project: Ticket Tracker Platform

**Document Version:** 1.0  
**Created Date:** 2026-02-03  
**Related Document:** feature-requirements.md

---

## Overview

This document contains user test case scenarios for validating the Ticket Tracker platform functionality. Test cases are organized by feature requirement.

---

## TC-001: Ticket Creation

### TC-001.1: Create Ticket with Valid Data

| Attribute | Details |
|-----------|---------|
| **Prerequisite** | User has access to the platform |
| **Priority** | High |
| **Related Requirement** | FR-001 |

**Test Steps:**
1. Navigate to the home page (Create Ticket page)
2. Enter a valid title: "Fix login bug"
3. Enter a description: "Users cannot log in with special characters in password"
4. Select a due date in the future
5. Click "Create Ticket" button

**Expected Result:**
- Success message "✅ Ticket created successfully!" is displayed
- Form fields are cleared
- Ticket is visible on the Ticket Board page in "To Do" column

---

### TC-001.2: Create Ticket with Missing Required Fields

| Attribute | Details |
|-----------|---------|
| **Prerequisite** | User has access to the platform |
| **Priority** | High |
| **Related Requirement** | FR-001 |

**Test Steps:**
1. Navigate to the Create Ticket page
2. Leave the title field empty
3. Enter a description
4. Select a due date
5. Click "Create Ticket" button

**Expected Result:**
- Browser validation prevents form submission
- Error indication on required field
- Ticket is NOT created

---

### TC-001.3: Create Ticket with Past Due Date

| Attribute | Details |
|-----------|---------|
| **Prerequisite** | User has access to the platform |
| **Priority** | Medium |
| **Related Requirement** | FR-001 |

**Test Steps:**
1. Navigate to the Create Ticket page
2. Enter valid title and description
3. Attempt to select a past date

**Expected Result:**
- Date picker does not allow selection of past dates (min date set to today)

---

## TC-002: Ticket Workflow Management

### TC-002.1: View Tickets on Kanban Board

| Attribute | Details |
|-----------|---------|
| **Prerequisite** | At least one ticket exists in the system |
| **Priority** | High |
| **Related Requirement** | FR-002 |

**Test Steps:**
1. Navigate to the Ticket Board page
2. Observe the Kanban board layout

**Expected Result:**
- Four columns displayed: To Do, In Progress, Review, Completed
- Each column shows ticket count
- Existing tickets appear in their respective columns
- Each ticket shows title, description (truncated), and due date

---

### TC-002.2: Move Ticket to In Progress

| Attribute | Details |
|-----------|---------|
| **Prerequisite** | A ticket exists in "To Do" status |
| **Priority** | High |
| **Related Requirement** | FR-002 |

**Test Steps:**
1. Navigate to the Ticket Board page
2. Locate a ticket in the "To Do" column
3. Click the status dropdown on the ticket
4. Select "In Progress"

**Expected Result:**
- Ticket moves to "In Progress" column
- "To Do" count decreases by 1
- "In Progress" count increases by 1
- Board updates without page refresh

---

### TC-002.3: Move Ticket Through Complete Workflow

| Attribute | Details |
|-----------|---------|
| **Prerequisite** | A ticket exists in "To Do" status |
| **Priority** | High |
| **Related Requirement** | FR-002 |

**Test Steps:**
1. Move ticket from "To Do" to "In Progress"
2. Move ticket from "In Progress" to "Review"
3. Move ticket from "Review" to "Completed"

**Expected Result:**
- Ticket successfully transitions through all phases
- Column counts update correctly at each step
- Ticket appears in "Completed" column at the end

---

### TC-002.4: Move Ticket Backwards in Workflow

| Attribute | Details |
|-----------|---------|
| **Prerequisite** | A ticket exists in "In Progress" or later status |
| **Priority** | Medium |
| **Related Requirement** | FR-002 |

**Test Steps:**
1. Locate a ticket in "In Progress" column
2. Change status back to "To Do"

**Expected Result:**
- Ticket moves back to "To Do" column
- No restrictions on backward movement
- Column counts update correctly

---

## TC-003: Ticket Deletion

### TC-003.1: Delete Ticket with Confirmation

| Attribute | Details |
|-----------|---------|
| **Prerequisite** | At least one ticket exists |
| **Priority** | High |
| **Related Requirement** | FR-003 |

**Test Steps:**
1. Navigate to the Ticket Board page
2. Locate a ticket to delete
3. Click the 🗑️ (delete) button
4. Click "OK" on the confirmation dialog

**Expected Result:**
- Ticket is removed from the board
- Column count decreases by 1
- Ticket no longer exists in the system

---

### TC-003.2: Cancel Ticket Deletion

| Attribute | Details |
|-----------|---------|
| **Prerequisite** | At least one ticket exists |
| **Priority** | Medium |
| **Related Requirement** | FR-003 |

**Test Steps:**
1. Navigate to the Ticket Board page
2. Locate a ticket to delete
3. Click the 🗑️ (delete) button
4. Click "Cancel" on the confirmation dialog

**Expected Result:**
- Ticket remains on the board
- No changes to column counts
- Ticket still exists in the system

---

### TC-003.3: Delete Last Ticket in Column

| Attribute | Details |
|-----------|---------|
| **Prerequisite** | A column has exactly one ticket |
| **Priority** | Medium |
| **Related Requirement** | FR-003 |

**Test Steps:**
1. Ensure a column has only one ticket
2. Delete that ticket

**Expected Result:**
- Ticket is removed
- Column shows "No tickets" empty state message
- Column count shows 0

---

## TC-004: Ticket Search (NOT YET IMPLEMENTED)

### TC-004.1: Search Ticket by Title

| Attribute | Details |
|-----------|---------|
| **Prerequisite** | Multiple tickets exist with different titles |
| **Priority** | High |
| **Related Requirement** | FR-004 |

**Test Steps:**
1. Navigate to the Ticket Board page
2. Enter search term in the search field
3. Observe filtered results

**Expected Result:**
- Only tickets matching the search term are displayed
- Search is case-insensitive
- Results update as user types

**Status:** ⏳ Pending Implementation

---

### TC-004.2: Search with No Results

| Attribute | Details |
|-----------|---------|
| **Prerequisite** | Tickets exist in the system |
| **Priority** | Medium |
| **Related Requirement** | FR-004 |

**Test Steps:**
1. Enter a search term that matches no tickets
2. Observe the board

**Expected Result:**
- All columns show empty state
- Clear indication that no results match the search
- Option to clear search is available

**Status:** ⏳ Pending Implementation

---

### TC-004.3: Clear Search

| Attribute | Details |
|-----------|---------|
| **Prerequisite** | Search filter is currently active |
| **Priority** | Medium |
| **Related Requirement** | FR-004 |

**Test Steps:**
1. With active search filter, clear the search field
2. Or click a "Clear" button if available

**Expected Result:**
- All tickets are displayed again
- Board returns to normal view

**Status:** ⏳ Pending Implementation

---

## TC-005: About and FAQ Page (NOT YET IMPLEMENTED)

### TC-005.1: Access About Page

| Attribute | Details |
|-----------|---------|
| **Prerequisite** | About page is implemented |
| **Priority** | Low |
| **Related Requirement** | FR-005 |

**Test Steps:**
1. Click on "About" or "Help" link in navigation
2. Observe the About page content

**Expected Result:**
- About page loads successfully
- Platform overview is displayed
- Navigation back to main features is available

**Status:** ⏳ Pending Implementation

---

### TC-005.2: View FAQ Section

| Attribute | Details |
|-----------|---------|
| **Prerequisite** | FAQ section is implemented |
| **Priority** | Low |
| **Related Requirement** | FR-005 |

**Test Steps:**
1. Navigate to the About/FAQ page
2. Locate the FAQ section
3. Expand/view FAQ items

**Expected Result:**
- FAQ questions are visible
- Answers are accessible (expandable or always visible)
- Common usage questions are covered

**Status:** ⏳ Pending Implementation

---

## Test Summary

| Test Case ID | Description | Status |
|--------------|-------------|--------|
| TC-001.1 | Create Ticket with Valid Data | ✅ Ready to Test |
| TC-001.2 | Create Ticket with Missing Fields | ✅ Ready to Test |
| TC-001.3 | Create Ticket with Past Due Date | ✅ Ready to Test |
| TC-002.1 | View Tickets on Kanban Board | ✅ Ready to Test |
| TC-002.2 | Move Ticket to In Progress | ✅ Ready to Test |
| TC-002.3 | Move Ticket Through Complete Workflow | ✅ Ready to Test |
| TC-002.4 | Move Ticket Backwards in Workflow | ✅ Ready to Test |
| TC-003.1 | Delete Ticket with Confirmation | ✅ Ready to Test |
| TC-003.2 | Cancel Ticket Deletion | ✅ Ready to Test |
| TC-003.3 | Delete Last Ticket in Column | ✅ Ready to Test |
| TC-004.1 | Search Ticket by Title | ⏳ Pending Implementation |
| TC-004.2 | Search with No Results | ⏳ Pending Implementation |
| TC-004.3 | Clear Search | ⏳ Pending Implementation |
| TC-005.1 | Access About Page | ⏳ Pending Implementation |
| TC-005.2 | View FAQ Section | ⏳ Pending Implementation |

**Ready to Test:** 10  
**Pending Implementation:** 5
