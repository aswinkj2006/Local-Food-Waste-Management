
-- 1) Providers and receivers count by city
SELECT city, COUNT(*) AS providers_count
FROM providers
GROUP BY city
ORDER BY providers_count DESC;

SELECT city, COUNT(*) AS receivers_count
FROM receivers
GROUP BY city
ORDER BY receivers_count DESC;

-- 2) Provider type contributing the most (by total quantity listed)
SELECT provider_type, SUM(quantity) AS total_quantity
FROM food_listings
GROUP BY provider_type
ORDER BY total_quantity DESC;

-- 3) Contact info of providers in a given city (use :city param in apps/clients)
-- For SQLite in Streamlit we'll parameterize with ?
SELECT name, type, address, city, contact
FROM providers
WHERE city = ?
ORDER BY name;

-- 4) Receivers who claimed the most food (by number of claims)
SELECT r.receiver_id, r.name, COUNT(*) AS claims_count
FROM claims c
JOIN receivers r ON r.receiver_id = c.receiver_id
GROUP BY r.receiver_id, r.name
ORDER BY claims_count DESC;

-- 5) Total quantity available from all providers (current listings table)
SELECT SUM(quantity) AS total_quantity_available FROM food_listings;

-- 6) City with highest number of food listings
SELECT location AS city, COUNT(*) AS listings_count
FROM food_listings
GROUP BY location
ORDER BY listings_count DESC;

-- 7) Most commonly available food types
SELECT food_type, COUNT(*) AS appearances
FROM food_listings
GROUP BY food_type
ORDER BY appearances DESC;

-- 8) Claims made for each food item
SELECT f.food_id, f.food_name, COUNT(c.claim_id) AS claim_count
FROM food_listings f
LEFT JOIN claims c ON c.food_id = f.food_id
GROUP BY f.food_id, f.food_name
ORDER BY claim_count DESC;

-- 9) Provider with highest number of successful claims
SELECT p.provider_id, p.name, COUNT(*) AS successful_claims
FROM claims c
JOIN food_listings f ON f.food_id = c.food_id
JOIN providers p ON p.provider_id = f.provider_id
WHERE LOWER(c.status) = 'completed'
GROUP BY p.provider_id, p.name
ORDER BY successful_claims DESC;

-- 10) Percentage of claims by status
WITH total AS (
  SELECT COUNT(*) AS n FROM claims
)
SELECT status,
       COUNT(*) AS cnt,
       ROUND(100.0 * COUNT(*) / (SELECT n FROM total), 2) AS pct
FROM claims
GROUP BY status
ORDER BY cnt DESC;

-- 11) Average quantity claimed per receiver
-- We approximate quantity claimed = associated food listing quantity (can be adjusted if you track partial claims)
SELECT r.receiver_id, r.name,
       AVG(f.quantity) AS avg_quantity_claimed
FROM claims c
JOIN receivers r ON r.receiver_id = c.receiver_id
JOIN food_listings f ON f.food_id = c.food_id
WHERE LOWER(c.status) = 'completed'
GROUP BY r.receiver_id, r.name
ORDER BY avg_quantity_claimed DESC;

-- 12) Most claimed meal type
SELECT f.meal_type, COUNT(*) AS claims_count
FROM claims c
JOIN food_listings f ON f.food_id = c.food_id
WHERE LOWER(c.status) = 'completed'
GROUP BY f.meal_type
ORDER BY claims_count DESC;

-- 13) Total quantity donated by each provider
SELECT p.provider_id, p.name, SUM(f.quantity) AS total_donated_quantity
FROM food_listings f
JOIN providers p ON p.provider_id = f.provider_id
GROUP BY p.provider_id, p.name
ORDER BY total_donated_quantity DESC;

-- 14) Near-expiry items within next 48 hours
-- Works if expiry_date is ISO-like text; otherwise adapt with date functions
SELECT food_id, food_name, quantity, expiry_date, location
FROM food_listings
WHERE DATE(expiry_date) <= DATE('now', '+2 days')
ORDER BY DATE(expiry_date) ASC;

-- 15) Unclaimed items (no claims)
SELECT f.food_id, f.food_name, f.quantity, f.location
FROM food_listings f
LEFT JOIN claims c ON c.food_id = f.food_id
WHERE c.claim_id IS NULL;

-- 16) Provider fulfillment rate (completed / total claims for provider)
WITH stats AS (
  SELECT p.provider_id,
         SUM(CASE WHEN LOWER(c.status)='completed' THEN 1 ELSE 0 END) AS completed,
         COUNT(*) AS total
  FROM claims c
  JOIN food_listings f ON f.food_id = c.food_id
  JOIN providers p ON p.provider_id = f.provider_id
  GROUP BY p.provider_id
)
SELECT s.provider_id, p.name,
       ROUND(100.0 * completed / NULLIF(total,0), 2) AS completion_rate_pct,
       completed, total
FROM stats s
JOIN providers p ON p.provider_id = s.provider_id
ORDER BY completion_rate_pct DESC;

-- 17) Daily claim trend (last 30 days)
SELECT DATE(timestamp) AS day, COUNT(*) AS claims_count
FROM claims
WHERE DATE(timestamp) >= DATE('now', '-30 days')
GROUP BY DATE(timestamp)
ORDER BY day ASC;

-- 18) Top cities by completed claims
SELECT f.location AS city, COUNT(*) AS completed_claims
FROM claims c
JOIN food_listings f ON f.food_id = c.food_id
WHERE LOWER(c.status)='completed'
GROUP BY f.location
ORDER BY completed_claims DESC;
