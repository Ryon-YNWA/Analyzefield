# coding: utf-8
import re

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


user = 'ryon'
password = 'ryon8821'
database = 'PremierLeague'
host = '127.0.0.1'
charset = 'utf8'

engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}?charset={charset}', convert_unicode=True , echo=True)
db_session = scoped_session(
                sessionmaker(
                    autocommit = False,
                    autoflush = False,
                    bind = engine
                )
             )
Base = declarative_base()
Base.query = db_session.query_property()

def delete_regexp(str, regexp):
    print(str)
    print(regexp)
    if str is None:
        return None
    return re.sub(regexp, '', str)
    # return str.replace(regexp, '')

def extract_regexp(str, regexp):
    if str is None:
        return None
    return re.search(regexp, str).group()

def init_db():
    import assets.models
    Base.metadata.create_all(bind=engine)

def insert_match_info(records):
    from assets import models

    for record in records:
        row = models.MatchInfoData(
                match_id = record.get('match_id', None),
                tournament = record.get('tournament', None),
                round = record.get('round', None),
                start_date = record.get('start_date', None),
                location = record.get('location', None),
                venue = record.get('venue', None),
                referee_name = record.get('referee_name', None),
                referee_country = record.get('referee_country', None),
              )
        db_session.add(row)
 
    db_session.commit()

def insert_match_stats(records):
    from assets import models

    for record in records:
        row = models.MatchStatsData(
                match_id = record.get('match_id', None),
                team_name = record.get('team', None),
                side = record.get('side', None),
                half = record.get('half', None),
                ball_possession = record.get('Ball possession', '').replace('%', ''),
                total_shots = record.get('Total shots', None),
                shots_on_target = record.get('Shots on target', None),
                shots_off_target = record.get('Shots off target', None),
                shots_inside_box = record.get('Shots inside box', None),
                shots_outside_box = record.get('Shots outside box', None),
                blocked_shots = record.get('Blocked shots', None),
                goalkeeper_saves = record.get('Goalkeeper saves', None),
                big_chances = record.get('Big chances', None),
                big_chances_missed = record.get('Big chances missed', None),
                counter_attacks = record.get('Counter attacks', None),
                counter_attack_shots = record.get('Counter attack shots', None),
                corner_kicks = record.get('Corner kicks', None),
                offsides = record.get('Offsides', None),
                yellow_cards = record.get('Yellow cards', None),
                passes = record.get('Passes', None),
                pass_successes = delete_regexp(record.get('Acc. passes', None), r' (.*)'),
                long_balls = delete_regexp(delete_regexp(record.get('Long balls', None), r' (.*)'), r'/.*'),
                long_ball_successes = delete_regexp(delete_regexp(record.get('Long balls', None), r' (.*)'), r'.*/'),
                crosses = delete_regexp(delete_regexp(record.get('Crosses', None), r' (.*)'), r'/.*'),
                cross_successes = delete_regexp(delete_regexp(record.get('Crosses', None), r' (.*)'), r'.*/'),
                dribbles = delete_regexp(delete_regexp(record.get('Dribbles', None), r' (.*)'), r'/.*'),
                dribble_successes = delete_regexp(delete_regexp(record.get('Dribbles', None), r' (.*)'), r'.*/'),
                possession_lost = record.get('Possession lost', None),
                duels_won = record.get('Duels won', None),
                aerials_won = record.get('Aerials won', None),
                tackles = record.get('Tackles', None),
                interceptions = record.get('Interceptions', None),
                clearances = record.get('Clearances', None),
              )
        db_session.add(row)
 
    db_session.commit()

def insert_player_stats(records):
    from assets import models

    for record in records:
        row = models.PlayerStatsData(
                match_id = record.get('match_id', None),
                team_name = record.get('team_name', None),
                player_name = record.get('player_name', None),
                status = record.get('status', None),
                position = record.get('Position', None),
                minutes_played = delete_regexp(record.get('Minutes played', None), '\''),
                sofascore_rating = record.get('Rating', None),
                goals = record.get('Goals', None),
                assists = record.get('Assists', None),
                shots_on_target = record.get('Shots on target', None),
                shots_off_target = record.get('Shots off target', None),
                shots_blocked = record.get('Shots blocked', None),
                dribble_attempts = delete_regexp(record.get('Dribble attempts (succ.)', None), r' (.*)'),
                dribble_succeeds = extract_regexp(extract_regexp(record.get('Dribble attempts (succ.)', None), r'\(.*\)'), r'\d+'),
                clearances = record.get('Clearances', None),
                blocked_shots = record.get('Blocked shots', None),
                interceptions = record.get('Interceptions', None),
                tackles = record.get('Tackles', None),
                dribbled_past = record.get('Dribbled past', None),
                touches = record.get('Touches', None),
                passes = delete_regexp(delete_regexp(record.get('Acc. passes', None), r' (.*)'), r'.*/'),
                pass_succeeds = delete_regexp(delete_regexp(record.get('Acc. passes', None), r' (.*)'), r'/.*'),
                key_passes = record.get('Key passes', None),
                crosses = delete_regexp(record.get('Crosses (acc.)', None), r' (.*)'),
                cross_succeeds = extract_regexp(extract_regexp(record.get('Crosses (acc.)', None), r'\(.*\)'), r'\d+'),
                long_balls = delete_regexp(record.get('Long balls (acc.)', None), r' (.*)'),
                long_ball_succeeds = extract_regexp(extract_regexp(record.get('Long balls (acc.)', None), r'\(.*\)'), r'\d+'),
                ground_duels = delete_regexp(record.get('Ground duels (won)', None), r' (.*)'),
                ground_duels_won = extract_regexp(extract_regexp(record.get('Ground duels (won)', None), r'\(.*\)'), r'\d+'),
                aerial_duels = delete_regexp(record.get('Aerial duels (won)', None), r' (.*)'),
                aerial_duels_won = extract_regexp(extract_regexp(record.get('Aerial duels (won)', None), r'\(.*\)'), r'\d+'),
                possession_lost = record.get('Possession lost', None),
                fouls = record.get('Fouls', None),
                was_fouled = record.get('Was fouled', None),
                offsides = record.get('Offsides', None),
                saves = record.get('Saves', None),
                punches = record.get('Punches', None),
                runs_out = delete_regexp(record.get('Runs out (succ.)', None), r' (.*)'),
                runs_out_succeeds = extract_regexp(extract_regexp(record.get('Runs out (succ.)', None), r'\(.*\)'), r'\d+'),
                high_claims=record.get('High claims', None)
              )
        db_session.add(row)
 
    db_session.commit()