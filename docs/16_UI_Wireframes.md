# 16_UI_Wireframes.md

# DefaultSense AI

### UI Wireframes & Screen Flow

**Version:** 2.0
**Document Type:** UI Wireframes

---

# 1. Objective

This document defines the visual layout of every major screen in **DefaultSense AI**. The wireframes serve as the design blueprint for frontend development.

---

# 2. Screen Flow

```text
Login

↓

Dashboard

├── Customers
├── Loans
├── AI Prediction
├── Knowledge Graph
├── Reports
├── Alerts
└── Settings
```

---

# 3. Login Screen

```text
+--------------------------------------------------+
|                 DefaultSense AI                  |
|--------------------------------------------------|
|              Email Address                       |
|              Password                            |
|                                                  |
|          [ Login ]                               |
|                                                  |
|       Forgot Password (Future)                   |
+--------------------------------------------------+
```

---

# 4. Dashboard

```text
+--------------------------------------------------------------+
| Navbar                                                       |
+---------+----------------------------------------------------+
| Sidebar | Customers | Loans | Avg PD | High Risk Borrowers  |
|         |----------------------------------------------------|
|         | Portfolio Risk Chart                              |
|         |----------------------------------------------------|
|         | Loan Distribution | Prediction Trend              |
|         |----------------------------------------------------|
|         | Recent Alerts                                     |
+---------+----------------------------------------------------+
```

KPIs

* Total Customers
* Active Loans
* High Risk Loans
* Average PD
* Portfolio Risk

---

# 5. Customer List

```text
+--------------------------------------------------------------+
| Search | Filters                                             |
+--------------------------------------------------------------+
| Customer ID | Name | Loan Type | Risk | View                |
|--------------------------------------------------------------|
| C001        | Rahul | Home Loan | High | Details            |
| C002        | Anita | MSME Loan | Low  | Details            |
+--------------------------------------------------------------+
```

---

# 6. Customer Details

```text
Customer Information

-------------------------------------

Loan Summary

-------------------------------------

Repayment History

-------------------------------------

Prediction Result

-------------------------------------

SHAP Explanation

-------------------------------------

Knowledge Graph

-------------------------------------

Recommendation
```

---

# 7. AI Prediction Screen

```text
+--------------------------------------------------------------+
| Probability of Default                                       |
|                                                              |
|                    81 %                                      |
|                                                              |
| Confidence : 92%                                             |
| Risk Level : High                                            |
|                                                              |
| Recommendation : Additional Verification                     |
+--------------------------------------------------------------+
```

---

# 8. SHAP Explanation

```text
+--------------------------------------------------------------+
| Top Risk Factors                                             |
|--------------------------------------------------------------|
| Debt-to-Income Ratio                         +0.35           |
| Late EMI Payments                            +0.28           |
| Employer Risk                                +0.20           |
| Credit Utilization                           +0.15           |
+--------------------------------------------------------------+
```

---

# 9. Knowledge Graph

```text
                 Employer

                     |

Region ---- Customer ---- Loan

                     |

                Guarantor

                     |

                 Industry
```

Features

* Zoom
* Pan
* Search
* Node Details

---

# 10. Reports

```text
+--------------------------------------------------------------+
| Customer Report                                              |
| Portfolio Report                                             |
| Loan Report                                                  |
|                                                              |
| [Export PDF]   [Export CSV]                                 |
+--------------------------------------------------------------+
```

---

# 11. Alerts

```text
+--------------------------------------------------------------+
| High Risk Borrowers                                          |
|--------------------------------------------------------------|
| Customer      Risk       Status                              |
|--------------------------------------------------------------|
| Rahul         Critical   Pending Review                      |
| Priya         High       Verification Needed                 |
+--------------------------------------------------------------+
```

---

# 12. Responsive Layout

Desktop

* Sidebar Expanded
* Multi-column Dashboard

Tablet

* Collapsible Sidebar
* Two-column Layout

---

# 13. Design Guidelines

Primary Color

* Blue

Risk Colors

* Green → Low
* Yellow → Moderate
* Orange → High
* Red → Critical

Cards

* Rounded Corners
* Minimal Shadows
* Simple Charts

---

# 14. UI Deliverables

* Login
* Dashboard
* Customer Module
* Loan Module
* AI Prediction
* SHAP Visualization
* Knowledge Graph
* Reports
* Alerts
* Settings

These wireframes act as the reference for frontend implementation.
