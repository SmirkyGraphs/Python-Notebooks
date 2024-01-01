select 
    game_id, 
    game_type,
    berg_played,
    sum(case when team_name = 'Boston Bruins' then 1 end) faceoffs_won,
    sum(case when team_name != 'Boston Bruins' then 1 end) faceoffs_lost,
    count(*) total_faceoffs
from game_events
left join game_details using(game_id)
left join ( 
    select 
        game_id,
        sum(case when player_id = 8470638 and game_status = 'played' then 1 else 0 end) berg_played
	from game_players
    group by game_id
) as berg_played using(game_id)
where result_event = 'Faceoff'
and (home_team = 'Boston Bruins' or away_team = 'Boston Bruins')
group by 1,2,3





