Beauty Salon Berlin - AI Appointment System
An intelligent appointment booking system for beauty salons that uses AI to handle customer scheduling through natural conversation. The system checks calendar availability, suggests time slots, and automatically creates appointments in Google Calendar.

🎯 Business Use Case
Best Blowouts Berlin, a beauty salon, needs an automated appointment booking system that:

Allows customers to book appointments 24/7 through a chat interface
Checks real-time calendar availability
Suggests available time slots based on existing bookings
Collects customer information (name, email)
Creates calendar appointments automatically
Sends confirmation details to customers
This workflow eliminates manual appointment scheduling, reduces booking errors, and provides instant customer service.

🎨 Screenshots

![workflow image](./images/n8n-ai-appointment-workflow.png)

🏗️ Workflow Architecture
Components Overview
Chat Trigger → AI Agent → No Operation
                 ↑
                 |
    ┌────────────┴────────────┐
    |            |            |
  Memory    LLM Model    Tools (2)
    |            |            |
 Simple    Google Gemini   Calendar
 Memory                    Operations
Node Breakdown
1. When chat message received (Chat Trigger)
Type: @n8n/n8n-nodes-langchain.chatTrigger
Purpose: Entry point for customer conversations
Configuration: Private chat interface (requires authentication)
Output: Provides sessionId, action, and chatInput to the workflow
2. AI Agent (Orchestrator)
Type: @n8n/n8n-nodes-langchain.agent
Purpose: Central intelligence that manages the booking conversation
System Prompt: Defines the agent's role as a scheduling assistant
Booking Process:
Ask for preferred appointment day
Check calendar availability using tools
Present available time slots
Collect customer information (name, email)
Create appointment using tools
Confirm booking with details
Timezone: UTC+1 (Berlin time)
Business Context:
Salon name: Best Blowouts Berlin
Contact: +49 152 1234 0449
3. Google Gemini Chat Model (Language Model)
Type: @n8n/n8n-nodes-langchain.lmChatGoogleGemini
Purpose: Provides natural language understanding and generation
Model: gemini-2.5-flash
Connection: Supplies AI capabilities to the agent via ai_languageModel connection
4. Simple Memory (Conversation Context)
Type: @n8n/n8n-nodes-langchain.memoryBufferWindow
Purpose: Maintains conversation history for context-aware responses
Configuration:
Session-based memory (tracks individual customer conversations)
Window length: 5 messages
Session key: {{ $json.sessionId }}
Connection: Provides memory to agent via ai_memory connection
5. check_calendar_availability (Tool #1)
Type: n8n-nodes-base.googleCalendarTool
Purpose: Fetches existing appointments to identify free time slots
Operation: getAll (retrieve events)
Configuration:
Calendar: muhammadamir@gmail.com
Limit: 50 events
Dynamic parameters using $fromAI():
timeMin: eventsAfter - Start of search range
timeMax: eventsBefore - End of search range
Tool Description: Instructs AI to calculate available slots by finding gaps between existing appointments
Connection: Connected to agent as ai_tool
6. create_calendar_appointment (Tool #2)
Type: n8n-nodes-base.googleCalendarTool
Purpose: Creates new calendar appointments
Operation: create (add event)
Configuration:
Calendar: muhammadamir@gmail.com
Dynamic parameters using $fromAI():
startDateTime: Appointment start (ISO 8601 format)
endDateTime: Appointment end (ISO 8601 format)
summary: Appointment title
attendeeEmail: Customer email
description: Appointment details with customer name
Default reminders: Enabled
Connection: Connected to agent as ai_tool
7. No Operation, do nothing (Terminator)
Type: n8n-nodes-base.noOp
Purpose: Clean workflow termination point
Connection: Receives final output from AI Agent
🔄 Workflow Flow
Main Execution Path
1. Customer sends message → Chat Trigger
2. Chat Trigger → AI Agent (with chatInput)
3. AI Agent orchestrates:
   - Loads conversation history (Simple Memory)
   - Processes input (Google Gemini)
   - Calls tools as needed:
     a. check_calendar_availability (to find slots)
     b. create_calendar_appointment (to book)
4. AI Agent → No Operation (completion)
Connection Types
Main Connections (data flow):

When chat message received → AI Agent
AI Agent → No Operation, do nothing
AI Connections (capabilities):

Google Gemini Chat Model → AI Agent (ai_languageModel)
Simple Memory → AI Agent (ai_memory)
check_calendar_availability → AI Agent (ai_tool)
create_calendar_appointment → AI Agent (ai_tool)
🔧 Key Technical Features
1. $fromAI() Dynamic Parameters
Both calendar tools use $fromAI() expressions to allow the AI to dynamically determine parameter values at runtime:

// Check availability tool
timeMin: ={ $fromAI('eventsAfter', 'Return events after this date time, use 2025-01-22T00:00:00 format') }
timeMax: ={ $fromAI('eventsBefore', 'Return events before this date time, use 2025-01-22T00:00:00 format') }

// Create appointment tool
start: ={ $fromAI('startDateTime', 'Appointment start date and time in ISO 8601 format, e.g., 2025-01-22T15:30:00') }
end: ={ $fromAI('endDateTime', 'Appointment end date and time in ISO 8601 format, e.g., 2025-01-22T16:30:00') }
summary: ={ $fromAI('summary', 'Appointment title/summary') }
attendeeEmail: ={ $fromAI('attendeeEmail', 'Customer email address') }
description: ={ $fromAI('description', 'Appointment description including customer name') }
2. Session-Based Memory
Maintains separate conversation contexts for different customers using session IDs, enabling personalized multi-turn conversations.

3. Tool Descriptions
Each tool has detailed descriptions that guide the AI on:

When to use the tool
What parameters to provide
How to interpret results
4. Structured Booking Process
The AI follows a 6-step process defined in the system prompt, ensuring consistent customer experience.

📋 Prerequisites
Required Credentials
Google Calendar OAuth2 API

Used by both calendar tools
Requires access to the target calendar (muhammadamir@gmail.com)
Google Gemini (PaLM) API

Used by the language model
Requires valid API key
Required Permissions
Google Calendar: Read and write access to events
Google Gemini: API access for model gemini-2.5-flash
🚀 Setup Instructions
Configure Google Calendar Credentials

Add Google Calendar OAuth2 credentials in n8n
Ensure access to the target calendar
Configure Google Gemini Credentials

Add Google Gemini API credentials in n8n
Verify model access
Customize Business Details (in AI Agent system prompt)

Update salon name
Update phone number
Adjust timezone if needed
Modify appointment confirmation format
Activate Workflow

Enable the workflow
Test with sample conversations
💬 Example Conversation Flow
Customer: Hi, I'd like to book an appointment
AI: Hello! I'd be happy to help you book an appointment at Best Blowouts Berlin. 
    What day would you prefer for your appointment?

Customer: How about next Tuesday?
AI: [Checks calendar using check_calendar_availability tool]
    I have the following time slots available on Tuesday, January 23rd:
    - 9:00 AM
    - 11:30 AM
    - 2:00 PM
    - 4:30 PM
    Which time works best for you?

Customer: 2:00 PM sounds good
AI: Perfect! To complete your booking, I'll need:
    - Your full name
    - Your email address

Customer: John Smith, john@example.com
AI: [Creates appointment using create_calendar_appointment tool]
    I have successfully booked your appointment, here are the details:
    **Date & Time**: 14:00 on Tuesday, 23 January, 2025
    **Email for booking**: john@example.com
    If you need to cancel your appointment please call +49 152 1234 0449
🎨 Customization Options
Adjust Appointment Duration
Modify the AI's instructions to specify default appointment lengths or ask customers for service type.

Add More Tools
Extend functionality with additional tools:

Send confirmation emails
SMS notifications
Payment processing
Service selection
Multi-Calendar Support
Configure different calendars for different services or staff members.

Business Hours Validation
Add logic to prevent bookings outside business hours.

📊 Business Benefits
24/7 Availability: Customers can book anytime
Reduced No-Shows: Automatic calendar invites with email notifications
Staff Efficiency: Eliminates manual scheduling tasks
Better Customer Experience: Instant responses and confirmations
Scalability: Handles multiple concurrent booking conversations
Data Collection: Automatically captures customer information
🔒 Security Considerations
Chat interface is set to private (requires authentication)
Calendar access is restricted to authorized Google account
Customer data (email, name) is only stored in Google Calendar
Session-based memory ensures conversation privacy
📈 Future Enhancements
Add cancellation/rescheduling capabilities
Integrate payment processing
Multi-language support
Service type selection
Staff member selection
Automated reminder emails/SMS
Analytics and reporting

