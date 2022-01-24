# coding: utf-8
import uuid
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date

from assets.database import Base


class MatchInfoData(Base):

    __tablename__ = "match_info"

    #Column情報を設定する
    match_id = Column(String(36), primary_key=True)
    tournament = Column(String(100), unique=False)
    round = Column(String(100), unique=False)
    start_date = Column(DateTime, unique=False)
    location = Column(String(100), unique=False)
    venue = Column(String(100), unique=False)
    referee_name = Column(String(100), unique=False)
    referee_country = Column(String(100), unique=False)

    def __init__(
            self, 
            match_id,
            tournament=None,
            round=None,
            start_date=None,
            location=None,
            venue=None,
            referee_name=None,
            referee_country=None
        ):

        self.match_id = match_id
        self.tournament = tournament
        self.round = round
        self.start_date = start_date
        self.location = location
        self.venue = venue
        self.referee_name = referee_name
        self.referee_country = referee_country


class MatchStatsData(Base):

    __tablename__ = "match_stats"

    #Column情報を設定する
    id = Column(String(36), primary_key=True)
    match_id = Column(String(36), unique=False)
    team_name = Column(String(100), unique=False)
    side = Column(String(100), unique=False)
    half = Column(String(100), unique=False)
    ball_possession = Column(Integer, unique=False)
    total_shots = Column(Integer, unique=False)
    shots_on_target = Column(Integer, unique=False)
    shots_off_target = Column(Integer, unique=False)
    shots_inside_box = Column(Integer, unique=False)
    shots_outside_box = Column(Integer, unique=False)
    blocked_shots = Column(Integer, unique=False)
    goalkeeper_saves = Column(Integer, unique=False)
    big_chances = Column(Integer, unique=False)
    big_chances_missed = Column(Integer, unique=False)
    counter_attacks = Column(Integer, unique=False)
    counter_attack_shots = Column(Integer, unique=False)
    corner_kicks = Column(Integer, unique=False)
    offsides = Column(Integer, unique=False)
    yellow_cards = Column(Integer, unique=False)
    passes = Column(Integer, unique=False)
    pass_successes = Column(Integer, unique=False)
    long_balls = Column(Integer, unique=False)
    long_ball_successes = Column(Integer, unique=False)
    crosses = Column(Integer, unique=False)
    cross_successes = Column(Integer, unique=False)
    dribbles = Column(Integer, unique=False)
    dribble_successes = Column(Integer, unique=False)
    possession_lost = Column(Integer, unique=False)
    duels_won = Column(Integer, unique=False)
    aerials_won = Column(Integer, unique=False)
    tackles = Column(Integer, unique=False)
    interceptions = Column(Integer, unique=False)
    clearances = Column(Integer, unique=False)

    def __init__(
            self, 
            match_id,
            team_name=None,
            side=None,
            half=None,
            ball_possession=None,
            total_shots=None,
            shots_on_target=None,
            shots_off_target=None,
            shots_inside_box=None,
            shots_outside_box=None,
            blocked_shots=None,
            goalkeeper_saves=None,
            big_chances=None,
            big_chances_missed=None,
            counter_attacks=None,
            counter_attack_shots=None,
            corner_kicks=None,
            offsides=None,
            yellow_cards=None,
            passes=None,
            pass_successes=None,
            long_balls=None,
            long_ball_successes=None,
            crosses=None,
            cross_successes=None,
            dribbles=None,
            dribble_successes=None,
            possession_lost=None,
            duels_won=None,
            aerials_won=None,
            tackles=None,
            interceptions=None,
            clearances=None
        ):

        self.id = str(uuid.uuid4())
        self.match_id = match_id
        self.team_name = team_name
        self.side = side
        self.half = half
        self.ball_possession = ball_possession
        self.total_shots = total_shots
        self.shots_on_target = shots_on_target
        self.shots_off_target = shots_off_target
        self.shots_inside_box = shots_inside_box
        self.shots_outside_box = shots_outside_box
        self.blocked_shots = blocked_shots
        self.goalkeeper_saves = goalkeeper_saves
        self.big_chances = big_chances
        self.big_chances_missed = big_chances_missed
        self.counter_attacks = counter_attacks
        self.counter_attack_shots = counter_attack_shots
        self.corner_kicks = corner_kicks
        self.offsides = offsides
        self.yellow_cards = yellow_cards
        self.passes = passes
        self.pass_successes = pass_successes
        self.long_balls = long_balls
        self.long_ball_successes = long_ball_successes
        self.crosses = crosses
        self.cross_successes = cross_successes
        self.dribbles = dribbles
        self.dribble_successes = dribble_successes
        self.possession_lost = possession_lost
        self.duels_won = duels_won
        self.aerials_won = aerials_won
        self.tackles = tackles
        self.interceptions = interceptions
        self.clearances =clearances


class PlayerStatsData(Base):

    __tablename__ = "player_stats"

    #Column情報を設定する
    id = Column(String(36), primary_key=True)
    match_id = Column(String(36), unique=False)
    team_name = Column(String(100), unique=False)
    player_name = Column(String(100), unique=False)
    status = Column(String(100), unique=False)
    position = Column(String(100), unique=False)
    minutes_played = Column(Integer, unique=False)
    sofascore_rating = Column(Integer, unique=False)
    goals = Column(Integer, unique=False)
    assists = Column(Integer, unique=False)
    shots_on_target = Column(Integer, unique=False)
    shots_off_target = Column(Integer, unique=False)
    shots_blocked = Column(Integer, unique=False)
    dribble_attempts = Column(Integer, unique=False)
    dribble_succeeds = Column(Integer, unique=False)
    clearances = Column(Integer, unique=False)
    blocked_shots = Column(Integer, unique=False)
    interceptions = Column(Integer, unique=False)
    tackles = Column(Integer, unique=False)
    dribbled_past = Column(Integer, unique=False)
    touches = Column(Integer, unique=False)
    passes = Column(Integer, unique=False)
    pass_succeeds = Column(Integer, unique=False)
    key_passes = Column(Integer, unique=False)
    crosses = Column(Integer, unique=False)
    cross_succeeds = Column(Integer, unique=False)
    long_balls = Column(Integer, unique=False)
    long_ball_succeeds = Column(Integer, unique=False)
    ground_duels = Column(Integer, unique=False)
    ground_duels_won = Column(Integer, unique=False)
    aerial_duels = Column(Integer, unique=False)
    aerial_duels_won = Column(Integer, unique=False)
    possession_lost = Column(Integer, unique=False)
    fouls = Column(Integer, unique=False)
    was_fouled = Column(Integer, unique=False)
    offsides = Column(Integer, unique=False)
    saves = Column(Integer, unique=False)
    punches = Column(Integer, unique=False)
    runs_out = Column(Integer, unique=False)
    runs_out_succeeds = Column(Integer, unique=False)
    high_claims = Column(Integer, unique=False)

    def __init__(
            self, 
            match_id,
            team_name=None,
            player_name=None,
            status=None,
            position=None,
            minutes_played=None,
            sofascore_rating=None,
            goals=None,
            assists=None,
            shots_on_target=None,
            shots_off_target=None,
            shots_blocked=None,
            dribble_attempts=None,
            dribble_succeeds=None,
            clearances=None,
            blocked_shots=None,
            interceptions=None,
            tackles=None,
            dribbled_past=None,
            touches=None,
            passes=None,
            pass_succeeds=None,
            key_passes=None,
            crosses=None,
            cross_succeeds=None,
            long_balls=None,
            long_ball_succeeds=None,
            ground_duels=None,
            ground_duels_won=None,
            aerial_duels=None,
            aerial_duels_won=None,
            possession_lost=None,
            fouls=None,
            was_fouled=None,
            offsides=None,
            saves=None,
            punches=None,
            runs_out=None,
            runs_out_succeeds=None,
            high_claims=None
        ):

        self.id = str(uuid.uuid4())
        self.match_id = match_id
        self.team_name = team_name
        self.player_name = player_name
        self.status = status
        self.position = position
        self.minutes_played = minutes_played
        self.sofascore_rating = sofascore_rating
        self.goals = goals
        self.assists = assists
        self.shots_on_target = shots_on_target
        self.shots_off_target = shots_off_target
        self.shots_blocked = shots_blocked
        self.dribble_attempts = dribble_attempts
        self.dribble_succeeds = dribble_succeeds
        self.clearances = clearances
        self.blocked_shots = blocked_shots
        self.interceptions = interceptions
        self.tackles = tackles
        self.dribbled_past = dribbled_past
        self.touches = touches
        self.passes = passes
        self.pass_succeeds = pass_succeeds
        self.key_passes = key_passes
        self.crosses = crosses
        self.cross_succeeds = cross_succeeds
        self.long_balls = long_balls
        self.long_ball_succeeds = long_ball_succeeds
        self.ground_duels = ground_duels
        self.ground_duels_won = ground_duels_won
        self.aerial_duels = aerial_duels
        self.aerial_duels_won = aerial_duels_won
        self.possession_lost = possession_lost
        self.fouls = fouls
        self.was_fouled = was_fouled
        self.offsides = offsides
        self.saves = saves
        self.punches = punches
        self.runs_out = runs_out
        self.runs_out_succeeds = runs_out_succeeds
        self.high_claims = high_claims