-- use this line to grant access to a specific user for a specific table
-- must be executed by the postgres user
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE full_records TO "cbs-project-user";