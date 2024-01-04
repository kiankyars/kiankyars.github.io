---
layout: post
title:  "Chess World Models"
date:   2024-01-03 16:46:58 -0600
categories: machine_learning
---

## A Chess-GPT Linear Emergent World Representation

## Introduction

Among the many recent developments in ML, there were two I found interesting and wanted to dig into further. The first was `gpt-3.5-turbo-instruct`'s ability to [play chess at 1800 ELO](https://github.com/adamkarvonen/chess_gpt_eval). The fact that an LLM could learn to play chess well from random text scraped off the internet seemed almost magical. The second was Kenneth Li's [Emergent World Representations](https://arxiv.org/abs/2210.13382) paper. There is an excellent [summary on the gradient](https://thegradient.pub/othello/) and a [follow-up from Neel Nanda](https://www.neelnanda.io/mechanistic-interpretability/othello). In it, they trained a 25 million parameter GPT to predict the next character in an Othello game. It learns to accurately make moves in games unseen in its training dataset, and using both non-linear and linear probes it was found that the model accurately tracks the state of the board.

However, this only worked for a model trained on a synthetic dataset of games uniformly sampled from the Othello game tree. They tried the same techniques on a model trained using games played by humans and had poor results. To me, this seemed like a major caveat to the findings of the paper. We cannot generate code by uniformly sampling from a code tree.

So I dug into it. I trained some models on chess games and used linear probes on the trained models. My results were very positive, and answered all of my previous questions (although of course, more questions were generated).

A 50 million parameter GPT trained on 10 million games of chess learns to play at ~1300 ELO in one day on 4 RTX 3090 GPUs. This model is only trained to predict the next character in PGN strings (1.e4 e5 2.Nf3 ...) and is never explicitly given the state of the board of the rules of chess. Despite this, in order to better predict the next character, it learns to compute the state of the board at any point of the game. In addition, to better predict the next character it also learns to estimate latent variables such as the ELO rating of the players in the game.

## Training Chess GPT

My initial hypothesis was that Othello-GPT trained on human games performed poorly due to a lack of data. They only had 130k human Othello games, but the synthetic model was trained on 20 million games. I tried two different approaches to create my datasets: First, I had Stockfish ELO 3200 play 5 million games as White against a range of Stockfish 1300-3200 as Black. Hopefully, this synthetic dataset of superhuman chess bot games would provide higher quality data than human games. Second, I grabbed 16 million games from Lichess's [public chess game database](https://database.lichess.org/). I am also actively experimenting with different mixes of these datasets.

Initially, I looked at fine-tuning open source models like LLama 7B or OpenLlama 3B. However, I almost immediately had to abandon that approach to keep my GPU costs down (I used RTX 3090s from [runpod](https://www.runpod.io/)). Instead, I started training models from scratch using Andrej Karpathy's [nanogpt](https://github.com/karpathy/nanoGPT) repository. I experimented with 25M and 50M parameter models.

![A graph of Chess-GPT vs Stockfish](../images/chess_world_models/50M-Chess-GPT-win-rate.png)

It basically worked on the first try. The 50M parameter model played at 1300 ELO with 99.8% of its moves being legal within one day of training. I find it fairly impressive that a model with only 8 layers can correctly make a legal move 80 turns into a game. I left one training for a few more days and it reached 1500 ELO. I'm still investigating dataset mixes and I'm sure there's room for improvement.

So, `gpt-3.5-turbo-instruct`'s performance is not magic. If you give an LLM a few million chess games, it will learn to play chess. My 50M parameter model is orders of magnitude smaller than any reasonable estimate of `gpt-3.5`'s size, and it is within 300 ELO of its performance. In addition, we recently had confirmation that GPT-4's training dataset included [a collection of PGN format chess games](https://cdn.openai.com/papers/weak-to-strong-generalization.pdf) from players with an ELO over 1800.

I also checked if it was playing unique games not found in its training dataset. There are often allegations that LLMs just memorize such a wide swath of the internet that they appear to generalize. Because I had access to the training dataset, I could easily examine this question. In a random sample of 100 games, every game was unique and not found in the training dataset by move 20. This should be unsurprising considering there are more possible games of chess than atoms in the universe.

## Chess-GPT's Internal World Model

Next, I wanted to see if my model could accurately track the state of the board. A quick overview of linear probes: We can take the internal activations of a model as it's predicting the next token, and train a linear model to take the model's activations as inputs and predict board state as output. Because a linear probe is very simple, we can have confidence that it reflects the model's internal knowledge rather than the capacity of the probe itself. We can also train a non-linear probe using a small neural network instead of a linear model, but we risk our non-linear probe capturing noise and misleading us. 

In the original Othello paper, they found that only non-linear probes could accurately construct the board state of "this square has a black / white / blank piece". For this objective, the probe is trained on the model's activations at every move. However, Neel Nanda then found that a linear probe can accurately construct the state of the board of "this square has my / their / blank piece". To do this, the linear probe is only trained on model activation's as its predicting the Black XOR White move.

Armed with this knowledge, I trained some linear probes on my model. And once again, it basically worked on my first try. I also found that my Chess-GPT uses a "my / their" board state, rather than a "black / white" board state. My guess is that the model learns one "program" to predict the next move given a board state, and reuses the same "program" for both players. The linear probe's objective was to classify every square into one of 13 classes (blank, white / black pawn, rook, bishop, knight, king, queen). The linear probe accurately classified 99.2% of squares over 10,000 games.

I visualised some of these probe outputs. When visualising, I would create two heatmaps: one with abs(probe output) clipped to < 5, and one without clipping. In this case, we can see with clipping that the model is very confident on the location of the black king. Without clipping, we can see it's extremely confident that the black king is not on white's side of the board.

![3 heatmaps of the linear probe for black king location](../images/chess_world_models/king_probe.png)

We see a very similar result for the location of the white pawns, although the model is less confident. This board state comes from the 12th move in a chess game, and the model is extremely confident that no pawns are in the opposite side's back rank.

![3 heatmaps of the linear probe for white pawn location](../images/chess_world_models/pawn_probe.png)

The model still knows where the blank squares are, but it is once again less confident this.

![3 heatmaps of the linear probe for blank squares location](../images/chess_world_models/blank_probe.png)

For this move in this chess game, the linear probe perfectly reconstructs the state of the board.

![2 heatmaps of the linear probe for board state](../images/chess_world_models/board_state.png)

## Probing for latent variables

Because Chess-GPT learned to predict the next move in a competitive game, rather than a game uniformly sampled from a game tree, there are interesting latent variables we can probe for. In particular, I hypothesised that to better predict the next character, it would learn to estimate the skill level of the players involved.

Initially, I trained the probe using Mean Squared Error loss, where its task is to predict the ELO of the White player. However, the majority of the games in the Lichess dataset are between 1500 ELO and 1900 ELO, which is a relatively narrow band. The linear probe performed better than the baseline of predicting the mean ELO, but with the narrow window it was hard to get a clear signal of the model's knowledge. 