import json
from pathlib import Path

extra_docs = [
    {
        "id": "doc-016",
        "title": "Social Login with Google and GitHub",
        "category": "Authentication",
        "content": "## Social Login with Google and GitHub\n\nYou can sign in using your Google or GitHub account instead of a username and password. On the login page, click Continue with Google or Continue with GitHub to start the OAuth flow. You will be redirected to the provider to authorize access, then returned to your workspace.\n\nOn first sign-in via social login, an account is created automatically using the email address from the provider. If an account with that email already exists, the social provider is linked to it. You can view and manage linked providers in Account Settings > Security > Connected Accounts.\n\nIf your organization uses SSO, social login is disabled and all authentication must go through the configured identity provider. Admins can control whether social login is permitted from Settings > Security > Authentication Methods.\n\nUnlinking a social provider is allowed only if you have a password or another provider configured. You cannot remove all authentication methods from your account."
    },
    {
        "id": "doc-017",
        "title": "Session Management and Timeout",
        "category": "Authentication",
        "content": "## Session Management and Timeout\n\nSessions expire after 7 days of inactivity by default. Active sessions are extended automatically on each interaction. You can view all active sessions in Account Settings > Security > Active Sessions, including device type, browser, IP address, and last activity time.\n\nTo terminate a specific session, click Revoke next to that session. To log out everywhere at once, use Revoke All Other Sessions.\n\nOrganization admins can configure a shorter session timeout from Settings > Security > Session Policy. Options range from 1 hour to 30 days. Changes apply to new sessions immediately; existing sessions are not affected until they next interact with the server.\n\nIf your account is compromised, revoking all sessions immediately invalidates every active login across all devices. Follow this with a password change and 2FA enable or reset."
    },
    {
        "id": "doc-018",
        "title": "IP Allowlisting",
        "category": "Security",
        "content": "## IP Allowlisting\n\nBusiness and Enterprise plans can restrict access to specific IP addresses or CIDR ranges. When an allowlist is active, login attempts and API requests from unlisted IPs are rejected with a 403 response before authentication is checked.\n\nConfigure the allowlist in Settings > Security > IP Allowlist. Add individual IPs or ranges in CIDR notation (e.g. 192.168.1.0/24). Before saving, confirm your current IP is included. Saving an allowlist that excludes your own IP will lock you out immediately.\n\nAllowlists apply to both the web UI and the API. If you use CI/CD pipelines that call the API, add the pipeline runner IP ranges. Major CI providers publish their IP ranges in documentation.\n\nIf you are locked out due to an incorrect allowlist, contact support from a verified email address and provide your organization name. Allowlist removal requires identity verification from an admin."
    },
    {
        "id": "doc-019",
        "title": "Pagination and Cursors",
        "category": "API",
        "content": "## Pagination and Cursors\n\nAll list endpoints are paginated. Results are not returned in a single response. Use pagination parameters to retrieve additional pages.\n\nWe use cursor-based pagination rather than offset pagination. Cursor pagination is stable: inserting or deleting records between page fetches does not cause items to be skipped or duplicated. Each response includes a next_cursor field. Pass this value as the cursor parameter in your next request to fetch the following page. When next_cursor is null, you have reached the last page.\n\nThe default page size is 20. You can increase this up to 100 using the limit parameter. Requesting more than 100 items per page returns a 400 error.\n\nFor full dataset exports, cursor pagination is slower than using the Data Export feature, which generates optimized bulk files. Use the API for interactive use cases and the export system for large one-time or scheduled data pulls."
    },
    {
        "id": "doc-020",
        "title": "Filtering and Sorting",
        "category": "API",
        "content": "## Filtering and Sorting\n\nList endpoints accept filter and sort parameters to reduce and order results server-side. Filtering client-side after fetching all records is inefficient and should be avoided.\n\nFilters are passed as query parameters. Simple equality filters use the field name directly: status=active. Range filters use operators appended to the field name: created_at_gte=2024-01-01 and created_at_lte=2024-12-31. Multiple filters are ANDed together.\n\nSorting uses the sort parameter with the field name and direction: sort=created_at:desc. Multiple sort fields are comma-separated: sort=status:asc,created_at:desc. Only indexed fields can be used for sorting; attempting to sort on an unindexed field returns a 400 error.\n\nComplex filter logic (OR conditions, nested expressions) is available via the POST /query endpoint, which accepts a filter object in the request body."
    },
    {
        "id": "doc-021",
        "title": "API Versioning and Deprecation",
        "category": "API",
        "content": "## API Versioning and Deprecation\n\nThe API is versioned via the URL path. The current stable version is v2 (e.g. /api/v2/records). Version v1 is deprecated but still operational with a sunset date of December 31, 2025.\n\nWhen a version is deprecated, all API responses include a Deprecation header with the sunset date and a Link header pointing to the migration guide. Subscribe to the developer changelog to receive advance notice of upcoming deprecations. We commit to at least six months notice before sunsetting any version.\n\nBreaking changes are never made within a version. Non-breaking changes (new optional fields, new endpoints) are added without a version bump.\n\nTo pin to a specific minor behavior, use the API-Version header to specify a date-stamped behavior snapshot. This is intended for high-stability integrations that need strict consistency across deployments."
    },
    {
        "id": "doc-022",
        "title": "Idempotency Keys",
        "category": "API",
        "content": "## Idempotency Keys\n\nMutating requests (POST, PUT, PATCH, DELETE) can be made idempotent by including an Idempotency-Key header. If a request fails mid-flight due to a network error, you can safely retry it with the same key and the operation will not be executed twice.\n\nThe key can be any string up to 255 characters. Use a UUID generated per request. Keys are stored for 24 hours. Within that window, a duplicate request with the same key returns the same response as the first attempt, without re-executing the operation.\n\nIdempotency is particularly important for payment and billing operations, user creation, and any workflow where duplicate execution would cause data inconsistency.\n\nIf two concurrent requests arrive with the same key, the second is held until the first completes, then returns the first request's result. There is no conflict or error in this case."
    },
    {
        "id": "doc-023",
        "title": "Bulk Operations",
        "category": "API",
        "content": "## Bulk Operations\n\nSeveral endpoints support bulk operations to reduce API call volume when working with many records simultaneously.\n\nBulk create accepts an array of up to 100 objects. Each object is validated independently. The response includes a results array with the outcome for each item: either the created record or an error object. Partial success is possible. The HTTP status is 207 Multi-Status when results are mixed.\n\nBulk fetch accepts a comma-separated list of IDs in the ids query parameter, up to 100 IDs. Records not found are omitted from the response without error.\n\nBulk update and bulk delete follow the same pattern. All bulk endpoints are rate-limited per request, not per record, making them significantly more efficient than individual calls for large volumes.\n\nFor operations on more than 100 records, loop through batches of 100 with a small delay between batches to avoid hitting rate limits."
    },
    {
        "id": "doc-024",
        "title": "Payment Methods",
        "category": "Billing",
        "content": "## Payment Methods\n\nWe accept credit and debit cards (Visa, Mastercard, American Express, Discover), ACH bank transfers for US-based customers, and SEPA direct debit for EU customers. Wire transfer and purchase orders are available for Enterprise plans.\n\nAdd and manage payment methods in Settings > Billing > Payment Methods. You can have multiple methods on file. The primary method is charged automatically on the billing date. Designate a backup method to handle cases where the primary fails.\n\nCard details are never stored on our servers. We use Stripe as our payment processor and store only a token referencing the card. PCI compliance is maintained by Stripe.\n\nFor ACH and SEPA, a micro-deposit verification step is required on first setup. Two small deposits are made to the account and you must confirm the amounts in the billing portal to activate the payment method. Verification typically takes one business day."
    },
    {
        "id": "doc-025",
        "title": "Failed Payments and Recovery",
        "category": "Billing",
        "content": "## Failed Payments and Recovery\n\nWhen a charge fails, we attempt recovery automatically before suspending service. The retry schedule is: 3 days after the first failure, 5 days later, then 7 days after that. If all retries fail, the subscription enters a grace period.\n\nDuring the grace period (7 days), full service access continues. Admins receive email notifications on each failed attempt. The Billing page shows a banner with the payment status and a prompt to update the payment method.\n\nIf payment is not resolved within the grace period, the account moves to restricted mode, read-only access until the outstanding balance is paid. Update the payment method and use the Retry Charge button in Settings > Billing to immediately retry.\n\nPayment failures are almost always caused by expired cards, updated card numbers, or insufficient funds. The failure reason is shown in the billing portal."
    },
    {
        "id": "doc-026",
        "title": "Discount Codes and Account Credits",
        "category": "Billing",
        "content": "## Discount Codes and Account Credits\n\nPromotion codes can be applied during initial signup or from Settings > Billing > Apply Promotion Code. Each code is single-use per organization and has an expiry date. Codes cannot be combined. Only one active promotion applies at a time.\n\nAccount credits are issued by the billing team in response to service disruptions, billing errors, or as part of negotiated agreements. Credits appear in Settings > Billing > Credits and are automatically applied to your next invoice before any card charge. Credits do not expire unless tied to a specific promotion with stated terms.\n\nProrated credits from plan downgrades accumulate as account credit rather than returning to your payment method.\n\nYou cannot convert account credits to cash or transfer them to another organization. If you cancel with a remaining credit balance, credits are forfeited unless you contact billing support before cancellation."
    },
    {
        "id": "doc-027",
        "title": "Data Import",
        "category": "Data Management",
        "content": "## Data Import\n\nData can be imported from CSV or JSON files up to 500 MB per file. Access the import tool from Settings > Data > Import. Larger datasets should be split into multiple files before importing.\n\nBefore importing, map your file columns to the system fields using the mapping UI. Required fields are flagged. The import will not proceed until all required fields are mapped. Optional fields can be left unmapped and will receive default values.\n\nThe importer validates data before committing. Validation errors are shown in a preview table with affected rows highlighted. You can download a CSV of error rows, correct them, and re-upload. A partial import (committing valid rows and skipping errors) is available as an option.\n\nLarge imports run asynchronously. You receive an email when the import completes with a summary of rows imported, skipped, and any errors encountered."
    },
    {
        "id": "doc-028",
        "title": "Data Retention Policy",
        "category": "Data Management",
        "content": "## Data Retention Policy\n\nActive subscription data is retained indefinitely while your subscription is active. After cancellation, data is held for 90 days in a read-only state, then permanently deleted.\n\nSoft-deleted records (deleted via the UI or API) are retained for 30 days and can be restored within that window. After 30 days, soft-deleted records are permanently removed. Permanent deletion cannot be undone.\n\nAudit logs are retained for 12 months on Business plans and 36 months on Enterprise plans. Starter and Growth plans retain 30 days of audit logs.\n\nCustom retention schedules are available on Enterprise plans. You can configure per-object-type retention periods from 30 days to 7 years to meet compliance requirements. Custom schedules apply to new records from the point of configuration."
    },
    {
        "id": "doc-029",
        "title": "GDPR and Data Deletion Requests",
        "category": "Data Management",
        "content": "## GDPR and Data Deletion Requests\n\nFor EU-based organizations and any organization processing personal data of EU residents, we act as a data processor. Our Data Processing Agreement (DPA) is available for signature from Settings > Legal > DPA.\n\nTo fulfill a data subject access request (DSAR), export all data associated with a specific user from Settings > Data > Export, filtering by user ID.\n\nTo fulfill a right-to-erasure request, use the API endpoint DELETE /users/{id}/personal-data. This anonymizes all personal identifiers (name, email, IP addresses) in records created by that user while preserving the records for audit purposes.\n\nWe maintain a sub-processors list at our Trust Center. Significant changes to sub-processors are communicated 30 days in advance by email to DPA signatories."
    },
    {
        "id": "doc-030",
        "title": "Storage Limits",
        "category": "Data Management",
        "content": "## Storage Limits\n\nStorage is measured in terms of records and file attachments. Record counts vary by plan:\n\n- Starter: 100,000 records, 5 GB file storage\n- Growth: 1,000,000 records, 50 GB file storage\n- Business: 10,000,000 records, 500 GB file storage\n- Enterprise: Custom, negotiated\n\nStorage usage is visible in Settings > Usage. An alert is sent at 80% and 95% capacity. At 100%, write operations are blocked until capacity is increased.\n\nFiles are deduplicated: uploading the same file twice does not double the storage consumed.\n\nArchived records count toward storage. If you need to free up storage without deleting data, export records and delete them from the system. Exports can be re-imported later if the data is needed again."
    },
    {
        "id": "doc-031",
        "title": "SCIM Provisioning",
        "category": "Team Management",
        "content": "## SCIM Provisioning\n\nSCIM (System for Cross-domain Identity Management) automates user provisioning and deprovisioning. When a user is added to the application in your IdP, they are automatically created in your workspace. When removed from the IdP, they are deactivated.\n\nSCIM 2.0 is supported and available on Enterprise plans. To enable it, go to Settings > Security > SCIM and generate a SCIM bearer token. In your IdP, configure a new SCIM integration using our SCIM base URL and the token.\n\nSupported SCIM operations: create user, update user attributes, deactivate user, and reactivate user. Group sync is supported. Role assignment via SCIM uses the role attribute: admin, member, or viewer.\n\nSCIM deactivation sets the user to inactive but does not delete their data. To permanently delete user data, use the GDPR data deletion endpoint after deactivating."
    },
    {
        "id": "doc-032",
        "title": "Audit Logs",
        "category": "Security",
        "content": "## Audit Logs\n\nAll security-relevant actions are logged in the audit trail: logins, permission changes, data exports, API key creation and revocation, billing changes, and admin actions. Audit logs cannot be modified or deleted.\n\nAccess audit logs from Settings > Security > Audit Log. Filter by user, action type, date range, or IP address. Each log entry shows the timestamp, actor, action, target resource, IP address, and outcome.\n\nAudit logs can be exported as CSV or streamed to an external SIEM via webhook. Configure streaming in Settings > Security > Audit Log > Export.\n\nRetention periods: 30 days (Starter/Growth), 12 months (Business), 36 months (Enterprise). Log entries older than the retention limit are permanently deleted.\n\nFailed login attempts are logged regardless of whether an account exists for the email, to prevent user enumeration via audit log analysis."
    },
    {
        "id": "doc-033",
        "title": "Security Overview",
        "category": "Security",
        "content": "## Security Overview\n\nWe maintain SOC 2 Type II certification, reviewed annually. The current report is available under NDA from Settings > Legal > Security Documents.\n\nData is encrypted at rest using AES-256 and in transit using TLS 1.2 minimum. Database backups are encrypted using the same standard. Encryption keys are managed via a dedicated KMS and rotated annually.\n\nOur infrastructure runs on AWS in multiple availability zones. We publish real-time service status and historical uptime at our status page. Incidents are posted within 15 minutes of detection.\n\nVulnerability disclosures can be submitted via our security contact in Settings > Legal > Security. We follow a 90-day responsible disclosure policy. Confirmed vulnerabilities with CVSS score above 7.0 are remediated and disclosed within 90 days.\n\nPenetration tests are conducted annually by an independent firm. Executive summaries are available to Enterprise customers upon request."
    },
    {
        "id": "doc-034",
        "title": "Guest Access",
        "category": "Team Management",
        "content": "## Guest Access\n\nGuest users are external collaborators with access to specific projects or resources, rather than the full workspace. Guests do not consume a seat on your plan.\n\nInvite a guest from the sharing settings of a specific project: click Share > Invite Guest and enter their email address. Guests receive an email invitation. They create a guest account or log in with Google.\n\nGuests can view and comment on the resources shared with them. They cannot access other parts of the workspace, view team member lists, or see billing information. Guest permissions are fixed and cannot be elevated.\n\nGuest access can be revoked at any time from the resource's sharing settings or from Settings > Team > Guests. When access is revoked, the guest's session is terminated immediately."
    },
    {
        "id": "doc-035",
        "title": "GitHub Integration",
        "category": "Integrations",
        "content": "## GitHub Integration\n\nThe GitHub integration connects your repositories to your workspace. Once installed, you can link records to pull requests and commits, trigger workflows on GitHub events, and surface deployment status.\n\nInstall from Settings > Integrations > GitHub. You will be redirected to GitHub to authorize and select which repositories to grant access to. Access can be modified later from your GitHub organization settings.\n\nLinked pull requests display status (open, merged, closed) and check results inline. When a PR is merged, linked records can be automatically transitioned to a specified status.\n\nThe integration uses GitHub's webhook system to receive events in real time. If events stop arriving, check the webhook delivery history in your GitHub repository settings and verify the endpoint is receiving payloads."
    },
    {
        "id": "doc-036",
        "title": "Jira Integration",
        "category": "Integrations",
        "content": "## Jira Integration\n\nThe Jira integration enables bidirectional sync between Jira issues and your workspace records. Changes to a Jira issue update the linked record, and vice versa.\n\nInstall from Settings > Integrations > Jira. Enter your Jira domain, create a dedicated Jira service account with API access, and provide the API token. Select which Jira projects to sync and configure field mappings.\n\nSync is event-driven: changes trigger an immediate update on the linked side rather than waiting for a scheduled sync. For changes made while the integration is offline, a catch-up sync runs on reconnection.\n\nConflict resolution: if both sides change the same field simultaneously, the most recent change wins. Conflicts are logged in the integration error log for review."
    },
    {
        "id": "doc-037",
        "title": "Google Workspace Integration",
        "category": "Integrations",
        "content": "## Google Workspace Integration\n\nThe Google Workspace integration enables single sign-on via Google, calendar syncing, and file attachment from Google Drive.\n\nSSO via Google is enabled by default and requires no additional configuration. For organizations that want to enforce this and block other login methods, configure it in Settings > Security > Authentication Methods.\n\nGoogle Calendar sync is optional and must be configured per user from Account Settings > Integrations > Google Calendar.\n\nGoogle Drive attachments: from any record, click Attach > From Google Drive to attach a file without uploading a copy. The attached file is accessed from Google Drive directly, subject to the user's Drive permissions, so collaborators need Drive access to view it."
    },
    {
        "id": "doc-038",
        "title": "HubSpot Integration",
        "category": "Integrations",
        "content": "## HubSpot Integration\n\nThe HubSpot integration syncs contacts, companies, and deals between HubSpot and your workspace. This is useful for teams that use both systems and need a unified view of customer data.\n\nInstall from Settings > Integrations > HubSpot. Connect using a HubSpot admin account. During setup, select which HubSpot object types to sync and configure the field mapping for each.\n\nSync direction is configurable: one-way from HubSpot to your workspace, one-way the other direction, or bidirectional. Most teams start with HubSpot as the system of record.\n\nHubSpot CRM activities (calls, emails, notes) can optionally be synced as a timeline view on linked records. New activities appear within 5 minutes, limited by HubSpot's webhook delivery latency."
    },
    {
        "id": "doc-039",
        "title": "Notifications and Alerts",
        "category": "Getting Started",
        "content": "## Notifications and Alerts\n\nNotifications inform you of activity relevant to your work. Configure notification preferences in Account Settings > Notifications. Each notification type can be enabled for in-app delivery, email, or both.\n\nIn-app notifications appear in the notification bell in the top navigation. Clicking a notification navigates to the relevant record or event.\n\nEmail notifications are batched by default. Choose between immediate delivery, hourly digest, or daily digest per notification type. High-priority alerts (security events, payment failures) always deliver immediately.\n\nOrganization-wide alerts are sent to all admins. You cannot opt out of organization-level alerts if you have the Admin role.\n\nSlack notification routing is available via the Slack integration. Route specific notification types to specific channels for team-wide visibility."
    },
    {
        "id": "doc-040",
        "title": "File Upload Limits",
        "category": "Technical",
        "content": "## File Upload Limits\n\nThe maximum single file size for attachments is 100 MB. Files larger than this must be split before uploading or stored externally and linked rather than attached.\n\nSupported file types: images (PNG, JPG, GIF, WebP, SVG), documents (PDF, DOCX, XLSX, PPTX, TXT), archives (ZIP, TAR.GZ up to 50 MB), and code files (any text-based format). Executable files (EXE, DMG, BAT, SH) are rejected for security reasons.\n\nUploads use multipart form upload for files over 5 MB to improve reliability on slow connections.\n\nFiles are virus-scanned on upload. Infected files are rejected and the upload attempt is logged.\n\nFile storage counts toward your plan storage limit. Deleting an attachment removes it from storage within 24 hours."
    },
    {
        "id": "doc-041",
        "title": "Browser Compatibility",
        "category": "Technical",
        "content": "## Browser Compatibility\n\nWe support the two most recent major versions of Chrome, Firefox, Safari, and Edge. Older browser versions may work but are not tested.\n\nInternet Explorer is not supported.\n\nJavaScript must be enabled. Browser extensions that aggressively block scripts can interfere with specific features. If you encounter unexplained failures, test in a private window with extensions disabled.\n\nCookies are required for session management. Third-party cookies are not used. Some features require pop-ups to be allowed from our domain.\n\nIf you encounter display issues, a hard refresh (Cmd+Shift+R on Mac, Ctrl+Shift+R on Windows) clears cached JS and CSS and is the first troubleshooting step."
    },
    {
        "id": "doc-042",
        "title": "Network Requirements and Firewall Setup",
        "category": "Technical",
        "content": "## Network Requirements and Firewall Setup\n\nThe web application and API require HTTPS access on port 443 to our domains. No other ports are required. Our domains and static IP ranges are published in the developer documentation.\n\nFor webhook delivery, your endpoint must be reachable from our egress IPs on port 443. Our egress IP list is static and published at our Trust Center. Subscribe to the IP change notification list for advance notice of any additions.\n\nIf your organization uses a proxy server, configure your browser and API clients to route requests through it. The API supports standard HTTP_PROXY and HTTPS_PROXY environment variables.\n\nWebSocket connections (used by the real-time notification system) must not be terminated by the proxy. Allow upgrade headers to pass through."
    },
    {
        "id": "doc-043",
        "title": "Report Building",
        "category": "Analytics",
        "content": "## Report Building\n\nReports display aggregated data from your workspace. Create a report from Analytics > Reports > New Report. Choose a data source, add metrics (aggregate functions like count, sum, average), and optionally break down results by a dimension.\n\nFilters scope the report to a subset of data. Filters can be set at the report level or as interactive controls that viewers can adjust.\n\nReports are snapshots unless configured to refresh. Set the refresh schedule from the report settings: real-time, hourly, daily, or manual.\n\nReports can be shared with specific team members, shared as a view-only link, or embedded in external tools using the embed code from the Share menu."
    },
    {
        "id": "doc-044",
        "title": "Dashboard Creation",
        "category": "Analytics",
        "content": "## Dashboard Creation\n\nDashboards are collections of reports and metrics displayed on a single page. Create a dashboard from Analytics > Dashboards > New Dashboard.\n\nAdd widgets by clicking Add Widget. Widgets can be existing reports, raw metric tiles, or text blocks. Drag widgets to rearrange them. Resize by dragging the bottom-right corner.\n\nDashboard-level date filters apply to all widgets that use a date dimension, overriding widget-level date settings. This lets viewers compare the same date range across all panels simultaneously.\n\nSet a default dashboard for the organization from Settings > Analytics > Default Dashboard. This is the first page members see when navigating to Analytics."
    },
    {
        "id": "doc-045",
        "title": "Scheduled Reports",
        "category": "Analytics",
        "content": "## Scheduled Reports\n\nReports can be delivered on a schedule via email or Slack. Open a report, click Schedule, and configure the frequency (daily, weekly, monthly), recipients, and delivery format (email with embedded screenshot, PDF attachment, or CSV data).\n\nScheduled reports run at the time of delivery and reflect current data. The same report can have multiple schedules with different recipients and frequencies.\n\nIf a scheduled report fails to generate, the delivery is skipped and a failure notification is sent to the report owner. The next scheduled delivery runs at the normal time.\n\nReport recipients do not need a workspace account to receive email deliveries. For Slack, the channel must exist and the Slack integration must be active."
    },
    {
        "id": "doc-046",
        "title": "Custom Metrics",
        "category": "Analytics",
        "content": "## Custom Metrics\n\nCustom metrics let you define computed values that appear alongside standard metrics in reports and dashboards. Create a custom metric from Analytics > Metrics > New Metric.\n\nMetrics are defined using a formula syntax that supports arithmetic operators, standard aggregate functions (sum, count, average, min, max, distinct_count), and conditional expressions.\n\nExamples of useful custom metrics:\n- Conversion rate: completed / created * 100\n- Average resolution time: sum(resolution_time_hours) / count(id)\n- SLA compliance: percentage of tickets resolved within 24 hours\n\nCustom metrics can be used as columns in any report using the matching data source. Once created, they cannot be deleted if referenced in a saved report. Remove references first.\n\nMetric calculations run on the server. Complex formulas on large datasets may be slow. Use the preview mode to test performance before saving."
    },
    {
        "id": "doc-047",
        "title": "Mobile App Support",
        "category": "Technical",
        "content": "## Mobile App Support\n\nNative iOS and Android apps are available. Download from the App Store (iOS 15+) and Google Play (Android 8+). The apps provide access to core functionality: viewing records, receiving notifications, approving requests, and leaving comments. Complex configuration and bulk operations are best done from the web app.\n\nPush notifications are enabled by default on first install. Configure which notifications trigger push alerts from the notification settings within the app.\n\nThe mobile app uses the same API as external integrations. API rate limits apply per account, not per device.\n\nIf the mobile app is not loading data, check that Background App Refresh is enabled for the app in your device settings. Some corporate MDM policies restrict this."
    },
    {
        "id": "doc-048",
        "title": "Search Functionality",
        "category": "Technical",
        "content": "## Search Functionality\n\nGlobal search is available from the top navigation bar and finds records, users, and settings pages across your workspace. Results are ranked by relevance and recency.\n\nSearch indexes record titles, descriptions, and all text-type fields. Attachments and file contents are not indexed. Boolean operators are supported: AND, OR, NOT (must be uppercase).\n\nSearch results are filtered by the permissions of the searching user. Searches always reflect the current state of the workspace.\n\nFor programmatic search, use the search API endpoint (GET /search?q=) which returns the same results with pagination support.\n\nSearch indexing is near-real-time. New or updated records are searchable within 30 seconds. Bulk imports may take a few minutes to fully index."
    },
    {
        "id": "doc-049",
        "title": "Annual vs Monthly Plans",
        "category": "Billing",
        "content": "## Annual vs Monthly Plans\n\nBoth billing frequencies provide identical features and support. The choice is purely financial and contractual.\n\nAnnual plans are discounted at approximately 20% compared to 12 months of monthly billing. The full year is billed upfront on the subscription anniversary. Annual plans are eligible for a prorated refund within the first 60 days minus a 10% early-termination fee.\n\nMonthly plans offer flexibility: cancel anytime with no long-term commitment. Monthly subscribers are eligible for a full refund within 7 days of initial signup only.\n\nSwitching from monthly to annual takes effect immediately. Switching from annual to monthly takes effect at the next annual renewal date. You cannot downgrade to monthly mid-year.\n\nLarge organizations can negotiate custom annual pricing with a multi-year commitment."
    },
    {
        "id": "doc-050",
        "title": "Developer Quickstart",
        "category": "Getting Started",
        "content": "## Developer Quickstart\n\nThis guide gets you from zero to your first API call in under 10 minutes.\n\n1. Create an account and verify your email.\n2. Go to Developer Settings > API Keys > New Key. Name it, select the scopes you need, and save. Copy the key immediately.\n3. Make your first request: include the key as Authorization: Bearer YOUR_API_KEY in the header.\n4. Install the official client library for your language. Libraries are available for Python, Node.js, Ruby, Go, and Java.\n5. Use the interactive API explorer at the developer portal to browse endpoints and test requests without writing code.\n\nCommon first mistakes: forgetting the Bearer prefix in the Authorization header, using deprecated v1 endpoints, and not handling 429 rate-limit responses with backoff."
    },
    {
        "id": "doc-051",
        "title": "Migration Guide",
        "category": "Getting Started",
        "content": "## Migration Guide\n\nMigrating from another tool involves three steps: exporting your data, importing it into your new workspace, and reconfiguring your integrations.\n\nStep 1: Export your data from the old tool in CSV or JSON format.\n\nStep 2: Use Settings > Data > Import. Map the fields from your export file to the system fields. Run a test import with a small sample first to verify mappings.\n\nStep 3: Reconnect any third-party integrations. API keys and OAuth tokens from the old workspace do not carry over.\n\nCutover planning: run the old and new systems in parallel for at least one week before switching. Verify reports match between systems and communicate the cutover date to your team in advance.\n\nAfter migration, archive the old workspace rather than deleting it immediately. Keep it accessible for 30 days in case questions arise about historical data."
    },
    {
        "id": "doc-052",
        "title": "Admin Guide",
        "category": "Getting Started",
        "content": "## Admin Guide\n\nAs an organization admin, you are responsible for configuring the workspace and maintaining security.\n\nUser management: invite members with appropriate roles, set the organization 2FA policy, configure session timeout, and set up SSO. Review the pending invitations list weekly.\n\nBilling: keep payment information current, monitor seat usage against plan limits, and review invoices monthly. Set up a backup payment method to prevent service interruption.\n\nIntegrations: regularly review connected integrations and revoke any no longer needed. Check the integration error log monthly. Rotate API keys for critical integrations quarterly.\n\nSecurity monitoring: review the audit log weekly for unusual activity. Configure audit log streaming to your SIEM if your organization has one.\n\nData hygiene: deactivate users promptly when they leave the organization. Set up scheduled data exports to ensure backup copies exist outside the workspace."
    },
    {
        "id": "doc-053",
        "title": "Real-Time Collaboration",
        "category": "Technical",
        "content": "## Real-Time Collaboration\n\nMultiple users can view and edit the same record simultaneously. Real-time presence shows who is currently viewing or editing a record via avatar indicators.\n\nConflict handling: if two users edit the same field simultaneously, the last write wins. A toast notification informs the user whose change was overwritten. For frequent simultaneous editing, consider using the record lock feature.\n\nComments support @mentions to notify specific team members. Mentioned users receive an in-app notification and email.\n\nActivity history on each record shows all changes with timestamps and authors. This log is immutable and available even after a user leaves the organization.\n\nReal-time sync uses WebSocket connections. If your network blocks WebSockets, the app falls back to long polling, which is functional but has higher latency."
    },
    {
        "id": "doc-054",
        "title": "Automation Rules",
        "category": "Technical",
        "content": "## Automation Rules\n\nAutomation rules trigger actions automatically when defined conditions are met. Create rules from Settings > Automation > New Rule.\n\nEach rule has a trigger (the event that starts the automation), optional conditions (filters that must match), and one or more actions (what happens when triggered).\n\nTriggers: record created, record updated, field value changed, date reached, webhook received.\n\nActions: update a field, send a notification, create a record, call an external webhook, send an email, or assign to a user.\n\nRules run in listed order. If a rule action changes a field that triggers another rule, that second rule also fires. Be careful with loops: two rules that trigger each other will run until a loop-detection limit is reached and both are paused.\n\nEach rule shows a run history with the trigger event, conditions evaluated, and actions taken."
    },
    {
        "id": "doc-055",
        "title": "Custom Fields",
        "category": "Technical",
        "content": "## Custom Fields\n\nCustom fields extend records with data specific to your workflow. Admins create custom fields from Settings > Fields > New Field.\n\nSupported field types: text (single line), long text, number, currency, percentage, date, datetime, checkbox, select (single choice), multi-select, user reference, record link, and URL.\n\nEach field can be marked required, unique, or indexed. Indexed fields enable filtering and sorting but add storage overhead.\n\nField visibility can be controlled per view: show a field in a table view without showing it in the form view.\n\nDeleting a field permanently removes all data in that field across all records. The deletion requires a confirmation step and cannot be undone. If you need to remove a field from views without deleting its data, hide it instead."
    },
    {
        "id": "doc-056",
        "title": "Workflow Templates",
        "category": "Getting Started",
        "content": "## Workflow Templates\n\nTemplates are pre-configured workspace setups for common use cases. Apply a template when creating a new workspace or in an existing workspace from Settings > Templates.\n\nAvailable templates: Software Engineering (sprints, bugs, deployments), Customer Support (tickets, escalations, SLAs), Project Management (milestones, tasks, dependencies), Sales Pipeline (leads, opportunities, forecast), and HR Onboarding (tasks, documents, approvals).\n\nApplying a template creates the field structure, views, and automation rules for that workflow. Existing data is not affected. You can customize everything after applying.\n\nCreate your own template from any workspace configuration via Settings > Templates > Save as Template. Custom templates can be shared across workspaces in the same organization.\n\nTemplates do not include data records, only configuration. To clone a workspace including its data, use the export and import flow."
    },
    {
        "id": "doc-057",
        "title": "Email Integration",
        "category": "Integrations",
        "content": "## Email Integration\n\nThe email integration lets you create records by sending an email to a special address, and optionally reply to comments via email.\n\nEach workspace has a unique inbound email address found in Settings > Integrations > Email. Emails sent to this address are parsed into records: the subject becomes the record title, the email body becomes the description, and attachments are added as file attachments.\n\nReply via email: when a team member comments on a record, the notification email sent to watchers includes a reply address. Replying to that email adds the reply as a comment on the record.\n\nTo disable email-to-record creation if the inbound address is misused, rotate the inbound address from Settings > Integrations > Email > Rotate Address. The old address stops working immediately."
    },
    {
        "id": "doc-058",
        "title": "Calendar View",
        "category": "Technical",
        "content": "## Calendar View\n\nCalendar view displays records on a calendar based on a date or datetime field. Switch to calendar view from the view selector in any table.\n\nConfigure calendar view by selecting which date field to use for positioning and optionally a second field for event duration. Records without a value in the selected date field do not appear on the calendar.\n\nDrag records on the calendar to change their date. Records can be created directly on the calendar by clicking a date.\n\nGroup by a field (e.g. assignee, status) to show color-coded records. This is useful for seeing team workload across a week or month at a glance.\n\nCalendar view does not replace Google or Outlook calendar integrations. To surface records in an external calendar, use the calendar feed URL from the view settings, which generates an iCal-compatible subscription link."
    },
    {
        "id": "doc-059",
        "title": "Kanban View",
        "category": "Technical",
        "content": "## Kanban View\n\nKanban view organizes records as cards in columns. Each column represents a value of a select or status field. Switch to kanban view from the view selector.\n\nConfigure kanban by choosing the grouping field. Columns appear in the order the field options are defined. Optionally set a WIP limit: a visual indicator appears when the limit is exceeded.\n\nDrag cards between columns to update the grouping field value. This triggers any automation rules that watch that field. Drag within a column to reorder cards.\n\nFilter and sort apply inside kanban view. Filtering reduces which cards are visible; sorting controls the order within each column.\n\nCards show a configurable set of fields below the title. Edit the card layout in view settings to show fields most relevant to your workflow."
    },
    {
        "id": "doc-060",
        "title": "Gantt View",
        "category": "Technical",
        "content": "## Gantt View\n\nGantt view shows records as horizontal bars on a timeline, positioned by start and end date fields. Available on Growth plans and above.\n\nConfigure gantt by selecting the start date field, end date field, and optionally a dependency field. Records without both date fields set appear in an unscheduled sidebar.\n\nDependency lines connect records where one must complete before another begins. If a dependency creates a conflict, it is highlighted in red and you can choose to auto-adjust dates.\n\nBaseline view: save the current schedule as a baseline and compare it against actuals as dates change. The baseline appears as a thin bar behind the current bar.\n\nZoom controls adjust the timeline from day-level to year-level. Export the gantt view as PNG or PDF from the view menu for sharing with stakeholders."
    },
    {
        "id": "doc-061",
        "title": "Access Tokens for Integrations",
        "category": "API",
        "content": "## Access Tokens for Integrations\n\nWhen building integrations that access data on behalf of specific users rather than the organization as a whole, use OAuth 2.0 access tokens rather than organization-level API keys.\n\nAccess tokens are scoped to the permissions of the user who granted them. If that user is a Viewer, the token cannot perform write operations regardless of what the integration requests.\n\nTokens can be inspected using the token info endpoint: GET /api/v2/token/info. This returns the token owner, granted scopes, and expiry time.\n\nManage all active OAuth tokens from Account Settings > Security > Authorized Applications. Revoking a token here invalidates it immediately. Users should periodically review this list and revoke access for any applications they no longer use."
    },
    {
        "id": "doc-062",
        "title": "Keyboard Shortcuts",
        "category": "Technical",
        "content": "## Keyboard Shortcuts\n\nKeyboard shortcuts speed up navigation and common actions. View the full list by pressing ? in any view.\n\nGlobal shortcuts:\n- Cmd/Ctrl + K: Open command palette\n- G then H: Go to Home\n- G then I: Go to Inbox\n- G then A: Go to Analytics\n- Escape: Close modal or panel\n\nRecord shortcuts:\n- E: Edit mode\n- Cmd/Ctrl + S: Save changes\n- C: Open comment box\n- Cmd/Ctrl + Shift + D: Duplicate record\n\nTable view shortcuts:\n- Arrow keys: Navigate cells\n- Enter: Edit selected cell\n- Cmd/Ctrl + A: Select all records\n\nShortcuts can be customized from Account Settings > Preferences > Keyboard Shortcuts."
    },
    {
        "id": "doc-063",
        "title": "Dark Mode and Display Preferences",
        "category": "Technical",
        "content": "## Dark Mode and Display Preferences\n\nDisplay preferences are configured per user from Account Settings > Preferences > Appearance.\n\nTheme options: Light, Dark, and System (follows your operating system setting). Changes apply immediately without a page refresh. The selected theme is synced across all browsers and devices.\n\nDensity settings control the amount of information shown per row in table views: comfortable (more padding), compact (denser rows), and ultra-compact (minimal padding, maximum data density).\n\nFont size: adjust the base font size from 14px to 18px. This scales all text proportionally.\n\nLanguage: the interface is available in English, French, German, Spanish, Japanese, and Portuguese. The language setting affects UI elements only."
    },
    {
        "id": "doc-064",
        "title": "Commenting and Mentions",
        "category": "Technical",
        "content": "## Commenting and Mentions\n\nComments can be added to any record from the activity panel on the right side. Press C as a keyboard shortcut to open the comment box.\n\nComments support markdown formatting: bold, italic, inline code, and code blocks. URLs are auto-linked. Images can be pasted directly into the comment box.\n\nMention a team member using @name to send them a notification. The mention autocomplete opens after typing @ and filters as you type.\n\nComments can be edited or deleted by the author within 30 minutes of posting. After that window, comments are permanent. Admins can delete any comment at any time for moderation purposes.\n\nThread replies keep discussions organized. Reply to a specific comment to create a nested thread. Unresolved threads are tracked at the top of the activity panel."
    },
    {
        "id": "doc-065",
        "title": "Record Templates",
        "category": "Technical",
        "content": "## Record Templates\n\nRecord templates pre-fill fields and descriptions for new records. They are useful for recurring workflows like bug reports, feature requests, or onboarding tasks where every new record should have the same starting structure.\n\nCreate a record template from Settings > Templates > Record Templates > New Template, or by opening an existing record and selecting Save as Template from the record menu.\n\nTemplates can pre-fill: title, description (with structured markdown content), any field value, default assignee, and initial status.\n\nWhen creating a new record, a template picker appears. Templates do not lock fields. Everything can be edited after applying.\n\nTemplates can be shared with the whole organization or scoped to specific teams. Pin frequently used templates to the top of the template picker."
    },
    {
        "id": "doc-066",
        "title": "Duplicate Detection",
        "category": "Data Management",
        "content": "## Duplicate Detection\n\nThe platform flags potential duplicate records to help maintain data quality. Duplicates are detected based on matching field values in key fields configurable per record type from Settings > Data Quality.\n\nWhen creating a record, if potential duplicates are found, a sidebar panel shows the matching records with similarity scores. You can proceed with a new record, open the existing one, or merge.\n\nBulk duplicate detection runs as a scheduled job and generates a report in Settings > Data Quality > Duplicates.\n\nMerging two records: select a primary record (its ID is preserved) and a secondary. All data, comments, attachments, and activity history from the secondary are merged into the primary. The secondary is then deleted.\n\nDuplicate detection can be disabled for specific record types from Settings > Data Quality if false positives are frequent."
    },
    {
        "id": "doc-067",
        "title": "Approvals and Review Flows",
        "category": "Technical",
        "content": "## Approvals and Review Flows\n\nApproval flows add a structured review step before a record can advance to a certain status. Configure approval rules from Settings > Automation > Approvals.\n\nEach approval rule specifies a trigger condition, required approvers (specific users, any user in a role, or a quorum), and the action on approval or rejection.\n\nWhen an approval is triggered, approvers receive a notification with options to approve or reject directly from the notification. Approvers can add a comment explaining their decision.\n\nIf multiple approvers are required, the approval completes when the quorum is reached. If any required approver rejects, the approval fails immediately.\n\nApproval requests time out after a configurable period (1-30 days). On timeout, the approval can be set to auto-approve, auto-reject, or escalate to a fallback approver."
    },
    {
        "id": "doc-068",
        "title": "Time Tracking",
        "category": "Technical",
        "content": "## Time Tracking\n\nTime tracking lets team members log time spent on records. Enable the feature per record type from Settings > Fields > Enable Time Tracking.\n\nLog time from a record by clicking Log Time. Enter hours and minutes, select the date, and optionally add a description. Multiple entries can be logged per record by different users.\n\nThe timer feature allows real-time tracking: click Start Timer on a record, work, then click Stop. The elapsed time is automatically entered as a time log entry. Only one timer can be active at a time per user.\n\nTime summary on a record shows total logged hours, a breakdown by user, and a log of all entries.\n\nTime tracking reports in Analytics show time logged by user, record type, or project. Useful for client billing, identifying workflow bottlenecks, or tracking sprint velocity."
    },
    {
        "id": "doc-069",
        "title": "Dependencies and Relationships",
        "category": "Technical",
        "content": "## Dependencies and Relationships\n\nRecords can be linked to other records through dependency and relationship fields. A linked record field stores a live reference that updates if the linked record's data changes.\n\nDependencies (blocks/is blocked by): indicate sequencing. One record cannot be completed until another is done. Dependency relationships are visible in Gantt view as connecting lines.\n\nRelationships (parent/child): hierarchical grouping where a parent record contains child records. A parent record shows a rollup of child record status.\n\nGeneral links: non-typed links between any two records for reference. Useful for linking a bug to the feature request it was reported from.\n\nAll relationships are bidirectional. If A links to B, B also shows a link to A."
    },
    {
        "id": "doc-070",
        "title": "Access Control for Views",
        "category": "Team Management",
        "content": "## Access Control for Views\n\nViews can be personal (visible only to the creator) or shared (visible to the team or specific members). A single table can have many views with different filters, sorts, and field configurations.\n\nPersonal views are created by default. To share a view, open the view menu and click Share View. Choose whether to share with the entire workspace or specific members.\n\nEditing a shared view: by default, anyone with access can edit the view configuration. Lock a view to prevent changes. Only the creator or an admin can edit a locked view.\n\nDefault view: set a default view that all new members see when they first open a record type.\n\nView permissions do not affect underlying data permissions. A Viewer role user can see all records in a shared view but cannot edit them."
    },
    {
        "id": "doc-071",
        "title": "Rollups and Lookups",
        "category": "Technical",
        "content": "## Rollups and Lookups\n\nRollup fields aggregate values from linked child records into the parent record. Lookup fields pull a specific field value from a linked record into the current record.\n\nTo create a rollup field: add a new field, choose type Rollup, select the linked record field to roll up from, and choose the aggregation function (sum, count, average, min, max, percent complete). The rollup value updates automatically when linked records change.\n\nCommon rollup uses: counting open subtasks on an epic, summing logged hours across a project, calculating average resolution time.\n\nLookup fields display a value from a linked record without aggregation. Useful for showing the assignee of a parent record on each child task.\n\nBoth rollups and lookups are read-only. The values are computed at query time and do not consume additional storage."
    },
    {
        "id": "doc-072",
        "title": "Formulas",
        "category": "Technical",
        "content": "## Formulas\n\nFormula fields compute a value based on other fields in the same record. Add a formula field from Settings > Fields > New Field > Formula.\n\nFormula syntax supports arithmetic operators (+, -, *, /), comparison operators, logical operators (AND, OR, NOT), and a library of functions.\n\nUseful built-in functions:\n- IF(condition, then, else): conditional value\n- DATEDIF(date1, date2, unit): difference between dates\n- CONCATENATE(str1, str2): combine text fields\n- ROUND(number, decimals): round a number\n- NOW(): current timestamp\n\nFormulas can reference other formula fields but not in circular references. The formula editor shows errors inline as you type.\n\nFormula results are computed fresh on every record load. Formula fields do not support indexing and cannot be used for sort or filter in high-volume tables."
    },
    {
        "id": "doc-073",
        "title": "Record Locking",
        "category": "Technical",
        "content": "## Record Locking\n\nRecord locking prevents changes to a record while it is being edited by another user, or to protect finalized records from accidental modification.\n\nManual lock: from the record menu, click Lock Record. A locked record shows a lock indicator and prevents editing by all users except the locker and admins. To unlock, click Unlock. This is available to the locker, any Admin, or a user explicitly granted unlock permission.\n\nAutomation-based lock: configure a rule to lock records when a certain condition is met, such as locking all invoices when status is set to Approved.\n\nLocked records can still receive comments. Locking prevents field edits, not communication.\n\nBulk lock: select multiple records in table view and use the bulk action menu to lock all selected records simultaneously."
    },
    {
        "id": "doc-074",
        "title": "Import from Spreadsheet",
        "category": "Data Management",
        "content": "## Import from Spreadsheet\n\nImporting from a spreadsheet is the fastest way to migrate existing data. Supported formats: CSV, XLSX, and Google Sheets via a share link.\n\nFor CSV import: the first row must be a header row with column names. UTF-8 encoding is required.\n\nFor XLSX import: only the first sheet is imported. Remove any pivot tables or charts from that sheet before exporting.\n\nFor Google Sheets: share the sheet with link access, paste the URL in the import dialog, and the sheet is fetched directly.\n\nDuring import, the column mapping UI shows a preview of the first five rows to help verify mappings are correct. Date columns require selecting the format that matches your data.\n\nAfter import, review the import summary. Download the error report if any rows failed."
    },
    {
        "id": "doc-075",
        "title": "Email Templates",
        "category": "Integrations",
        "content": "## Email Templates\n\nEmail templates define the content of automated notification emails. They are used by automation rules that trigger email actions and by scheduled report deliveries.\n\nCreate and edit templates from Settings > Automation > Email Templates. Templates use a variable syntax for dynamic content such as record title, assignee name, and current user name.\n\nTemplates support basic HTML for formatting. Inline styles are recommended since email clients strip external CSS. Preview the rendered template using the Preview button before saving.\n\nSystem templates (welcome email, password reset, billing notifications) cannot be deleted but can be customized in appearance. Add your organization logo and adjust the color scheme from Settings > Brand > Email Branding.\n\nUnsubscribe links are required for marketing emails. For transactional emails (notifications, alerts), they are optional but recommended."
    },
    {
        "id": "doc-076",
        "title": "Localization and Timezones",
        "category": "Technical",
        "content": "## Localization and Timezones\n\nTimestamps are stored in UTC and displayed in each user's local timezone. Set your timezone in Account Settings > Preferences > Timezone. If not set, the browser's detected timezone is used.\n\nDate fields without a time component display without timezone conversion. A due date of Jan 15 is Jan 15 for all users regardless of timezone. Datetime fields include time and are displayed in the viewer's local timezone.\n\nWhen filtering by date ranges via the API, all datetimes must be in ISO 8601 format with UTC offset.\n\nThe interface language is set per user in Account Settings > Preferences > Language. Exported CSV and JSON files always use period as decimal separator and ISO 8601 for dates, regardless of locale."
    },
    {
        "id": "doc-077",
        "title": "Backup and Restore",
        "category": "Data Management",
        "content": "## Backup and Restore\n\nWe perform automated daily backups of all data with a 30-day retention period stored in a geographically separate region. Backups are encrypted and are not directly accessible to customers. They are used by our team for disaster recovery.\n\nFor your own backup copies, use the scheduled export feature to deliver exports to your S3 bucket on a daily or weekly basis.\n\nPoint-in-time restore: if you accidentally delete records, soft-deleted records are recoverable for 30 days from Settings > Data > Trash. Permanent deletions cannot be recovered through self-service. Contact support within 24 hours for a potential restore from backup.\n\nFor major incidents, contact support immediately. We can restore to a point in time within the last 30 days. Restore operations take 2-8 hours depending on data volume."
    },
    {
        "id": "doc-078",
        "title": "Multi-Workspace Management",
        "category": "Team Management",
        "content": "## Multi-Workspace Management\n\nAn organization can have multiple workspaces, one per department or client for example. Each workspace has independent data, settings, and member lists. Users can belong to multiple workspaces under the same organization.\n\nCreate a new workspace from the workspace switcher in the top left navigation. Only organization owners can create workspaces.\n\nUsers are invited to workspaces individually. Being a member of one workspace does not grant access to others. An organization admin can view and manage all workspaces from the Admin Console.\n\nBilling is aggregated at the organization level across all workspaces. A single invoice covers all workspace seat counts combined.\n\nCross-workspace data sharing is not supported. Records cannot be linked between workspaces. Copying records between workspaces requires exporting from one and importing into the other."
    },
    {
        "id": "doc-079",
        "title": "SSO with Azure AD",
        "category": "Authentication",
        "content": "## SSO with Azure AD\n\nAzure Active Directory (Entra ID) SAML integration is supported and tested on Business and Enterprise plans.\n\nIn the Azure portal, create a new Enterprise Application. Under Single sign-on, choose SAML. Fill in the Identifier (Entity ID) and Reply URL (ACS URL) from your SSO settings page.\n\nAttribute mapping for Azure AD:\n- User.userprincipalname maps to email (NameID)\n- User.givenname maps to firstName\n- User.surname maps to lastName\n\nAzure AD by default sends the UPN as the NameID. If users log in with a different email than their UPN, change the NameID claim to use user.mail instead.\n\nGroup-based access: configure Azure AD to only allow specific groups to use the application. Users not in the assigned groups cannot log in via SSO even if they have an Azure AD account."
    },
    {
        "id": "doc-080",
        "title": "SSO with Okta",
        "category": "Authentication",
        "content": "## SSO with Okta\n\nOkta SAML integration is fully supported and is the most commonly used IdP in our customer base. Setup typically takes under 30 minutes.\n\nIn Okta, go to Applications > Create App Integration > SAML 2.0. In the SAML settings, enter the Single Sign On URL (your ACS URL) and the Audience URI (your Entity ID), both found in Settings > Security > SSO.\n\nAttribute statements in Okta:\n- user.email maps to email\n- user.firstName maps to firstName\n- user.lastName maps to lastName\n\nJIT provisioning: when a new user logs in via Okta SSO for the first time, an account is created automatically. If the email matches an existing account, the SSO identity is linked to it.\n\nOkta's User Import feature combined with SCIM provides fully automated provisioning and deprovisioning."
    },
    {
        "id": "doc-081",
        "title": "Compliance and Data Residency",
        "category": "Security",
        "content": "## Compliance and Data Residency\n\nBy default, all customer data is stored in the US (AWS us-east-1). EU data residency is available on Enterprise plans, storing all data in AWS eu-west-1 (Ireland).\n\nTo request EU data residency, contact your account manager before your first data is written. Migrating an existing workspace to a different region requires a planned maintenance window.\n\nCompliance certifications held: SOC 2 Type II, ISO 27001, and GDPR-ready (DPA available). HIPAA BAA is available for Enterprise customers with a signed agreement.\n\nData processing addendum (DPA): available for EU and UK organizations as required by GDPR. Sign via Settings > Legal > Data Processing Agreement. The DPA covers standard contractual clauses for international data transfers.\n\nWe publish a Trust Center with current certifications, sub-processor list, security policies, and penetration test summaries."
    },
    {
        "id": "doc-082",
        "title": "Custom Domain Setup",
        "category": "Technical",
        "content": "## Custom Domain Setup\n\nEnterprise plans can host the workspace on a custom domain instead of the default subdomain.\n\nTo set up a custom domain: go to Settings > Workspace > Custom Domain, enter the desired hostname, and add the provided CNAME record to your DNS configuration. DNS propagation can take up to 48 hours but usually completes within one hour.\n\nSSL certificate provisioning is automatic. The certificate is provisioned once the CNAME is live and renews automatically every 90 days.\n\nEmail notifications, SSO callbacks, and API documentation links use the custom domain once it is active. Existing bookmarks to the default subdomain redirect automatically via a 301 redirect.\n\nIf you need to remove or change the custom domain, update the IdP ACS URL before making the DNS change to avoid SSO breakage."
    },
    {
        "id": "doc-083",
        "title": "Webhook Rate Limits",
        "category": "Integrations",
        "content": "## Webhook Rate Limits\n\nWebhook delivery rate limits exist on both the sending side (events delivered per second to your endpoint) and the receiving side (how fast your endpoint must respond).\n\nDelivery rate: we deliver up to 200 events per second per webhook endpoint. Events exceeding this are queued. The queue holds up to 10,000 events. If the queue fills, newer events are dropped and logged.\n\nResponse timeout: your endpoint must respond within 10 seconds. Responses that take longer are treated as failures and trigger the retry sequence. If your handler takes more than a second, respond with HTTP 200 immediately and process the payload asynchronously.\n\nBest practice: use a message queue (SQS, RabbitMQ) as your webhook endpoint. The endpoint immediately returns 200 and enqueues the payload for a worker to process.\n\nStore the event ID from each payload and check for duplicates before processing to ensure idempotency."
    },
    {
        "id": "doc-084",
        "title": "Embedding Reports",
        "category": "Analytics",
        "content": "## Embedding Reports\n\nReports can be embedded in external websites, internal wikis, or customer-facing portals using an iframe embed code. Access the embed code from any report via Share > Embed.\n\nThe embed URL includes a signed token that grants read-only access without requiring the viewer to log in. Tokens expire after 24 hours and are automatically refreshed when the page loads.\n\nConfigure what the embedded viewer can interact with: date range filter (allow or fix), dimension drill-down, and CSV export. More permissive settings improve the viewer experience but expose more data.\n\nEmbed tokens are scoped to the specific report or dashboard and cannot access other workspace data.\n\nFor customer-facing embeds where different customers should see different data subsets, use the API to generate report URLs with pre-applied filters combined with signed short-lived tokens."
    },
    {
        "id": "doc-085",
        "title": "Offline Mode",
        "category": "Technical",
        "content": "## Offline Mode\n\nThe web application supports limited offline functionality. When connectivity is lost, a banner appears. You can continue viewing recently accessed records and adding comments. Changes are queued locally.\n\nWhen connection is restored, queued changes sync automatically in the order they were made. Conflicts are resolved by the last-write-wins rule with a notification showing what changed.\n\nOffline mode is not available for: creating new records, loading records not previously visited in the session, bulk operations, and file uploads.\n\nThe mobile apps have more robust offline support. Records are cached based on recency and starred status. The mobile app can create and edit records offline.\n\nOffline mode is not suitable for mission-critical real-time operations. Build API integrations with proper retry logic rather than relying on the browser UI's offline queue."
    },
    {
        "id": "doc-086",
        "title": "User Deactivation vs Deletion",
        "category": "Team Management",
        "content": "## User Deactivation vs Deletion\n\nWhen a team member leaves your organization, you have two options: deactivate or delete.\n\nDeactivation (recommended): the user can no longer log in and does not consume a seat. All records, comments, and activity remain intact and attributed to them. Their account can be reactivated if they rejoin.\n\nDeletion: removes the user account permanently. Their records and comments remain but become unattributed. Activity log entries retain the user ID for audit purposes but the display name is anonymized.\n\nFor GDPR right-to-erasure requests: deactivation alone does not satisfy an erasure request. Use the personal data anonymization endpoint to remove identifying information, then deactivate the account.\n\nAdmin users cannot be deactivated if they are the last admin. Transfer admin to another user first."
    },
    {
        "id": "doc-087",
        "title": "Troubleshooting Login Issues",
        "category": "Authentication",
        "content": "## Troubleshooting Login Issues\n\nIf you cannot log in, work through these steps before contacting support.\n\n1. Check Caps Lock. Passwords are case-sensitive.\n2. Try the password reset flow even if you think you know your password.\n3. Check if your account is locked due to too many failed attempts. Wait 30 minutes or contact support to clear the lock.\n4. If using SSO, verify the IdP is reachable and not experiencing an outage.\n5. Try a different browser or a private window. Browser extensions and corrupted cache can interfere with login.\n6. Check if your IP is allowlisted if your organization uses IP restrictions.\n7. If you recently changed your email, log in with the new email address.\n8. Check your organization's SSO policy. If SSO is enforced, you cannot log in with a password even if you have one set.\n\nIf none of these steps resolve the issue, contact support with your email, what you see on the login page, and your browser and OS."
    },
    {
        "id": "doc-088",
        "title": "Command Palette",
        "category": "Technical",
        "content": "## Command Palette\n\nThe command palette (Cmd/Ctrl + K) provides keyboard-first access to navigation, search, and actions across the workspace. It is the fastest way to get anywhere without using the mouse.\n\nType to search across records, workspace pages, settings, users, and available actions. Results are ranked by recency and relevance. Use arrow keys to navigate and Enter to select.\n\nCommon uses:\n- Jump to a record: type part of the record title\n- Navigate to a settings page: type the setting name such as billing, integrations, or team\n- Run a global action: type create, export, or invite to surface quick-action commands\n- Switch workspace: type the workspace name to jump directly\n\nThe command palette learns from your usage and surfaces frequently used items higher in results over time."
    },
    {
        "id": "doc-089",
        "title": "Changelog and Release Notes",
        "category": "Getting Started",
        "content": "## Changelog and Release Notes\n\nWe publish release notes for every product update. Subscribe to the changelog RSS feed or email newsletter to receive updates automatically.\n\nUpdates are categorized: New (net-new features), Improved (enhancements to existing features), and Fixed (bug fixes). Breaking changes are marked explicitly and communicated at least 30 days in advance via email to all organization admins.\n\nThe in-app What's New banner highlights recent changes relevant to your plan and role. Clicking an item links to the full changelog entry.\n\nMajor releases include a migration guide if any action is required from admins. Check for required migration actions before major releases.\n\nWe follow a continuous deployment model. Updates are released frequently rather than in large batched releases. Downtime is not required for most updates."
    },
    {
        "id": "doc-090",
        "title": "Exporting Reports to PDF and CSV",
        "category": "Analytics",
        "content": "## Exporting Reports to PDF and CSV\n\nAny report or dashboard can be exported as PDF or CSV. Access the export option from the report's action menu.\n\nPDF export captures the visual report as rendered. The PDF includes the report title, filter state at the time of export, and a timestamp. Reports wider than one page are split across multiple pages.\n\nCSV export outputs the underlying data table. If the report has grouping or aggregations, the CSV reflects those. To export raw records, use the Data Export feature from Settings > Data > Export instead.\n\nScheduled PDF delivery sends a fresh export to email recipients or Slack on a configured schedule. This is useful for weekly executive summaries or daily operational reports."
    },
    {
        "id": "doc-091",
        "title": "Feature Flags and Beta Features",
        "category": "Technical",
        "content": "## Feature Flags and Beta Features\n\nSome features are released gradually behind feature flags before becoming available to all users. Beta features are accessible before general availability and may have rough edges.\n\nOpt into beta features from Settings > Preferences > Beta Features. Each feature is listed with a description and the expected general availability date. Enabling a beta feature is reversible.\n\nOrganization admins can enable or disable beta features for the entire organization from Settings > Workspace > Beta Features. The admin setting applies to all members.\n\nBeta features are not covered by the standard SLA. If a beta feature causes disruption, disabling it restores the previous behavior.\n\nProvide feedback on beta features using the feedback button that appears when a beta feature is active. Beta feedback is reviewed by the product team and influences the final implementation."
    },
    {
        "id": "doc-092",
        "title": "Database Connections",
        "category": "Integrations",
        "content": "## Database Connections\n\nDirect database connections allow you to query your own databases and display results alongside workspace data. Supported databases: PostgreSQL, MySQL, Microsoft SQL Server, and BigQuery.\n\nSet up a connection from Settings > Integrations > Databases > New Connection. Enter the host, port, database name, and credentials. Use a read-only database user with access only to the schemas needed.\n\nIf your database is behind a firewall, allowlist our database connector IP ranges. Alternatively, use our IP tunnel feature (Enterprise only) to connect via an encrypted SSH tunnel.\n\nOnce connected, create database views in Analytics > Data Sources. Write a SQL query, name the view, and it becomes available as a data source for reports. SQL queries run with a row limit of 100,000 during preview.\n\nDatabase connections are tested at creation and re-checked every 15 minutes. A failed health check triggers an alert to workspace admins."
    },
    {
        "id": "doc-093",
        "title": "Team-Level Permissions",
        "category": "Team Management",
        "content": "## Team-Level Permissions\n\nTeams allow you to group workspace members and assign permissions at the team level rather than individually. Available on Business and Enterprise plans.\n\nCreate a team from Settings > Team > Teams > New Team. Add members and assign team roles (team admin or team member). Team admins can manage team membership but do not gain elevated organization-level permissions.\n\nAssign resources to teams with read or write access. A user's effective access is the combination of their organization role and any team-based access. Team access can expand but not restrict what an organization role already grants.\n\nSCIM group sync maps identity provider groups to workspace teams. When a user is added to or removed from an IdP group, they are automatically added to or removed from the corresponding team."
    },
    {
        "id": "doc-094",
        "title": "Webhooks vs Polling",
        "category": "API",
        "content": "## Webhooks vs Polling: When to Use Which\n\nBoth approaches retrieve data from the platform but suit different use cases.\n\nPolling: your system calls the API at regular intervals to check for changes. Simple to implement, works behind firewalls that block inbound connections, and does not require a public endpoint. Downsides: latency is limited by your poll interval, and every poll consumes rate limit quota even when nothing has changed.\n\nWebhooks: the platform calls your endpoint when an event occurs. Near-real-time delivery, typically under one second. No wasted rate limit calls when there is no activity. Requires a publicly accessible HTTPS endpoint.\n\nUse polling when: you need data infrequently, your system is behind a firewall, or the latency of your poll interval is acceptable.\n\nUse webhooks when: you need low-latency notifications, high event volume would exhaust poll-based rate limits, or you are building real-time workflows."
    },
    {
        "id": "doc-095",
        "title": "GraphQL API",
        "category": "API",
        "content": "## GraphQL API\n\nA GraphQL API is available alongside the REST API. The endpoint is at /api/graphql and accepts POST requests with an application/json body containing a query field.\n\nAuthentication uses the same API key as the REST API via the Authorization header.\n\nThe GraphQL schema is introspectable. Use the developer console at the developer portal for an interactive explorer with autocomplete and inline documentation.\n\nGraphQL advantages: request exactly the fields you need (no over-fetching), batch multiple queries in one request, and use subscriptions for real-time updates.\n\nRate limiting for GraphQL is based on query complexity rather than request count. Each field has a cost assigned, and the total cost per request cannot exceed your plan's query budget. Complex queries may hit complexity limits even if request count is low."
    },
    {
        "id": "doc-096",
        "title": "Data Masking",
        "category": "Security",
        "content": "## Data Masking and Sensitive Fields\n\nFields containing sensitive information can be marked as sensitive from the field settings. Sensitive fields have additional access controls and display protections.\n\nMasking behavior: sensitive fields show only the last four characters to users without the View Sensitive Data permission. Admins and users explicitly granted view access see the full value. Masking applies in the UI, API responses, and exports.\n\nThe View Sensitive Data permission is available on Business and Enterprise plans. Add it to a custom role or grant it to specific users from Settings > Team > Permissions.\n\nAudit logging: every access to a sensitive field (read, write, export) is logged in the audit trail with the user, timestamp, and IP address.\n\nSensitive fields cannot be used as search or filter criteria by users without view permission."
    },
    {
        "id": "doc-097",
        "title": "API Client Libraries",
        "category": "API",
        "content": "## API Client Libraries\n\nOfficial client libraries are maintained for Python, Node.js (TypeScript), Ruby, Go, and Java.\n\nInstallation:\n- Python: pip install example-sdk\n- Node.js: npm install @example/sdk\n- Ruby: gem install example-sdk\n- Go: go get github.com/example/sdk-go\n\nAll libraries implement automatic retry with exponential backoff on 429 and 5xx responses, cursor-based pagination helpers, request signing, and type-safe response objects.\n\nLibraries are updated within one week of any API change. Pin to a specific major version in production to avoid breaking changes from major version bumps.\n\nFor languages without an official library, use the OpenAPI specification available at the developer portal to generate a client using tools like OpenAPI Generator."
    },
    {
        "id": "doc-098",
        "title": "Structured Logging for API Integrations",
        "category": "API",
        "content": "## Structured Logging for API Integrations\n\nFor production API integrations, structured logging is essential for debugging and observability. Every API response includes headers that should be captured in your logs.\n\nKey headers to log:\n- X-Request-ID: unique identifier for the request. Required when contacting support about a specific failure.\n- X-RateLimit-Remaining: requests remaining in the current window.\n- X-RateLimit-Reset: Unix timestamp when the rate limit window resets.\n- Retry-After: seconds to wait before retrying (only on 429 responses).\n\nLog at minimum: timestamp, request method and URL, response status code, X-Request-ID, and elapsed time.\n\nCorrelate your internal trace IDs with X-Request-ID by including your trace ID in the X-Correlation-ID request header. This flows through to our server logs, enabling end-to-end trace correlation."
    },
    {
        "id": "doc-099",
        "title": "Handling Concurrent Edits via API",
        "category": "API",
        "content": "## Handling Concurrent Edits via API\n\nWhen multiple systems or users update the same record concurrently, conflicts can occur. The platform uses optimistic concurrency control to detect and surface these conflicts.\n\nEvery record response includes an etag header. When updating a record, include the If-Match header with the etag value. If the record has been modified since you last fetched it, the update fails with HTTP 412 Precondition Failed.\n\nOn a 412: re-fetch the record to get the current state and etag, merge your intended changes with the current data, then retry the update with the new etag.\n\nFor integrations where conflicts are frequent, use the patch endpoint instead of the full update endpoint. PATCH applies field-level changes rather than replacing the full record, reducing the conflict surface area.\n\nIf you do not include an If-Match header, updates succeed regardless of concurrent changes (last write wins)."
    },
    {
        "id": "doc-100",
        "title": "Troubleshooting Integration Errors",
        "category": "Integrations",
        "content": "## Troubleshooting Integration Errors\n\nWhen an integration stops working, follow this diagnostic sequence before contacting support.\n\n1. Check the integration status in Settings > Integrations. A red indicator means the connection has failed.\n\n2. Open the integration error log. Each error entry includes a timestamp, the operation attempted, the HTTP status received, and the error response body.\n\n3. Common causes by error type:\n   - 401/403: OAuth token expired or revoked. Reconnect via OAuth flow.\n   - 404: Resource deleted in the third-party system.\n   - 422: Field mapping mismatch. The value format does not match what the third-party expects.\n   - 429: Rate limit hit on the third-party side. Reduce sync frequency.\n   - 5xx: Third-party system experiencing issues. Check their status page.\n\n4. If the error log is clear but sync is not happening, check the sync schedule and confirm the integration is not paused.\n\n5. Trigger a manual sync to observe behavior in real time.\n\nIf none of these steps identify the issue, contact support with the integration name, the error log entries, and the time the issue started."
    },
]

data_path = Path("data/mock_data.json")
with open(data_path) as f:
    data = json.load(f)

existing_ids = {d["id"] for d in data["docs"]}
new_docs = [d for d in extra_docs if d["id"] not in existing_ids]
data["docs"].extend(new_docs)

with open(data_path, "w") as f:
    json.dump(data, f, indent=2)

print(f"Total docs: {len(data['docs'])}")
print(f"Total tickets: {len(data['tickets'])}")
