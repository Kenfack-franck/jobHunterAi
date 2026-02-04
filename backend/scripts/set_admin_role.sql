-- Script to set admin role for specific users
-- Execute this after running alembic migrations

-- Set your account as admin
UPDATE users 
SET role = 'admin' 
WHERE email = 'kenfackfranck08@gmail.com';

-- Verify the change
SELECT id, email, full_name, role, is_active, created_at
FROM users
WHERE role = 'admin';

-- Show all roles distribution
SELECT role, COUNT(*) as count
FROM users
GROUP BY role;
