-- Latest close price
SELECT time, close FROM ohlc ORDER BY time DESC LIMIT 1;

-- Average close price in last 24 hours
SELECT AVG(close) FROM ohlc
WHERE time >= NOW() - INTERVAL 1 DAY;

-- Detect 3 consecutive up candles
SELECT time, open, close FROM ohlc
WHERE close > open
ORDER BY time;
