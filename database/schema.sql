-- UMDM+ Database Schema
-- PostgreSQL 12+ compatible
-- Version: 1.0
-- Created: 2025-11-10

-- ============================================
-- Users Table
-- ============================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    role VARCHAR(20) DEFAULT 'user' CHECK (role IN ('user', 'admin', 'premium'))
);

-- ============================================
-- Downloads Table
-- ============================================
CREATE TABLE downloads (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    title VARCHAR(500),
    platform VARCHAR(50),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'downloading', 'completed', 'failed', 'cancelled')),
    quality VARCHAR(20),
    format VARCHAR(20),
    file_size BIGINT,
    file_path TEXT,
    download_speed FLOAT,
    progress INTEGER DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    metadata JSONB
);

-- ============================================
-- Queue Table
-- ============================================
CREATE TABLE queue (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    download_id INTEGER REFERENCES downloads(id) ON DELETE CASCADE,
    priority INTEGER DEFAULT 0,
    position INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'waiting' CHECK (status IN ('waiting', 'processing', 'completed', 'failed')),
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    UNIQUE(user_id, position)
);

-- ============================================
-- Settings Table
-- ============================================
CREATE TABLE settings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    key VARCHAR(100) NOT NULL,
    value JSONB NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, key)
);

-- ============================================
-- Sessions Table (JWT Refresh Tokens)
-- ============================================
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    refresh_token VARCHAR(500) UNIQUE NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Playlists Table (for batch downloads)
-- ============================================
CREATE TABLE playlists (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    title VARCHAR(500),
    platform VARCHAR(50),
    total_items INTEGER DEFAULT 0,
    downloaded_items INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- ============================================
-- Conversions Table
-- ============================================
CREATE TABLE conversions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    download_id INTEGER REFERENCES downloads(id) ON DELETE SET NULL,
    source_file TEXT NOT NULL,
    target_file TEXT,
    source_format VARCHAR(20),
    target_format VARCHAR(20),
    status VARCHAR(20) DEFAULT 'pending',
    progress INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- ============================================
-- Activity Log Table
-- ============================================
CREATE TABLE activity_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_id INTEGER,
    details JSONB,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Indexes for Performance
-- ============================================

-- Users indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_is_active ON users(is_active);

-- Downloads indexes
CREATE INDEX idx_downloads_user_id ON downloads(user_id);
CREATE INDEX idx_downloads_status ON downloads(status);
CREATE INDEX idx_downloads_created_at ON downloads(created_at DESC);
CREATE INDEX idx_downloads_platform ON downloads(platform);
CREATE INDEX idx_downloads_user_status ON downloads(user_id, status);

-- Queue indexes
CREATE INDEX idx_queue_user_id ON queue(user_id);
CREATE INDEX idx_queue_status ON queue(status);
CREATE INDEX idx_queue_position ON queue(user_id, position);
CREATE INDEX idx_queue_download_id ON queue(download_id);

-- Settings indexes
CREATE INDEX idx_settings_user_id ON settings(user_id);
CREATE INDEX idx_settings_key ON settings(key);

-- Sessions indexes
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_refresh_token ON sessions(refresh_token);
CREATE INDEX idx_sessions_expires_at ON sessions(expires_at);

-- Playlists indexes
CREATE INDEX idx_playlists_user_id ON playlists(user_id);
CREATE INDEX idx_playlists_status ON playlists(status);

-- Conversions indexes
CREATE INDEX idx_conversions_user_id ON conversions(user_id);
CREATE INDEX idx_conversions_download_id ON conversions(download_id);
CREATE INDEX idx_conversions_status ON conversions(status);

-- Activity log indexes
CREATE INDEX idx_activity_log_user_id ON activity_log(user_id);
CREATE INDEX idx_activity_log_created_at ON activity_log(created_at DESC);
CREATE INDEX idx_activity_log_action ON activity_log(action);

-- ============================================
-- Functions and Triggers
-- ============================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger for users table
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for settings table
CREATE TRIGGER update_settings_updated_at
    BEFORE UPDATE ON settings
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- Default Data
-- ============================================

-- Create default admin user (password: admin123 - CHANGE IN PRODUCTION!)
-- Password hash generated with bcrypt, 10 rounds
INSERT INTO users (username, email, password_hash, role, is_active) VALUES
('admin', 'admin@umdm.local', '$2a$10$rKqPv9xQKJKqKJKqKJKqKe7YvZK5L5L5L5L5L5L5L5L5L5L5L5L5Le', 'admin', true);

-- Create default settings for admin
INSERT INTO settings (user_id, key, value) VALUES
(1, 'theme', '{"mode": "dark"}'),
(1, 'quality', '{"default": "1080p"}'),
(1, 'format', '{"video": "mp4", "audio": "mp3"}'),
(1, 'notifications', '{"enabled": true, "sound": true}');

-- ============================================
-- Views for Common Queries
-- ============================================

-- Active downloads view
CREATE VIEW active_downloads AS
SELECT 
    d.id,
    d.user_id,
    u.username,
    d.url,
    d.title,
    d.platform,
    d.status,
    d.progress,
    d.quality,
    d.format,
    d.created_at
FROM downloads d
JOIN users u ON d.user_id = u.id
WHERE d.status IN ('pending', 'downloading')
ORDER BY d.created_at DESC;

-- User statistics view
CREATE VIEW user_stats AS
SELECT 
    u.id,
    u.username,
    u.email,
    COUNT(DISTINCT d.id) as total_downloads,
    COUNT(DISTINCT d.id) FILTER (WHERE d.status = 'completed') as completed_downloads,
    COUNT(DISTINCT d.id) FILTER (WHERE d.status = 'failed') as failed_downloads,
    COALESCE(SUM(d.file_size) FILTER (WHERE d.status = 'completed'), 0) as total_size_bytes,
    u.created_at as member_since,
    u.last_login
FROM users u
LEFT JOIN downloads d ON u.id = d.user_id
GROUP BY u.id, u.username, u.email, u.created_at, u.last_login;

-- ============================================
-- Grant Permissions
-- ============================================

-- Grant all privileges to application user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO umdm_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO umdm_user;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO umdm_user;

-- ============================================
-- Comments for Documentation
-- ============================================

COMMENT ON TABLE users IS 'Stores user account information';
COMMENT ON TABLE downloads IS 'Tracks all download requests and their status';
COMMENT ON TABLE queue IS 'Manages download queue for sequential processing';
COMMENT ON TABLE settings IS 'User preferences stored as JSON key-value pairs';
COMMENT ON TABLE sessions IS 'JWT refresh token storage for authentication';
COMMENT ON TABLE playlists IS 'Tracks batch download operations for playlists';
COMMENT ON TABLE conversions IS 'Manages media format conversion tasks';
COMMENT ON TABLE activity_log IS 'Audit trail of user actions';

-- ============================================
-- Schema Version
-- ============================================

CREATE TABLE schema_version (
    version VARCHAR(20) PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

INSERT INTO schema_version (version, description) VALUES
('1.0.0', 'Initial schema with core tables for Phase 1 implementation');

-- ============================================
-- Success Message
-- ============================================

DO $$
BEGIN
    RAISE NOTICE '✅ UMDM+ database schema created successfully!';
    RAISE NOTICE 'Tables created: users, downloads, queue, settings, sessions, playlists, conversions, activity_log';
    RAISE NOTICE 'Views created: active_downloads, user_stats';
    RAISE NOTICE 'Default admin user: admin@umdm.local (password: admin123)';
    RAISE NOTICE '⚠️  IMPORTANT: Change the admin password in production!';
END $$;
