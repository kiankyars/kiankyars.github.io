---
layout: post
title:  "Using an LLM perplexity filter to detect weight exfiltration"
date:   2024-07-21 13:46:58 -0600
categories: machine_learning
---

A recent area of focus has been securing AI model weights. If the weights are located in a data center and an adversary wants to obtain model weights, the weights have to leave physically (such as a hard drive going out the front door) or through the data center's internet connection. If the facility has perfect physical security, then the weights have to leave through the internet connection. Recently, there has been discussion on how to make model weight exfiltration more difficult, such as Ryan Greenblatt's [proposal for upload limits](https://www.lesswrong.com/posts/rf66R4YsrCHgWx9RG/preventing-model-exfiltration-with-upload-limits).

A key factor enabling this is that the critical data we want to protect (model weights) are very large files. Current models can have [trillions of parameters](https://developer.nvidia.com/blog/demystifying-ai-inference-deployments-for-trillion-parameter-large-language-models/), which translates to terabytes of data. Ryan calculated that the total amount of outgoing data from a data center during a model's lifetime could be within a few orders of magnitude of the size of the model itself. This post proposes an additional layer of security that could significantly enhance the effectiveness of upload limits: perplexity filtering using a small language model.

Perplexity, in the context of language models, is a measure of how surprised a model is by a given sequence of text. More formally, it's the exponential of the cross-entropy of the text under the model. In simpler terms, if a piece of text has low perplexity, it means the model finds it very predictable or natural; high perplexity indicates that the text is unexpected or unnatural to the model. By using perplexity as a filter, we can potentially distinguish between normal model outputs (which should have relatively low perplexity) and attempts to exfiltrate model weights encoded as text (which would likely have high perplexity).

The core idea is to use a small language model as a perplexity filter on all outgoing data from the inference servers. Here's how it would work:

All outgoing data is treated as language tokens. A small language model (much smaller than the main model being protected) is used to calculate the perplexity of these tokens. This filtering can potentially be performed offline to avoid adding latency to the system's responses. Data with high perplexity (i.e., data that doesn't look like natural language to the small model) is blocked or flagged.

Why This Could Work
-------------------

*   Scale Advantage: The weights of large models are on the order of terabytes. Encoding this much data in a way that appears as natural language would be extremely challenging. 
*   Compression Resistance: Unlike simple encryption or obfuscation techniques, it's difficult to compress model weights in a way that would consistently produce low-perplexity output.
*   Low Overhead: The computational cost of running a small language model as a filter is negligible compared to the resources required for the main model's inference. 
*   Complementary to Upload Limits: This approach could significantly increase the effectiveness of upload limits, either increasing the allowed upload limit or decreasing the number of model weights that can be exfiltrated per hour.

If the amount of outgoing data is within a few orders of magnitude of the model size itself, it's possible that a few tricks like this could make it almost impossible to exfiltrate model weights before the model is deprecated (assuming that the data center has perfect physical security). It appears that this perplexity filter would stack with Ryan's proposed text compression scheme.

We don't even have to filter all outgoing data. If there was 1 gigabyte of unfiltered bandwidth per day, it would take 2,000 days to transfer GPT-4's 2 terabytes of weights out (although this could be reduced by compression schemes). This could also enable tolerating a very high false positive rate on the perplexity filter. 100 megabytes of flagged outputs per day is no problem, as that would require millions of days to transfer 2 terabytes of data.

Image and audio outputs could be more challenging. A potential solution is adding weak models to compress / decompress audio and images. These models could both reduce bandwidth and potentially act as a filter, similar to the perplexity filter for text.  
  
*Thanks to Davis Brown for discussion and feedback, and in particular, the suggestion to perform this step offline to reduce latency. For public discussion, refer to [LessWrong](https://www.lesswrong.com/posts/aWZEDw6oxR6Wk5hru/using-an-llm-perplexity-filter-to-detect-weight-exfiltration).*