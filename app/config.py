# -*- coding: utf8 -*-
import os

default_roi_floor = .14
default_amount = 25
default_default_floor = .2

# TODO Add feature to select configuration
main_config = dict(credentials=os.environ['LENDING_CLUB_API'], investor_id=5809260,
                   portfolio_id=65013027)

iteration_2 = dict(credentials=os.environ['LENDING_CLUB_API'], investor_id=5809260,
                   portfolio_id=70552224) # Iteration 2 config

will_ira = dict(credentials=os.environ['IRA_LENDING_CLUB_API'], investor_id=None,
             portfolio_id = None)

ira_2 = dict(credentials=os.environ['IRA_2_LENDING_CLUB_API'], investor_id=None,
             portfolio_id = None)
