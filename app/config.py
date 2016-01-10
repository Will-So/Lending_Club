# -*- coding: utf8 -*-
import os

default_roi_floor = .10
default_amount = 25
default_default_floor = .2

# TODO Add feature to select configuration
main_config = dict(credentials=os.environ['LENDING_CLUB_API'], investor_id=5809260,
                   portfolio_id=65013027)

iteration_2 = dict(credentials=os.environ['LENDING_CLUB_API'], investor_id=5809260,
                   portfolio_id=70552224) # Iteration 2 config