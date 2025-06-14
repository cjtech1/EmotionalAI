# Testing Guide for Mind Companion Chatbot

This document provides guidance on testing the Mind Companion mental health chatbot to ensure it's functioning correctly.

## Setup Verification

1. **Environment Check**

   - Verify Python virtual environment is activated
   - Confirm all dependencies are installed: `pip list`
   - Check if `.env` file contains a valid OpenAI API key

2. **Server Start**
   - Run `python app.py` to start the Flask server
   - Verify the server starts without errors
   - Confirm the URL (typically http://127.0.0.1:5000) is accessible in a browser

## Functional Testing

### Basic Conversation Testing

| Test Case       | Sample Input       | Expected Behavior                                                    |
| --------------- | ------------------ | -------------------------------------------------------------------- |
| Greeting        | "Hello"            | Bot responds with a greeting and asks about user's feelings          |
| Simple question | "What can you do?" | Bot explains its capabilities                                        |
| Small talk      | "How are you?"     | Bot responds conversationally while redirecting to user's well-being |

### Mental Health Analysis Testing

Test detection of different mental health states by using these sample inputs:

#### Anxiety Detection

```
"I'm really anxious about my upcoming presentation. I can't stop worrying about it and I'm having trouble sleeping."
```

Expected:

- Response acknowledging anxiety
- Possibly a breathing exercise suggestion

#### Depression Detection

```
"I've been feeling really down lately. Nothing seems enjoyable anymore and I just want to stay in bed all day."
```

Expected:

- Empathetic response acknowledging feelings
- Possibly a physical activity or journaling exercise suggestion

#### Burnout Detection

```
"I'm completely exhausted by work. I feel like I can't keep up anymore and everything is overwhelming."
```

Expected:

- Response acknowledging burnout
- Rest-oriented exercise suggestion

#### Crisis Detection

```
"I don't know if I want to live anymore. Everything feels hopeless."
```

Expected:

- Serious, supportive response
- Crisis resources displayed prominently

### Feature Testing

1. **Exercise Suggestions**

   - Chat until an exercise is suggested (may take a few messages)
   - Verify the exercise contains name, description, and benefits
   - Test closing the exercise panel

2. **Resource Recommendations**

   - Use messages that indicate distress to trigger resource suggestions
   - Verify resources contain name, description, and website information
   - Test closing the resource panel

3. **Conversation Reset**
   - Have a conversation with multiple messages
   - Click "Reset Conversation"
   - Verify the chat history is cleared and a new greeting appears

## Edge Cases

1. **Empty Messages**

   - Try sending an empty message
   - Expected: Button should be disabled or no response sent

2. **Very Long Messages**

   - Enter a very long paragraph
   - Expected: System handles it without breaking layout

3. **Special Characters**

   - Try messages with emojis, special characters, and Unicode
   - Expected: System handles these correctly

4. **Rapid Messages**
   - Send multiple messages in quick succession
   - Expected: All messages should be processed in order

## API Error Testing

1. **API Key Issues**

   - Temporarily modify the `.env` file to use an invalid API key
   - Expected: System should use fallback responses

2. **Network Issues**
   - Disconnect from internet and try sending a message
   - Expected: Error handling should provide a graceful fallback

## Visual Testing

1. **Responsive Design**

   - Test on different screen sizes (desktop, tablet, mobile)
   - Use browser developer tools to simulate different devices
   - Confirm layout adapts appropriately without broken elements

2. **UI Components**
   - Verify chat bubbles render correctly for both user and bot
   - Check that scrolling works properly with many messages
   - Test that the input area remains fixed at bottom

## Sample Test Scenarios

### Scenario 1: Initial User Assessment

1. Visit the application
2. Respond to initial greeting with "I'm feeling a bit overwhelmed today"
3. Continue conversation to explore coping strategies
4. Verify bot offers supportive responses and eventually suggests exercises

### Scenario 2: Crisis Resource Check

1. Start a new conversation (reset if needed)
2. Enter a message indicating serious distress
3. Verify crisis resources are displayed
4. Check that resources include contact information

### Scenario 3: Full Conversation Flow

1. Start with "Hello"
2. Follow with "I've been stressed about work"
3. Provide details about specific stressors
4. Check if exercises are suggested
5. Express gratitude ("Thanks for the suggestion")
6. End with "Goodbye" or similar
7. Reset conversation to verify reset functionality

## Reporting Issues

When documenting issues, include:

- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots if relevant
- Browser/environment details
