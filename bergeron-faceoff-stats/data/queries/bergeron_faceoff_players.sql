with faceoffs as (
  select
    case when winner = 8470638 then loser else winner end player_id,
    case when winner = 8470638 then 1 else 0 end bergeron_win,
    case when winner != 8470638 then 1 else 0 end bergeron_lose
  from event_faceoff
  left join game_details using(game_id)
  where 
    (winner = 8470638 or loser = 8470638)
    and game_type = 'R'
)

select 
  player_id,
  full_name,
  sum(bergeron_win) as berg_win,
  sum(bergeron_lose) as berg_los,
  sum(bergeron_win + bergeron_lose) as total
from faceoffs
left join player_details using(player_id)
group by player_id, full_name


