USE master;
GO

IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = '$(MSSQL_DB)') 
BEGIN
PRINT ('CREATING DATABASE...')
CREATE DATABASE $(MSSQL_DB);
END
ELSE PRINT ("DATABASE ALREADY EXISTS...");
GO

USE $(MSSQL_DB);
PRINT ('SET UP DATABASE DEFAULT LANGUAGE...');
EXEC sp_configure 'default language', 21;
RECONFIGURE;
GO

IF NOT EXISTS (SELECT loginname FROM master.dbo.syslogins WHERE name = N'$(MSSQL_USER)')
BEGIN
    PRINT('CREATING LOGIN...');
    CREATE LOGIN $(MSSQL_USER) WITH PASSWORD = '$(MSSQL_PASSWORD)';
    CREATE USER $(MSSQL_USER) FOR LOGIN $(MSSQL_USER);    
    ALTER SERVER ROLE sysadmin ADD MEMBER [$(MSSQL_USER)];    
END
ELSE PRINT('LOGIN ALREADY EXISTS...');
GO

USE $(MSSQL_DB);
IF OBJECT_ID('dbo.XMLData', 'U') IS NULL
    BEGIN
        PRINT('CREATE TABLE...');
        CREATE TABLE [dbo].[XMLData] (
            [id] [int] IDENTITY (1,1) NOT NULL,
            [xml_data] [xml] NOT NULL,
            [processed] [bit] NULL,
            [error] [bit] NULL,
            [empty_doc] [bit] NULL,
            [unsupported_doc] [bit] NULL
        );    
        ALTER TABLE [dbo].[XMLData] ADD  CONSTRAINT [DF_XMLData_processed]  DEFAULT ((0)) FOR [processed];        
        ALTER TABLE [dbo].[XMLData] ADD  CONSTRAINT [DF_XMLData_error]  DEFAULT ((0)) FOR [error];        
        ALTER TABLE [dbo].[XMLData] ADD  CONSTRAINT [DF_XMLData_empty_doc]  DEFAULT ((0)) FOR [empty_doc];        
        ALTER TABLE [dbo].[XMLData] ADD  CONSTRAINT [DF_XMLData_unsupported_doc]  DEFAULT ((0)) FOR [unsupported_doc]
    END
ELSE PRINT('TABLE ALREADY EXISTS...');
GO

USE $(MSSQL_DB);
GO

IF OBJECT_ID('dbo.DocumentCompletedXml') IS NOT NULL
DROP PROCEDURE DocumentCompletedXml
GO

CREATE PROCEDURE DocumentCompletedXml
    @documentXml xml,
    @result int OUTPUT

AS   
    SET NOCOUNT ON;                

    INSERT INTO XMLData (
        xml_data,
        processed              
    )
    VALUES (@documentXml, 'False')
    SET @result=1
GO

