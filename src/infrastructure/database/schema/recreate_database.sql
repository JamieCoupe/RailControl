-- Disconnect any active sessions (Postgres requires this)
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'RailControl';

-- Drop old database
DROP DATABASE IF EXISTS RailControl;

-- Then run \c RailControl and \i setup_database.sql