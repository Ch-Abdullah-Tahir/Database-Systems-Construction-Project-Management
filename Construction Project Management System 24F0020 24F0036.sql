-- =============================================
-- CONSTRUCTION MANAGEMENT SYSTEM
-- COMPLETE SQL SCRIPT
-- =============================================

-- =============================================
-- TABLE CREATION
-- =============================================

-- 1. PERSON
CREATE TABLE PERSON (
    PersonId INT PRIMARY KEY,
    FullName VARCHAR2(50) NOT NULL,
    CNIC VARCHAR2(15) UNIQUE,
    DOB DATE,
    Phone VARCHAR2(15),
    Gender VARCHAR2(6) CHECK (Gender IN ('Male','Female','Other')),
    Address VARCHAR2(100),
    Email VARCHAR2(50) UNIQUE
    CHECK (Email LIKE '%@%')
);

ALTER TABLE PERSON 
ADD PersonType VARCHAR2(10) NOT NULL 
    CHECK (PersonType IN ('Employee', 'Client'));

-- 2. EMPLOYEE
CREATE TABLE EMPLOYEE (
    PersonId    INT REFERENCES Person(PersonId) ON DELETE CASCADE,
    EmployeeId  INT PRIMARY KEY,
    HireDate    DATE NOT NULL,
    Salary      NUMBER(10,2) CHECK (Salary > 0),
    JobTitle    VARCHAR2(50),
    Department  VARCHAR2(50)
);

ALTER TABLE EMPLOYEE
ADD CONSTRAINT uq_emp_personid UNIQUE (PersonId);

ALTER TABLE EMPLOYEE
ADD EmployeeType VARCHAR2(15) NOT NULL CHECK (EmployeeType IN ('Architect', 'Engineer', 'Contractor'));

-- 3. CLIENT
CREATE TABLE CLIENT (
    PersonId         INT REFERENCES PERSON(PersonId) ON DELETE CASCADE,
    ClientId         INT PRIMARY KEY,
    OrganizationType VARCHAR2(20) CHECK (OrganizationType IN ('Private','Government','NGO')),
    CreditRating     VARCHAR2(10) CHECK (CreditRating IN ('A','B','C','D')),
    CONSTRAINT uq_client_personid UNIQUE (PersonId)
);

-- 4. ARCHITECT
CREATE TABLE ARCHITECT (
    EmployeeId        INT REFERENCES EMPLOYEE(EmployeeId) ON DELETE CASCADE,
    ArchitectId       INT PRIMARY KEY,
    LicenseNo         VARCHAR2(20) UNIQUE NOT NULL,
    Specialization    VARCHAR2(50),
    YearsExperience   INT CHECK (YearsExperience >= 0),
    CONSTRAINT uq_arch_empid UNIQUE (EmployeeId)
);

-- 5. CONTRACTOR
CREATE TABLE CONTRACTOR (
    EmployeeId     INT REFERENCES EMPLOYEE(EmployeeId) ON DELETE CASCADE,
    ContractorId   INT PRIMARY KEY,
    ContractType   VARCHAR2(20) CHECK (ContractType IN ('Prime','Sub')),
    Rating         NUMBER(3,1) CHECK (Rating BETWEEN 0 AND 5),
    CONSTRAINT uq_cont_empid UNIQUE (EmployeeId)
);

-- 6. ENGINEER
CREATE TABLE ENGINEER (
    EmployeeId     INT REFERENCES EMPLOYEE(EmployeeId) ON DELETE CASCADE,
    EngineerId     INT PRIMARY KEY,
    Discipline     VARCHAR2(20) CHECK (Discipline IN ('Civil','Structural','Electrical','Mechanical')),
    CONSTRAINT uq_eng_empid UNIQUE (EmployeeId)
);

-- 7. SITE
CREATE TABLE SITE(
    SiteId INT PRIMARY KEY,
    SiteName Varchar2(50) UNIQUE NOT NULL,
    SiteAddress Varchar2(100),
    AreaSqMeters INT
);

-- 8. PROJECT
CREATE TABLE PROJECT(
    ProjectId INT PRIMARY KEY,
    ProjectName VARCHAR2(50) UNIQUE NOT NULL,
    ClientId  INT REFERENCES CLIENT(ClientId) ON DELETE SET NULL,
    ProjectType VARCHAR2(12) CHECK(ProjectType IN ('Residential','Commercial','Industrial','Infrastructure')),
    Priority VARCHAR2(10) CHECK (Priority IN ('Low','Medium','High','Critical')),
    Status   VARCHAR2(10) CHECK (Status IN ('Planned','Active','OnHold','Completed')),
    StartDate DATE,
    EndDate DATE,
    CONSTRAINT chk_dates CHECK (EndDate > StartDate)
);

-- 9. CONTRACT
CREATE TABLE CONTRACT (
    ContractId     INT PRIMARY KEY,
    ProjectId      INT REFERENCES PROJECT(ProjectId) ON DELETE CASCADE,
    ContractorId   INT REFERENCES CONTRACTOR(ContractorId) ON DELETE SET NULL,
    ContractType   VARCHAR2(20) CHECK (ContractType IN ('Fixed','Hourly','Milestone')),
    SignedDate     DATE,
    StartDate      DATE,
    EndDate        DATE,
    TotalValue     NUMBER(15,2) CHECK (TotalValue > 0),
    Status         VARCHAR2(15) CHECK (Status IN ('Active','Terminated','Completed')),
    CONSTRAINT chk_contract_dates CHECK (EndDate > StartDate)
);

-- 10. BUDGET
CREATE TABLE BUDGET (
    BudgetId       INT PRIMARY KEY,
    ProjectId      INT REFERENCES PROJECT(ProjectId) ON DELETE CASCADE,
    TotalAllocated NUMBER(15,2) CHECK (TotalAllocated > 0),
    CONSTRAINT uq_budget_project UNIQUE (ProjectId)
);

ALTER TABLE BUDGET
MODIFY ProjectId INT NOT NULL;

-- 11. MATERIAL
CREATE TABLE MATERIAL (
    MaterialId     INT PRIMARY KEY,
    MaterialName   VARCHAR2(50) NOT NULL,
    Category       VARCHAR2(20) CHECK (Category IN ('Concrete','Steel','Timber','Glass','Finishing')),
    Unit           VARCHAR2(10) CHECK (Unit IN ('kg','ton','m3','m2','litre'))
);

-- 12. EQUIPMENT
CREATE TABLE EQUIPMENT (
    EquipmentId      INT PRIMARY KEY,
    EquipmentName    VARCHAR2(50) NOT NULL,
    EquipmentType    VARCHAR2(20) CHECK (EquipmentType IN ('Crane','Excavator','Mixer','Scaffold','Bulldozer'))
);

-- 13. TASK
CREATE TABLE TASK (
    TaskId          INT PRIMARY KEY,
    ProjectId       INT NOT NULL REFERENCES PROJECT(ProjectId) ON DELETE CASCADE,
    TaskName        VARCHAR2(100) NOT NULL,
    StartDate       DATE,
    EndDate         DATE,
    Status          VARCHAR2(15) CHECK (Status IN ('NotStarted','InProgress','Completed','Delayed'))
);

-- 14. PERMIT
CREATE TABLE PERMIT (
    PermitId     INT PRIMARY KEY,
    IssuedBy     VARCHAR2(50) NOT NULL,
    IssueDate    DATE,
    PermitType   VARCHAR2(20) CHECK (PermitType IN ('Building','Environmental','Zoning','Safety','Demolition')),
    Status       VARCHAR2(10) CHECK (Status IN ('Pending','Approved','Rejected','Expired'))
);

-- 15. INSPECTION
CREATE TABLE INSPECTION (
    InspectionId     INT PRIMARY KEY,
    SiteId           INT NOT NULL REFERENCES SITE(SiteId) ON DELETE CASCADE,
    InspectionType   VARCHAR2(20) CHECK (InspectionType IN ('Structural','Electrical','Safety','Environmental','Final')),
    ConductedDate    DATE,
    Result           VARCHAR2(15) CHECK (Result IN ('Pass','Fail','Conditional')),
    Remarks          VARCHAR2(500)
);

-- 16. INCIDENT
CREATE TABLE INCIDENT (
    IncidentId   INT PRIMARY KEY,
    ProjectId    INT NOT NULL REFERENCES PROJECT(ProjectId) ON DELETE CASCADE,
    IncidentType VARCHAR2(20) CHECK (IncidentType IN ('Injury','NearMiss','PropertyDamage','Fire')),
    DateOccurred DATE NOT NULL,
    Severity     VARCHAR2(10) CHECK (Severity IN ('Low','Medium','High','Critical')),
    Description  VARCHAR2(500),
    ReportedBy   INT REFERENCES EMPLOYEE(EmployeeId) ON DELETE SET NULL,
    ActionTaken  VARCHAR2(500)
);

-- 17. PAYMENT
CREATE TABLE PAYMENT (
    PaymentId    INT PRIMARY KEY,
    ContractId   INT NOT NULL REFERENCES CONTRACT(ContractId) ON DELETE CASCADE,
    ContractorId INT NOT NULL REFERENCES CONTRACTOR(ContractorId) ON DELETE CASCADE,
    Amount       NUMBER(15,2) CHECK (Amount > 0),
    PaymentDate  DATE NOT NULL,
    Method       VARCHAR2(15) CHECK (Method IN ('BankTransfer','Cheque','Cash')),
    Status       VARCHAR2(10) CHECK (Status IN ('Pending','Completed','Disputed'))
);

-- 18. MATERIAL_SUPPLIER
CREATE TABLE MATERIAL_SUPPLIER (
    SupplierId      INT PRIMARY KEY,
    CompanyName     VARCHAR2(50) NOT NULL,
    ContactPerson   VARCHAR2(50),
    Phone           VARCHAR2(15) UNIQUE,
    Email           VARCHAR2(50) UNIQUE CHECK (Email LIKE '%@%'),
    Address         VARCHAR2(100),
    Rating          NUMBER(3,1) CHECK (Rating BETWEEN 0 AND 5)
);

-- 19. MATERIAL_ORDER
CREATE TABLE MATERIAL_ORDER (
    OrderId           INT PRIMARY KEY,
    SupplierId        INT NOT NULL REFERENCES MATERIAL_SUPPLIER(SupplierId) ON DELETE SET NULL,
    ProjectId         INT NOT NULL REFERENCES PROJECT(ProjectId) ON DELETE CASCADE,
    OrderDate         DATE NOT NULL,
    DeliveryDate      DATE,
    QuantityOrdered   NUMBER(10,2) CHECK (QuantityOrdered > 0),
    QuantityDelivered NUMBER(10,2) CHECK (QuantityDelivered >= 0),
    TotalCost         NUMBER(15,2) CHECK (TotalCost >= 0),
    Status            VARCHAR2(10) CHECK (Status IN ('Pending','Delivered','Partial','Cancelled')),
    CONSTRAINT chk_order_dates CHECK (DeliveryDate >= OrderDate),
    CONSTRAINT chk_qty CHECK (QuantityDelivered <= QuantityOrdered)
);

-- RELATIONSHIP TABLES


-- 20. PROJECT_SITE
CREATE TABLE PROJECT_SITE (
    ProjectId INT NOT NULL REFERENCES PROJECT(ProjectId) ON DELETE CASCADE,
    SiteId    INT NOT NULL REFERENCES SITE(SiteId) ON DELETE CASCADE,
    CONSTRAINT pk_project_site PRIMARY KEY (ProjectId, SiteId)
);

-- 21. PROJECT_ARCHITECT
CREATE TABLE PROJECT_ARCHITECT (
    ProjectId   INT NOT NULL REFERENCES PROJECT(ProjectId) ON DELETE CASCADE,
    ArchitectId INT NOT NULL REFERENCES ARCHITECT(ArchitectId) ON DELETE CASCADE,
    Role        VARCHAR2(50),
    CONSTRAINT pk_project_architect PRIMARY KEY (ProjectId, ArchitectId)
);

-- 22. PROJECT_ENGINEER
CREATE TABLE PROJECT_ENGINEER (
    ProjectId  INT NOT NULL REFERENCES PROJECT(ProjectId) ON DELETE CASCADE,
    EngineerId INT NOT NULL REFERENCES ENGINEER(EngineerId) ON DELETE CASCADE,
    Role       VARCHAR2(50),
    CONSTRAINT pk_project_engineer PRIMARY KEY (ProjectId, EngineerId)
);

-- 23. PROJECT_MATERIAL
CREATE TABLE PROJECT_MATERIAL (
    ProjectId  INT NOT NULL REFERENCES PROJECT(ProjectId) ON DELETE CASCADE,
    MaterialId INT NOT NULL REFERENCES MATERIAL(MaterialId) ON DELETE CASCADE,
    Quantity   NUMBER(10,2) CHECK (Quantity > 0),
    TotalCost  NUMBER(15,2) CHECK (TotalCost >= 0),
    CONSTRAINT pk_project_material PRIMARY KEY (ProjectId, MaterialId)
);

-- 24. PROJECT_EQUIPMENT
CREATE TABLE PROJECT_EQUIPMENT (
    ProjectId   INT NOT NULL REFERENCES PROJECT(ProjectId) ON DELETE CASCADE,
    EquipmentId INT NOT NULL REFERENCES EQUIPMENT(EquipmentId) ON DELETE CASCADE,
    RentalStart DATE,
    RentalEnd   DATE,
    CONSTRAINT pk_project_equipment PRIMARY KEY (ProjectId, EquipmentId),
    CONSTRAINT chk_rental_dates CHECK (RentalEnd > RentalStart)
);

-- 25. TASK_EMPLOYEE
CREATE TABLE TASK_EMPLOYEE (
    TaskId     INT NOT NULL REFERENCES TASK(TaskId) ON DELETE CASCADE,
    EmployeeId INT NOT NULL REFERENCES EMPLOYEE(EmployeeId) ON DELETE CASCADE,
    CONSTRAINT pk_task_employee PRIMARY KEY (TaskId, EmployeeId)
);

-- 26. INCIDENT_EMPLOYEE
CREATE TABLE INCIDENT_EMPLOYEE (
    IncidentId INT NOT NULL REFERENCES INCIDENT(IncidentId) ON DELETE CASCADE,
    EmployeeId INT NOT NULL REFERENCES EMPLOYEE(EmployeeId) ON DELETE CASCADE,
    CONSTRAINT pk_incident_employee PRIMARY KEY (IncidentId, EmployeeId)
);

-- 27. MATERIAL_SUPPLIER_LINK
CREATE TABLE MATERIAL_SUPPLIER_LINK (
    MaterialId INT NOT NULL REFERENCES MATERIAL(MaterialId) ON DELETE CASCADE,
    SupplierId INT NOT NULL REFERENCES MATERIAL_SUPPLIER(SupplierId) ON DELETE CASCADE,
    UnitPrice  NUMBER(10,2) CHECK (UnitPrice > 0),
    LeadDays   INT CHECK (LeadDays >= 0),
    CONSTRAINT pk_material_supplier PRIMARY KEY (MaterialId, SupplierId)
);

-- 28. PERMIT_PROJECT
CREATE TABLE PERMIT_PROJECT (
    PermitId  INT NOT NULL REFERENCES PERMIT(PermitId) ON DELETE CASCADE,
    ProjectId INT NOT NULL REFERENCES PROJECT(ProjectId) ON DELETE CASCADE,
    CONSTRAINT pk_permit_project PRIMARY KEY (PermitId, ProjectId)
);


-- VIEWS


-- 1. Active Projects
CREATE VIEW v_active_projects AS
SELECT ProjectId, ProjectName, ClientId, ProjectType, StartDate, EndDate
FROM Project
WHERE Status = 'Active';

-- 2. Approved Permits
CREATE VIEW v_approved_permits AS
SELECT
    p.PermitId,
    p.PermitType,
    p.IssuedBy,
    p.IssueDate,
    p.Status
FROM PERMIT p
WHERE p.Status = 'Approved';

-- 3. Failed Inspections
CREATE OR REPLACE VIEW v_failed_inspections AS
SELECT
    InspectionId,
    SiteId,
    InspectionType,
    ConductedDate,
    Result,
    Remarks
FROM INSPECTION
WHERE Result = 'Fail';

-- 4. Critical Incidents
CREATE OR REPLACE VIEW v_critical_incidents AS
SELECT
    IncidentId,
    ProjectId,
    IncidentType,
    DateOccurred,
    Severity,
    Description,
    ReportedBy,
    ActionTaken
FROM INCIDENT
WHERE Severity IN ('High','Critical');

-- 5. Project and Client Details
CREATE VIEW v_projectnClient_details AS
SELECT
    p.ProjectId,
    p.ProjectName,
    p.ProjectType,
    p.Status,
    p.ClientId,
    c.OrganizationType,
    c.PersonId,
    pr.FullName
FROM PROJECT p
JOIN CLIENT c ON c.ClientId = p.ClientId
JOIN PERSON pr ON c.PersonId = pr.PersonId;

-- 6. Employee and Person Details
CREATE OR REPLACE VIEW v_employeeenPerson_details AS
SELECT
    e.EmployeeId,
    e.HireDate,
    e.Salary,
    e.JobTitle,
    e.Department,
    e.EmployeeType,
    p.FullName,
    p.CNIC,
    p.Phone,
    p.Email,
    p.Gender,
    p.Address
FROM EMPLOYEE e
JOIN PERSON p ON e.PersonId = p.PersonId;

-- 7. Contract Details
CREATE OR REPLACE VIEW v_contract_details AS
SELECT
    c.ContractId,
    c.ContractType,
    c.SignedDate,
    c.StartDate,
    c.EndDate,
    c.TotalValue,
    c.Status,
    p.ProjectName,
    p.ProjectType,
    con.ContractorId,
    con.Rating
FROM CONTRACT c
JOIN PROJECT p ON c.ProjectId = p.ProjectId
JOIN CONTRACTOR con ON c.ContractorId = con.ContractorId;

-- 8. Payment Summary
CREATE OR REPLACE VIEW v_payment_summary AS
SELECT
    pay.PaymentId,
    pay.Amount,
    pay.PaymentDate,
    pay.Method,
    pay.Status,
    c.ContractType,
    c.TotalValue,
    con.ContractorId,
    con.Rating
FROM PAYMENT pay
JOIN CONTRACT c ON pay.ContractId = c.ContractId
JOIN CONTRACTOR con ON pay.ContractorId = con.ContractorId;

-- 9. Project Material Cost
CREATE OR REPLACE VIEW v_project_material_cost AS
SELECT
    p.ProjectId,
    p.ProjectName,
    SUM(pm.TotalCost) AS TotalMaterialCost
FROM PROJECT p
JOIN PROJECT_MATERIAL pm ON p.ProjectId = pm.ProjectId
GROUP BY p.ProjectId, p.ProjectName;

-- 10. Contractor Payments
CREATE VIEW v_contractor_payments AS
SELECT
    pay.ContractorId,
    SUM(pay.Amount) AS TotalPayment,
    p.FullName,
    COUNT(pay.PaymentId) AS NumberOfPayments
FROM CONTRACTOR con
JOIN EMPLOYEE e ON con.EmployeeId = e.EmployeeId
JOIN PERSON p ON e.PersonId = p.PersonId
JOIN PAYMENT pay ON con.ContractorId = pay.ContractorId
GROUP BY pay.ContractorId, p.FullName;

-- =============================================
-- JOINS
-- =============================================

-- 11. Project with Site Details (INNER JOIN)
SELECT
    p.ProjectId,
    p.ProjectName,
    p.ProjectType,
    p.Status,
    s.SiteId,
    s.SiteName,
    s.SiteAddress,
    s.AreaSqMeters
FROM PROJECT p
JOIN PROJECT_SITE ps ON p.ProjectId = ps.ProjectId
JOIN SITE s ON ps.SiteId = s.SiteId;

-- 12. Employee with Subtype Details (LEFT JOIN)
SELECT
    p.FullName,
    p.Gender,
    p.Email,
    e.EmployeeId,
    e.HireDate,
    e.Salary,
    e.JobTitle,
    e.Department,
    e.EmployeeType,
    a.ArchitectId,
    a.Specialization,
    c.ContractorId,
    c.ContractType,
    c.Rating,
    engr.EngineerId,
    engr.Discipline
FROM EMPLOYEE e
JOIN PERSON p ON p.PersonId = e.PersonId
LEFT JOIN ARCHITECT a ON e.EmployeeId = a.EmployeeId
LEFT JOIN CONTRACTOR c ON e.EmployeeId = c.EmployeeId
LEFT JOIN ENGINEER engr ON e.EmployeeId = engr.EmployeeId;

--Task with Employee and Project(INNER JOIN)
SELECT 
    t.TaskId,
    t.TaskName,
    t.TaskStartDate AS TaskStart,
    t.TaskEndDate AS TaskEnd,
    t.Status AS TaskStatus,
    p.ProjectName,
    p.ProjectType,
    p.Status AS ProjectStatus,
    p.StartDate AS ProjectStart,
    p.EndDate AS ProjectEnd,
    e.EmployeeId,
    e.EmployeeType
FROM TASK t
JOIN PROJECT p ON t.ProjectId = p.ProjectId
JOIN EMPLOYEE e ON e.EmployeeId = t.EmployeeId;


-- 14. Material with Supplier and Price (INNER JOIN)
SELECT
    m.MaterialId,
    m.MaterialName,
    m.Category,
    m.Unit,
    ms.CompanyName,
    ms.ContactPerson,
    ms.Phone,
    msl.UnitPrice,
    msl.LeadDays
FROM MATERIAL m
JOIN MATERIAL_SUPPLIER_LINK msl ON m.MaterialId = msl.MaterialId
JOIN MATERIAL_SUPPLIER ms ON msl.SupplierId = ms.SupplierId;

-- 15. Permit with Associated Projects (RIGHT JOIN)
SELECT
    p.ProjectId,
    p.ProjectName,
    p.ProjectType,
    p.Status AS ProjectStatus,
    per.PermitId,
    per.PermitType,
    per.IssuedBy,
    per.IssueDate,
    per.Status AS PermitStatus
FROM PERMIT per
JOIN PERMIT_PROJECT pp ON per.PermitId = pp.PermitId
RIGHT JOIN PROJECT p ON pp.ProjectId = p.ProjectId;


-- SUBQUERIES


-- 16. Projects whose budget is above average
SELECT
    p.ProjectId,
    p.ProjectName,
    p.ProjectType,
    p.Status,
    b.TotalAllocated
FROM PROJECT p
JOIN BUDGET b ON p.ProjectId = b.ProjectId
WHERE b.TotalAllocated > (
    SELECT AVG(TotalAllocated)
    FROM BUDGET
);

-- 17. Employees involved in an incident
SELECT
    e.EmployeeId,
    e.Department,
    e.EmployeeType
FROM EMPLOYEE e
WHERE e.EmployeeId IN (
    SELECT i.EmployeeId
    FROM INCIDENT_EMPLOYEE i
);

-- 18. Materials used in more than one project
SELECT
    m.MaterialId,
    m.MaterialName,
    m.Category,
    m.Unit
FROM MATERIAL m
WHERE m.MaterialId IN (
    SELECT MaterialId
    FROM PROJECT_MATERIAL
    GROUP BY MaterialId
    HAVING COUNT(ProjectId) > 1
);

-- 19. Employee with third highest salary
SELECT
    e.EmployeeId,
    p.FullName,
    e.EmployeeType,
    e.Department,
    e.Salary
FROM EMPLOYEE e
JOIN PERSON p ON p.PersonId = e.PersonId
WHERE e.Salary = (
    SELECT MAX(Salary)
    FROM EMPLOYEE
    WHERE Salary < (
        SELECT MAX(Salary)
        FROM EMPLOYEE
        WHERE Salary < (
            SELECT MAX(Salary)
            FROM EMPLOYEE
        )
    )
);

-- 20. Contractors who have received payments
SELECT
    c.ContractorId,
    c.ContractType,
    c.Rating,
    p.FullName,
    p.Phone
FROM CONTRACTOR c
JOIN EMPLOYEE e ON c.EmployeeId = e.EmployeeId
JOIN PERSON p ON e.PersonId = p.PersonId
WHERE c.ContractorId IN (
    SELECT ContractorId
    FROM PAYMENT
);

-- 21. Projects that have no permit yet
SELECT
    p.ProjectId,
    p.ProjectName,
    p.ProjectType,
    p.Status,
    p.StartDate,
    p.EndDate
FROM PROJECT p
WHERE p.ProjectId NOT IN (
    SELECT ProjectId
    FROM PERMIT_PROJECT
);

-- =============================================
-- PROCEDURES
-- =============================================

-- 22. Add Project
CREATE OR REPLACE PROCEDURE add_project (
    P_ProjectId   IN INT,
    P_ProjectName IN VARCHAR2,
    P_ClientId    IN INT,
    P_ProjectType IN VARCHAR2,
    P_Priority    IN VARCHAR2,
    P_Status      IN VARCHAR2,
    P_StartDate   IN DATE,
    P_EndDate     IN DATE
)
IS
BEGIN
    INSERT INTO PROJECT (
        ProjectId, ProjectName, ClientId,
        ProjectType, Priority, Status, StartDate, EndDate
    )
    VALUES (
        P_ProjectId, P_ProjectName, P_ClientId,
        P_ProjectType, P_Priority, P_Status, P_StartDate, P_EndDate
    );
    COMMIT;
    DBMS_OUTPUT.PUT_LINE('Project Added Successfully');
    DBMS_OUTPUT.PUT_LINE('Project Name : ' || P_ProjectName);
    DBMS_OUTPUT.PUT_LINE('Type         : ' || P_ProjectType);
    DBMS_OUTPUT.PUT_LINE('Status       : ' || P_Status);
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
END add_project;
/

-- 23. Call add_project (valid)
BEGIN
    add_project(5, 'New Housing Scheme', 201, 'Residential', 'High', 'Planned', DATE '2024-01-01', DATE '2026-01-01');
END;
/

-- 24. Call add_project (invalid)
BEGIN
    add_project(6, 'Invalid Project', 201, 'Residential', 'High', 'Running', DATE '2024-01-01', DATE '2026-01-01');
END;
/

-- 25. Update Project Status
CREATE OR REPLACE PROCEDURE update_project_status (
    p_ProjectId IN INT,
    p_NewStatus IN VARCHAR2
)
IS
    v_OldStatus   VARCHAR2(10);
    v_ProjectName VARCHAR2(50);
BEGIN
    SELECT Status, ProjectName
    INTO v_OldStatus, v_ProjectName
    FROM PROJECT
    WHERE ProjectId = p_ProjectId;
    UPDATE PROJECT
    SET Status = p_NewStatus
    WHERE ProjectId = p_ProjectId;
    COMMIT;
    DBMS_OUTPUT.PUT_LINE('Project    : ' || v_ProjectName);
    DBMS_OUTPUT.PUT_LINE('Old Status : ' || v_OldStatus);
    DBMS_OUTPUT.PUT_LINE('New Status : ' || p_NewStatus);
    DBMS_OUTPUT.PUT_LINE('Updated Successfully');
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
END update_project_status;
/

-- 26. Call update_project_status
BEGIN
    update_project_status(1, 'Completed');
END;
/

-- 27. Assign Architect
CREATE OR REPLACE PROCEDURE assign_architect(
    v_ProjectId   IN INT,
    v_ArchitectId IN INT,
    v_Role        IN VARCHAR2
)
IS
    v_ProjectName   VARCHAR2(50);
    v_ArchitectName VARCHAR2(50);
BEGIN
    SELECT ProjectName INTO v_ProjectName
    FROM PROJECT
    WHERE ProjectId = v_ProjectId;
    SELECT p.FullName INTO v_ArchitectName
    FROM ARCHITECT a
    JOIN EMPLOYEE e ON a.EmployeeId = e.EmployeeId
    JOIN PERSON p ON e.PersonId = p.PersonId
    WHERE a.ArchitectId = v_ArchitectId;
    INSERT INTO PROJECT_ARCHITECT (ProjectId, ArchitectId, Role)
    VALUES (v_ProjectId, v_ArchitectId, v_Role);
    COMMIT;
    DBMS_OUTPUT.PUT_LINE('Architect Assigned Successfully');
    DBMS_OUTPUT.PUT_LINE('Project Name   : ' || v_ProjectName);
    DBMS_OUTPUT.PUT_LINE('Architect Name : ' || v_ArchitectName);
    DBMS_OUTPUT.PUT_LINE('Role           : ' || v_Role);
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
END assign_architect;
/

-- 28. Call assign_architect
BEGIN
    assign_architect(2, 303, 'Lead Designer');
END;
/

-- 29. Add Incident
CREATE OR REPLACE PROCEDURE add_incident(
    v_IncidentId   IN INT,
    v_ProjectId    IN INT,
    v_IncidentType IN VARCHAR2,
    v_DateOccurred IN DATE,
    v_Severity     IN VARCHAR2,
    v_Description  IN VARCHAR2,
    v_ReportedBy   IN INT,
    v_ActionTaken  IN VARCHAR2
)
IS
    v_ProjectName  VARCHAR2(50);
    v_ReporterName VARCHAR2(50);
BEGIN
    SELECT ProjectName INTO v_ProjectName
    FROM PROJECT
    WHERE ProjectId = v_ProjectId;
    SELECT p.FullName INTO v_ReporterName
    FROM PERSON p
    JOIN EMPLOYEE e ON p.PersonId = e.PersonId
    WHERE e.EmployeeId = v_ReportedBy;
    INSERT INTO INCIDENT (
        IncidentId, ProjectId, IncidentType, DateOccurred,
        Severity, Description, ReportedBy, ActionTaken
    )
    VALUES (
        v_IncidentId, v_ProjectId, v_IncidentType, v_DateOccurred,
        v_Severity, v_Description, v_ReportedBy, v_ActionTaken
    );
    COMMIT;
    DBMS_OUTPUT.PUT_LINE('Incident Reported Successfully');
    DBMS_OUTPUT.PUT_LINE('Project Name  : ' || v_ProjectName);
    DBMS_OUTPUT.PUT_LINE('Reported By   : ' || v_ReporterName);
    DBMS_OUTPUT.PUT_LINE('Incident Type : ' || v_IncidentType);
    DBMS_OUTPUT.PUT_LINE('Severity      : ' || v_Severity);
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
END add_incident;
/


-- TRIGGERS


-- 30. Prevent deleting an active contract
CREATE OR REPLACE TRIGGER prevent_active_contract_delete
BEFORE DELETE ON CONTRACT
FOR EACH ROW
BEGIN
    IF :OLD.Status = 'Active' THEN
        RAISE_APPLICATION_ERROR(-20001, 'Cannot delete an Active Contract');
    END IF;
END;
/

-- 31. Auto log critical incident
CREATE OR REPLACE TRIGGER log_critical_incident
AFTER INSERT ON INCIDENT
FOR EACH ROW
BEGIN
    IF :NEW.Severity = 'Critical' THEN
        DBMS_OUTPUT.PUT_LINE('ALERT: Critical Incident Reported on Project ' || :NEW.ProjectId);
    END IF;
END;
/

-- 32. Prevent payment status change from Completed to Pending
CREATE OR REPLACE TRIGGER prevent_payment_status_change
BEFORE UPDATE ON PAYMENT
FOR EACH ROW
BEGIN
    IF :OLD.Status = 'Completed' AND :NEW.Status = 'Pending' THEN
        RAISE_APPLICATION_ERROR(-20002, 'Cannot change Completed payment back to Pending');
    END IF;
END;
/


-- TRIGGER TESTS


-- 33. Test Trigger 1 (delete active contract)
DELETE FROM CONTRACT WHERE ContractId = 1;

-- 34. Test Trigger 2 (critical incident)
BEGIN
    add_incident(6, 1, 'Fire', DATE '2024-02-01', 'Critical', 'Fire broke out', 101, 'Fire brigade called');
END;
/

-- 35. Test Trigger 3 (payment status change)
UPDATE PAYMENT SET Status = 'Pending' WHERE PaymentId = 1;