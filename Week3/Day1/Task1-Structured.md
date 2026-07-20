# Code Converter Web App

## Overview
A web-based tool that converts source code from one programming language to another using a backend LLM API. Users can convert code with or without creating an account, with usage limits based on account status and subscription tier.

## Core Features

- User registration and login system
- Large textbox for pasting code to convert (no account required)
- "Convert" button to trigger the conversion process
- Searchable dropdown menu to select the **source** language
- Searchable dropdown menu to select the **target** language
- Copyable output box for the converted code

## How It Works

1. User pastes their code into the input textbox.
2. User selects the source language and target language from the dropdown menus.
3. User clicks the **Convert** button.
4. The backend sends the code and language selection to an LLM API.
5. The converted code is returned and displayed in a copyable output box.

## Usage Limits

| User Type            | Daily Usage Limit         |
|-----------------------|---------------------------|
| Guest (no account)    | 3 conversions/day         |
| Registered (free tier)| 5 conversions/day         |
| Paid subscription     | Based on subscription tier|

## Backend Requirements

- Integration with an LLM API for code translation
- Language detection/mapping for supported programming languages
- Usage tracking system:
  - By IP/session for guests
  - By account for registered/subscribed users
- Authentication system for registration/login
- Subscription tier management (for paid limits)

## Example User Flow

1. User visits homepage
2. (Optional) User logs in or registers (For increased limits or subscription access)
3. User pastes code:

```python
   def add(a, b):
       return a + b
```

4. User selects:
   - From: Python
   - To: JavaScript
5. User clicks "Convert"
6. Output is displayed:

```javascript
   function add(a, b) {
       return a + b;
   }
```

7. User clicks "Copy" to copy the converted code