# table creation statements
CREATE_USER_TABLE = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, uuid TEXT, password TEXT, company TEXT, macid TEXT);'
CREATE_DASHBOARD_ADMIN = 'CREATE TABLE IF NOT EXISTS admins (id INTEGER PRIMARY KEY, name TEXT, password TEXT);'
CREATE_DATA_TABLE = 'CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, uuid TEXT, timestamp TEXT, data TEXT,macid TEXT);'
CREATE_COMPANY_TABLE = 'CREATE TABLE IF NOT EXISTS company (companyname TEXT PRIMARY KEY);'
# new queries
GET_ALL_USERS = 'SELECT * FROM users'
CHECK_IF_USER_EXISTS = 'SELECT * FROM users WHERE uuid = ? AND password = ? AND company = ?'
CHECK_IF_USER_DELETED = 'SELECT * FROM users WHERE uuid = ? AND company = ?'
CHECK_IF_ADMIN_EXISTS = 'SELECT * FROM admins WHERE name = ? AND password = ?;'
ADD_ADMIN = 'INSERT INTO admins (name, password) VALUES (?, ?);'
REGISTER_USER = 'INSERT INTO users (company, uuid, password, macid) VALUES (?, ?, ?, ?);'
DELETE_USER = 'DELETE FROM users WHERE uuid = ? AND company = ?'
GET_MAC_ID_OF_USER = 'SELECT macid FROM users WHERE uuid = ? AND password = ? AND company = ?'
EDIT_MAC_ID = 'UPDATE users SET macid = ? WHERE uuid = ? AND password = ? AND company = ?'
GET_COLUMN_NAMES_FOR_USER_TABLE = 'PRAGMA table_info(users);'
PUSH_DATA = 'INSERT INTO data (uuid, timestamp, data, macid) VALUES (?, ?, ?, ?);'
GET_DATA = 'SELECT * FROM data WHERE uuid = ? AND timestamp = ? AND macid = ?;'
GET_ALL_DATA = 'SELECT * FROM data WHERE uuid = ?;'
GET_ALL_DATA_2 = 'SELECT * FROM data'
DELETE_ALL_USERS = 'DELETE FROM users;'
REGISTER_COMPANY = "INSERT INTO company (companyname) VALUES (?);"
CHECK_COMPANY_EXISTS = 'SELECT * FROM company WHERE companyname = ?;'
GET_ALL_COMPANIES = 'SELECT companyname FROM company'