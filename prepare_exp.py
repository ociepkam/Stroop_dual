#!/usr/bin/env python
# -*- coding: utf8 -*

import random
from psychopy import visual

stim_text = {'CZERWONY': 'red', 'NIEBIESKI': '#5e75d9', 'BRAZOWY': '#574400', 'ZIELONY': 'green'}  # text: color
stim_neutral = "HHHHHHHH"
stim_distractor = ['WYSOKA', 'UKRYTA', u'GŁĘBOKA', 'DALEKA']

colors_text = stim_text.keys()
random.shuffle(colors_text)
colors_names = [stim_text[color] for color in colors_text]
left_hand = colors_text[:2]
right_hand = colors_text[2:]


def add_text(text1, text2):
    len1 = len(text1) - 0.4 * text1.count("I")
    len2 = len(text2) - 0.4 * text2.count("I")
    num = int(abs(len1 - len2) * 1.5)
    spaces = " " * num
    if len(text1) > len(text2):
        return text1 + "\n" + spaces + text2
    else:
        return spaces + text1 + "\n" + text2


def prepare_trial(trial_type, win, text_height):
    if trial_type == 'congruent_strong':
        text = random.choice(stim_text.keys())
        color = stim_text[text]
        text = add_text(text, text)

    elif trial_type == 'congruent_weak':
        text = random.choice(stim_text.keys())
        color = stim_text[text]
        stim_distr = random.choice(stim_distractor)
        text = add_text(text, stim_distr)

    elif trial_type == 'incongruent_strong':
        text = random.choice(stim_text.keys())
        if text in left_hand:
            possible_colors = [stim_text[key] for key in right_hand]
        else:
            possible_colors = [stim_text[key] for key in left_hand]
        color = random.choice(possible_colors)
        text = add_text(text, text)

    elif trial_type == 'incongruent_weak':
        text = random.choice(stim_text.keys())
        if text in left_hand:
            possible_colors = [stim_text[key] for key in right_hand]
        else:
            possible_colors = [stim_text[key] for key in left_hand]
        color = random.choice(possible_colors)
        stim_distr = random.choice(stim_distractor)
        text = add_text(text, stim_distr)

    elif trial_type == 'neutral':
        text = add_text(stim_neutral, stim_neutral)
        color = random.choice(stim_text.values())

    else:
        raise Exception('Wrong trigger type')

    stim = visual.TextStim(win, color=color, text=text, height=text_height, alignHoriz='center')

    return {'trial_type': trial_type, 'text': text, 'color': color, 'stim': stim}


def prepare_part(trials_congruent_strong, trials_congruent_weak, trials_incongruent_strong, trials_incongruent_weak,
                 trials_neutral, win, text_height):
    trials = ['congruent_strong'] * trials_congruent_strong + \
             ['congruent_weak'] * trials_congruent_weak + \
             ['incongruent_strong'] * trials_incongruent_strong + \
             ['incongruent_weak'] * trials_incongruent_weak + \
             ['neutral'] * trials_neutral
    random.shuffle(trials)
    return [prepare_trial(trial_type, win, text_height) for trial_type in trials]


def prepare_exp(data, win, text_size):
    text_height = 2 * text_size
    training1_trials = prepare_part(data['Training1_trials_congruent_strong'],
                                    data['Training1_trials_congruent_weak'],
                                    data['Training1_trials_incongruent_strong'],
                                    data['Training1_trials_incongruent_weak'],
                                    data['Training1_trials_neutral'], win, text_height)

    training2_trials = prepare_part(data['Training2_trials_congruent_strong'],
                                    data['Training2_trials_congruent_weak'],
                                    data['Training2_trials_incongruent_strong'],
                                    data['Training2_trials_incongruent_weak'],
                                    data['Training2_trials_neutral'], win, text_height)

    experiment_trials = prepare_part(data['Experiment_trials_congruent_strong'],
                                     data['Experiment_trials_congruent_weak'],
                                     data['Experiment_trials_incongruent_strong'],
                                     data['Experiment_trials_incongruent_weak'],
                                     data['Experiment_trials_neutral'], win, text_height)

    return [training1_trials, training2_trials], experiment_trials, colors_text, colors_names
