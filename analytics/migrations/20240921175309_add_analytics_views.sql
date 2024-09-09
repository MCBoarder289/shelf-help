CREATE VIEW total_unique_shelves AS
  SELECT COUNT(1) FROM shelves;

CREATE VIEW total_shelf_searches AS
  SELECT COUNT(1) FROM shelf_searches;

CREATE VIEW cumulative_shelf_counts_daily AS
WITH
  interval_series AS (
    SELECT
      GENERATE_SERIES(
        DATE_TRUNC('day', (SELECT current_date - INTERVAL '90 day')) - INTERVAL '1 day',
        DATE_TRUNC('day', CURRENT_DATE),
        '1 day'::INTERVAL
      ) AS date_interval
  ),
  shelf_counts AS (
    SELECT
      DATE_TRUNC('day', s.date_added) AS date,
      COUNT(s.shelf_id) AS shelf_count
    FROM shelves s
    GROUP BY
    1
  )
  SELECT
    TO_CHAR(i.date_interval, 'YYYY-MM-DD') AS date,
    TO_CHAR(i.date_interval, 'MON DD') AS date_axis,
    COALESCE(sc.shelf_count, 0) AS shelf_count,
    SUM(COALESCE(sc.shelf_count, 0)) OVER (
      ORDER BY
      i.date_interval
    ) AS "Cumulative Shelf Count"
  FROM interval_series i
    LEFT JOIN shelf_counts sc
      ON i.date_interval = sc.date
  ORDER BY
    i.date_interval;

CREATE VIEW cumulative_shelf_counts_weekly AS
WITH
  interval_series AS (
    SELECT
      GENERATE_SERIES(
        DATE_TRUNC('week', (SELECT min(date_added) FROM shelves)) - INTERVAL '1 week',
        DATE_TRUNC('week', CURRENT_DATE),
        '1 week'::INTERVAL
      ) AS date_interval
  ),
  shelf_counts AS (
    SELECT
      DATE_TRUNC('week', s.date_added) AS date,
      COUNT(s.shelf_id) AS shelf_count
    FROM shelves s
    GROUP BY
    1
  )
  SELECT
    TO_CHAR(i.date_interval, 'YYYY-MM-DD') AS date,
    TO_CHAR(i.date_interval, 'MON DD') AS date_axis,
    COALESCE(sc.shelf_count, 0) AS shelf_count,
    SUM(COALESCE(sc.shelf_count, 0)) OVER (
      ORDER BY
      i.date_interval
    ) AS "Cumulative Shelf Count"
  FROM interval_series i
    LEFT JOIN shelf_counts sc
      ON i.date_interval = sc.date
  ORDER BY
    i.date_interval;

CREATE VIEW cumulative_shelf_counts_monthly AS
WITH
  interval_series AS (
    SELECT
      GENERATE_SERIES(
        DATE_TRUNC('month', (SELECT min(date_added) FROM shelves)) - INTERVAL '1 month',
        DATE_TRUNC('month', CURRENT_DATE),
        '1 month'::INTERVAL
      ) AS date_interval
  ),
  shelf_counts AS (
    SELECT
      DATE_TRUNC('month', s.date_added) AS date,
      COUNT(s.shelf_id) AS shelf_count
    FROM shelves s
    GROUP BY
    1
  )
  SELECT
    TO_CHAR(i.date_interval, 'YYYY-MM-DD') AS date,
    TO_CHAR(i.date_interval, 'MON') AS date_axis,
    COALESCE(sc.shelf_count, 0) AS shelf_count,
    SUM(COALESCE(sc.shelf_count, 0)) OVER (
      ORDER BY
      i.date_interval
    ) AS "Cumulative Shelf Count"
  FROM interval_series i
    LEFT JOIN shelf_counts sc
      ON i.date_interval = sc.date
  ORDER BY
    i.date_interval;

CREATE VIEW total_library_searches AS
SELECT COUNT(1) FROM library_searches;

CREATE VIEW library_avail_rate AS
SELECT
  ROUND(
      CAST(
        CAST(
          SUM(
            CASE
              WHEN available IS TRUE THEN 1
              ELSE 0
              END
            ) AS FLOAT) / COUNT(1) * 100 AS NUMERIC), 2 ) AS availability_perc
  FROM library_searches;

CREATE VIEW library_availability_by_medium AS
SELECT
  CASE
    WHEN is_libby IS TRUE THEN 'Libby'
    ELSE 'Book' END AS medium,

  SUM(CASE WHEN available IS TRUE THEN 1 ELSE 0 END) AS "Available",
  SUM(CASE WHEN available IS NOT TRUE THEN 1 ELSE 0 END) AS "Unavailable"

  FROM library_searches
  GROUP BY
  1;

CREATE VIEW hourly_shelf_searches AS
WITH
  interval_series AS (
    SELECT
      GENERATE_SERIES(0, 23, 1) AS hour_interval
  ),
  hourly_searches AS (
    SELECT
      DATE_PART('hour', time_start) AS hour_interval,
      COUNT(1) AS count
      FROM shelf_searches
      GROUP BY
      1
      ORDER BY
      1 ASC
  )
  SELECT
    i.hour_interval AS "Hour",
    COALESCE(hs.count, 0) AS "Searches"
    FROM interval_series i
    LEFT JOIN hourly_searches hs
      ON i.hour_interval = hs.hour_interval
  ORDER BY
  1;
