SELECT * FROM information_schema.tables

-- league:= league and cup
create table league (
	id serial primary key,
	code VARCHAR(30) unique not null
);

create table season(
    id serial primary key,
    code VARCHAR(9) unique not null,
    league_id int not null,
    CONSTRAINT fk_season_league
      FOREIGN KEY(league_id)
	  REFERENCES league(id)
);

 create table round(
     id serial primary key,
     number VARCHAR(4) unique NOT NULL,
     season_id int not null,
     CONSTRAINT fk_round_season
       FOREIGN KEY(season_id)
 	  REFERENCES season(id)
 );

create table team(
    id serial primary key,
    code varchar(30) not null,
    nickname varchar(10)
);

create table team_standing(
    id serial primary key,
    ranking int,
    points int,
    win_ratio decimal(4,2),
    win_last6 int,
    draw_last6 int,
    lost_last6 int,
    round_id int,
    team_id int not null,
    CONSTRAINT fk_teamstanding_team
       FOREIGN KEY(team_id)
 	  REFERENCES team(id),
 	CONSTRAINT fk_teamstanding_round
       FOREIGN KEY(round_id)
 	  REFERENCES round(id)
)

create table euroOdds(
    id serial primary key,
    code varchar(30) not null,
    open_home_win decimal(3,2),
    open_draw decimal(3,2),
    open_guest_win decimal(3,2),
    end_home_win decimal(3,2),
    end_draw decimal(3,2),
    end_guest_win decimal(3,2),
    open_home_winprob decimal(4,2),
    open_drawprob decimal(4,2),
    open_guest_winprob decimal(4,2),
    end_home_winprob decimal(4,2),
    end_drawprob decimal(4,2),
    end_guest_winprob decimal(4,2),
    host_teamstanding_id int not null,
    guest_teamstanding_id int not null,

    CONSTRAINT fk_euroodds_host_teamstanding
       FOREIGN KEY(host_teamstanding_id)
 	  REFERENCES team_standing(id),
 	CONSTRAINT fk_euroodds_guest_teamstanding
       FOREIGN KEY(guest_teamstanding_id)
 	  REFERENCES team_standing(id)
)

create table asiaOdds(
    id serial primary key,
    code varchar(30) not null,
    open_homewager decimal(3,2),
    open_handicap decimal(3,2),
    open_guestwager decimal(3,2),
    end_homewager decimal(3,2),
    end_handicap decimal(3,2),
    end_guestwager decimal(3,2),
    host_teamstanding_id int not null,
    guest_teamstanding_id int not null,

    CONSTRAINT fk_asiaodds_host_teamstanding
       FOREIGN KEY(host_teamstanding_id)
 	  REFERENCES team_standing(id),
 	CONSTRAINT fk_asiaodds_guest_teamstanding
       FOREIGN KEY(guest_teamstanding_id)
 	  REFERENCES team_standing(id)
)

create table bookie(
    id serial primary key,
    code varchar(30) not null,
    nickname varchar(30),
    euroodds_id int,
    asiaodds_id int,
    CONSTRAINT fk_bookie_euroodds
       FOREIGN KEY(euroodds_id)
 	  REFERENCES euroOdds(id),
 	CONSTRAINT fk_bookie_asiaodds
       FOREIGN KEY(asiaodds_id)
 	  REFERENCES asiaOdds(id)
)

create table votes(
    id serial primary key,
    host_win_vote int,
    draw_vote int,
    guest_win_vote int,
    host_win_ratio decimal(4,2),
    draw_ratio decimal(4,2),
    guest_win_ratio decimal(4,2),
    host_teamstanding_id int not null,
    guest_teamstanding_id int not null,
    CONSTRAINT fk_asiaodds_host_teamstanding
       FOREIGN KEY(host_teamstanding_id)
 	  REFERENCES team_standing(id),
 	CONSTRAINT fk_asiaodds_guest_teamstanding
       FOREIGN KEY(guest_teamstanding_id)
 	  REFERENCES team_standing(id)
)

-- drop table team_standing;
-- drop table team;
-- drop table round;
-- drop table season;
-- drop table league;
-- drop table bookie;
-- drop table votes;
-- drop table euroOdds;
-- drop table asiaOdds;