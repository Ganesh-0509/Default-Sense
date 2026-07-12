# 06_Frontend_UI_UX.md

# DefaultSense AI

### Hybrid Multi-Modal Loan Default Prediction & Decision Intelligence Platform

**Version:** 2.0
**Document Type:** Frontend UI/UX Design

---

# 1. Objective

The frontend provides an intuitive, responsive, and explainable banking dashboard that enables credit officers and risk analysts to monitor borrowers, predict loan defaults, understand AI decisions, and take proactive actions.

The interface is designed for **clarity, speed, and decision-making**, ensuring complex AI insights remain easy to interpret.

---

# 2. Design Principles

* Clean & Professional Banking UI
* Explainable AI First
* Minimal Learning Curve
* Responsive Design
* Accessibility (WCAG-friendly)
* Fast Navigation
* Consistent User Experience

---

# 3. Technology Stack

| Component           | Technology   |
| ------------------- | ------------ |
| Framework           | React + Vite |
| Styling             | Tailwind CSS |
| Icons               | Lucide React |
| Charts              | Recharts     |
| Graph Visualization | React Flow   |
| State Management    | Zustand      |
| Routing             | React Router |
| API Client          | Axios        |

---

# 4. Application Structure

```text id="w3gh5n"
Login

↓

Dashboard

├── Customers
├── Loans
├── AI Predictions
├── Knowledge Graph
├── Documents
├── Reports
├── Alerts
└── Settings
```

---

# 5. Navigation Menu

### Sidebar

* Dashboard
* Customers
* Loans
* Predictions
* Knowledge Graph
* Documents
* Reports
* Alerts
* Settings
* Logout

---

### Top Navigation

* Search
* Notifications
* User Profile
* Theme Toggle *(Optional)*
* Current Branch

---

# 6. Screens

## 1. Login

Features

* Secure Login
* Remember Me
* Forgot Password *(Future)*

---

## 2. Dashboard

Displays

* Total Customers
* Active Loans
* High-Risk Borrowers
* Average PD Score
* Portfolio Risk
* Recent Alerts
* Loan Distribution
* Monthly Trends

---

## 3. Customer Management

Features

* Customer List
* Search
* Filters
* Customer Details
* Loan History
* Prediction History

---

## 4. Loan Details

Displays

* Loan Information
* EMI Schedule
* Repayment History
* Outstanding Balance
* Default Probability
* Recommendations

---

## 5. AI Prediction

Displays

* Probability of Default (12 Months)
* Risk Category
* Confidence Score
* SHAP Feature Importance
* Risk Drivers
* Recommended Action

---

## 6. Knowledge Graph

Features

* Interactive Relationship Graph
* Zoom & Pan
* Node Search
* Connected Borrowers
* Employer & Industry View

---

## 7. Documents

Displays

* Uploaded Documents
* OCR Extracted Text
* Loan Officer Notes
* Document Status

---

## 8. Reports

Generate

* Customer Report
* Portfolio Report
* Risk Report

Export

* PDF
* CSV

---

## 9. Alerts

Displays

* High-Risk Customers
* Critical Predictions
* Pending Reviews
* Recent Notifications

---

## 10. Settings

Manage

* User Profile
* Password
* Notification Preferences
* System Preferences

---

# 7. Dashboard Layout

```text id="o1msvh"
--------------------------------------------------------

Navbar

--------------------------------------------------------

Sidebar      KPI Cards

             Portfolio Risk Chart

             Loan Distribution

             Recent Alerts

             High Risk Customers

--------------------------------------------------------
```

---

# 8. Customer Details Layout

```text id="f69tux"
Customer Information

Loan Summary

Repayment History

AI Prediction

SHAP Explanation

Knowledge Graph

Recommendations
```

---

# 9. AI Prediction Card

Displays

* Probability of Default
* Risk Level
* Confidence Score
* Last Prediction Date

Example

```text id="jlwm7f"
Probability of Default

81%

Risk Level

High

Confidence

92%
```

---

# 10. SHAP Explanation Panel

Displays

* Top Positive Factors
* Top Negative Factors
* Feature Contributions
* AI Explanation

Example

```text id="h2gbxv"
High Debt-to-Income Ratio

Late EMI Payments

Employer Under Stress

High Credit Utilization
```

---

# 11. Knowledge Graph View

Displays relationships between

* Customer
* Employer
* Industry
* Guarantor
* Branch
* Region

Features

* Zoom
* Pan
* Search
* Node Details
* Relationship Highlighting

---

# 12. Color System

| Status        | Color  |
| ------------- | ------ |
| Low Risk      | Green  |
| Moderate Risk | Yellow |
| High Risk     | Orange |
| Critical Risk | Red    |
| Information   | Blue   |

---

# 13. Responsive Design

Supports

* Desktop
* Laptop
* Tablet

*(Mobile support is planned for a future release.)*

---

# 14. Accessibility

* Keyboard Navigation
* Screen Reader Support
* High Contrast Colors
* Accessible Form Labels
* Focus Indicators

---

# 15. User Journey

```text id="j8mqm7"
Login

↓

Dashboard

↓

Select Customer

↓

View Loan Details

↓

Run AI Prediction

↓

Review SHAP Explanation

↓

View Knowledge Graph

↓

Take Recommended Action

↓

Generate Report
```

---

# 16. UI Components

Reusable Components

* Navbar
* Sidebar
* KPI Cards
* Data Tables
* Search Bar
* Filters
* Forms
* Charts
* Graph Viewer
* SHAP Panel
* Recommendation Card
* Alert Card
* Report Card
* Notification Toast
* Loading Skeletons

---

# 17. Future UI Enhancements

* Dark Mode
* Voice Search
* AI Chat Assistant
* Real-time Notifications
* Advanced Dashboard Customization
* Mobile Application

---

# 18. Frontend Deliverables

* Responsive Banking Dashboard
* Customer & Loan Management Screens
* AI Prediction Interface
* Explainable AI Visualization
* Interactive Knowledge Graph
* Document Viewer with OCR Results
* Reports & Export Features
* Alerts & Notifications
* Modern, Accessible UI
