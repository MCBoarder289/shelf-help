DROP VIEW cumulative_shelf_counts_daily;

CREATE VIEW cumulative_shelf_counts_daily AS
WITH
  interval_series AS (
    SELECT
      GENERATE_SERIES(
        DATE_TRUNC('day', (SELECT current_date - INTERVAL '90 day')),
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
  ),
  shelf_count_offset AS (
    SELECT
      SUM(shelf_count) AS count_offset
      FROM shelf_counts
      WHERE
      date <= (SELECT current_date - INTERVAL '90 day')
  )
  SELECT
    TO_CHAR(i.date_interval, 'YYYY-MM-DD') AS date,
    TO_CHAR(i.date_interval, 'MON DD') AS date_axis,
    COALESCE(sc.shelf_count, 0) AS shelf_count,
    SUM(COALESCE(sc.shelf_count, 0)) OVER (
      ORDER BY
      i.date_interval
    ) + (SELECT count_offset FROM shelf_count_offset) AS "Cumulative Shelf Count"
  FROM interval_series i
    LEFT JOIN shelf_counts sc
      ON i.date_interval = sc.date
  ORDER BY
    i.date_interval