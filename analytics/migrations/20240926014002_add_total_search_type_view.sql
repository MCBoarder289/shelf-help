CREATE VIEW search_type_summary AS
SELECT
  search_type as name,
  COUNT(1) AS value,
  CASE
    WHEN search_type = 'Shuffle' THEN 'indigo.6'
    WHEN search_type = 'Search' THEN 'blue.6'
    END AS color
  FROM shelf_searches
  GROUP BY
  1