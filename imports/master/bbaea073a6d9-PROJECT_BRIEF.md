# Savvy Life MVP Project Brief

## Project Goal

Build a lean, modular Progressive Web App called **Savvy Life** for independent contractors, freelancers, mobile service providers, and small businesses.

The product will reduce manual paperwork by allowing users to photograph or upload business documents, extract useful information, correct the results, organize records, and generate professional invoices.

The first release must remain inexpensive to build, simple to deploy, and structured so additional modules can be added later without rebuilding the core platform.

## Initial MVP Modules

### 1. Snap-to-Fill Document Capture

Users can photograph or upload supported business documents.

Initial document types:

- Receipts
- Work orders
- Service estimates
- Basic invoices

Required capabilities:

- Take a photo from a phone.
- Upload an image or PDF.
- Extract structured document fields using OCR and AI-assisted processing.
- Let the user review and correct every extracted field.
- Store the original file and structured data.
- Assign documents to customers, jobs, vehicles, or categories.
- Search by keyword, date, customer, merchant, category, or document type.

Suggested extracted fields:

- Customer or merchant name
- Document date
- Description
- Labor amount
- Material amount
- Taxes
- Total amount
- Invoice or reference number
- Payment terms
- Document category
- Notes

The system must never rely entirely on automated extraction. Users must approve or correct extracted data before it becomes final.

### 2. Invoice Builder

Users can create professional invoices manually or from extracted document data.

Required capabilities:

- Create and manage customer records.
- Enter or dictate job details.
- Add labor, materials, taxes, discounts, notes, due dates, and payment terms.
- Reuse information from receipts, work orders, estimates, or prior invoices.
- Review and edit invoice details.
- Generate a professional PDF.
- Download, email, or share the invoice.
- Track status as draft, sent, paid, overdue, or canceled.
- View basic invoice history.

Do not include payroll, full bookkeeping, advanced accounting, or tax filing in the MVP.

### 3. Subscription and Cancellation Assistant

Users can record subscriptions, free trials, and recurring expenses.

Required capabilities:

- Add a subscription manually.
- Track provider, amount, billing frequency, renewal date, and cancellation deadline.
- Save the provider website or cancellation URL.
- Select reminder timing.
- Send email and browser reminders.
- Open the provider cancellation page.
- Mark subscriptions as active, canceled, renewed, or ignored.

The MVP provides assisted cancellation only. It must not promise automatic cancellation with unrelated third-party businesses.

## Target Users

Initial users include:

- Independent contractors
- Tradespeople
- Mobile service providers
- Freelancers
- Delivery and transportation workers
- Sole proprietors
- Small service businesses

These users regularly manage receipts, invoices, work orders, fuel records, customer information, estimates, and recurring expenses from their phones.

## Primary User Journey

1. Create an account.
2. Photograph or upload a supported document.
3. Extract structured fields.
4. Review and correct the extracted information.
5. Save the document to a customer, job, vehicle, or category.
6. Convert the information into an invoice.
7. Generate and share a PDF.
8. Create subscription reminders when needed.

## Platform Strategy

Build the first release as a responsive **Progressive Web App** rather than separate native iOS and Android applications.

The PWA must:

- Work on phones, tablets, and desktop computers.
- Be installable from a browser.
- Use one shared codebase.
- Avoid initial app-store costs and approval delays.
- Support rapid deployment and updates.
- Be designed for later native packaging only if demand is proven.

## Architecture

Use a **modular monolith**, not microservices.

Shared platform services should include:

- Authentication
- User profiles
- Customers
- Jobs
- Document storage
- OCR and field extraction
- Search
- Invoice generation
- Notifications
- Payments
- Audit history

Initial internal modules:

1. Document Capture
2. Invoice Builder
3. Subscription Assistant

Future modules may include:

- Mileage tracking
- Fuel records
- Warranty management
- Tax-ready exports
- Household document storage
- Bill reminders
- Voice-to-form completion
- Appointment management
- Insurance records
- Vehicle records
- Automated administrative agents

Design for these future modules, but do not build them during the MVP.

## Preferred Technology Stack

- TypeScript
- React or Next.js
- Responsive PWA frontend
- Supabase PostgreSQL
- Supabase Authentication
- Supabase private file storage
- Server-side API routes, edge functions, or protected server functions
- Stripe Checkout for future paid subscriptions
- Replaceable OCR and AI provider adapters
- Server-generated PDF invoices
- Email and browser notifications
- Role-based access controls
- Row-level security for all user-owned data

## Security Requirements

- Keep authorization and business logic server-authoritative.
- Use strict row-level security.
- Isolate every user's data.
- Store uploaded documents privately.
- Never expose service-role keys or secrets in frontend code.
- Validate file type, size, ownership, and permissions server-side.
- Preserve original uploaded files.
- Record document-processing status and errors.
- Maintain an audit trail for meaningful data changes.
- Allow users to delete their own documents and account data.
- Treat OCR and AI output as untrusted until reviewed.

## MVP Acceptance Criteria

The MVP is functional when a user can:

1. Create an account.
2. Sign in securely.
3. Upload or photograph a supported document.
4. Receive extracted document fields.
5. Correct inaccurate fields.
6. Save and retrieve the document.
7. Search saved documents.
8. Convert extracted or manually entered data into an invoice.
9. Generate and share a PDF invoice.
10. Create a subscription reminder.
11. Receive a scheduled reminder.
12. Open a saved cancellation website.
13. Use the system from phone and desktop browsers.

## Features Excluded From the MVP

Do not build:

- Universal support for every document type
- Guaranteed automatic subscription cancellation
- Native iOS or Android applications
- Bank-account aggregation
- Full bookkeeping
- Payroll
- Tax filing
- Legal or tax advice
- Complex accounting integrations
- Automated phone calls
- Household administration modules
- Multi-agent AI orchestration
- Enterprise workflow management
- Microservices

## Pilot Validation

Test the MVP with approximately 20 independent contractors or small service businesses.

Recommended pilot pricing:

- $15 to $25 per month
- Or a limited founding-user plan

Minimum validation targets:

- At least 8 of 20 users agree to pay.
- At least 5 remain active after 30 days.
- Active users upload at least 10 documents or create at least 3 invoices.
- Users return without personal reminders.
- At least 3 users say losing the product would materially disrupt their workflow.
- Users demonstrate demand for at least one additional module.

## Success Metrics

Track:

- Account creation
- Document uploads
- Extraction completion rate
- User correction rate
- Documents saved
- Search usage
- Invoices created
- Invoices shared
- Subscription reminders created
- Weekly active users
- Thirty-day retention
- Free-to-paid conversion
- Monthly recurring revenue
- Cost per processed document
- Support requests per user

## Required Initial Deliverables

Before writing production code, produce:

1. A concise architecture plan.
2. The proposed folder structure.
3. The database schema and relationships.
4. The application routes and primary screens.
5. Security and row-level-security rules.
6. A phased implementation plan.
7. A `.env.example`.
8. Local setup instructions.
9. Testing strategy.
10. Deployment plan.

Then build incrementally, keeping every phase runnable and tested.

## Core Product Hypothesis

Independent workers and small service businesses will pay for a mobile-friendly platform that converts everyday paperwork into organized records and usable invoices with less manual data entry.

Optimize for:

- Low operating cost
- Rapid deployment
- Clean module boundaries
- Strong security
- Simple user experience
- Measurable validation
- Avoiding unnecessary complexity
