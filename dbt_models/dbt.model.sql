WITH possession_data AS (
    SELECT 
        player_id,
        team,
        event_type,
        COUNT(*) as event_count
    FROM {{ ref('raw_soccer_events') }}
    WHERE event_type = 'possession'
    GROUP BY player_id, team
)

SELECT
    team,
    SUM(event_count) / (SELECT SUM(event_count) FROM possession_data) * 100 AS possession_percentage
FROM possession_data
GROUP BY team
