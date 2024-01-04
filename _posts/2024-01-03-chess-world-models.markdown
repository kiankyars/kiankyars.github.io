---
layout: post
title:  "Chess World Models"
date:   2024-01-03 16:46:58 -0600
categories: machine_learning
---

# A Chess-GPT Linear Emergent World Representation

## Introduction

Among the many recent developments in ML, there were two I found interesting and wanted to dig into further. The first was `gpt-3.5-turbo-instruct`'s ability to [play chess at 1800 ELO](https://github.com/adamkarvonen/chess_gpt_eval). The fact that an LLM could learn to play chess well from random text scraped off the internet seemed almost magical. The second was Kenneth Li's [Emergent World Representations](https://arxiv.org/abs/2210.13382) paper. There is an excellent [summary on the gradient](https://thegradient.pub/othello/) and a [follow-up from Neel Nanda](https://www.neelnanda.io/mechanistic-interpretability/othello). In it, they trained a 25 million parameter GPT to predict the next character in an Othello game. It learns to accurately make moves in games unseen in its training dataset, and using both non-linear and linear probes it was found that the model accurately tracks the state of the board.

However, this only worked for a model trained on a synthetic dataset of games uniformly sampled from the Othello game tree. They tried the same techniques on a model trained using games played by humans and had poor results. To me, this seemed like a major caveat to the findings of the paper which may limit its real world applicability. We cannot, for example, generate code by uniformly sampling from a code tree.

So I dug into it. I trained some models on chess games and used linear probes on the trained models. My results were very positive, and answered all of my previous questions (although of course, more questions were generated).

A 50 million parameter GPT trained on 10 million games of chess learns to play at ~1300 ELO in one day on 4 RTX 3090 GPUs. This model is only trained to predict the next character in PGN strings (1.e4 e5 2.Nf3 ...) and is never explicitly given the state of the board or the rules of chess. Despite this, in order to better predict the next character, it learns to compute the state of the board at any point of the game, and learns a diverse set of rules, including check, checkmate, castling, en passant, promotion, pinned pieces, etc. In addition, to better predict the next character it also learns to estimate latent variables such as the ELO rating of the players in the game.

## Training Chess GPT

My initial hypothesis was that Othello-GPT trained on human games performed poorly due to a lack of data. They only had 130k human Othello games, but the synthetic model was trained on 20 million games. I tried two different approaches to create my datasets: First, I had Stockfish ELO 3200 play 5 million games as White against a range of Stockfish 1300-3200 as Black. Hopefully, this synthetic dataset of superhuman chess bot games would provide higher quality data than human games. Second, I grabbed 16 million games from Lichess's [public chess game database](https://database.lichess.org/).

Initially, I looked at fine-tuning open source models like LLama 7B or OpenLlama 3B. However, I almost immediately had to abandon that approach to keep my GPU costs down (I used RTX 3090s from [runpod](https://www.runpod.io/)). Instead, I started training models from scratch using Andrej Karpathy's [nanogpt](https://github.com/karpathy/nanoGPT) repository. I experimented with 25M and 50M parameter models.

![A graph of Chess-GPT vs Stockfish](/images/chess_world_models/50M-Chess-GPT-win-rate.png)

It basically worked on the first try. The 50M parameter model played at 1300 ELO with 99.8% of its moves being legal within one day of training. I find it fairly impressive that a model with only 8 layers can correctly make a legal move 80 turns into a game. I left one training for a few more days and it reached 1500 ELO. I'm still investigating dataset mixes and I'm sure there's room for improvement.

So, `gpt-3.5-turbo-instruct`'s performance is not magic. If you give an LLM a few million chess games, it will learn to play chess. My 50M parameter model is orders of magnitude smaller than any reasonable estimate of `gpt-3.5`'s size, and it is within 300 ELO of its performance. In addition, we recently had confirmation that GPT-4's training dataset included [a collection of PGN format chess games](https://cdn.openai.com/papers/weak-to-strong-generalization.pdf) from players with an ELO over 1800.

I also checked if it was playing unique games not found in its training dataset. There are often allegations that LLMs just memorize such a wide swath of the internet that they appear to generalize. Because I had access to the training dataset, I could easily examine this question. In a random sample of 100 games, every game was unique and not found in the training dataset by move 20. This should be unsurprising considering there are more possible games of chess than atoms in the universe.

## Chess-GPT's Internal World Model

Next, I wanted to see if my model could accurately track the state of the board. A quick overview of linear probes: We can take the internal activations of a model as it's predicting the next token, and train a linear model to take the model's activations as inputs and predict board state as output. Because a linear probe is very simple, we can have confidence that it reflects the model's internal knowledge rather than the capacity of the probe itself. We can also train a non-linear probe using a small neural network instead of a linear model, but we risk our non-linear probe capturing noise and misleading us. 

In the original Othello paper, they found that only non-linear probes could accurately construct the board state of "this square has a black / white / blank piece". For this objective, the probe is trained on the model's activations at every move. However, Neel Nanda then found that a linear probe can accurately construct the state of the board of "this square has my / their / blank piece". To do this, the linear probe is only trained on model activation's as its predicting the Black XOR White move.

Armed with this knowledge, I trained some linear probes on my model. And once again, it basically worked on my first try. I also found that my Chess-GPT uses a "my / their" board state, rather than a "black / white" board state. My guess is that the model learns one "program" to predict the next move given a board state, and reuses the same "program" for both players. The linear probe's objective was to classify every square into one of 13 classes (blank, white / black pawn, rook, bishop, knight, king, queen). The linear probe accurately classified 99.2% of squares over 10,000 games.

I visualized some of these probe outputs. When visualizing, I would create two heat maps: one with `abs(probe output)` clipped to < 5, and one without clipping. In this case, we can see with clipping that the model is very confident on the location of the black king. Without clipping, we can see it's extremely confident that the black king is not on white's side of the board.

![3 heatmaps of the linear probe for black king location](/images/chess_world_models/king_probe.png)

We see a very similar result for the location of the white pawns, although the model is less confident. This board state comes from the 12th move in a chess game, and the model is extremely confident that no white pawns are in the either side's back rank.

![3 heatmaps of the linear probe for white pawn location](/images/chess_world_models/pawn_probe.png)

The model still knows where the blank squares are, but it is once again less confident this.

![3 heatmaps of the linear probe for blank squares location](/images/chess_world_models/blank_probe.png)

For this move in this chess game, the linear probe perfectly reconstructs the state of the board.

![2 heatmaps of the linear probe for board state](/images/chess_world_models/board_state.png)

## Probing for latent variables

Because Chess-GPT learned to predict the next move in a competitive game, rather than a game uniformly sampled from a game tree, there are interesting latent variables we can probe for. In particular, I hypothesized that to better predict the next character, it would learn to estimate the skill level of the players involved.

Initially, I trained the probe on a regression task, where its task is to predict the ELO of the White player. It would do this by training on the internal activations of the model between moves 25 and 35, as it would be extremely difficult to predict player skill early in the game. However, the majority of the games in the Lichess dataset are between 1550 ELO and 1930 ELO, which is a relatively narrow band (I'm not sure what's going on with their rating system, as chess.com's average ELO is around 800). The linear probe trained on Chess-GPT had an average error of 150 ELO, which seemed good at first glance. However, a linear probe trained on a randomly initialized model had an average error of 215 ELO. The narrow window of ELO in most games made it difficult to discern the model's level of knowledge. Distinguishing between a 1700 and 1900 ELO player just seems like a very difficult task.

So, I then trained the probe on a classification task, where it had to identify players below an ELO of 1550 or above an ELO of 2050. In this case, the probe performed much better. A probe trained on a randomly initialized model correctly classified 65% of players, while a probe trained on Chess-GPT correctly classified 89% of players.

To an extent, this is unsurprising. This reminds me of the OpenAI [Sentiment Neuron](https://openai.com/research/unsupervised-sentiment-neuron) paper. In it, they trained a LSTM to predict the next character in Amazon reviews. When they trained a linear probe on the model's internals using just 232 examples, it became a state of the art sentiment classifier. OpenAI wrote then that "We believe the phenomenon is not specific to our model, but is instead a general property of certain large neural networks that are trained to predict the next step or dimension in their inputs". With this context, it's almost an expected result.

## Caveats

The evidence here would be stronger if I also performed casual interventions on the model using these probes. For example, I could intervene to change the model's internal representation of the board state, and see if it makes legal moves under the new state of the board. Or, I could intervene on the model's representation of player skill and see if it plays better or worse. Unfortunately, I just ran out of time. This was a Christmas break project, and it's time to get back to work.

However, I still consider the findings to be strong. Linear probes have a limited capacity, and are a relatively accepted method of benchmarking what a model has learned. I followed general best practices of training the probes on a training set, and testing them on a separate test set. The board state in particular is a very concrete task to probe against. Probing for skill level does have a possibility that the model is learning some feature that is mostly correlated with skill, but 89% is a relatively good result for the difficult task of discerning the ELO of players in a chess game after 25 moves.

## Potential future work

As Neel Nanda discussed, there are many advantages to interpreting models trained on narrow, constrained tasks such as Othello or Chess. We cannot interpret what a LLM like Llama is internally modeling when predicting the next token in a poem. We can do some interpretation of simple models trained on toy tasks like sorting a list. Models trained on games provide a good intermediate step that is both tractable and interesting.

My immediate thought is that Chess-GPT is better at chess than I am. When I play chess, I perform a sort of minimax algorithm, where I first consider a range of moves, then consider my opponent's responses to these moves. Does Chess-GPT perform a similar internal calculation when predicting the next character? Considering that it is better than I am, it seems plausible.

Other potential directions:

- Perform casual interventions on the model using these linear probes.
- Investigate why the model sometimes to make a legal move or model the true state of the board.
- How does the model compute the state of the board, or the location of a specific piece?

# Appendix

## Technical probing details

Both Neel Nanda and I trained our probes to predict "my piece / their piece" instead of "white piece / black piece". To predict "white piece / black piece", you just have to train the linear probe on the model's activations at every move. To predict "my piece / their piece", you have to train the linear probe on the model's activations at every white XOR black move.

In Othello-GPT, the model had a vocabulary of 60 tokens, corresponding to the 60 legal squares where a piece could be placed. So, Neel Nanda just probed at every even move for a white "my piece / their piece" probe, and at every odd move for a black "my piece / their piece" probe. In my case, the input to Chess-GPT was a string like "1.e4 e5 2.Nf3 ...". So, I trained the white "my piece / their piece" probe on the model's activations at the index of every "." as it's predicting the next character. For example, the probe would be trained on "1." and "1.e4 e5 2." as inputs. For a black "my piece / their piece" probe, I trained it on the index of every even " " character.

## Open source code, models, and datasets

TODO