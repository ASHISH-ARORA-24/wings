WINGS FAMILY ONBOARDING FLOW
────────────────────────────────────────

[Homepage]
      │
      ▼
[Login Button]
      │
      ▼
[Login Modal]
 ├─ Family
 └─ Vendor
      │
      ▼
[Family Login]
      │
      ├─ Email + OTP
      ├─ Mobile + OTP
      ├─ Google Login
      └─ Microsoft Login
      │
      ▼
[Authentication Success]
      │
      ▼
{First Login?}
      │
      ├─ No ───────────────► [Homepage]
      │
      └─ Yes
            │
            ▼
    [Update User Profile]
            │
            ├─ username (unique)
            ├─ first name
            ├─ last name
            ├─ email
            ├─ phone
            └─ whatsapp
            │
            ▼
    [Submit Profile]
            │
            ▼
{Has Family ID?}
      │
      ├─────────────────────────────────────┐
      │                                     │
      ▼                                     ▼

[YES]                                [CREATE NEW FAMILY]
      │                                     │
      ▼                                     ▼
[Enter Family ID]                 [Generate Family ID]
      │                            (8-char alphanumeric)
      ▼                                     │
[Send Approval Request]                     ▼
to existing family members         [Redirect to Homepage]
      │                                     │
      ▼                                     ▼
[Pending Approval State]          [Family Created]
      │                                     │
      ├─ Can View Posts                     ├─ Address optional initially
      ├─ Cannot Create Posts                ├─ Kids optional initially
      └─ Cannot Show Interest               │
      │                                     ▼
      ▼                            [Limited Access State]
[Redirect to Homepage]                     │
                                           ├─ Can View Posts
                                           ├─ Cannot Create Posts
                                           └─ Cannot Show Interest


FAMILY COMPLETION REQUIREMENT
────────────────────────────────────────

Before posting or showing interest:

Mandatory:
 ├─ One Family Address
 └─ Minimum One Kid

Until completed:
 └─ View-only access


FAMILY DASHBOARD
────────────────────────────────────────

[Top Right Dropdown]
 ├─ Family Dashboard
 └─ Logout
      │
      ▼
[Family Dashboard]
 ├─ Family Members
 ├─ Family Address
 ├─ Kids
 └─ Pending Join Requests

Family Members
 └─ All approved members shown

Address
 ├─ Only one address per family
 └─ Any approved member can edit/update

Kids
 ├─ Multiple kids allowed
 ├─ All members can view/edit
 └─ Shows selected kid options

Pending Requests
 └─ Any approved family member can approve

Approval Rules
 ├─ Any one approved member can approve
 ├─ Only one approval needed
 └─ All family members have equal rights