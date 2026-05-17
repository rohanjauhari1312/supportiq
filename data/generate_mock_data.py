"""
Generates realistic mock support data and writes it to data/mock_data.json.
Run from repo root: python data/generate_mock_data.py
"""
import json
from pathlib import Path


def generate() -> dict:
    docs = [
        {
            "id": "doc-001",
            "title": "Password Reset Flow",
            "category": "Authentication",
            "content": (
                "## Password Reset Flow\n\n"
                "Resetting your password is a self-service action available from the login page. "
                "Click \"Forgot password?\" and enter the email address associated with your account. "
                "You will receive a reset link within a few minutes. Check your spam folder if it does not arrive "
                "— some corporate email filters flag automated messages.\n\n"
                "The reset link is valid for 24 hours. Clicking an expired link will show an error asking you to "
                "request a new one. Each new request invalidates any previously issued links, so if you requested "
                "multiple times, only the most recent link will work.\n\n"
                "After clicking the link, you will be taken to a page where you must enter your new password twice. "
                "Passwords must be at least 12 characters and include at least one uppercase letter, one number, "
                "and one special character. You cannot reuse your last five passwords.\n\n"
                "### Locked Account Edge Cases\n\n"
                "After five consecutive failed login attempts, the account is locked for 30 minutes as a security "
                "measure. During this window, even a correct password will be rejected. You have two options: wait "
                "out the lockout period or contact support to have the lock manually cleared.\n\n"
                "If your account was locked and you also need to reset your password, do both steps in the right "
                "order: first have support clear the lock, then initiate the password reset flow. Starting the "
                "reset while the account is locked will result in the reset email being sent but the new password "
                "failing on first use.\n\n"
                "Organization admins can also reset passwords on behalf of members from the team management panel. "
                "This generates a one-time link delivered to the member's email. The member is required to change "
                "the password again on first login when this method is used."
            ),
        },
        {
            "id": "doc-002",
            "title": "Two-Factor Authentication Setup",
            "category": "Authentication",
            "content": (
                "## Two-Factor Authentication Setup\n\n"
                "Two-factor authentication (2FA) adds a second verification step on top of your password. "
                "We support time-based one-time passwords (TOTP) via any standard authenticator app — "
                "Google Authenticator, Authy, 1Password, and Bitwarden all work correctly.\n\n"
                "### Enabling 2FA\n\n"
                "Go to Account Settings > Security > Two-Factor Authentication and click \"Enable\". You will see "
                "a QR code and a text-based secret. Open your authenticator app, tap the option to add a new "
                "account, and scan the QR code. The app will immediately start generating 6-digit codes that "
                "rotate every 30 seconds. Enter the current code in the confirmation field to complete setup.\n\n"
                "### Backup Codes\n\n"
                "Immediately after enabling 2FA, you are shown ten single-use backup codes. Download or print "
                "these and store them somewhere secure and offline. Each code can only be used once. If you "
                "exhaust your backup codes, go to Security Settings and generate a new set, which invalidates "
                "the previous set.\n\n"
                "Backup codes are the only way to access your account if you lose access to your authenticator "
                "app and cannot restore from a cloud backup. Support cannot bypass 2FA without identity "
                "verification via your organization admin or a government-issued ID.\n\n"
                "### Disabling 2FA\n\n"
                "To turn off 2FA, go to Account Settings > Security and click \"Disable two-factor "
                "authentication\". You must authenticate with your current TOTP code or a backup code before the "
                "change takes effect. If your organization has enforced 2FA at the admin level, you will not see "
                "the option to disable it — contact your admin instead.\n\n"
                "### Switching Authenticator Apps\n\n"
                "If you are moving to a new phone or a different app, do not simply scan the existing QR code "
                "in the new app — that code may no longer be shown. Instead, disable 2FA entirely (using your "
                "old device or a backup code), then re-enable it and complete the setup on the new device."
            ),
        },
        {
            "id": "doc-003",
            "title": "API Authentication",
            "category": "API",
            "content": (
                "## API Authentication\n\n"
                "The API supports two authentication mechanisms: API keys and OAuth 2.0. Which one you should "
                "use depends on your use case.\n\n"
                "### API Keys\n\n"
                "API keys are the simplest option and are suitable for server-side integrations where the key "
                "can be stored securely. Generate a key from the Developer Settings page. Keys are shown in "
                "full only at creation time — after you close the dialog, only the last four characters are "
                "visible. If you lose a key, revoke it and generate a new one.\n\n"
                "Include the key in every request using the Authorization header: "
                "`Authorization: Bearer YOUR_API_KEY`. Never embed API keys in client-side JavaScript or mobile "
                "app bundles, as these are easily extracted.\n\n"
                "### Key Rotation\n\n"
                "Rotate API keys regularly and always rotate immediately if you suspect exposure. The recommended "
                "approach is to generate a new key, update your integration to use it, verify the integration is "
                "working, then revoke the old key. Both keys can be active simultaneously during the transition "
                "period to avoid downtime.\n\n"
                "### OAuth 2.0\n\n"
                "OAuth 2.0 is required when your application acts on behalf of individual users. We support the "
                "authorization code flow with PKCE. Register your application in Developer Settings to get a "
                "client ID and secret. During the authorization flow, the user is redirected to our consent "
                "screen, grants permissions, and is redirected back to your callback URL with an authorization "
                "code. Exchange that code for an access token and refresh token.\n\n"
                "Access tokens expire after one hour. Use the refresh token to get a new access token without "
                "requiring the user to log in again. Refresh tokens expire after 90 days of inactivity.\n\n"
                "### Scopes\n\n"
                "Both key and OAuth token permissions are governed by scopes. Available scopes include "
                "`read:data`, `write:data`, `manage:users`, and `manage:billing`. Request only the scopes your "
                "application actually needs. Overly permissive tokens are a significant security risk if compromised."
            ),
        },
        {
            "id": "doc-004",
            "title": "API Rate Limits",
            "category": "API",
            "content": (
                "## API Rate Limits\n\n"
                "Rate limits exist to ensure consistent performance for all users and to protect the service "
                "from abuse. Limits are applied per API key (or per OAuth token), not per IP address.\n\n"
                "### Tier Limits\n\n"
                "Limits vary by plan tier:\n\n"
                "- Starter: 60 requests per minute, 5,000 per day\n"
                "- Growth: 300 requests per minute, 50,000 per day\n"
                "- Business: 1,000 requests per minute, 500,000 per day\n"
                "- Enterprise: Custom limits, negotiated per contract\n\n"
                "Limits are enforced on a rolling 60-second window, not a fixed clock minute. This means "
                "bursting to your per-minute limit and then waiting 60 seconds will not cause problems, but "
                "sustained traffic above the limit will result in throttling.\n\n"
                "### Handling 429 Responses\n\n"
                "When you exceed the rate limit, the API returns HTTP 429 with a JSON body indicating why you "
                "were throttled. Two headers accompany the response: X-RateLimit-Remaining (requests left in "
                "the current window) and Retry-After (seconds until you can retry). Always honor the "
                "Retry-After value — retrying immediately just burns your quota faster.\n\n"
                "### Backoff Strategy\n\n"
                "For services that need to stay within rate limits under variable load, implement exponential "
                "backoff with jitter. On a 429, wait min(base * 2^attempt, max_wait) + random(0, jitter) seconds "
                "before retrying. A reasonable configuration is base=1s, max_wait=60s, jitter=0.5s. After five "
                "consecutive failures, surface the error to your users rather than continuing to retry silently.\n\n"
                "For batch operations, use our bulk endpoints where available — they are rate-limited per call "
                "rather than per record, making them significantly more efficient for large datasets."
            ),
        },
        {
            "id": "doc-005",
            "title": "API Error Codes",
            "category": "API",
            "content": (
                "## API Error Codes\n\n"
                "All API errors return a JSON body with a `code` field (machine-readable), a `message` field "
                "(human-readable description), and occasionally a `details` object with additional context.\n\n"
                "### 4xx Client Errors\n\n"
                "invalid_request (400): Malformed JSON or missing required fields. Check request body against "
                "the schema in the API reference.\n\n"
                "unauthorized (401): Missing or invalid API key. Verify the Authorization header format and "
                "key validity.\n\n"
                "forbidden (403): Valid key but insufficient scope. Check the scopes assigned to your API key.\n\n"
                "not_found (404): Resource does not exist. Confirm the resource ID; it may have been deleted.\n\n"
                "conflict (409): State conflict, e.g. duplicate creation. Check if the resource already exists "
                "before creating.\n\n"
                "unprocessable (422): Semantically invalid request. Read the `details` field for specific "
                "field-level errors.\n\n"
                "rate_limited (429): Exceeded rate limit. Back off and retry after Retry-After seconds.\n\n"
                "### 5xx Server Errors\n\n"
                "internal_error (500): Unexpected server error. Retry with backoff; if persistent, file a "
                "support ticket with the request ID.\n\n"
                "service_unavailable (503): Planned or unplanned downtime. Check the status page; retry when "
                "service resumes.\n\n"
                "gateway_timeout (504): Request took too long. Reduce payload size or use async endpoints for "
                "large operations.\n\n"
                "Every error response includes a `request_id` header. Include this in any support ticket — it "
                "allows the team to look up the exact request in server logs and diagnose the issue quickly. "
                "Without it, debugging intermittent 5xx errors is significantly slower."
            ),
        },
        {
            "id": "doc-006",
            "title": "Billing Overview",
            "category": "Billing",
            "content": (
                "## Billing Overview\n\n"
                "Billing is managed at the organization level. Only users with the Admin or Billing Manager "
                "role can view or change billing information.\n\n"
                "### Plan Tiers\n\n"
                "Plans are priced per seat (per active user per month). A seat is consumed by any user who "
                "logged in at least once during the billing period. Deactivated users do not consume seats. "
                "Seats are counted at the time of invoice generation, not at the time of user creation.\n\n"
                "- Starter: Up to 5 seats, flat rate, monthly billing only\n"
                "- Growth: 6-50 seats, per-seat pricing, monthly or annual billing\n"
                "- Business: 51-500 seats, per-seat pricing with volume discount, annual billing preferred\n"
                "- Enterprise: 500+ seats, custom pricing, negotiated SLA, dedicated support\n\n"
                "### Billing Cycle\n\n"
                "Monthly plans bill on the same calendar day each month — the anniversary of when you first "
                "subscribed. Annual plans bill once per year on that same anniversary. If you subscribe on the "
                "31st and a given month has fewer days, billing occurs on the last day of that month.\n\n"
                "### Prorations\n\n"
                "When you add seats mid-cycle, you are charged for the prorated cost of those seats for the "
                "remaining days in the current period. When you remove seats, the credit is applied to your "
                "next invoice rather than refunded to your payment method, unless you are downgrading plans, "
                "in which case the refund policy applies.\n\n"
                "Upgrading plans mid-cycle also prorates both the old plan's credit and the new plan's charge. "
                "The net difference is charged immediately if positive, or credited to your account if negative."
            ),
        },
        {
            "id": "doc-007",
            "title": "Invoice Management",
            "category": "Billing",
            "content": (
                "## Invoice Management\n\n"
                "All invoices are available in your organization's billing portal. Navigate to "
                "Settings > Billing > Invoices to see the full history.\n\n"
                "### Accessing Invoices\n\n"
                "Invoices are generated within 24 hours of a successful payment. Each invoice shows the "
                "billing period, a line-item breakdown of charges, the payment method used, and the payment "
                "status. Invoices with status 'open' indicate a failed charge; 'paid' invoices are finalized.\n\n"
                "### Downloading Invoices\n\n"
                "Every invoice has a PDF download option. The PDF is formatted for accounting purposes and "
                "includes your organization's legal name, address, and tax ID if you have provided them. "
                "If you need to update the legal name or address on invoices, update the billing information "
                "in Settings > Billing > Details before the next billing cycle — changes do not retroactively "
                "update past invoices.\n\n"
                "### VAT and Tax\n\n"
                "If your organization is based in the EU or another jurisdiction that requires VAT collection, "
                "you will be charged VAT at the applicable rate unless you provide a valid VAT registration "
                "number. Enter your VAT number in Settings > Billing > Tax Information. Upon saving, the system "
                "validates the number against the EU VIES database and, if valid, immediately applies the "
                "zero-VAT rate to future invoices. VAT is never refunded on past invoices where it was "
                "correctly charged.\n\n"
                "US-based organizations in states where we collect sales tax will see that tax itemized on "
                "their invoice. If your organization is tax-exempt, upload your exemption certificate through "
                "the billing portal and allow up to one business day for review."
            ),
        },
        {
            "id": "doc-008",
            "title": "Refund and Cancellation Policy",
            "category": "Billing",
            "content": (
                "## Refund and Cancellation Policy\n\n"
                "### Cancellation\n\n"
                "You can cancel your subscription at any time from Settings > Billing > Plan. Cancellation "
                "takes effect at the end of your current billing period — you retain access to all features "
                "until then. After the period ends, the organization is downgraded to a read-only state: "
                "members can view existing data but cannot create, edit, or delete anything. Data is retained "
                "for 90 days post-cancellation, after which it is permanently deleted.\n\n"
                "To cancel immediately (forfeiting remaining access), contact billing support. This is rarely "
                "necessary but is handled case by case.\n\n"
                "### Refund Eligibility\n\n"
                "Monthly plan subscribers are eligible for a full refund within 7 days of initial signup. "
                "After that window, monthly charges are non-refundable but you can cancel to stop future "
                "charges. There is no partial-month refund for cancellations mid-cycle.\n\n"
                "Annual plan subscribers are eligible for a prorated refund for the unused portion of their "
                "term, minus a 10% early-termination fee, within the first 60 days of the annual term. After "
                "60 days, annual plans are non-refundable.\n\n"
                "### Process\n\n"
                "Refund requests must be submitted through the billing portal or by emailing billing support "
                "with your organization name and the reason for the request. Approved refunds are credited "
                "back to the original payment method within 5-10 business days. If the original payment method "
                "is no longer valid, the team will arrange an alternative.\n\n"
                "Plan downgrades that result in a credit are applied to your next invoice rather than refunded, "
                "unless you are also cancelling the subscription."
            ),
        },
        {
            "id": "doc-009",
            "title": "Data Export",
            "category": "Data Management",
            "content": (
                "## Data Export\n\n"
                "You can export your organization's data at any time from Settings > Data > Export. Only Admin "
                "users can initiate exports.\n\n"
                "### Formats\n\n"
                "Exports are available in three formats:\n\n"
                "JSON: Complete data with all fields and nested objects. Use this for re-importing into another "
                "system or for programmatic processing.\n\n"
                "CSV: Flattened tabular data. Nested objects are serialized as JSON strings within cells. Good "
                "for spreadsheet analysis.\n\n"
                "Parquet: Columnar format optimized for large datasets and analytics tools like DuckDB, Spark, "
                "or BigQuery. Available only for datasets over 100,000 rows.\n\n"
                "### Scheduling Exports\n\n"
                "Recurring exports can be scheduled daily, weekly, or monthly. Scheduled exports are delivered "
                "to an S3-compatible object storage bucket you configure in the export settings. You must "
                "provide a bucket name, region, and IAM credentials with s3:PutObject permission. Test the "
                "connection before saving the schedule — the UI will attempt a test write to confirm the "
                "credentials are valid.\n\n"
                "### Large Dataset Handling\n\n"
                "Exports over 1 GB are split into multiple files automatically, each capped at 500 MB. The "
                "export job runs asynchronously — you receive an email notification with a download link when "
                "the job completes. Download links expire after 7 days.\n\n"
                "For very large datasets (over 10 million rows), exports can take 30-60 minutes. During this "
                "time the export job is visible in Settings > Data > Export History with a status of "
                "'processing'. Do not restart the job if it appears stuck — check the history page first and "
                "contact support only if status has not changed after two hours."
            ),
        },
        {
            "id": "doc-010",
            "title": "User Roles and Permissions",
            "category": "Team Management",
            "content": (
                "## User Roles and Permissions\n\n"
                "Access control is managed through a role-based system. Each organization member is assigned "
                "exactly one role. Roles cannot be combined — if a user needs permissions from two roles, "
                "grant the higher of the two.\n\n"
                "### Roles\n\n"
                "Admin: Full access to all features, settings, billing, and user management. Admins can invite "
                "and remove members, change roles, configure SSO, and manage integrations. Every organization "
                "must have at least one Admin at all times.\n\n"
                "Member: Can access and use all core product features within the organization's workspace. "
                "Cannot access billing, cannot invite or remove other users, and cannot change "
                "organization-level settings.\n\n"
                "Viewer: Read-only access. Can view data and reports but cannot create, edit, or delete "
                "anything. Useful for stakeholders, auditors, or contractors who need visibility without "
                "write access.\n\n"
                "### Custom Roles (Business and Enterprise)\n\n"
                "Business and Enterprise plans can define custom roles with granular permission sets. "
                "Permissions are grouped into categories: Data, Integrations, Reporting, and Administration. "
                "Each category has read, write, and delete permissions that can be toggled independently. "
                "Custom roles are defined at the organization level and can be assigned to any member.\n\n"
                "### Transferring Ownership\n\n"
                "Organization ownership can be transferred to any existing Admin. The current owner goes to "
                "Settings > Team > Transfer Ownership, selects the new owner, and confirms with their "
                "password. The outgoing owner is downgraded to Admin. If the original owner needs to leave "
                "the organization entirely, they should complete the transfer first, then remove themselves.\n\n"
                "### Role Change Behavior\n\n"
                "Role changes take effect immediately. If you downgrade a user from Admin to Member while they "
                "are actively logged in, their permissions change on the next page load without requiring them "
                "to log out."
            ),
        },
        {
            "id": "doc-011",
            "title": "Onboarding Checklist",
            "category": "Getting Started",
            "content": (
                "## Onboarding Checklist\n\n"
                "This guide covers the first things to do after creating your organization account. Completing "
                "all of these steps typically takes 20-30 minutes and ensures the rest of the platform works "
                "as expected.\n\n"
                "### Account Setup\n\n"
                "1. Verify your email address if you have not already. Some features are gated until email "
                "is confirmed.\n"
                "2. Complete your profile: set a display name and upload a profile picture.\n"
                "3. Enable two-factor authentication (2FA). Go to Account Settings > Security.\n"
                "4. Set your notification preferences in Account Settings > Notifications.\n\n"
                "### First Integration\n\n"
                "5. Connect your first data source or integration from the Integrations page. If you are "
                "connecting a database, you will need the host, port, username, password, and database name.\n"
                "6. Run a test query or sync to confirm the connection is working.\n"
                "7. Set up a webhook if your workflow requires real-time event delivery.\n\n"
                "### Team Invite\n\n"
                "8. Invite teammates from Settings > Team > Invite Members. Enter email addresses and select "
                "roles before sending. Invites expire after 7 days.\n"
                "9. If your organization uses SSO, configure it before inviting large numbers of users — "
                "SSO-invited users cannot set a local password.\n"
                "10. Share the onboarding checklist with invited members so they can complete their own "
                "account setup steps.\n\n"
                "Once all ten steps are complete, your organization is ready for production use. If you run "
                "into any issues during onboarding, contact support and reference which step you are on."
            ),
        },
        {
            "id": "doc-012",
            "title": "Third-Party Integrations Overview",
            "category": "Integrations",
            "content": (
                "## Third-Party Integrations Overview\n\n"
                "The platform supports a growing catalog of third-party integrations accessible from the "
                "Integrations page. Integrations are installed at the organization level and managed by Admins.\n\n"
                "### Zapier\n\n"
                "The Zapier integration lets you connect to thousands of other apps without writing code. "
                "Use our Zapier app to trigger actions in external tools when events happen in your workspace, "
                "or to create records in your workspace based on events in external apps. The integration "
                "requires a Zapier account (free tier works for basic use cases).\n\n"
                "### Slack\n\n"
                "Connecting Slack enables notifications and interactive workflows directly in your channels. "
                "Admins install the Slack app from our Integrations page, which redirects to Slack's OAuth "
                "flow. Once installed, configure which events send messages to which channels from the "
                "integration settings. You can also configure Slack alerts for specific thresholds or "
                "anomalies if your plan includes alerting.\n\n"
                "### Salesforce\n\n"
                "The Salesforce integration syncs data bidirectionally between the two platforms. Set up "
                "requires a Salesforce account with API access enabled and a dedicated integration user with "
                "appropriate object permissions. The field mapping is configurable from the integration "
                "settings. Sync runs on a configurable schedule (minimum 15 minutes). Data that fails to sync "
                "is logged in the integration error log.\n\n"
                "### General Notes\n\n"
                "All integrations use OAuth or webhook-based authentication — we do not store raw credentials "
                "for third-party systems. If an integration shows a 'disconnected' status, it typically means "
                "the OAuth token expired or the third-party permissions were revoked. Reconnect by clicking "
                "'Reconnect' and completing the OAuth flow again."
            ),
        },
        {
            "id": "doc-013",
            "title": "Webhook Configuration",
            "category": "Integrations",
            "content": (
                "## Webhook Configuration\n\n"
                "Webhooks deliver real-time event notifications to a URL of your choosing. When a specified "
                "event occurs in your workspace, a POST request is sent to your endpoint with a JSON payload "
                "describing the event.\n\n"
                "### Setup\n\n"
                "Create a webhook from Settings > Integrations > Webhooks > New Webhook. You must provide:\n\n"
                "Endpoint URL: The HTTPS URL of your receiving server. HTTP endpoints are not accepted.\n\n"
                "Events: One or more event types to subscribe to. Available events depend on your plan tier.\n\n"
                "Secret: A string used to sign webhook payloads. We recommend generating a random 32-byte string.\n\n"
                "After creating the webhook, the system sends a test ping to your endpoint. Your server must "
                "respond with HTTP 200 within 5 seconds for the test to pass.\n\n"
                "### Retry Logic\n\n"
                "If your endpoint is unavailable or returns a non-2xx response, we retry delivery with "
                "exponential backoff: 30 seconds, 5 minutes, 30 minutes, 2 hours, and finally 8 hours. After "
                "the fifth failure, the event is dropped and logged as 'failed' in the webhook delivery log. "
                "Webhooks that fail consistently are automatically disabled after 48 hours of consecutive "
                "failures. You will receive an email alert when this happens.\n\n"
                "### Signature Verification\n\n"
                "Every webhook request includes an X-Signature-SHA256 header containing an HMAC-SHA256 "
                "signature of the request body, keyed with your webhook secret. Verify this signature on "
                "every incoming request before processing the payload. To verify: compute "
                "HMAC-SHA256(raw_request_body, webhook_secret) and compare it to the value in the header "
                "using a constant-time comparison function to prevent timing attacks."
            ),
        },
        {
            "id": "doc-014",
            "title": "SSO / SAML Setup",
            "category": "Authentication",
            "content": (
                "## SSO / SAML Setup\n\n"
                "Single sign-on via SAML 2.0 is available on Business and Enterprise plans. SSO allows your "
                "team members to log in using your organization's identity provider (IdP) — Okta, Azure AD, "
                "Google Workspace, and OneLogin are all confirmed to work.\n\n"
                "### IdP Configuration\n\n"
                "In your IdP, create a new SAML application. You will need to configure:\n\n"
                "ACS URL (Assertion Consumer Service URL): Found in Settings > Security > SSO. This is where "
                "the IdP sends the SAML response after authentication.\n\n"
                "Entity ID: Also found in the SSO settings page. Use this as the SP Entity ID in your IdP.\n\n"
                "NameID format: Set to emailAddress.\n\n"
                "### Attribute Mapping\n\n"
                "The following attributes must be included in the SAML assertion: email (used as the unique "
                "identifier), firstName and lastName (used to populate the display name), and role (optional "
                "— maps to admin, member, or viewer; defaults to member if omitted).\n\n"
                "### Completing Setup\n\n"
                "In Settings > Security > SSO, paste your IdP metadata XML or enter the SSO URL and "
                "certificate manually. Save the configuration and use the 'Test SSO' button to trigger a "
                "test login. The test opens a new browser window — complete the login there. If it succeeds, "
                "SSO is live.\n\n"
                "### Troubleshooting\n\n"
                "Common issues: incorrect ACS URL (copy it directly from settings, do not type it manually), "
                "attribute names that do not match exactly (case-sensitive), and clock skew between IdP and "
                "SP servers (SAML assertions are time-sensitive; clocks must be within 5 minutes of each "
                "other)."
            ),
        },
        {
            "id": "doc-015",
            "title": "Performance Troubleshooting",
            "category": "Technical",
            "content": (
                "## Performance Troubleshooting\n\n"
                "If you are experiencing slow responses, timeouts, or degraded performance, this guide walks "
                "through the most common causes and how to diagnose them.\n\n"
                "### Slow Queries\n\n"
                "The most frequent cause of slow responses is an unoptimized query against a large dataset. "
                "Check whether the slow operation involves filtering or aggregating a large table. If so:\n\n"
                "1. Confirm that the fields you are filtering on are indexed. You can view index status from "
                "Settings > Data > Indexes.\n"
                "2. Avoid using unbounded queries (no date range or limit clause). Always scope your query to "
                "a reasonable time window.\n"
                "3. Use the query analyzer (available in the developer console) to see estimated row counts "
                "and query plan details before running expensive operations.\n\n"
                "### Timeouts\n\n"
                "API requests that take longer than 30 seconds are terminated with a 504 gateway timeout. "
                "For operations that legitimately take longer — bulk data processing, large exports — use the "
                "async endpoints. Submit the job, receive a job ID, and poll the status endpoint until the "
                "job completes.\n\n"
                "### Profiling Tips\n\n"
                "Enable query profiling from Settings > Developer > Profiling. This adds response headers "
                "with timing breakdowns for each request: time spent in the database, serialization, and "
                "network. Compare these values when a request is slow versus fast to isolate where time is "
                "being spent.\n\n"
                "### Common Patterns to Avoid\n\n"
                "N+1 query patterns: fetching a list and then making one API call per item. Use the bulk "
                "fetch endpoints instead.\n\n"
                "Synchronous retries on timeout: these pile up and worsen the problem. Always retry "
                "asynchronously with backoff.\n\n"
                "Polling at high frequency: if you need real-time updates, use webhooks rather than polling "
                "the API every few seconds."
            ),
        },
    ]

    tickets = [
        {
            "id": "ticket-001",
            "subject": "Password reset email never arrived",
            "body": "I requested a password reset 20 minutes ago and nothing has shown up in my inbox. I have checked spam and everything.",
            "resolution": "We confirmed the email was sent to the address on file. The customer's corporate email server was rejecting automated messages due to a strict DMARC policy. We asked IT to allowlist our sending domain. After the allowlist was applied, the customer received the email within minutes.",
            "category": "Authentication",
            "tags": ["password-reset", "email-delivery"],
        },
        {
            "id": "ticket-002",
            "subject": "Reset link says it has expired",
            "body": "I got the reset link in my email but when I click it, it says the link has expired. I'm clicking it right now.",
            "resolution": "The customer had requested three resets in quick succession. Only the most recently issued link is valid. We asked the customer to request one final reset and use that link without requesting additional ones. The process completed successfully.",
            "category": "Authentication",
            "tags": ["password-reset", "expired-link"],
        },
        {
            "id": "ticket-003",
            "subject": "Account locked after forgotten password attempts",
            "body": "My account got locked because I tried my password too many times. I also need to reset my password but the reset isn't working.",
            "resolution": "We cleared the account lock from the admin panel. We then walked the customer through the correct sequence: first use the lock-cleared account to request a password reset email, then follow the link. Attempting reset only after the lock was confirmed cleared resolved the issue.",
            "category": "Authentication",
            "tags": ["account-locked", "password-reset"],
        },
        {
            "id": "ticket-004",
            "subject": "Admin reset my password but it's not working on login",
            "body": "My admin said they reset my password for me but when I try the link they sent I get an error saying my password is invalid.",
            "resolution": "Admin-initiated password resets generate a one-time link that forces the user to set a new password on first use. The customer was entering the link itself as a password. We clarified that clicking the link opens a form to set a new password, and the customer completed the process successfully.",
            "category": "Authentication",
            "tags": ["password-reset", "admin-reset"],
        },
        {
            "id": "ticket-005",
            "subject": "Lost my phone and can't get past 2FA",
            "body": "I got a new phone and didn't transfer my authenticator app. Now I can't log in because it keeps asking for the 2FA code I don't have.",
            "resolution": "The customer did not have their backup codes saved. We escalated to their organization admin for identity verification. Once the admin confirmed the identity, we disabled 2FA on the account. The customer was advised to immediately re-enable 2FA on their new device and securely store backup codes.",
            "category": "Authentication",
            "tags": ["2fa", "locked-out", "backup-codes"],
        },
        {
            "id": "ticket-006",
            "subject": "2FA codes are being rejected even when they look correct",
            "body": "I'm entering the 6-digit code from my authenticator app and it says it's wrong. I double-checked the code is current and hasn't expired.",
            "resolution": "The issue was clock drift on the customer's phone. The TOTP algorithm requires the device clock to be within 30 seconds of the server. The customer's phone was 2 minutes slow. Enabling automatic time sync in the phone's date/time settings corrected the drift and codes were accepted.",
            "category": "Authentication",
            "tags": ["2fa", "totp", "clock-drift"],
        },
        {
            "id": "ticket-007",
            "subject": "How do I move my 2FA to a new authenticator app?",
            "body": "I want to switch from Google Authenticator to Authy. How do I do that without losing access to my account?",
            "resolution": "We explained that you cannot re-scan the original QR code because it is no longer shown after initial setup. The correct process is to disable 2FA (confirming with a current code), then re-enable it to get a new QR code to scan into Authy. We advised completing this while still having access to the old app.",
            "category": "Authentication",
            "tags": ["2fa", "authenticator-app", "migration"],
        },
        {
            "id": "ticket-008",
            "subject": "Organization enforces 2FA but I can't disable it",
            "body": "I want to turn off 2FA but I don't see the option in my settings. It looks like it might be greyed out.",
            "resolution": "The customer's organization admin had enforced 2FA at the organization level, preventing individual users from disabling it. Only the organization admin can lift this policy. We confirmed this was the case and provided the customer with their admin's contact information.",
            "category": "Authentication",
            "tags": ["2fa", "org-policy", "admin"],
        },
        {
            "id": "ticket-009",
            "subject": "API key is being rejected with 401 error",
            "body": "I just generated a new API key and put it in my request header but I'm getting a 401 Unauthorized response. The key looks correct.",
            "resolution": "The customer was including the API key directly in the Authorization header without the 'Bearer' prefix. The correct format is `Authorization: Bearer YOUR_API_KEY`. After updating the header format, the request succeeded.",
            "category": "API",
            "tags": ["api-key", "authentication", "401"],
        },
        {
            "id": "ticket-010",
            "subject": "Lost my API key — only last 4 digits visible",
            "body": "I forgot to copy my API key after generating it. Now I can only see the last 4 characters. Can you show me the full key?",
            "resolution": "For security reasons we cannot retrieve full API keys after creation. We guided the customer to revoke the existing key and generate a new one, emphasizing that the key must be copied and stored securely immediately after generation.",
            "category": "API",
            "tags": ["api-key", "lost-key", "security"],
        },
        {
            "id": "ticket-011",
            "subject": "How do I rotate an API key without causing downtime?",
            "body": "We need to rotate our API key for security reasons but our integration is running 24/7 and we can't have any downtime.",
            "resolution": "We described the zero-downtime rotation process: generate a new key (the old remains active), update the integration to use the new key, verify it is working in production, then revoke the old key. Both keys can be active simultaneously during the transition for as long as needed.",
            "category": "API",
            "tags": ["api-key", "key-rotation", "zero-downtime"],
        },
        {
            "id": "ticket-012",
            "subject": "OAuth token expired after 1 hour — do I need to re-authenticate?",
            "body": "Our OAuth access token expired and now our integration is broken. Do users need to log in again every hour?",
            "resolution": "Access tokens expire after one hour but users do not need to re-authenticate. The OAuth flow also issues a refresh token valid for 90 days. The integration should detect a 401, use the refresh token to get a new access token, and retry the request. We shared a code snippet demonstrating the refresh flow.",
            "category": "API",
            "tags": ["oauth", "token-refresh", "authentication"],
        },
        {
            "id": "ticket-013",
            "subject": "Getting 429 errors under normal load",
            "body": "We're hitting rate limit errors but our request volume should be well within the Growth plan limits. Something seems wrong.",
            "resolution": "The customer's service had multiple instances all using the same API key. The rate limit is applied per key, so combined traffic from all instances exceeded the per-minute limit. We recommended distributing traffic across multiple keys or implementing a centralized rate-limiting layer.",
            "category": "API",
            "tags": ["rate-limiting", "429", "multiple-instances"],
        },
        {
            "id": "ticket-014",
            "subject": "What is the right backoff strategy for 429 errors?",
            "body": "Our integration sometimes hits rate limits and just crashes. We want to implement proper retry logic.",
            "resolution": "We recommended exponential backoff with jitter: wait base * 2^attempt seconds (capped at 60s) plus small random jitter. Always read the Retry-After header first and use that value if present. After five consecutive failures, surface the error rather than retrying indefinitely.",
            "category": "API",
            "tags": ["rate-limiting", "backoff", "retry-logic"],
        },
        {
            "id": "ticket-015",
            "subject": "429 errors even after waiting the Retry-After time",
            "body": "I'm respecting the Retry-After header but I'm still getting 429s immediately when I retry. Why?",
            "resolution": "The customer was pausing only the failed request while continuing full traffic volume on all others. The rate limit had not reset because other concurrent requests were still consuming quota. We explained that the entire API key's traffic must pause for the Retry-After duration before resuming.",
            "category": "API",
            "tags": ["rate-limiting", "429", "retry-after"],
        },
        {
            "id": "ticket-016",
            "subject": "500 errors with no useful information in the response body",
            "body": "We keep getting intermittent 500 errors from the API. The response body just says 'internal error' and there's no other info.",
            "resolution": "We asked for the request_id header from the failing responses and used it to locate the server-side logs. The root cause was a downstream dependency timing out under heavy load. A backend fix resolved the errors. We reminded the customer to always log the request_id header to speed up future diagnostics.",
            "category": "API",
            "tags": ["500-error", "request-id", "debugging"],
        },
        {
            "id": "ticket-017",
            "subject": "Getting 403 even though my API key should have write access",
            "body": "I can read data fine but when I try to create a record I get a 403 Forbidden. My key should have write access.",
            "resolution": "The customer's API key had only the read:data scope. Write operations require write:data. Since scopes cannot be added to an existing key, we guided the customer to generate a new key with both read:data and write:data scopes. After updating the integration, write operations succeeded.",
            "category": "API",
            "tags": ["api-key", "scopes", "403"],
        },
        {
            "id": "ticket-018",
            "subject": "What does error code 'unprocessable' mean?",
            "body": "I'm getting an HTTP 422 with error code 'unprocessable' but the message doesn't say what's wrong.",
            "resolution": "The 422 unprocessable error means the request is syntactically valid but semantically invalid. The details field in the error response body contains field-level error messages. In this case the start_date was after the end_date. After correcting the field values, the request succeeded.",
            "category": "API",
            "tags": ["422", "error-codes", "validation"],
        },
        {
            "id": "ticket-019",
            "subject": "Where can I find my invoices?",
            "body": "I need to download invoices for our accounting department. I can't find where they are in the dashboard.",
            "resolution": "Invoices are in Settings > Billing > Invoices, accessible only to Admin or Billing Manager roles. We confirmed the customer had the correct role and walked them through the navigation. All historical invoices and PDF downloads were available from that page.",
            "category": "Billing",
            "tags": ["invoices", "billing", "pdf-download"],
        },
        {
            "id": "ticket-020",
            "subject": "Invoice shows wrong company name and address",
            "body": "Our company recently changed its legal name and our invoices still show the old name. We need this corrected.",
            "resolution": "We directed the customer to update the legal name and billing address in Settings > Billing > Details. This applies to future invoices only — past invoices are finalized and cannot be amended. The updated details appeared correctly on their next monthly invoice.",
            "category": "Billing",
            "tags": ["invoices", "billing-details", "company-name"],
        },
        {
            "id": "ticket-021",
            "subject": "VAT not being applied even though we're based in Germany",
            "body": "We're a German company and our invoices don't show any VAT. Is this correct?",
            "resolution": "The customer had a valid VAT registration number entered in their account. This correctly triggers the reverse-charge mechanism for EU B2B transactions, so we do not charge VAT and the customer reports it through their own VAT return. We explained this is correct EU practice and provided a written explanation for their accountant.",
            "category": "Billing",
            "tags": ["vat", "invoices", "eu-billing"],
        },
        {
            "id": "ticket-022",
            "subject": "Invoice for last month hasn't arrived yet",
            "body": "Our monthly invoice usually arrives on the 5th but it's now the 7th and we haven't received it.",
            "resolution": "The customer's payment method had failed on the billing date, leaving the invoice in 'open' status. The card on file had expired. We asked the customer to update their payment method and manually retry the charge. After the retry succeeded, the invoice PDF was generated and emailed within 24 hours.",
            "category": "Billing",
            "tags": ["invoices", "payment-failure", "billing-cycle"],
        },
        {
            "id": "ticket-023",
            "subject": "Can I get a refund after cancelling my annual plan?",
            "body": "We cancelled our annual subscription last week, about 3 months into the year. We expected a prorated refund but haven't heard anything.",
            "resolution": "Annual plan cancellations are eligible for a prorated refund minus a 10% early-termination fee only within the first 60 days. The customer was at 90 days, past the eligibility window. We explained the policy with reference to the Terms of Service and confirmed access would continue through the full paid annual period.",
            "category": "Billing",
            "tags": ["refund", "cancellation", "annual-plan"],
        },
        {
            "id": "ticket-024",
            "subject": "Charged twice this month",
            "body": "I see two charges on my credit card statement from you this month. I only have one subscription.",
            "resolution": "The customer had upgraded their plan mid-cycle. The proration generated an immediate charge for the plan difference for the remaining days, which combined with the regular monthly charge appeared as two charges. We explained the proration mechanic and confirmed neither charge was erroneous.",
            "category": "Billing",
            "tags": ["billing", "proration", "plan-upgrade"],
        },
        {
            "id": "ticket-025",
            "subject": "How do I request a refund for my monthly plan?",
            "body": "I signed up 3 days ago and realized this product isn't the right fit for my team. I'd like a refund.",
            "resolution": "The customer was within the 7-day refund window for new monthly subscribers and was fully eligible. We processed the full refund immediately and cancelled the subscription. The refund appears on their credit card statement within 5-10 business days.",
            "category": "Billing",
            "tags": ["refund", "cancellation", "7-day-window"],
        },
        {
            "id": "ticket-026",
            "subject": "How do I export all my data as CSV?",
            "body": "We're doing an audit and need all of our data exported in a format we can open in Excel.",
            "resolution": "We directed the customer to Settings > Data > Export and walked them through selecting CSV format and the relevant date range. We noted that nested objects are serialized as JSON strings within CSV cells, which is acceptable for most audit purposes. The export completed in minutes and a download link was emailed.",
            "category": "Data Management",
            "tags": ["data-export", "csv", "audit"],
        },
        {
            "id": "ticket-027",
            "subject": "Export download link expired before I could download it",
            "body": "I received the export email but I didn't download it right away and now the link says it's expired.",
            "resolution": "Export links expire after 7 days. We initiated a new export job for the same parameters and sent the fresh link. We recommended that for long-term data retention they set up scheduled exports to an S3 bucket, where files persist under their own retention policy.",
            "category": "Data Management",
            "tags": ["data-export", "expired-link", "download"],
        },
        {
            "id": "ticket-028",
            "subject": "Export job stuck in 'processing' for 3 hours",
            "body": "I started a data export this morning and it still says 'processing'. The status hasn't changed in 3 hours.",
            "resolution": "The export had actually completed but a bug in the status webhook caused the UI to remain stuck. The download link was already accessible via the Export History page. We directed the customer there to retrieve their file and filed an internal bug for the status display issue, which was fixed the same day.",
            "category": "Data Management",
            "tags": ["data-export", "processing-status", "bug"],
        },
        {
            "id": "ticket-029",
            "subject": "Can I schedule weekly exports to our S3 bucket?",
            "body": "We want to automatically receive a data export every week without having to manually trigger it.",
            "resolution": "Scheduled exports are supported from Settings > Data > Export > Schedule. We walked the customer through entering the weekly frequency, format, and S3 bucket details. We recommended using an IAM user with only s3:PutObject on the specific bucket path, and triggered a test write to confirm the credentials before the first scheduled run.",
            "category": "Data Management",
            "tags": ["data-export", "scheduled-exports", "s3"],
        },
        {
            "id": "ticket-030",
            "subject": "Large export split into multiple files — which order do I combine them?",
            "body": "My export came as 12 separate files. How do I know the order they go in and how to combine them?",
            "resolution": "Each filename includes a sequential part number (e.g. export_2024-01-01_part001.json). Concatenate the JSON arrays from each file in numbered order. For CSV, concatenate the files with the header row from the first file only. We shared a short Python snippet and noted that Parquet files can be read as a directory by tools like DuckDB without manual combining.",
            "category": "Data Management",
            "tags": ["data-export", "large-export", "multipart"],
        },
        {
            "id": "ticket-031",
            "subject": "Need to give a contractor view-only access",
            "body": "We have an external auditor who needs to see our data but shouldn't be able to change anything. What role do I assign?",
            "resolution": "The Viewer role is exactly what's needed — read-only access to all data and reports with no create, edit, or delete permissions. We walked the customer through Settings > Team > Invite Members, selecting the Viewer role before sending the invite.",
            "category": "Team Management",
            "tags": ["roles", "permissions", "viewer", "contractor"],
        },
        {
            "id": "ticket-032",
            "subject": "Admin accidentally removed the only other admin",
            "body": "I removed my co-admin from the team by mistake. Now I'm the only admin left. Is there anything I can do?",
            "resolution": "Since the customer was still an admin, they could re-invite the removed user from Settings > Team > Invite Members and assign them the Admin role again. The user needs to accept the new invitation. There is no undo for removal, but re-invitation is the correct recovery path.",
            "category": "Team Management",
            "tags": ["roles", "admin", "team-management"],
        },
        {
            "id": "ticket-033",
            "subject": "Member can't see the billing section",
            "body": "One of our team members needs to view invoices but they say they can't see the billing section at all.",
            "resolution": "The Billing section is restricted to Admin and Billing Manager roles. The team member had the Member role. The customer could upgrade the member to Admin or, on the Business plan, create a custom Billing Manager role with only billing permissions. The customer chose to create a custom role.",
            "category": "Team Management",
            "tags": ["roles", "permissions", "billing-access"],
        },
        {
            "id": "ticket-034",
            "subject": "How does role change affect a user who is currently logged in?",
            "body": "If I change someone's role from Admin to Member right now while they're actively using the app, what happens?",
            "resolution": "Role changes take effect immediately server-side. The affected user sees their permissions change on the next page load without needing to log out. Accessing an Admin-only feature before the page refreshes returns a 403 error, which triggers a reload that picks up the new role.",
            "category": "Team Management",
            "tags": ["roles", "permissions", "live-session"],
        },
        {
            "id": "ticket-035",
            "subject": "Invite expired before new member could accept",
            "body": "I invited a new teammate a week and a half ago and they just told me they never saw the email. The invite link they got is expired.",
            "resolution": "Team invitations expire after 7 days. We guided the customer to Settings > Team > Pending Invitations to resend the invite, which generates a fresh 7-day link. The original email had gone to the recipient's spam folder, so we also recommended they check there after the resend.",
            "category": "Team Management",
            "tags": ["invitations", "expired-invite", "team-management"],
        },
        {
            "id": "ticket-036",
            "subject": "Integration setup — what's the checklist for a new account?",
            "body": "We just signed up and I want to make sure we don't miss any important setup steps. Is there an onboarding guide?",
            "resolution": "We directed the customer to the Onboarding Checklist in the Help Center covering all 10 steps. We highlighted the most commonly missed: enabling 2FA, configuring notification preferences, and setting up SSO before inviting large numbers of users. We also offered to schedule a 30-minute onboarding call.",
            "category": "Getting Started",
            "tags": ["onboarding", "setup", "checklist"],
        },
        {
            "id": "ticket-037",
            "subject": "Invited teammates but they say they got no email",
            "body": "I sent invites to 5 teammates and none of them received the invitation email.",
            "resolution": "Delivery logs confirmed all five emails were sent successfully. The customer's organization used a strict email allowlist managed by IT that blocked all external mail by default. We provided our sending domain for the allowlist. After IT updated it, we resent all five invites and they arrived within minutes.",
            "category": "Getting Started",
            "tags": ["onboarding", "invitations", "email-delivery"],
        },
        {
            "id": "ticket-038",
            "subject": "Can't complete onboarding — email not verified",
            "body": "Some features are greyed out and I keep seeing a banner about verifying my email. I clicked the verify link but it didn't work.",
            "resolution": "The customer's verification link had expired — they had clicked it 3 days after receiving it. We resent a new verification email from the admin panel. After clicking the fresh link immediately, the gated features became available. We noted the link can also be resent by the user from Account Settings > Profile.",
            "category": "Getting Started",
            "tags": ["onboarding", "email-verification", "feature-gate"],
        },
        {
            "id": "ticket-039",
            "subject": "Confused about where to start with first integration",
            "body": "I'm new to the platform and I want to connect our database. I have the credentials but I don't know where to go.",
            "resolution": "We directed the customer to the Integrations page > Data Sources. The connection form required host, port, username, password, and database name. We walked through each field, used the Test Connection button to confirm the connection succeeded, and showed how to run a first query to verify data flow.",
            "category": "Getting Started",
            "tags": ["onboarding", "integrations", "database-connection"],
        },
        {
            "id": "ticket-040",
            "subject": "Zapier integration not showing our account events",
            "body": "I set up the Zapier integration but when I try to create a Zap I don't see any of the trigger events we need.",
            "resolution": "The Zapier integration uses polling-based triggers that check for new events approximately every 15 minutes. The events were available but had not yet appeared in the first polling cycle. After waiting one cycle, the expected triggers appeared in the Zapier UI as expected.",
            "category": "Integrations",
            "tags": ["zapier", "integrations", "trigger-events"],
        },
        {
            "id": "ticket-041",
            "subject": "Slack notifications stopped after we changed Slack workspace",
            "body": "We moved to a new Slack workspace and now we're not getting any notifications. The integration appears connected.",
            "resolution": "The OAuth token was specific to the old workspace and was invalid for the new one despite the UI showing 'connected'. We guided the customer to disconnect and reconnect the Slack integration via the OAuth flow for the new workspace, then reconfigure the channel mappings. Notifications resumed immediately.",
            "category": "Integrations",
            "tags": ["slack", "integrations", "oauth"],
        },
        {
            "id": "ticket-042",
            "subject": "Salesforce sync keeps failing for some records",
            "body": "Our Salesforce integration syncs most records fine but about 5% fail every run. The error log just says 'field mapping error'.",
            "resolution": "The failing records had a custom Salesforce field not mapped in the integration settings. We helped the customer add the custom field in Settings > Integrations > Salesforce > Field Mapping. After adding it and running a manual sync, the failure rate dropped to zero.",
            "category": "Integrations",
            "tags": ["salesforce", "integrations", "field-mapping"],
        },
        {
            "id": "ticket-043",
            "subject": "Integration shows 'disconnected' status with no explanation",
            "body": "Our third-party integration started showing 'disconnected' with no warning. We haven't changed anything.",
            "resolution": "The Salesforce admin had rotated the OAuth credentials for the integration user, invalidating the token stored in our system. We guided the customer to click 'Reconnect' to initiate a fresh OAuth flow with the updated credentials. Sync resumed automatically at the next scheduled interval.",
            "category": "Integrations",
            "tags": ["integrations", "oauth", "disconnected"],
        },
        {
            "id": "ticket-044",
            "subject": "Webhook isn't receiving events — all deliveries failing",
            "body": "I set up a webhook endpoint but none of the events are coming through. The delivery log shows failures.",
            "resolution": "The delivery log showed HTTP 403 responses from the customer's endpoint. Their server firewall blocked requests from our egress IPs. We provided the static egress IP list from the developer docs and asked them to allowlist those IPs. After the firewall update, a test ping succeeded and subsequent events delivered normally.",
            "category": "Integrations",
            "tags": ["webhook", "firewall", "delivery-failure"],
        },
        {
            "id": "ticket-045",
            "subject": "How do I verify the webhook signature in Python?",
            "body": "I'm receiving webhook events but I want to verify the signature to make sure they're coming from you. How do I do that in Python?",
            "resolution": "We provided a Python snippet: compute `hmac.new(secret.encode(), request_body, hashlib.sha256).hexdigest()` and compare it to the X-Signature-SHA256 header using `hmac.compare_digest()` to prevent timing attacks. We emphasized reading the raw body bytes before parsing, as any JSON reformatting changes the body and breaks the signature.",
            "category": "Integrations",
            "tags": ["webhook", "signature-verification", "python"],
        },
        {
            "id": "ticket-046",
            "subject": "Webhook was auto-disabled — how do I re-enable it?",
            "body": "I got an email saying my webhook was disabled. I fixed the endpoint issue. How do I turn it back on?",
            "resolution": "Webhooks disabled after 48 hours of consecutive failures can be re-enabled from Settings > Integrations > Webhooks by clicking 'Enable' on the disabled webhook. We recommended using 'Send Test Ping' first to confirm the endpoint responds before re-enabling.",
            "category": "Integrations",
            "tags": ["webhook", "auto-disabled", "re-enable"],
        },
        {
            "id": "ticket-047",
            "subject": "SSO login fails with 'audience mismatch' error",
            "body": "We set up SSO but when users try to log in through Okta they get an 'audience mismatch' error.",
            "resolution": "The Entity ID in Okta had a trailing slash that did not match our expected value. We asked the customer to copy the Entity ID directly from Settings > Security > SSO and update it in Okta without modification. After saving and retesting, SSO login worked correctly.",
            "category": "Authentication",
            "tags": ["sso", "saml", "entity-id"],
        },
        {
            "id": "ticket-048",
            "subject": "New SSO users created with wrong role",
            "body": "Users who log in via SSO are all being created as Members, but we want them to be Viewers by default.",
            "resolution": "When no role attribute is in the SAML assertion, new users default to Member. The customer could either configure the role attribute in the IdP or change the default SSO role in Settings > Security > SSO > Default User Role. They chose to update the setting in our UI, which required no IdP changes. New SSO logins after that were created as Viewers.",
            "category": "Authentication",
            "tags": ["sso", "saml", "user-roles"],
        },
        {
            "id": "ticket-049",
            "subject": "SSO setup test fails with 'clock skew' error",
            "body": "When I test the SSO configuration it immediately fails with a message about clock skew. Our IdP is Okta.",
            "resolution": "The customer's Okta server clock had drifted 7 minutes, exceeding the 5-minute SAML tolerance window. We extended our tolerance to 10 minutes temporarily and asked the customer to work with Okta support to correct the server time sync. Once corrected, the tolerance was returned to normal.",
            "category": "Authentication",
            "tags": ["sso", "saml", "clock-skew"],
        },
        {
            "id": "ticket-050",
            "subject": "SSO users can't set a local password",
            "body": "Some of our team members that we invited through SSO are asking how to set a password so they can log in without SSO if needed.",
            "resolution": "SSO-provisioned users cannot set a local password when SSO is enforced — all authentication must go through the IdP. This is by design so access revocation is centralized in the identity provider. For emergency IdP-down scenarios, the customer should review their IdP vendor's availability and fallback options.",
            "category": "Authentication",
            "tags": ["sso", "local-password", "authentication"],
        },
        {
            "id": "ticket-051",
            "subject": "API responses are extremely slow — 10+ second latency",
            "body": "Our integration has been seeing API response times of 10-15 seconds for the past two days. It was much faster before.",
            "resolution": "The customer was running unbounded queries against a table that had grown to 50 million rows. Adding a `created_after` filter and enabling server-side pagination via `limit` and `cursor` parameters reduced response times from 10+ seconds to under 300ms.",
            "category": "Technical",
            "tags": ["performance", "slow-queries", "optimization"],
        },
        {
            "id": "ticket-052",
            "subject": "Getting 504 timeout errors on large data operations",
            "body": "When I run our nightly data processing job via the API I keep getting 504 gateway timeouts. It worked fine a few months ago.",
            "resolution": "The synchronous endpoint had a 30-second limit and the dataset had grown beyond what could be processed in time. We recommended migrating to the async bulk endpoint: submit the job, receive a job ID, poll `/jobs/{id}/status` until complete. We provided a Python code example for the async pattern.",
            "category": "Technical",
            "tags": ["performance", "504-timeout", "async"],
        },
        {
            "id": "ticket-053",
            "subject": "How do I enable query profiling to see what's slow?",
            "body": "Our requests are slower than expected and I want to understand where the time is being spent.",
            "resolution": "We enabled query profiling in Settings > Developer > Profiling, which adds timing headers to every response: X-Timing-DB, X-Timing-Serialize, and X-Timing-Network. The customer's bottleneck was high serialization time. Switching to field selection using the `fields` query parameter reduced response time significantly.",
            "category": "Technical",
            "tags": ["performance", "profiling", "debugging"],
        },
        {
            "id": "ticket-054",
            "subject": "High CPU on our server correlates with API polling loop",
            "body": "We're polling the API every 2 seconds to check for new events and our server's CPU usage has spiked. Is there a better way?",
            "resolution": "We recommended replacing the polling loop with webhooks for the event types they care about. Webhooks push events within seconds of occurrence, eliminating the polling loop and its associated CPU and rate-limit costs. After switching to webhooks, CPU usage dropped substantially.",
            "category": "Technical",
            "tags": ["performance", "polling", "webhooks"],
        },
        {
            "id": "ticket-055",
            "subject": "N+1 query pattern is causing thousands of API calls",
            "body": "Our integration makes one API call to get a list of records and then one more call per record to get details. This adds up to thousands of calls.",
            "resolution": "We pointed the customer to the bulk fetch endpoint: `/records?ids=id1,id2,...` supports up to 100 IDs per call. This reduced their sync from ~4,000 API calls per cycle to ~40. We shared the API reference section on bulk operations and a batching code example.",
            "category": "Technical",
            "tags": ["performance", "n+1", "bulk-api"],
        },
        {
            "id": "ticket-056",
            "subject": "Indexes missing after data migration",
            "body": "We migrated our data to a new workspace and now queries that were fast before are extremely slow.",
            "resolution": "Indexes are not automatically carried over during data migration. We helped the customer identify which fields had been indexed in the old workspace using profiling data from their logs, then recreate those indexes in Settings > Data > Indexes in the new workspace. Query performance returned to the previous baseline.",
            "category": "Technical",
            "tags": ["performance", "indexes", "data-migration"],
        },
        {
            "id": "ticket-057",
            "subject": "What should I do first when setting up a new account?",
            "body": "We just created our company account. There are a lot of settings and I don't know what's important to do first.",
            "resolution": "We walked the customer through the priority order: verify admin email, configure SSO before bulk user invites, set the organization 2FA policy, invite team members with appropriate roles, connect the first data source, and configure notification preferences. We shared the Onboarding Checklist link in the Help Center.",
            "category": "Getting Started",
            "tags": ["onboarding", "account-setup", "getting-started"],
        },
        {
            "id": "ticket-058",
            "subject": "Can't find where to enable SSO — is it on my plan?",
            "body": "I want to set up SSO for our team but I can't find it in the security settings.",
            "resolution": "SSO/SAML is available on Business and Enterprise plans. The customer was on the Growth plan, which does not include it, so the option is hidden entirely. We explained the feature gating and provided a plan comparison. The customer decided to upgrade to Business to unlock SSO.",
            "category": "Getting Started",
            "tags": ["onboarding", "sso", "plan-features"],
        },
        {
            "id": "ticket-059",
            "subject": "Salesforce sync frequency — what's the minimum interval?",
            "body": "We need near-real-time sync with Salesforce. What's the fastest sync schedule we can configure?",
            "resolution": "The minimum scheduled sync interval is 15 minutes. For near-real-time needs, we recommended supplementing with event-driven updates: configure Salesforce Flow to call our webhook endpoint on record changes, achieving effective latency under one minute. We shared the webhook endpoint URL and auth requirements.",
            "category": "Integrations",
            "tags": ["salesforce", "sync-frequency", "webhooks"],
        },
        {
            "id": "ticket-060",
            "subject": "Webhook signature verification keeps failing intermittently",
            "body": "Most webhook events verify fine but occasionally the signature check fails even though the payload looks correct.",
            "resolution": "The customer's framework was auto-parsing the request body as JSON before the signature check ran. Any JSON reformatting changes the raw bytes, breaking the signature. We advised reading the raw request body bytes first, computing the signature on those, and then separately parsing the body. After this fix all verifications passed.",
            "category": "Integrations",
            "tags": ["webhook", "signature-verification", "body-parsing"],
        },
    ]

    return {"docs": docs, "tickets": tickets}


def main():
    output_path = Path(__file__).parent / "mock_data.json"
    data = generate()
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Wrote {len(data['docs'])} docs and {len(data['tickets'])} tickets to {output_path}")


main()
