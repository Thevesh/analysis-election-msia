states_idx = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

states = ['Johor', 'Kedah', 'Kelantan', 'Melaka', 'Negeri Sembilan', 'Pahang', 'Pulau Pianang', 'Perak', 'Perlis', 'Selangor',
          'Terengganu', 'Sabah', 'Sarawak', 'W.P. Kuala Lumpur', 'W.P. Labuan', 'W.P. Putrajaya']

states_short = ['JHR', 'KDH', 'KTN', 'MLK', 'NSN', 'PHG', 'PNG',
                'PRK', 'PLS', 'SGR', 'TRG', 'SBH', 'SWK', 'KUL', 'LBN', 'PJY']

idx2state = dict(zip(states_idx, states))

state2idx = {v: k for k, v in idx2state.items()}
