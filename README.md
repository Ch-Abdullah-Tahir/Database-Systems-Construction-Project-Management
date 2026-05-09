# 🏗️ Construction System — Database Project

A complete Oracle SQL database project for managing construction operations,
paired with a React web interface to present the schema and all SQL queries.

---

## 👥 Team

| Name | Roll Number |
|------|------------|
| Abdullah Tahir | 24F-0020 |
| Muhammad Umar | 24F-0036 |

---

## 📋 Project Overview

The Construction System is a relational database designed to manage all aspects
of construction project operations including sites, personnel, contracts,
materials, equipment, permits, inspections, incidents and payments.

The project covers all major DBMS concepts:
- Entity Relationship Design with specialization and categorization
- 28 fully normalized tables with proper constraints
- 10 Views
- 5 Joins (INNER, LEFT, RIGHT)
- 6 Subqueries (single row, IN, NOT IN, nested)
- 4 Stored Procedures
- 3 Triggers

---

## 🗄️ Database — Oracle APEX

### Tables (28 Total)

**Core Entities**
- PERSON, EMPLOYEE, CLIENT
- ARCHITECT, ENGINEER, CONTRACTOR
- SITE, PROJECT, CONTRACT, BUDGET

**Resource Tables**
- MATERIAL, EQUIPMENT, TASK
- PERMIT, INSPECTION, INCIDENT, PAYMENT
- MATERIAL_SUPPLIER, MATERIAL_ORDER

**Relationship Tables**
- PROJECT_SITE, PROJECT_ARCHITECT, PROJECT_ENGINEER
- PROJECT_MATERIAL, PROJECT_EQUIPMENT
- TASK_EMPLOYEE, INCIDENT_EMPLOYEE
- MATERIAL_SUPPLIER_LINK, PERMIT_PROJECT

### Specializations
| Superclass | Subclasses | Constraint |
|-----------|------------|------------|
| PERSON | EMPLOYEE, CLIENT | Disjoint, Total |
| EMPLOYEE | ARCHITECT, ENGINEER, CONTRACTOR | Disjoint, Total |

### Views (10)
1. v_active_projects
2. v_approved_permits
3. v_failed_inspections
4. v_critical_incidents
5. v_projectnClient_details
6. v_employeeenPerson_details
7. v_contract_details
8. v_payment_summary
9. v_project_material_cost
10. v_contractor_payments

### Stored Procedures (4)
1. add_project — insert new project with validation
2. update_project_status — update status with old/new display
3. assign_architect — assign architect to project with role
4. add_incident — log incident with reporter details

### Triggers (3)
1. prevent_active_contract_delete — BEFORE DELETE on CONTRACT
2. log_critical_incident — AFTER INSERT on INCIDENT
3. prevent_payment_status_change — BEFORE UPDATE on PAYMENT

---

## 💻 Web Interface — React

A single page React application that displays the complete database
schema with live inserted data and all 28 SQL queries organized by category.

### Pages
- **Home** — project overview, team info, category stats
- **Schema** — all 28 tables with columns and inserted data
- **Queries** — all queries with SQL syntax highlighting and output

### Tech Stack
| Technology | Purpose |
|-----------|---------|
| Python | Image processing and App.js generation |
| React | Frontend UI framework |
| JSX | Component syntax |
| Inline CSS | Styling |
| Base64 | Offline image embedding |
| Node.js / npm | Development server |
| Oracle APEX | Database platform |

---

## 🚀 How to Run

### Prerequisites
- Node.js installed
- Python 3 installed
- Images named Image1.jpeg, Image2.jpeg, Image3.jpeg, Image4.jpeg on Desktop

### Steps

**1. Create React App**
```bash
