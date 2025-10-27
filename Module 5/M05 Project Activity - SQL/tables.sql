--SQLITE

--Start new transaction
BEGIN TRANSACTION;

--Create all tables needed for the database
CREATE TABLE Customer(CustomerID INTEGER NOT NULL UNIQUE
, CustomerFirstName VARCHAR(35)
, CustomerLastName VARCHAR(35)
, CompanyName VARCHAR(35)
, PhoneNumber VARCHAR(10)
, Email VARCHAR(35)
, Address VARCHAR(35)
, DateOfBirth DATE
, IdentityVerified VARCHAR(3)
, VendorID INTEGER
, PRIMARY KEY (CustomerID)
, FOREIGN KEY (VendorID) REFERENCES Vendor(VendorID) ON UPDATE CASCADE);

CREATE TABLE Spaceship(SpaceshipID INTEGER NOT NULL UNIQUE
, SerialNumber VARCHAR(35)
, VendorID INTEGER
, InvoiceID INTEGER
, Make VARCHAR(35)
, Model VARCHAR(35)
, ShipName VARCHAR(35)
, ModelYear INTEGER
, Condition VARCHAR(35)
, Modifications VARCHAR(35)
, SalePrice DECIMAL
, LastMaintenanceDate DATE
, Available INTEGER
, PRIMARY KEY (SpaceshipID)
, FOREIGN KEY (VendorID) REFERENCES Vendor(VendorID) ON UPDATE CASCADE
, FOREIGN KEY (InvoiceID) REFERENCES Invoice(InvoiceID) ON UPDATE CASCADE);

CREATE TABLE Orders(OrderID INTEGER NOT NULL UNIQUE
, InvoiceID INTEGER
, CustomerID INTEGER
, SpaceshipID INTEGER
, OrderDateTime DATE
, Destination VARCHAR(35)
, OrderStatus VARCHAR(35)
, DiscountApplied DECIMAL
, OrderTotal DECIMAL
, PRIMARY KEY (OrderID)
, FOREIGN KEY (InvoiceID) REFERENCES Invoice(InvoiceID) ON UPDATE CASCADE
, FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON UPDATE CASCADE
, FOREIGN KEY (SpaceshipID) REFERENCES Spaceship(SpaceshipID) ON UPDATE CASCADE);

CREATE TABLE OrderParts(OrderID INTEGER
, PartID INTEGER
, QuantityUsed INTEGER
, PRIMARY KEY(OrderID, PartID)
, FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON UPDATE CASCADE
, FOREIGN KEY (PartID) REFERENCES Part(PartID) ON UPDATE CASCADE);

CREATE TABLE Part(PartID INTEGER NOT NULL UNIQUE
 , SpaceshipID INTEGER
, QuantityInStock INTEGER
, UnitPrice DECIMAL
, PartName VARCHAR(35)
, PartDescription VARCHAR(35)
, Manufacturer VARCHAR(35)
, WarrantyExpirationDate DATE
, PartNumber VARCHAR(35)
, PartStatus VARCHAR(35)
, PRIMARY KEY (PartID)
, FOREIGN KEY (SpaceshipID) REFERENCES Spaceship(SpaceshipID) ON UPDATE CASCADE);

CREATE TABLE Payment(PaymentID INTEGER
 NOT NULL UNIQUE, InvoiceID INTEGER
, VendorID INTEGER
, OrderID INTEGER
, CustomerID INTEGER
, PaymentMethod VARCHAR(35)
, PaymentAmount DECIMAL
, PaymentDateTime DATE
, TransactionID INTEGER
, PaymentStatus VARCHAR(35)
, Currency VARCHAR(35)
, PRIMARY KEY (PaymentID)
, FOREIGN KEY (InvoiceID) REFERENCES Invoice(InvoiceID) ON UPDATE CASCADE
, FOREIGN KEY (VendorID) REFERENCES Vendor(VendorID) ON UPDATE CASCADE
, FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON UPDATE CASCADE
, FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON UPDATE CASCADE);

CREATE TABLE Employee(EmployeeID INTEGER NOT NULL UNIQUE
, EmployeeFirstName VARCHAR(35)
, EmployeeLastName VARCHAR(35)
, Role VARCHAR(35)
, HireDate DATE
, Department VARCHAR(35)
, SupervisorID INTEGER
, EmploymentStatus VARCHAR(35)
, Salary DECIMAL
, PRIMARY KEY (EmployeeID)
, FOREIGN KEY (SupervisorID) REFERENCES Employee(EmployeeID) ON UPDATE CASCADE);

CREATE TABLE MaintenanceRequest(MaintenanceRequestID INTEGER NOT NULL UNIQUE
, SpaceshipID INTEGER
, PartID INTEGER
, RequestedBy INTEGER
, RequestDate DATE
, RequestType VARCHAR(35)
, RequestDescription VARCHAR(35)
, PriorityLevel VARCHAR(35)
, RequestStatus VARCHAR(35)
, CompletionDate DATE
, PRIMARY KEY (MaintenanceRequestID)
, FOREIGN KEY (RequestedBy) REFERENCES Employee(EmployeeID) ON UPDATE CASCADE
, FOREIGN KEY (SpaceshipID) REFERENCES Spaceship(SpaceshipID) ON UPDATE CASCADE
, FOREIGN KEY (PartID) REFERENCES Part(PartID) ON UPDATE CASCADE);

CREATE TABLE FinanceRequest(FinanceRequestID INTEGER NOT NULL UNIQUE
, SpaceshipID INTEGER
, RequestedBy INTEGER
, ReviewedBy INTEGER
, RequestDate DATE
, RequestType VARCHAR(35)
, FinancedAmount DECIMAL
, DateReviewed DATE
, ApprovalStatus VARCHAR(35)
, RequestNotes VARCHAR(35)
, PRIMARY KEY (FinanceRequestID)
, FOREIGN KEY (SpaceshipID) REFERENCES Spaceship(SpaceshipID) ON UPDATE CASCADE
, FOREIGN KEY (RequestedBy) REFERENCES Employee(EmployeeID) ON UPDATE CASCADE
, FOREIGN KEY (ReviewedBy) REFERENCES Employee(EmployeeID) ON UPDATE CASCADE);

CREATE TABLE Invoice(InvoiceID INTEGER NOT NULL UNIQUE, InvoiceDateTime DATE, InvoiceAmount DECIMAL
, TaxAmount DECIMAL
, Currency VARCHAR(35)
, VendorID INTEGER
, CustomerID INTEGER
, OrderID INTEGER
, PaymentID INTEGER
, DueDate DATE
, DateReceived DATE
, ReviewedBy INTEGER
, InvoiceNumber INTEGER
, PRIMARY KEY (InvoiceID)
, FOREIGN KEY (VendorID) REFERENCES Vendor(VendorID) ON UPDATE CASCADE
, FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON UPDATE CASCADE
, FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON UPDATE CASCADE
, FOREIGN KEY (PaymentID) REFERENCES Payment(PaymentID) ON UPDATE CASCADE
, FOREIGN KEY (ReviewedBy) REFERENCES Employee(EmployeeID) ON UPDATE CASCADE);

CREATE TABLE Vendor(VendorID INTEGER NOT NULL UNIQUE
, VendorName VARCHAR(35)
, VendorContact VARCHAR(35)
, PhoneNumber VARCHAR(10)
, Address VARCHAR(35)
, VendorType VARCHAR(35)
, VendorStatus VARCHAR(35)
, VendorRating DECIMAL
, ContractStartDate DATE
, ContractEndDate DATE
, PRIMARY KEY (VendorID));

--Save preceding steps to disk
COMMIT;

--end of tables.sql
