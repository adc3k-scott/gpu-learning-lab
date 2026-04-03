-- ============================================
-- MISSION CONTROL — Supabase Schema
-- Run this in Supabase SQL Editor
-- ============================================

-- === CUSTOM TYPES ===
DO $$ BEGIN
  CREATE TYPE subscription_tier AS ENUM ('free', 'premium', 'pro');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
  CREATE TYPE platform_type AS ENUM ('harley', 'auto', 'trucking', 'ebike', 'scooter');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
  CREATE TYPE billing_interval AS ENUM ('monthly', 'annual');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- === TABLE 1: PROFILES ===
CREATE TABLE IF NOT EXISTS profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT,
  full_name TEXT,
  avatar_url TEXT,
  tier subscription_tier DEFAULT 'free',
  stripe_customer_id TEXT UNIQUE,
  stripe_subscription_id TEXT,
  platforms platform_type[] DEFAULT '{}',
  units TEXT DEFAULT 'imperial',
  brief_frequency TEXT DEFAULT 'daily',
  onboarding_complete BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile" ON profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON profiles FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Users can insert own profile" ON profiles FOR INSERT WITH CHECK (auth.uid() = id);

-- === TABLE 2: VEHICLES ===
CREATE TABLE IF NOT EXISTS vehicles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  platform platform_type NOT NULL,
  nickname TEXT,
  year INTEGER,
  make TEXT NOT NULL,
  model TEXT NOT NULL,
  vin TEXT,
  mileage INTEGER DEFAULT 0,
  color TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE vehicles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own vehicles" ON vehicles FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own vehicles" ON vehicles FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own vehicles" ON vehicles FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own vehicles" ON vehicles FOR DELETE USING (auth.uid() = user_id);

-- === TABLE 3: SERVICE RECORDS ===
CREATE TABLE IF NOT EXISTS service_records (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  vehicle_id UUID REFERENCES vehicles(id) ON DELETE CASCADE NOT NULL,
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  service_type TEXT NOT NULL,
  service_date DATE NOT NULL DEFAULT CURRENT_DATE,
  mileage_at_service INTEGER,
  cost DECIMAL(10,2) DEFAULT 0,
  parts_used TEXT,
  shop_name TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE service_records ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own service records" ON service_records FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own service records" ON service_records FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own service records" ON service_records FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own service records" ON service_records FOR DELETE USING (auth.uid() = user_id);

-- === TABLE 4: FUEL LOGS ===
CREATE TABLE IF NOT EXISTS fuel_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  vehicle_id UUID REFERENCES vehicles(id) ON DELETE CASCADE NOT NULL,
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  fill_date DATE NOT NULL DEFAULT CURRENT_DATE,
  gallons DECIMAL(8,3) NOT NULL,
  price_per_gallon DECIMAL(6,3),
  total_cost DECIMAL(10,2),
  odometer INTEGER,
  is_full_tank BOOLEAN DEFAULT true,
  station_name TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE fuel_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own fuel logs" ON fuel_logs FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own fuel logs" ON fuel_logs FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can delete own fuel logs" ON fuel_logs FOR DELETE USING (auth.uid() = user_id);

-- === TABLE 5: FORUM THREADS ===
CREATE TABLE IF NOT EXISTS forum_threads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  author_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  platform platform_type,
  reply_count INTEGER DEFAULT 0,
  upvote_count INTEGER DEFAULT 0,
  is_pinned BOOLEAN DEFAULT false,
  is_locked BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE forum_threads ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can view threads" ON forum_threads FOR SELECT USING (true);
CREATE POLICY "Auth users can create threads" ON forum_threads FOR INSERT WITH CHECK (auth.uid() = author_id);
CREATE POLICY "Authors can update own threads" ON forum_threads FOR UPDATE USING (auth.uid() = author_id);

-- === TABLE 6: FORUM REPLIES ===
CREATE TABLE IF NOT EXISTS forum_replies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  thread_id UUID REFERENCES forum_threads(id) ON DELETE CASCADE NOT NULL,
  author_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  parent_reply_id UUID REFERENCES forum_replies(id) ON DELETE SET NULL,
  content TEXT NOT NULL,
  upvote_count INTEGER DEFAULT 0,
  is_solution BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE forum_replies ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can view replies" ON forum_replies FOR SELECT USING (true);
CREATE POLICY "Auth users can create replies" ON forum_replies FOR INSERT WITH CHECK (auth.uid() = author_id);
CREATE POLICY "Authors can update own replies" ON forum_replies FOR UPDATE USING (auth.uid() = author_id);

-- === TABLE 7: UPVOTES ===
CREATE TABLE IF NOT EXISTS upvotes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  thread_id UUID REFERENCES forum_threads(id) ON DELETE CASCADE,
  reply_id UUID REFERENCES forum_replies(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT now(),
  CONSTRAINT upvote_target CHECK (
    (thread_id IS NOT NULL AND reply_id IS NULL) OR
    (thread_id IS NULL AND reply_id IS NOT NULL)
  ),
  CONSTRAINT unique_thread_upvote UNIQUE (user_id, thread_id),
  CONSTRAINT unique_reply_upvote UNIQUE (user_id, reply_id)
);

ALTER TABLE upvotes ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own upvotes" ON upvotes FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own upvotes" ON upvotes FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can delete own upvotes" ON upvotes FOR DELETE USING (auth.uid() = user_id);

-- === TABLE 8: EMAIL SIGNUPS ===
CREATE TABLE IF NOT EXISTS email_signups (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  platform_interest platform_type,
  source TEXT DEFAULT 'landing',
  utm_source TEXT,
  utm_medium TEXT,
  utm_campaign TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE email_signups ENABLE ROW LEVEL SECURITY;
-- No public access — service role only for inserts from API

-- === TABLE 9: AI CHAT USAGE ===
CREATE TABLE IF NOT EXISTS ai_chat_usage (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  platform platform_type,
  query_text TEXT,
  tokens_in INTEGER DEFAULT 0,
  tokens_out INTEGER DEFAULT 0,
  latency_ms INTEGER DEFAULT 0,
  query_date DATE DEFAULT CURRENT_DATE,
  created_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE ai_chat_usage ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own AI usage" ON ai_chat_usage FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own AI usage" ON ai_chat_usage FOR INSERT WITH CHECK (auth.uid() = user_id);

-- === TRIGGERS ===

-- Auto-create profile on signup
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO profiles (id, email, full_name, avatar_url)
  VALUES (
    NEW.id,
    NEW.email,
    COALESCE(NEW.raw_user_meta_data->>'full_name', NEW.raw_user_meta_data->>'name', ''),
    COALESCE(NEW.raw_user_meta_data->>'avatar_url', NEW.raw_user_meta_data->>'picture', '')
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_user();

-- Auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS profiles_updated_at ON profiles;
CREATE TRIGGER profiles_updated_at BEFORE UPDATE ON profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at();

DROP TRIGGER IF EXISTS vehicles_updated_at ON vehicles;
CREATE TRIGGER vehicles_updated_at BEFORE UPDATE ON vehicles FOR EACH ROW EXECUTE FUNCTION update_updated_at();

DROP TRIGGER IF EXISTS service_records_updated_at ON service_records;
CREATE TRIGGER service_records_updated_at BEFORE UPDATE ON service_records FOR EACH ROW EXECUTE FUNCTION update_updated_at();

DROP TRIGGER IF EXISTS forum_threads_updated_at ON forum_threads;
CREATE TRIGGER forum_threads_updated_at BEFORE UPDATE ON forum_threads FOR EACH ROW EXECUTE FUNCTION update_updated_at();

DROP TRIGGER IF EXISTS forum_replies_updated_at ON forum_replies;
CREATE TRIGGER forum_replies_updated_at BEFORE UPDATE ON forum_replies FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Sync reply count on threads
CREATE OR REPLACE FUNCTION sync_reply_count()
RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    UPDATE forum_threads SET reply_count = reply_count + 1 WHERE id = NEW.thread_id;
  ELSIF TG_OP = 'DELETE' THEN
    UPDATE forum_threads SET reply_count = GREATEST(reply_count - 1, 0) WHERE id = OLD.thread_id;
  END IF;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS sync_thread_reply_count ON forum_replies;
CREATE TRIGGER sync_thread_reply_count
  AFTER INSERT OR DELETE ON forum_replies
  FOR EACH ROW EXECUTE FUNCTION sync_reply_count();

-- Sync upvote counts
CREATE OR REPLACE FUNCTION sync_upvote_count()
RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    IF NEW.thread_id IS NOT NULL THEN
      UPDATE forum_threads SET upvote_count = upvote_count + 1 WHERE id = NEW.thread_id;
    ELSIF NEW.reply_id IS NOT NULL THEN
      UPDATE forum_replies SET upvote_count = upvote_count + 1 WHERE id = NEW.reply_id;
    END IF;
  ELSIF TG_OP = 'DELETE' THEN
    IF OLD.thread_id IS NOT NULL THEN
      UPDATE forum_threads SET upvote_count = GREATEST(upvote_count - 1, 0) WHERE id = OLD.thread_id;
    ELSIF OLD.reply_id IS NOT NULL THEN
      UPDATE forum_replies SET upvote_count = GREATEST(upvote_count - 1, 0) WHERE id = OLD.reply_id;
    END IF;
  END IF;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS sync_thread_upvotes ON upvotes;
CREATE TRIGGER sync_thread_upvotes
  AFTER INSERT OR DELETE ON upvotes
  FOR EACH ROW EXECUTE FUNCTION sync_upvote_count();

-- === VIEWS ===

CREATE OR REPLACE VIEW forum_threads_with_author AS
SELECT
  t.*,
  p.full_name AS author_name,
  p.avatar_url AS author_avatar,
  p.tier AS author_tier
FROM forum_threads t
LEFT JOIN profiles p ON t.author_id = p.id;

CREATE OR REPLACE VIEW forum_replies_with_author AS
SELECT
  r.*,
  p.full_name AS author_name,
  p.avatar_url AS author_avatar,
  p.tier AS author_tier
FROM forum_replies r
LEFT JOIN profiles p ON r.author_id = p.id;

CREATE OR REPLACE VIEW ai_chat_daily_usage AS
SELECT
  user_id,
  query_date,
  COUNT(*) AS query_count,
  SUM(tokens_in) AS total_tokens_in,
  SUM(tokens_out) AS total_tokens_out,
  AVG(latency_ms) AS avg_latency_ms
FROM ai_chat_usage
GROUP BY user_id, query_date;

-- === HELPER FUNCTIONS ===

CREATE OR REPLACE FUNCTION can_add_vehicle(p_user_id UUID)
RETURNS BOOLEAN AS $$
DECLARE
  user_tier subscription_tier;
  vehicle_count INTEGER;
  max_vehicles INTEGER;
BEGIN
  SELECT tier INTO user_tier FROM profiles WHERE id = p_user_id;

  SELECT COUNT(*) INTO vehicle_count FROM vehicles WHERE user_id = p_user_id;

  max_vehicles := CASE user_tier
    WHEN 'free' THEN 1
    WHEN 'premium' THEN 3
    WHEN 'pro' THEN 999999
    ELSE 1
  END;

  RETURN vehicle_count < max_vehicles;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION check_ai_rate_limit(p_user_id UUID)
RETURNS BOOLEAN AS $$
DECLARE
  user_tier subscription_tier;
  today_count INTEGER;
  daily_limit INTEGER;
BEGIN
  SELECT tier INTO user_tier FROM profiles WHERE id = p_user_id;

  SELECT COUNT(*) INTO today_count
  FROM ai_chat_usage
  WHERE user_id = p_user_id AND query_date = CURRENT_DATE;

  daily_limit := CASE user_tier
    WHEN 'free' THEN 3
    WHEN 'premium' THEN 20
    WHEN 'pro' THEN 999999
    ELSE 3
  END;

  RETURN today_count < daily_limit;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION calculate_mpg(p_vehicle_id UUID)
RETURNS DECIMAL AS $$
DECLARE
  avg_mpg DECIMAL;
BEGIN
  WITH ordered_logs AS (
    SELECT
      odometer,
      gallons,
      is_full_tank,
      LAG(odometer) OVER (ORDER BY fill_date, created_at) AS prev_odometer
    FROM fuel_logs
    WHERE vehicle_id = p_vehicle_id AND is_full_tank = true
    ORDER BY fill_date, created_at
  )
  SELECT AVG((odometer - prev_odometer) / NULLIF(gallons, 0))
  INTO avg_mpg
  FROM ordered_logs
  WHERE prev_odometer IS NOT NULL;

  RETURN COALESCE(avg_mpg, 0);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================
-- Schema complete! 9 tables, 22 RLS policies,
-- 5 triggers, 3 views, 3 functions
-- ============================================
