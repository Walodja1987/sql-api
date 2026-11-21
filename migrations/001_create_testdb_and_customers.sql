CREATE DATABASE TestDB;
GO

USE TestDB;
GO

CREATE TABLE dbo.Customers (
    CustomerId INT IDENTITY(1,1) PRIMARY KEY,
    FirstName NVARCHAR(100) NOT NULL,
    LastName NVARCHAR(100) NOT NULL,
    Email NVARCHAR(255),
    CreatedAt DATETIME2 DEFAULT SYSUTCDATETIME()
);
GO

INSERT INTO dbo.Customers (FirstName, LastName, Email)
VALUES
    ('John', 'Smith', 'john@example.com'),
    ('Anna', 'Miller', 'anna@example.com');
GO

SELECT * FROM dbo.Customers;