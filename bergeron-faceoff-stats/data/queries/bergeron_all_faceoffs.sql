with faceoffs as (
    select
        event_faceoff.game_id,
        event_key,
        winner,
        loser,
        season,
        game_type,
        game_date,
        about_eventid,
        about_eventidx,
        result_event,
        result_description,
        about_period,
        about_periodtime,
        about_goals_home,
        about_goals_away,
        home_team,
        away_team,
        about_game_seconds,
        about_period_seconds,
        about_datetime,
        case when winner = 8470638 -- bergerons player_id --
            then 'bergeon_won'
            else 'bergeron_loss'
        end,
        case when winner = 8470638 
            then loser
            else winner
        end as player_id
    from
    event_faceoff
        left join game_details using(game_id)
        left join game_events using(event_key)
    where (winner = 8470638 or loser = 8470638)
)

select * from faceoffs
left join player_details using(player_id)
