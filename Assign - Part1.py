from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import mysql.connector

'''
in this script, I am using Google Sheets API to pull the data from the Excel file online. Scraping the file from its
source code is hard, as it is abstracted away using JS by Google. I created a ServiceAccount(robot-robot interaction only)
for API credentials.
'''
scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/spreadsheets.readonly']
document = '1cnPUhCbUm5p3DMWw6wcSu4li7qChBrhd-UyRkW2RSUg'
sheet_range = ['product_listing!A1:E',
               'group_listing!A1:C']      # These are the field limits to the excel workbooks
# Auth
credentials = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\Student\Downloads\Cloud\GCP\Sheets '
                                                               r'Auth\SheetsTaskAPI-d99ac608f70f.json', scopes=scopes)
service = build('sheets', 'v4', credentials=credentials)  # API call definition along with its version and credentials
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='mysqlpython'
)
mycursor = mydb.cursor() # MySQL cursor initialization, which interacts with SQL backend
# The following are the SQL queries for creating TABLES and inserting their corresponding data elements
TABLE_QUERIES = ['CREATE TABLE Products (Product_Name VARCHAR(255), Model_Name VARCHAR(255), Product_SerialNo VARCHAR(255) PRIMARY KEY, Group_Associated VARCHAR(255), product_MRP VARCHAR(255))',
               'CREATE TABLE Groups_listing (Group_Name VARCHAR(255) PRIMARY KEY, group_description VARCHAR(255), isActive VARCHAR(255))']
INSERT_QUERIES = ['INSERT INTO Products (Product_Name, Model_Name, Product_SerialNo, Group_Associated, product_MRP) VALUES (%s, %s, %s, %s, %s)',
                  'INSERT INTO Groups_listing (Group_Name, group_description, isActive) VALUES (%s, %s, %s)']

sheet = service.spreadsheets()
for num, i in enumerate(sheet_range):
    result = sheet.values().get(spreadsheetId=document, range=i).execute()
    values = result.get('values', [])[1:] # API call to pull that corresponding workboook
    mycursor.execute(TABLE_QUERIES[num]) # Create Table based on the data pulled
    for row in values:
        mycursor.execute(INSERT_QUERIES[num], tuple(row))
    mydb.commit() # Insert all tuples into the table and commit all changes
