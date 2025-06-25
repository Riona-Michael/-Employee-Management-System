USE dc;

CREATE TABLE IF NOT EXISTS Department (
    DepartmentID INT PRIMARY KEY AUTO_INCREMENT,
    DepartmentName VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Emp (
    EmpID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Age INT,
    DepartmentID INT,
    Salary DECIMAL(10,2),
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
);

CREATE TABLE IF NOT EXISTS Users (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Projects (
    ProjectID INT PRIMARY KEY AUTO_INCREMENT,
    ProjectName VARCHAR(100) NOT NULL,
    StartDate DATE,
    EndDate DATE
);

CREATE TABLE IF NOT EXISTS EmployeeProject (
    EmpID INT,
    ProjectID INT,
    PRIMARY KEY (EmpID, ProjectID),
    FOREIGN KEY (EmpID) REFERENCES Emp(EmpID),
    FOREIGN KEY (ProjectID) REFERENCES Projects(ProjectID)
);

-- Insert sample departments
INSERT INTO Department (DepartmentName) VALUES
('HR'), ('Finance'), ('Engineering');

-- Insert sample users
INSERT INTO Users (username, password) VALUES
('admin', 'admin123'),
('user1', 'user123');

-- Insert sample projects
INSERT INTO Projects (ProjectName, StartDate, EndDate) VALUES
('Project A', '2025-01-01', '2025-06-30'),
('Project B', '2025-03-01', '2025-09-30');
