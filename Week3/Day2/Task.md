# Code Converter Web App — Project Context

## Purpose

A web app that converts source code from one programming language to another, using an LLM API on the backend. Usage is free-tier gated: guests get limited daily conversions, registered users get more, and paid tiers get more still.

## Core Features

- User registration and login
- Large textbox for pasting code — no account required to use it
- "Convert" button to trigger conversion
- Searchable dropdown to select the **source** language
- Searchable dropdown to select the **target** language
- Copyable output box for the converted code

## User Flow

1. User pastes code into the input textbox.
2. User selects source language and target language from the dropdowns.
3. User clicks **Convert**.
4. Backend sends code + language selection to the LLM API.
5. Converted code is returned and rendered in a copyable output box.

### Example

Input (Python → JavaScript):

```python
def add(a, b):
    return a + b
```

Output:

```javascript
function add(a, b) {
    return a + b;
}
```

## Usage Limits

| User Type              | Daily Limit                  |
|-------------------------|-------------------------------|
| Guest (no account)      | 3 conversions/day             |
| Registered (free tier)  | 5 conversions/day             |
| Paid subscription       | Set per subscription tier     |

## Backend Requirements

- LLM API integration for code translation
- Language list/mapping for supported source & target languages
- Usage tracking:
  - Guests → tracked by IP/session
  - Registered/paid users → tracked by account
- Authentication system (register/login)
- Subscription tier management (limits, billing hooks)