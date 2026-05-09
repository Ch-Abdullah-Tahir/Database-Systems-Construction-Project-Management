import base64, os

desktop = os.path.join(os.path.expanduser("~"), "Desktop")

def find_image(name):
    paths = [
        os.path.join(desktop, "construction-app", name),
        os.path.join(desktop, name),
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return None

imgs = {}
for var, name in [('IMG1','Image1.jpeg'),('IMG2','Image2.jpeg'),('IMG3','Image3.jpeg'),('IMG4','Image4.jpeg')]:
    path = find_image(name)
    mime = 'jpeg'
    if path:
        with open(path,'rb') as f:
            b64 = base64.b64encode(f.read()).decode()
        imgs[var] = f'data:image/{mime};base64,{b64}'
        print(f"OK  {var} <- {path}")
    else:
        imgs[var] = ''
        print(f"MISSING {var} ({name})")

out = os.path.join(desktop, "construction-app", "src", "App.js")

header = f'''import {{ useState }} from "react";

const IMG1 = "{imgs['IMG1']}";
const IMG2 = "{imgs['IMG2']}";
const IMG3 = "{imgs['IMG3']}";
const IMG4 = "{imgs['IMG4']}";
'''

body = r"""
const TEAM = [
  { name:"Abdullah Tahir", roll:"24F-0020" },
  { name:"Muhammad Umar",  roll:"24F-0036" },
];

const SCHEMA = [
  { table:"PERSON",         cols:["PersonId PK","FullName","CNIC","DOB","Phone","Gender","Address","Email","PersonType"] },
  { table:"EMPLOYEE",       cols:["EmployeeId PK","PersonId FK","HireDate","Salary","JobTitle","Department","EmployeeType"] },
  { table:"CLIENT",         cols:["ClientId PK","PersonId FK","OrganizationType","CreditRating"] },
  { table:"ARCHITECT",      cols:["ArchitectId PK","EmployeeId FK","LicenseNo","Specialization","YearsExperience"] },
  { table:"CONTRACTOR",     cols:["ContractorId PK","EmployeeId FK","ContractType","Rating"] },
  { table:"ENGINEER",       cols:["EngineerId PK","EmployeeId FK","Discipline"] },
  { table:"SITE",           cols:["SiteId PK","SiteName","SiteAddress","AreaSqMeters"] },
  { table:"PROJECT",        cols:["ProjectId PK","ProjectName","ClientId FK","ProjectType","Priority","Status","StartDate","EndDate"] },
  { table:"CONTRACT",       cols:["ContractId PK","ProjectId FK","ContractorId FK","ContractType","SignedDate","StartDate","EndDate","TotalValue","Status"] },
  { table:"BUDGET",         cols:["BudgetId PK","ProjectId FK","TotalAllocated"] },
  { table:"MATERIAL",       cols:["MaterialId PK","MaterialName","Category","Unit"] },
  { table:"EQUIPMENT",      cols:["EquipmentId PK","EquipmentName","EquipmentType"] },
  { table:"TASK",           cols:["TaskId PK","ProjectId FK","TaskName","StartDate","EndDate","Status"] },
  { table:"PERMIT",         cols:["PermitId PK","IssuedBy","IssueDate","PermitType","Status"] },
  { table:"INSPECTION",     cols:["InspectionId PK","SiteId FK","InspectionType","ConductedDate","Result","Remarks"] },
  { table:"INCIDENT",       cols:["IncidentId PK","ProjectId FK","IncidentType","DateOccurred","Severity","Description","ReportedBy FK","ActionTaken"] },
  { table:"PAYMENT",        cols:["PaymentId PK","ContractId FK","ContractorId FK","Amount","PaymentDate","Method","Status"] },
  { table:"MATERIAL_SUPPLIER", cols:["SupplierId PK","CompanyName","ContactPerson","Phone","Email","Address","Rating"] },
  { table:"MATERIAL_ORDER", cols:["OrderId PK","SupplierId FK","ProjectId FK","OrderDate","DeliveryDate","QuantityOrdered","QuantityDelivered","TotalCost","Status"] },
  { table:"PROJECT_SITE",      cols:["ProjectId FK","SiteId FK"] },
  { table:"PROJECT_ARCHITECT", cols:["ProjectId FK","ArchitectId FK","Role"] },
  { table:"PROJECT_ENGINEER",  cols:["ProjectId FK","EngineerId FK","Role"] },
  { table:"PROJECT_MATERIAL",  cols:["ProjectId FK","MaterialId FK","Quantity","TotalCost"] },
  { table:"PROJECT_EQUIPMENT", cols:["ProjectId FK","EquipmentId FK","RentalStart","RentalEnd"] },
  { table:"TASK_EMPLOYEE",     cols:["TaskId FK","EmployeeId FK"] },
  { table:"INCIDENT_EMPLOYEE", cols:["IncidentId FK","EmployeeId FK"] },
  { table:"MATERIAL_SUPPLIER_LINK", cols:["MaterialId FK","SupplierId FK","UnitPrice","LeadDays"] },
  { table:"PERMIT_PROJECT",    cols:["PermitId FK","ProjectId FK"] },
];

const DATA = {
  PERSON: {
    cols:["PersonId","FullName","CNIC","Phone","Gender","PersonType"],
    rows:[
      [1,"Ahmed Khan","35201-1234567-1","0300-1234567","Male","Employee"],
      [2,"Sara Ali","35202-2345678-2","0301-2345678","Female","Employee"],
      [3,"Usman Tariq","35203-3456789-3","0302-3456789","Male","Employee"],
      [4,"Ayesha Malik","35204-4567890-4","0303-4567890","Female","Employee"],
      [5,"Bilal Hassan","35205-5678901-5","0304-5678901","Male","Employee"],
      [6,"Zara Ahmed","35206-6789012-6","0305-6789012","Female","Employee"],
      [7,"Omar Sheikh","35207-7890123-7","0306-7890123","Male","Client"],
      [8,"Hina Qureshi","35208-8901234-8","0307-8901234","Female","Client"],
      [9,"Tariq Mehmood","35209-9012345-9","0308-9012345","Male","Client"],
      [10,"Nadia Hussain","35210-0123456-0","0309-0123456","Female","Client"],
      [11,"Doll","35211-1234567-1","0310-1111111","Female","Employee"],
    ]
  },
  EMPLOYEE: {
    cols:["EmployeeId","PersonId","HireDate","Salary","JobTitle","Department","EmployeeType"],
    rows:[
      [101,1,"2010-01-15",85000,"Senior Architect","Design","Architect"],
      [102,2,"2012-03-20",75000,"Civil Engineer","Engineering","Engineer"],
      [103,3,"2015-06-10",70000,"Structural Engineer","Engineering","Engineer"],
      [104,4,"2011-09-05",90000,"Lead Architect","Design","Architect"],
      [105,5,"2013-11-25",80000,"Prime Contractor","Operations","Contractor"],
      [106,6,"2016-02-14",65000,"Sub Contractor","Operations","Contractor"],
      [107,11,"2020-01-01",70000,"Architect","Design","Architect"],
    ]
  },
  CLIENT: {
    cols:["ClientId","PersonId","OrganizationType","CreditRating"],
    rows:[
      [201,7,"Private","A"],
      [202,8,"Government","B"],
      [203,9,"NGO","C"],
      [204,10,"Private","A"],
    ]
  },
  ARCHITECT: {
    cols:["ArchitectId","EmployeeId","LicenseNo","Specialization","YearsExperience"],
    rows:[
      [301,101,"ARCH-001","Urban Design",14],
      [302,104,"ARCH-002","Interior Design",18],
      [303,107,"ARCH-003","Structural Design",5],
    ]
  },
  ENGINEER: {
    cols:["EngineerId","EmployeeId","Discipline"],
    rows:[
      [401,102,"Civil"],
      [402,103,"Structural"],
    ]
  },
  CONTRACTOR: {
    cols:["ContractorId","EmployeeId","ContractType","Rating"],
    rows:[
      [501,105,"Prime",4.5],
      [502,106,"Sub",3.8],
    ]
  },
  SITE: {
    cols:["SiteId","SiteName","SiteAddress","AreaSqMeters"],
    rows:[
      [1,"Lahore Central Site","Main Boulevard Lahore",5000],
      [2,"Karachi Port Site","Clifton Block 5 Karachi",8000],
      [3,"Islamabad F-10 Site","F-10 Markaz Islamabad",3000],
      [4,"Faisalabad Industrial Zone","Susan Road Faisalabad",12000],
    ]
  },
  PROJECT: {
    cols:["ProjectId","ProjectName","ClientId","ProjectType","Priority","Status","StartDate","EndDate"],
    rows:[
      [1,"Lahore Tower",201,"Commercial","High","Active","2023-01-01","2025-12-31"],
      [2,"Karachi Bridge",202,"Infrastructure","Critical","Active","2022-06-01","2026-05-31"],
      [3,"Islamabad Residencia",203,"Residential","Medium","Planned","2024-03-01","2026-02-28"],
      [4,"Faisalabad Factory",204,"Industrial","High","OnHold","2023-07-01","2025-06-30"],
      [5,"New Housing Scheme",201,"Residential","High","Planned","2024-01-01","2026-01-01"],
    ]
  },
  CONTRACT: {
    cols:["ContractId","ProjectId","ContractorId","ContractType","SignedDate","StartDate","EndDate","TotalValue","Status"],
    rows:[
      [1,1,501,"Fixed","2022-12-01","2023-01-01","2025-12-31",5000000,"Active"],
      [2,2,502,"Milestone","2022-05-01","2022-06-01","2026-05-31",8000000,"Active"],
      [3,3,501,"Fixed","2024-02-01","2024-03-01","2026-02-28",3000000,"Active"],
      [4,4,502,"Hourly","2023-06-01","2023-07-01","2025-06-30",4000000,"Active"],
    ]
  },
  BUDGET: {
    cols:["BudgetId","ProjectId","TotalAllocated"],
    rows:[
      [1,1,6000000],
      [2,2,9000000],
      [3,3,3500000],
      [4,4,4500000],
    ]
  },
  MATERIAL: {
    cols:["MaterialId","MaterialName","Category","Unit"],
    rows:[
      [1,"Portland Cement","Concrete","kg"],
      [2,"Steel Rebar","Steel","ton"],
      [3,"Timber Planks","Timber","m2"],
      [4,"Float Glass","Glass","m2"],
      [5,"Wall Paint","Finishing","litre"],
    ]
  },
  EQUIPMENT: {
    cols:["EquipmentId","EquipmentName","EquipmentType"],
    rows:[
      [1,"Tower Crane","Crane"],
      [2,"Excavator X200","Excavator"],
      [3,"Concrete Mixer","Mixer"],
      [4,"Steel Scaffold","Scaffold"],
      [5,"Bulldozer D9","Bulldozer"],
    ]
  },
  TASK: {
    cols:["TaskId","ProjectId","TaskName","StartDate","EndDate","Status"],
    rows:[
      [1,1,"Foundation Work","2023-01-01","2023-06-30","Completed"],
      [2,1,"Structural Frame","2023-07-01","2024-06-30","InProgress"],
      [3,2,"Piling Work","2022-06-01","2023-01-31","Completed"],
      [4,2,"Bridge Deck","2023-02-01","2025-01-31","InProgress"],
      [5,3,"Site Preparation","2024-03-01","2024-06-30","NotStarted"],
      [6,4,"Factory Layout","2023-07-01","2023-12-31","Delayed"],
    ]
  },
  PERMIT: {
    cols:["PermitId","IssuedBy","IssueDate","PermitType","Status"],
    rows:[
      [1,"Lahore Development Authority","2022-11-01","Building","Approved"],
      [2,"Karachi Port Authority","2022-04-01","Environmental","Approved"],
      [3,"CDA Islamabad","2024-01-01","Zoning","Pending"],
      [4,"Faisalabad Municipal","2023-05-01","Safety","Approved"],
    ]
  },
  INSPECTION: {
    cols:["InspectionId","SiteId","InspectionType","ConductedDate","Result","Remarks"],
    rows:[
      [1,1,"Structural","2023-06-25","Pass","Foundation meets standards"],
      [2,2,"Environmental","2023-01-20","Conditional","Minor drainage issues"],
      [3,3,"Safety","2024-03-15","Pass","Site safety compliant"],
      [4,4,"Electrical","2023-08-10","Fail","Wiring not up to code"],
    ]
  },
  INCIDENT: {
    cols:["IncidentId","ProjectId","IncidentType","DateOccurred","Severity","ReportedBy","ActionTaken"],
    rows:[
      [1,1,"NearMiss","2023-03-10","Medium",101,"Safety briefing conducted"],
      [2,2,"PropertyDamage","2022-09-15","High",102,"Equipment replaced"],
      [3,4,"Injury","2023-08-20","Critical",103,"Medical assistance provided"],
      [4,3,"NearMiss","2024-04-05","Low",104,"Worker retrained"],
    ]
  },
  PAYMENT: {
    cols:["PaymentId","ContractId","ContractorId","Amount","PaymentDate","Method","Status"],
    rows:[
      [1,1,501,1000000,"2023-06-30","BankTransfer","Completed"],
      [2,1,501,1500000,"2024-01-15","BankTransfer","Completed"],
      [3,2,502,2000000,"2023-06-01","Cheque","Completed"],
      [4,3,501,500000,"2024-06-30","BankTransfer","Pending"],
      [5,4,502,800000,"2024-01-01","Cash","Disputed"],
    ]
  },
  MATERIAL_SUPPLIER: {
    cols:["SupplierId","CompanyName","ContactPerson","Phone","Rating"],
    rows:[
      [1,"DG Khan Cement Co","Ali Raza","0311-1111111",4.5],
      [2,"Amreli Steels","Hassan Mirza","0312-2222222",4.8],
      [3,"Packages Timber","Imran Butt","0313-3333333",4.2],
      [4,"AGC Glass","Sana Malik","0314-4444444",4.0],
    ]
  },
  MATERIAL_ORDER: {
    cols:["OrderId","SupplierId","ProjectId","OrderDate","DeliveryDate","QuantityOrdered","QuantityDelivered","TotalCost","Status"],
    rows:[
      [1,1,1,"2023-01-05","2023-01-20",10000,10000,500000,"Delivered"],
      [2,2,2,"2022-06-05","2022-06-25",500,500,1500000,"Delivered"],
      [3,3,3,"2024-03-05","2024-03-25",2000,0,200000,"Pending"],
      [4,4,4,"2023-07-05","2023-07-20",1000,800,300000,"Partial"],
    ]
  },
  PROJECT_SITE: {
    cols:["ProjectId","SiteId"],
    rows:[
      [1,1],[2,2],[3,3],[4,4],[1,3],
    ]
  },
  PROJECT_ARCHITECT: {
    cols:["ProjectId","ArchitectId","Role"],
    rows:[
      [1,301,"Lead Designer"],
      [2,302,"Consultant"],
      [3,301,"Principal Architect"],
      [4,302,"Site Architect"],
    ]
  },
  PROJECT_ENGINEER: {
    cols:["ProjectId","EngineerId","Role"],
    rows:[
      [1,401,"Structural Lead"],
      [2,402,"Bridge Engineer"],
      [3,401,"Site Engineer"],
      [4,402,"Factory Engineer"],
    ]
  },
  PROJECT_MATERIAL: {
    cols:["ProjectId","MaterialId","Quantity","TotalCost"],
    rows:[
      [1,1,5000,250000],
      [1,2,200,600000],
      [2,2,500,1500000],
      [3,1,3000,150000],
      [4,3,1000,100000],
    ]
  },
  PROJECT_EQUIPMENT: {
    cols:["ProjectId","EquipmentId","RentalStart","RentalEnd"],
    rows:[
      [1,1,"2023-01-01","2024-06-30"],
      [2,2,"2022-06-01","2023-06-30"],
      [3,3,"2024-03-01","2024-12-31"],
      [4,5,"2023-07-01","2024-06-30"],
    ]
  },
  TASK_EMPLOYEE: {
    cols:["TaskId","EmployeeId"],
    rows:[
      [1,101],[2,101],[3,102],[4,102],[5,103],[6,104],
    ]
  },
  INCIDENT_EMPLOYEE: {
    cols:["IncidentId","EmployeeId"],
    rows:[
      [1,101],[2,102],[3,103],[4,104],
    ]
  },
  MATERIAL_SUPPLIER_LINK: {
    cols:["MaterialId","SupplierId","UnitPrice","LeadDays"],
    rows:[
      [1,1,50,15],
      [2,2,3000,20],
      [3,3,100,10],
      [4,4,300,25],
    ]
  },
  PERMIT_PROJECT: {
    cols:["PermitId","ProjectId"],
    rows:[
      [1,1],[2,2],[3,3],[4,4],
    ]
  },
};

const QUERIES = [
  {
    id:1, cat:"Views", icon:"🏗️", label:"Active Projects",
    desc:"All projects with Status = Active",
    sql:`SELECT ProjectId, ProjectName, ClientId, ProjectType, StartDate, EndDate\nFROM Project\nWHERE Status = 'Active';`,
    result:{cols:["ProjectId","ProjectName","ClientId","ProjectType","StartDate","EndDate"],rows:[[1,"Lahore Tower",201,"Commercial","2023-01-01","2025-12-31"],[2,"Karachi Bridge",202,"Infrastructure","2022-06-01","2026-05-31"]]}
  },
  {
    id:2, cat:"Views", icon:"📋", label:"Approved Permits",
    desc:"Permits with Status = Approved",
    sql:`SELECT PermitId, PermitType, IssuedBy, IssueDate, Status\nFROM PERMIT\nWHERE Status = 'Approved';`,
    result:{cols:["PermitId","PermitType","IssuedBy","IssueDate","Status"],rows:[[1,"Building","Lahore Development Authority","2022-11-01","Approved"],[2,"Environmental","Karachi Port Authority","2022-04-01","Approved"],[4,"Safety","Faisalabad Municipal","2023-05-01","Approved"]]}
  },
  {
    id:3, cat:"Views", icon:"❌", label:"Failed Inspections",
    desc:"Inspections where Result = Fail",
    sql:`SELECT InspectionId, SiteId, InspectionType, ConductedDate, Result, Remarks\nFROM INSPECTION\nWHERE Result = 'Fail';`,
    result:{cols:["InspectionId","SiteId","InspectionType","ConductedDate","Result","Remarks"],rows:[[4,4,"Electrical","2023-08-10","Fail","Wiring not up to code"]]}
  },
  {
    id:4, cat:"Views", icon:"🚨", label:"Critical Incidents",
    desc:"Incidents with Severity High or Critical",
    sql:`SELECT IncidentId, ProjectId, IncidentType, DateOccurred, Severity\nFROM INCIDENT\nWHERE Severity IN ('High','Critical');`,
    result:{cols:["IncidentId","ProjectId","IncidentType","DateOccurred","Severity"],rows:[[2,2,"PropertyDamage","2022-09-15","High"],[3,4,"Injury","2023-08-20","Critical"]]}
  },
  {
    id:5, cat:"Views", icon:"🤝", label:"Project & Client Details",
    desc:"Projects joined with client and person info",
    sql:`SELECT p.ProjectId, p.ProjectName, p.ProjectType, p.Status,\n       c.OrganizationType, pr.FullName\nFROM PROJECT p\nJOIN CLIENT c ON c.ClientId = p.ClientId\nJOIN PERSON pr ON c.PersonId = pr.PersonId;`,
    result:{cols:["ProjectId","ProjectName","ProjectType","Status","OrgType","ClientName"],rows:[[1,"Lahore Tower","Commercial","Active","Private","Omar Sheikh"],[2,"Karachi Bridge","Infrastructure","Active","Government","Hina Qureshi"],[3,"Islamabad Residencia","Residential","Planned","NGO","Tariq Mehmood"],[4,"Faisalabad Factory","Industrial","OnHold","Private","Nadia Hussain"]]}
  },
  {
    id:6, cat:"Views", icon:"👷", label:"Employee & Person Details",
    desc:"Employee info joined with personal data",
    sql:`SELECT e.EmployeeId, e.Salary, e.JobTitle, e.Department,\n       e.EmployeeType, p.FullName, p.Phone, p.Gender\nFROM EMPLOYEE e\nJOIN PERSON p ON e.PersonId = p.PersonId;`,
    result:{cols:["EmployeeId","Salary","JobTitle","Department","Type","FullName","Phone"],rows:[[101,85000,"Senior Architect","Design","Architect","Ahmed Khan","0300-1234567"],[102,75000,"Civil Engineer","Engineering","Engineer","Sara Ali","0301-2345678"],[104,90000,"Lead Architect","Design","Architect","Ayesha Malik","0303-4567890"],[105,80000,"Prime Contractor","Operations","Contractor","Bilal Hassan","0304-5678901"],[107,70000,"Architect","Design","Architect","Doll","0310-1111111"]]}
  },
  {
    id:7, cat:"Views", icon:"📝", label:"Contract Details",
    desc:"Contracts with project and contractor info",
    sql:`SELECT c.ContractId, c.ContractType, c.TotalValue, c.Status,\n       p.ProjectName, con.Rating\nFROM CONTRACT c\nJOIN PROJECT p ON c.ProjectId = p.ProjectId\nJOIN CONTRACTOR con ON c.ContractorId = con.ContractorId;`,
    result:{cols:["ContractId","ContractType","TotalValue","Status","ProjectName","Rating"],rows:[[1,"Fixed",5000000,"Active","Lahore Tower",4.5],[2,"Milestone",8000000,"Active","Karachi Bridge",3.8],[3,"Fixed",3000000,"Active","Islamabad Residencia",4.5],[4,"Hourly",4000000,"Active","Faisalabad Factory",3.8]]}
  },
  {
    id:8, cat:"Views", icon:"💰", label:"Payment Summary",
    desc:"Payments with contract and contractor details",
    sql:`SELECT pay.PaymentId, pay.Amount, pay.PaymentDate, pay.Method, pay.Status,\n       c.ContractType, con.Rating\nFROM PAYMENT pay\nJOIN CONTRACT c ON pay.ContractId = c.ContractId\nJOIN CONTRACTOR con ON pay.ContractorId = con.ContractorId;`,
    result:{cols:["PaymentId","Amount","PaymentDate","Method","Status","ContractType"],rows:[[1,1000000,"2023-06-30","BankTransfer","Completed","Fixed"],[2,1500000,"2024-01-15","BankTransfer","Completed","Fixed"],[3,2000000,"2023-06-01","Cheque","Completed","Milestone"],[4,500000,"2024-06-30","BankTransfer","Pending","Fixed"],[5,800000,"2024-01-01","Cash","Disputed","Hourly"]]}
  },
  {
    id:9, cat:"Views", icon:"🧱", label:"Project Material Cost",
    desc:"Total material cost grouped per project",
    sql:`SELECT p.ProjectId, p.ProjectName, SUM(pm.TotalCost) AS TotalMaterialCost\nFROM PROJECT p\nJOIN PROJECT_MATERIAL pm ON p.ProjectId = pm.ProjectId\nGROUP BY p.ProjectId, p.ProjectName;`,
    result:{cols:["ProjectId","ProjectName","TotalMaterialCost"],rows:[[1,"Lahore Tower",850000],[2,"Karachi Bridge",1500000],[3,"Islamabad Residencia",150000],[4,"Faisalabad Factory",100000]]}
  },
  {
    id:10, cat:"Views", icon:"💸", label:"Contractor Payments",
    desc:"Total payments received per contractor",
    sql:`SELECT pay.ContractorId, p.FullName,\n       SUM(pay.Amount) AS TotalPayment,\n       COUNT(pay.PaymentId) AS NumberOfPayments\nFROM CONTRACTOR con\nJOIN EMPLOYEE e ON con.EmployeeId = e.EmployeeId\nJOIN PERSON p ON e.PersonId = p.PersonId\nJOIN PAYMENT pay ON con.ContractorId = pay.ContractorId\nGROUP BY pay.ContractorId, p.FullName;`,
    result:{cols:["ContractorId","FullName","TotalPayment","NumberOfPayments"],rows:[[501,"Bilal Hassan",2500000,3],[502,"Zara Ahmed",2800000,2]]}
  },
  {
    id:11, cat:"Joins", icon:"🏗️", label:"Project with Site Details",
    desc:"INNER JOIN — projects linked to physical sites",
    sql:`SELECT p.ProjectId, p.ProjectName, p.ProjectType, p.Status,\n       s.SiteId, s.SiteName, s.SiteAddress, s.AreaSqMeters\nFROM PROJECT p\nJOIN PROJECT_SITE ps ON p.ProjectId = ps.ProjectId\nJOIN SITE s ON ps.SiteId = s.SiteId;`,
    result:{cols:["ProjectId","ProjectName","ProjectType","Status","SiteName","AreaSqMeters"],rows:[[1,"Lahore Tower","Commercial","Active","Lahore Central Site",5000],[2,"Karachi Bridge","Infrastructure","Active","Karachi Port Site",8000],[3,"Islamabad Residencia","Residential","Planned","Islamabad F-10 Site",3000],[4,"Faisalabad Factory","Industrial","OnHold","Faisalabad Industrial Zone",12000],[1,"Lahore Tower","Commercial","Active","Islamabad F-10 Site",3000]]}
  },
  {
    id:12, cat:"Joins", icon:"🔧", label:"Employee with Subtype Details",
    desc:"LEFT JOIN — employees with Architect/Contractor/Engineer role",
    sql:`SELECT p.FullName, e.EmployeeId, e.Salary, e.EmployeeType,\n       a.Specialization, c.ContractType, c.Rating, engr.Discipline\nFROM EMPLOYEE e\nJOIN PERSON p ON p.PersonId = e.PersonId\nLEFT JOIN ARCHITECT a ON e.EmployeeId = a.EmployeeId\nLEFT JOIN CONTRACTOR c ON e.EmployeeId = c.EmployeeId\nLEFT JOIN ENGINEER engr ON e.EmployeeId = engr.EmployeeId;`,
    result:{cols:["FullName","EmployeeId","Salary","Type","Specialization","ContractType","Discipline"],rows:[["Ahmed Khan",101,85000,"Architect","Urban Design",null,null],["Sara Ali",102,75000,"Engineer",null,null,"Civil"],["Bilal Hassan",105,80000,"Contractor",null,"Prime",null],["Zara Ahmed",106,65000,"Contractor",null,"Sub",null],["Doll",107,70000,"Architect","Structural Design",null,null]]}
  },
  {
    id:13, cat:"Joins", icon:"✅", label:"Task with Employee & Project",
    desc:"INNER JOIN — tasks with assigned employees and project",
    sql:`SELECT t.TaskId, t.TaskName, t.Status AS TaskStatus,\n       p.ProjectName, e.EmployeeType\nFROM TASK t\nJOIN PROJECT p ON t.ProjectId = p.ProjectId\nJOIN TASK_EMPLOYEE te ON t.TaskId = te.TaskId\nJOIN EMPLOYEE e ON e.EmployeeId = te.EmployeeId;`,
    result:{cols:["TaskId","TaskName","TaskStatus","ProjectName","EmployeeType"],rows:[[1,"Foundation Work","Completed","Lahore Tower","Architect"],[2,"Structural Frame","InProgress","Lahore Tower","Architect"],[3,"Piling Work","Completed","Karachi Bridge","Engineer"],[6,"Factory Layout","Delayed","Faisalabad Factory","Architect"]]}
  },
  {
    id:14, cat:"Joins", icon:"📦", label:"Material with Supplier & Price",
    desc:"INNER JOIN — materials with supplier company and unit price",
    sql:`SELECT m.MaterialName, m.Category, m.Unit,\n       ms.CompanyName, ms.ContactPerson, msl.UnitPrice, msl.LeadDays\nFROM MATERIAL m\nJOIN MATERIAL_SUPPLIER_LINK msl ON m.MaterialId = msl.MaterialId\nJOIN MATERIAL_SUPPLIER ms ON msl.SupplierId = ms.SupplierId;`,
    result:{cols:["MaterialName","Category","Unit","CompanyName","UnitPrice","LeadDays"],rows:[["Portland Cement","Concrete","kg","DG Khan Cement Co",50,15],["Steel Rebar","Steel","ton","Amreli Steels",3000,20],["Timber Planks","Timber","m2","Packages Timber",100,10],["Float Glass","Glass","m2","AGC Glass",300,25]]}
  },
  {
    id:15, cat:"Joins", icon:"🪪", label:"Permit with Associated Projects",
    desc:"RIGHT JOIN — all projects with their permit if any",
    sql:`SELECT p.ProjectId, p.ProjectName, p.Status AS ProjectStatus,\n       per.PermitType, per.IssuedBy, per.Status AS PermitStatus\nFROM PERMIT per\nJOIN PERMIT_PROJECT pp ON per.PermitId = pp.PermitId\nRIGHT JOIN PROJECT p ON pp.ProjectId = p.ProjectId;`,
    result:{cols:["ProjectId","ProjectName","ProjectStatus","PermitType","IssuedBy","PermitStatus"],rows:[[1,"Lahore Tower","Active","Building","Lahore Dev Authority","Approved"],[2,"Karachi Bridge","Active","Environmental","Karachi Port Authority","Approved"],[3,"Islamabad Residencia","Planned","Zoning","CDA Islamabad","Pending"],[4,"Faisalabad Factory","OnHold","Safety","Faisalabad Municipal","Approved"],[5,"New Housing Scheme","Planned",null,null,null]]}
  },
  {
    id:16, cat:"Subqueries", icon:"📈", label:"Above-Average Budget Projects",
    desc:"Projects whose budget exceeds the average allocation",
    sql:`SELECT p.ProjectId, p.ProjectName, p.ProjectType, p.Status, b.TotalAllocated\nFROM PROJECT p\nJOIN BUDGET b ON p.ProjectId = b.ProjectId\nWHERE b.TotalAllocated > (SELECT AVG(TotalAllocated) FROM BUDGET);`,
    result:{cols:["ProjectId","ProjectName","ProjectType","Status","TotalAllocated"],rows:[[2,"Karachi Bridge","Infrastructure","Active",9000000],[4,"Faisalabad Factory","Industrial","OnHold",4500000]]}
  },
  {
    id:17, cat:"Subqueries", icon:"⚠️", label:"Employees in an Incident",
    desc:"Employees who appear in any incident record",
    sql:`SELECT e.EmployeeId, e.Department, e.EmployeeType\nFROM EMPLOYEE e\nWHERE e.EmployeeId IN (SELECT EmployeeId FROM INCIDENT_EMPLOYEE);`,
    result:{cols:["EmployeeId","Department","EmployeeType"],rows:[[101,"Design","Architect"],[102,"Engineering","Engineer"],[103,"Engineering","Engineer"],[104,"Design","Architect"]]}
  },
  {
    id:18, cat:"Subqueries", icon:"🔁", label:"Materials in Multiple Projects",
    desc:"Materials used in more than one project",
    sql:`SELECT m.MaterialId, m.MaterialName, m.Category, m.Unit\nFROM MATERIAL m\nWHERE m.MaterialId IN (\n    SELECT MaterialId FROM PROJECT_MATERIAL\n    GROUP BY MaterialId HAVING COUNT(ProjectId) > 1\n);`,
    result:{cols:["MaterialId","MaterialName","Category","Unit"],rows:[[1,"Portland Cement","Concrete","kg"],[2,"Steel Rebar","Steel","ton"]]}
  },
  {
    id:19, cat:"Subqueries", icon:"🥉", label:"3rd Highest Salary Employee",
    desc:"The employee earning the third highest salary",
    sql:`SELECT e.EmployeeId, p.FullName, e.EmployeeType, e.Department, e.Salary\nFROM EMPLOYEE e JOIN PERSON p ON p.PersonId = e.PersonId\nWHERE e.Salary = (\n    SELECT MAX(Salary) FROM EMPLOYEE\n    WHERE Salary < (\n        SELECT MAX(Salary) FROM EMPLOYEE\n        WHERE Salary < (SELECT MAX(Salary) FROM EMPLOYEE)\n    )\n);`,
    result:{cols:["EmployeeId","FullName","EmployeeType","Department","Salary"],rows:[[105,"Bilal Hassan","Contractor","Operations",80000]]}
  },
  {
    id:20, cat:"Subqueries", icon:"💳", label:"Contractors with Payments",
    desc:"Contractors who have received at least one payment",
    sql:`SELECT c.ContractorId, c.ContractType, c.Rating, p.FullName, p.Phone\nFROM CONTRACTOR c\nJOIN EMPLOYEE e ON c.EmployeeId = e.EmployeeId\nJOIN PERSON p ON e.PersonId = p.PersonId\nWHERE c.ContractorId IN (SELECT ContractorId FROM PAYMENT);`,
    result:{cols:["ContractorId","ContractType","Rating","FullName","Phone"],rows:[[501,"Prime",4.5,"Bilal Hassan","0304-5678901"],[502,"Sub",3.8,"Zara Ahmed","0305-6789012"]]}
  },
  {
    id:21, cat:"Subqueries", icon:"🚫", label:"Projects Without a Permit",
    desc:"Projects that have no permit assigned yet",
    sql:`SELECT p.ProjectId, p.ProjectName, p.ProjectType, p.Status, p.StartDate, p.EndDate\nFROM PROJECT p\nWHERE p.ProjectId NOT IN (SELECT ProjectId FROM PERMIT_PROJECT);`,
    result:{cols:["ProjectId","ProjectName","ProjectType","Status","StartDate","EndDate"],rows:[[5,"New Housing Scheme","Residential","Planned","2024-01-01","2026-01-01"]]}
  },
  {
    id:22, cat:"Procedures", icon:"➕", label:"Add Project",
    desc:"add_project — inserts a new project record",
    sql:`BEGIN\n    add_project(\n        5, 'New Housing Scheme', 201,\n        'Residential', 'High', 'Planned',\n        DATE '2024-01-01', DATE '2026-01-01'\n    );\nEND;\n/`,
    result:{cols:["Output"],rows:[["Project Added Successfully"],["Project Name : New Housing Scheme"],["Type         : Residential"],["Status       : Planned"]]}
  },
  {
    id:23, cat:"Procedures", icon:"🔄", label:"Update Project Status",
    desc:"update_project_status — changes a project status by ID",
    sql:`BEGIN\n    update_project_status(1, 'Completed');\nEND;\n/`,
    result:{cols:["Output"],rows:[["Project    : Lahore Tower"],["Old Status : Active"],["New Status : Completed"],["Updated Successfully"]]}
  },
  {
    id:24, cat:"Procedures", icon:"📐", label:"Assign Architect",
    desc:"assign_architect — assigns an architect to a project with a role",
    sql:`BEGIN\n    assign_architect(2, 303, 'Lead Designer');\nEND;\n/`,
    result:{cols:["Output"],rows:[["Architect Assigned Successfully"],["Project Name   : Karachi Bridge"],["Architect Name : Doll"],["Role           : Lead Designer"]]}
  },
  {
    id:25, cat:"Procedures", icon:"🔥", label:"Add Incident",
    desc:"add_incident — logs a critical site incident",
    sql:`BEGIN\n    add_incident(\n        6, 1, 'Fire', DATE '2024-02-01',\n        'Critical', 'Fire broke out',\n        101, 'Fire brigade called'\n    );\nEND;\n/`,
    result:{cols:["Output"],rows:[["Incident Reported Successfully"],["Project Name  : Lahore Tower"],["Reported By   : Ahmed Khan"],["Incident Type : Fire"],["Severity      : Critical"]]}
  },
  {
    id:26, cat:"Triggers", icon:"🔒", label:"Prevent Active Contract Delete",
    desc:"BEFORE DELETE — blocks deletion of any Active contract",
    sql:`DELETE FROM CONTRACT WHERE ContractId = 1;`,
    result:{cols:["Output"],rows:[["ERROR at line 1:"],["ORA-20001: Cannot delete an Active Contract"],["ORA-06512: at trigger PREVENT_ACTIVE_CONTRACT_DELETE"],["Rollback complete."]]}
  },
  {
    id:27, cat:"Triggers", icon:"🚒", label:"Auto Log Critical Incident",
    desc:"AFTER INSERT — prints alert when a Critical incident is inserted",
    sql:`BEGIN\n    add_incident(6, 1, 'Fire', DATE '2024-02-01',\n        'Critical', 'Fire broke out', 101, 'Fire brigade called');\nEND;\n/`,
    result:{cols:["Output"],rows:[["Incident Reported Successfully"],["ALERT: Critical Incident Reported on Project 1"],[">> Trigger log_critical_incident fired"]]}
  },
  {
    id:28, cat:"Triggers", icon:"⛔", label:"Prevent Payment Status Reversal",
    desc:"BEFORE UPDATE — blocks reverting Completed payment to Pending",
    sql:`UPDATE PAYMENT SET Status = 'Pending' WHERE PaymentId = 1;`,
    result:{cols:["Output"],rows:[["ERROR at line 1:"],["ORA-20002: Cannot change Completed payment back to Pending"],["ORA-06512: at trigger PREVENT_PAYMENT_STATUS_CHANGE"],["Rollback complete."]]}
  },
];

const CATS = ["Views","Joins","Subqueries","Procedures","Triggers"];
const CAT_COLOR = { Views:"#F5C518", Joins:"#4CAF7D", Subqueries:"#5B9BD5", Procedures:"#E8732A", Triggers:"#E05555" };
const CAT_ICON  = { Views:"👁️", Joins:"🔗", Subqueries:"🔍", Procedures:"⚙️", Triggers:"⚡" };

function Tape() {
  return <div style={{height:14,background:"repeating-linear-gradient(90deg,#F5C518 0,#F5C518 34px,#111 34px,#111 68px)"}}/>;
}

function SQLBox({ sql }) {
  const KW = new Set("SELECT FROM WHERE JOIN LEFT RIGHT INNER ON AND OR NOT IN GROUP BY HAVING ORDER INSERT INTO VALUES UPDATE SET DELETE BEGIN END CREATE REPLACE PROCEDURE TRIGGER VIEW AS COUNT SUM AVG MAX MIN COMMIT ROLLBACK IF THEN DATE INT VARCHAR2 NUMBER PRIMARY KEY UNIQUE CHECK NULL".split(" "));
  return (
    <pre style={{margin:0,padding:"14px 16px",background:"#060402",borderRadius:6,fontSize:12,lineHeight:1.85,fontFamily:"'Courier New',monospace",overflowX:"auto",whiteSpace:"pre-wrap",wordBreak:"break-word",border:"1px solid #1e1208"}}>
      {sql.split(/(\s+|[(),;]|--[^\n]*)/).map((p,i)=>{
        if(p.startsWith("--")) return <span key={i} style={{color:"#6a9955",fontStyle:"italic"}}>{p}</span>;
        if(/^'[^']*'$/.test(p)) return <span key={i} style={{color:"#ce9178"}}>{p}</span>;
        if(KW.has(p.trim().toUpperCase())&&p.trim()) return <span key={i} style={{color:"#F5C518",fontWeight:"bold"}}>{p}</span>;
        if(/^\d+$/.test(p.trim())&&p.trim()) return <span key={i} style={{color:"#b5cea8"}}>{p}</span>;
        return <span key={i} style={{color:"#d4bfa0"}}>{p}</span>;
      })}
    </pre>
  );
}

function ResultTable({ result }) {
  if(!result) return null;
  const isLog = result.cols.length===1 && result.cols[0]==="Output";
  return (
    <div style={{marginTop:10,overflowX:"auto"}}>
      {isLog ? (
        <div style={{background:"#0a0a0a",border:"1px solid #2a2a2a",borderRadius:6,padding:"12px 14px",fontFamily:"monospace",fontSize:12}}>
          {result.rows.map((r,i)=>(
            <div key={i} style={{color:r[0].startsWith("ERROR")||r[0].startsWith("ORA")||r[0].startsWith("Rollback")?"#E05555":r[0].startsWith("ALERT")?"#F5C518":r[0].startsWith(">>")?"#5B9BD5":"#4CAF7D",lineHeight:1.9}}>{r[0]}</div>
          ))}
        </div>
      ):(
        <table style={{width:"100%",borderCollapse:"collapse",fontSize:12}}>
          <thead><tr>{result.cols.map(c=><th key={c} style={{padding:"7px 10px",background:"#1e1208",color:"#F5C518",textAlign:"left",fontSize:10,letterSpacing:"0.08em",textTransform:"uppercase",borderBottom:"1px solid #2a1a08"}}>{c}</th>)}</tr></thead>
          <tbody>{result.rows.map((row,i)=>(
            <tr key={i} style={{background:i%2===0?"#0e0904":"#120c06"}}>
              {row.map((cell,j)=>(
                <td key={j} style={{padding:"7px 10px",color:cell===null?"#3d2810":cell==="Fail"||cell==="Rejected"||cell==="Terminated"?"#E05555":cell==="Pass"||cell==="Approved"||cell==="Completed"?"#4CAF7D":cell==="Pending"||cell==="Conditional"?"#F5C518":"#c8b08a",borderBottom:"1px solid #1a1208",whiteSpace:"nowrap"}}>
                  {cell===null?"—":String(cell)}
                </td>
              ))}
            </tr>
          ))}</tbody>
        </table>
      )}
    </div>
  );
}

function LandingPage({ setPage }) {
  return (
    <div>
      {/* HERO — IMG1 as full background, clearly visible */}
      <div style={{position:"relative",minHeight:"95vh",overflow:"hidden",display:"flex",alignItems:"flex-end"}}>
        <img src={IMG1} alt="Construction site" style={{position:"absolute",inset:0,width:"100%",height:"100%",objectFit:"cover",objectPosition:"center"}}/>
        {/* light gradient only at bottom for text readability */}
        <div style={{position:"absolute",top:0,left:0,right:0,bottom:0,background:"linear-gradient(to top,rgba(8,4,0,0.92) 0%,rgba(8,4,0,0.3) 50%,rgba(8,4,0,0.05) 100%)"}}/>
        <div style={{position:"relative",zIndex:2,padding:"0 60px 70px",maxWidth:700}}>
          <div style={{fontSize:10,letterSpacing:"0.3em",color:"#F5C518",textTransform:"uppercase",marginBottom:14}}>Construction System · Oracle SQL · 2026</div>
          <h1 style={{fontSize:62,fontWeight:900,color:"#fff",margin:"0 0 12px",lineHeight:1.0,fontFamily:"'Georgia',serif",textShadow:"0 2px 20px rgba(0,0,0,0.8)"}}>
            Construction<br/><span style={{color:"#F5C518"}}>System</span>
          </h1>
          <p style={{fontSize:15,color:"#d0b080",lineHeight:1.8,margin:"0 0 36px",textShadow:"0 1px 8px rgba(0,0,0,0.8)"}}>
            A complete Oracle SQL project featuring 28 tables,<br/>views, joins, subqueries, stored procedures and triggers.
          </p>
          <div style={{display:"flex",gap:14,marginBottom:36}}>
            {TEAM.map(m=>(
              <div key={m.roll} style={{background:"rgba(245,197,24,0.15)",border:"1px solid #F5C51860",borderRadius:8,padding:"10px 18px",backdropFilter:"blur(4px)"}}>
                <div style={{fontSize:13,fontWeight:"bold",color:"#fff"}}>{m.name}</div>
                <div style={{fontSize:10,color:"#F5C518",letterSpacing:"0.1em",marginTop:2}}>{m.roll}</div>
              </div>
            ))}
          </div>
          <div style={{display:"flex",gap:12,flexWrap:"wrap"}}>
            {[["Schema","🗂️"],["Queries","📊"]].map(([p,ic])=>(
              <button key={p} onClick={()=>setPage(p)} style={{background:"#F5C518",color:"#080400",border:"none",padding:"13px 28px",borderRadius:6,fontSize:14,fontWeight:"bold",cursor:"pointer",fontFamily:"inherit",letterSpacing:"0.06em"}}>{ic} View {p}</button>
            ))}
          </div>
        </div>
      </div>

      {/* 3 IMAGE ROW — bright, large, clearly visible */}
      <div style={{background:"#060402",padding:"24px 32px",display:"grid",gridTemplateColumns:"1fr 1fr 1fr",gap:12}}>
        {[
          {img:IMG2,caption:"Structure Phase"},
          {img:IMG3,caption:"On Site"},
          {img:IMG4,caption:"Final Phase"},
        ].map((s,i)=>(
          <div key={i} style={{position:"relative",height:220,borderRadius:8,overflow:"hidden",border:"1px solid #2a1a08"}}>
            <img src={s.img} alt={s.caption} style={{width:"100%",height:"100%",objectFit:"cover"}}/>
            <div style={{position:"absolute",bottom:0,left:0,right:0,background:"linear-gradient(transparent,rgba(0,0,0,0.7)",padding:"28px 14px 12px",fontSize:12,color:"#F5C518",letterSpacing:"0.1em",textTransform:"uppercase",fontWeight:"bold"}}>{s.caption}</div>
          </div>
        ))}
      </div>

      {/* STATS */}
      <div style={{background:"#080500",padding:"36px 60px",display:"grid",gridTemplateColumns:"repeat(5,1fr)",gap:12}}>
        {CATS.map(c=>{
          const col=CAT_COLOR[c];
          return (
            <div key={c} onClick={()=>setPage("Queries",c)} style={{background:"#100800",border:`1px solid ${col}30`,borderTop:`3px solid ${col}`,borderRadius:7,padding:"20px 14px",textAlign:"center",cursor:"pointer"}}>
              <div style={{fontSize:9,color:col,letterSpacing:"0.15em",textTransform:"uppercase",marginBottom:6}}>{CAT_ICON[c]}</div>
              <div style={{fontSize:28,fontWeight:900,color:col,fontFamily:"'Georgia',serif"}}>{QUERIES.filter(q=>q.cat===c).length}</div>
              <div style={{fontSize:10,color:"#4a3018",letterSpacing:"0.1em",textTransform:"uppercase",marginTop:4}}>{c}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function SchemaPage() {
  const [active,setActive]=useState(null);
  return (
    <div style={{background:"#060402",minHeight:"100vh"}}>
      {/* HEADER with IMG2 — fully visible */}
      <div style={{position:"relative",height:260,overflow:"hidden"}}>
        <img src={IMG2} alt="structure" style={{width:"100%",height:"100%",objectFit:"cover",objectPosition:"center"}}/>
        <div style={{position:"absolute",inset:0,background:"linear-gradient(to top,rgba(6,4,2,0.95) 0%,rgba(6,4,2,0.2) 60%)"}}/>
        <div style={{position:"absolute",bottom:0,left:0,right:0,padding:"0 60px 28px"}}>
          <div style={{fontSize:9,letterSpacing:"0.28em",color:"#F5C518",textTransform:"uppercase",marginBottom:8}}>Database Blueprint</div>
          <h2 style={{fontSize:36,fontWeight:900,color:"#fff",margin:0,fontFamily:"'Georgia',serif"}}>Schema <span style={{color:"#F5C518"}}>& Stored Data</span></h2>
          <p style={{fontSize:12,color:"#a08060",margin:"6px 0 0"}}>{SCHEMA.length} tables · Click any table to see its data</p>
        </div>
      </div>
      <div style={{padding:"28px 40px",display:"grid",gridTemplateColumns:"repeat(auto-fill,minmax(220px,1fr))",gap:10}}>
        {SCHEMA.map(t=>{
          const hasData=!!DATA[t.table];
          const isOpen=active===t.table;
          return (
            <div key={t.table} style={{background:isOpen?"#160e06":"#0e0904",border:isOpen?"1.5px solid #F5C518":"1px solid #1e1208",borderRadius:7,overflow:"hidden"}}>
              <div onClick={()=>setActive(isOpen?null:t.table)} style={{cursor:"pointer",padding:"12px 14px"}}>
                <div style={{display:"flex",alignItems:"center",justifyContent:"space-between",marginBottom:8}}>
                  <span style={{fontSize:11,fontWeight:"bold",color:"#F5C518",fontFamily:"monospace",letterSpacing:"0.05em"}}>{t.table}</span>
                  <span style={{fontSize:10,color:"#3d2810"}}>{isOpen?"▲":"▼"} {hasData?"📊":""}</span>
                </div>
                <div style={{display:"flex",flexWrap:"wrap",gap:4}}>
                  {t.cols.map(c=>(
                    <span key={c} style={{fontSize:9,padding:"2px 6px",borderRadius:3,background:c.includes("PK")?"#F5C51820":c.includes("FK")?"#5B9BD520":"#1e1208",color:c.includes("PK")?"#F5C518":c.includes("FK")?"#5B9BD5":"#5a3e20",fontFamily:"monospace"}}>{c}</span>
                  ))}
                </div>
              </div>
              {isOpen && hasData && (
                <div style={{padding:"0 14px 14px",overflowX:"auto"}}>
                  <table style={{width:"100%",borderCollapse:"collapse",fontSize:10}}>
                    <thead><tr>{DATA[t.table].cols.map(c=><th key={c} style={{padding:"5px 8px",background:"#1e1208",color:"#F5C518",textAlign:"left",borderBottom:"1px solid #2a1a08"}}>{c}</th>)}</tr></thead>
                    <tbody>{DATA[t.table].rows.map((row,i)=>(
                      <tr key={i} style={{background:i%2===0?"#0a0602":"#0e0904"}}>
                        {row.map((cell,j)=><td key={j} style={{padding:"5px 8px",color:"#9a7a50",borderBottom:"1px solid #0e0904",whiteSpace:"nowrap"}}>{String(cell)}</td>)}
                      </tr>
                    ))}</tbody>
                  </table>
                </div>
              )}
              {isOpen && !hasData && (
                <div style={{padding:"10px 14px 14px",fontSize:11,color:"#3d2810",fontStyle:"italic"}}>No data inserted for this table</div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

function QueriesPage({ initialCat }) {
  const [cat,setCat]=useState(initialCat||"Views");
  const [open,setOpen]=useState(null);
  const [tab,setTab]=useState({});
  const [copied,setCopied]=useState(false);
  const items=QUERIES.filter(q=>q.cat===cat);
  const accent=CAT_COLOR[cat];
  function copy(sql,e){e.stopPropagation();navigator.clipboard.writeText(sql);setCopied(true);setTimeout(()=>setCopied(false),2000);}
  function getTab(id){return tab[id]||"sql";}
  function setTabFor(id,t,e){e.stopPropagation();setTab(prev=>({...prev,[id]:t}));}
  return (
    <div style={{background:"#060402",minHeight:"100vh"}}>
      {/* HEADER with IMG3 — fully visible */}
      <div style={{position:"relative",height:240,overflow:"hidden"}}>
        <img src={IMG3} alt="onsite" style={{width:"100%",height:"100%",objectFit:"cover",objectPosition:"center"}}/>
        <div style={{position:"absolute",inset:0,background:"linear-gradient(to top,rgba(6,4,2,0.95) 0%,rgba(6,4,2,0.15) 60%)"}}/>
        <div style={{position:"absolute",bottom:0,left:0,right:0,padding:"0 60px 24px"}}>
          <div style={{fontSize:9,letterSpacing:"0.25em",color:accent,textTransform:"uppercase",marginBottom:6}}>Query Operations</div>
          <h2 style={{fontSize:32,fontWeight:900,color:"#fff",margin:0,fontFamily:"'Georgia',serif"}}>{cat} <span style={{color:accent}}>SQL</span></h2>
        </div>
      </div>
      <div style={{background:"#0a0602",borderBottom:"1px solid #1e1208",padding:"0 40px",display:"flex",gap:0,flexWrap:"wrap"}}>
        {CATS.map(c=>(
          <button key={c} onClick={()=>{setCat(c);setOpen(null);}} style={{background:"none",border:"none",fontFamily:"inherit",padding:"14px 16px",fontSize:12,color:cat===c?CAT_COLOR[c]:"#4a3018",borderBottom:cat===c?`2px solid ${CAT_COLOR[c]}`:"2px solid transparent",cursor:"pointer",letterSpacing:"0.05em",fontWeight:cat===c?"bold":"normal"}}>{CAT_ICON[c]} {c} <span style={{fontSize:10,opacity:0.6}}>({QUERIES.filter(q=>q.cat===c).length})</span></button>
        ))}
      </div>
      <div style={{padding:"24px 40px",display:"grid",gridTemplateColumns:"repeat(auto-fill,minmax(340px,1fr))",gap:14}}>
        {items.map(q=>{
          const isOpen=open===q.id;
          const currentTab=getTab(q.id);
          return (
            <div key={q.id} style={{background:isOpen?"#160e06":"#0e0904",border:isOpen?`2px solid ${accent}`:"1px solid #1a1208",borderRadius:8,overflow:"hidden"}}>
              <div onClick={()=>setOpen(isOpen?null:q.id)} style={{padding:"14px 16px",cursor:"pointer"}}>
                <div style={{display:"flex",alignItems:"center",gap:10}}>
                  <span style={{fontSize:22,flexShrink:0}}>{q.icon}</span>
                  <div style={{flex:1}}>
                    <div style={{fontSize:14,fontWeight:"bold",color:"#f0ddb0",marginBottom:2}}>{q.label}</div>
                    <div style={{fontSize:11,color:"#3d2810"}}>{q.desc}</div>
                  </div>
                  <div style={{fontSize:10,fontFamily:"monospace",color:"#2a1a08",flexShrink:0}}>#{String(q.id).padStart(2,"0")}</div>
                  <div style={{fontSize:12,color:accent,flexShrink:0}}>{isOpen?"▲":"▼"}</div>
                </div>
              </div>
              {isOpen && (
                <div style={{borderTop:"1px solid #1e1208",padding:"0 16px 16px"}} onClick={e=>e.stopPropagation()}>
                  <div style={{display:"flex",gap:0,margin:"12px 0 10px",borderBottom:"1px solid #1e1208"}}>
                    {["sql","result"].map(t=>(
                      <button key={t} onClick={e=>setTabFor(q.id,t,e)} style={{background:"none",border:"none",fontFamily:"inherit",padding:"7px 14px",fontSize:11,cursor:"pointer",color:currentTab===t?accent:"#3d2810",borderBottom:currentTab===t?`2px solid ${accent}`:"2px solid transparent",letterSpacing:"0.06em",textTransform:"uppercase"}}>{t==="sql"?"⌨️ SQL":"📊 Output"}</button>
                    ))}
                    <div style={{marginLeft:"auto",display:"flex",alignItems:"center"}}>
                      <button onClick={e=>copy(q.sql,e)} style={{background:copied?"#4CAF7D":"transparent",border:`1px solid ${copied?"#4CAF7D":accent}`,color:copied?"#060402":accent,borderRadius:4,padding:"4px 12px",fontSize:10,cursor:"pointer",fontFamily:"inherit",fontWeight:"bold"}}>{copied?"✅ Copied":"📋 Copy"}</button>
                    </div>
                  </div>
                  {currentTab==="sql"?<SQLBox sql={q.sql}/>:<ResultTable result={q.result}/>}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

function Nav({ page,setPage }) {
  return (
    <nav style={{background:"#060402",borderBottom:"2px solid #F5C518",display:"flex",alignItems:"center",padding:"0 40px",position:"sticky",top:0,zIndex:200}}>
      <div onClick={()=>setPage("Home")} style={{display:"flex",alignItems:"center",gap:10,padding:"12px 20px 12px 0",borderRight:"1px solid #1e1208",marginRight:20,cursor:"pointer",flexShrink:0}}>
        <span style={{fontSize:28}}>🏗️</span>
        <div>
          <div style={{fontSize:8,letterSpacing:"0.25em",color:"#F5C518",textTransform:"uppercase"}}>DB Project 2026</div>
          <div style={{fontSize:12,fontWeight:"bold",color:"#f5e8cc"}}>Construction System</div>
        </div>
      </div>
      {[["Home","🏠"],["Schema","🗂️"],["Queries","📊"]].map(([p,ic])=>(
        <button key={p} onClick={()=>setPage(p)} style={{background:"none",border:"none",fontFamily:"inherit",padding:"16px 14px",fontSize:12,fontWeight:page===p?"bold":"normal",color:page===p?"#F5C518":"#4a3018",borderBottom:page===p?"2px solid #F5C518":"2px solid transparent",cursor:"pointer",letterSpacing:"0.05em"}}>{ic} {p}</button>
      ))}
      <div style={{marginLeft:"auto",display:"flex",gap:12,alignItems:"center"}}>
        {TEAM.map(m=>(
          <div key={m.roll} style={{fontSize:10,textAlign:"right"}}>
            <div style={{color:"#f5e8cc",fontWeight:"bold"}}>{m.name}</div>
            <div style={{color:"#F5C518",letterSpacing:"0.08em"}}>{m.roll}</div>
          </div>
        ))}
        <span style={{fontSize:20,marginLeft:6}}>🪖</span>
      </div>
    </nav>
  );
}

export default function App() {
  const [page,setPage]=useState("Home");
  const [initCat,setInitCat]=useState("Views");
  function goPage(p,cat){setPage(p);if(cat)setInitCat(cat);}
  return (
    <div style={{minHeight:"100vh",background:"#060402",fontFamily:"'Georgia',serif",color:"#f5e8cc"}}>
      <style>{`*{box-sizing:border-box;margin:0;padding:0;}button:hover{opacity:0.85;}::-webkit-scrollbar{width:5px;background:#040300;}::-webkit-scrollbar-thumb{background:#1e1208;border-radius:3px;}`}</style>
      <div style={{height:14,background:"repeating-linear-gradient(90deg,#F5C518 0,#F5C518 34px,#111 34px,#111 68px)"}}/>
      <Nav page={page} setPage={goPage}/>
      {page==="Home"   && <LandingPage setPage={goPage}/>}
      {page==="Schema" && <SchemaPage/>}
      {page==="Queries"&& <QueriesPage initialCat={initCat}/>}
      <div style={{height:14,background:"repeating-linear-gradient(90deg,#F5C518 0,#F5C518 34px,#111 34px,#111 68px)"}}/>
      <footer style={{background:"#040300",padding:"14px 60px",display:"flex",justifyContent:"space-between",alignItems:"center",borderTop:"1px solid #1e1208"}}>
        <div>{TEAM.map(m=><span key={m.roll} style={{fontSize:10,color:"#2a1a08",marginRight:20}}>{m.name} · {m.roll}</span>)}</div>
        <div style={{fontSize:16}}>🏗️ 🪖 🚧 🦺 ⚙️</div>
        <div style={{fontSize:10,color:"#2a1a08"}}>Construction System · Database Project · 2026</div>
      </footer>
    </div>
  );
}
"""

content = header + body

with open(out, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nDone! Written to {out}")
print(f"{len(content):,} characters")
print("\nNow run:  npm start")
