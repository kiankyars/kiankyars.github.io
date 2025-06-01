# **Controlled CoT Intervention: Measuring CoT Determinism**

## Kian Kyars, Final Year Undergraduate Student

## **problem statement and why it interests me**

I was inspired by the research problems in the [Understanding thinking models](https://docs.google.com/document/d/1p-ggQV3vVWIQuCccXEl1fD0thJOgXimlbBpGk6FI32I/edit?tab=t.0) section and performed a “rigorous black box investigation[^1]” on intervening manually on the CoT to understand the extent to which DeepSeek R1 Llama 8B’s reasoning is deterministic, and whether reasoning processes which result in an incorrect versus correct answer have a role in determinism, i.e. are correct CoT paths deterministic and incorrect CoT paths stochastic? This problem is interesting to me for two reasons: firstly, the visible chain-of-thought from DeepSeek and other models has made it a mainstream concept, as opposed to other problems in interpretability research. Secondly, given the recentness of CoT models, I am convinced that there is a disproportionately higher amount of low-hanging fruit in this problem set.

## **high-level takeaway**

Both correct and incorrect chain of thought reasoning processes are non-deterministic, i.e. they diverge. This was despite my controlled CoT intervention, which ensured the first reasoning step was always the same. Notwithstanding, analyzing the [branching factor](#graph-1) and [similarity divergence](#graph-2) for correct versus incorrect paths shows an inherent difference.

The most interesting part of the project was learning about model internals so I could manually plant the first reasoning step, requiring understanding special tokens formatting with \<think\> and \<|Assistant|\> tags, etc. Secondly, it was a fun challenge to work in the constraints of google colab, having only 15 GB of VRAM, which I exceeded numerous times, resulting in the beloved: “RuntimeError: CUDA error: out of memory."

## **experiment breakdown**

Distilled R1 is prompted once with a formal logic multiple-choice MMLU question, then I reformat its chain-of-thought reasoning into an explicit step-by-step process using Gemini 2.0 Flash-Lite. Using the re-formated steps, I ‘plant’ the first reasoning step in every prompt and run 10 sample iterations for the same question. I do this for 100 questions. At the end, I have a dataset of 100 formal logic questions, each with 10 CoT answers. The below graphs are calculated by accumulating the reasoning steps over all 100 questions.

### 

### Graph 1 {#graph-1}

Reasoning paths which give the correct answer tend to have lower branching factors, suggesting more deterministic steps, while incorrect paths branch more, indicating greater uncertainty or divergence. The first step is planted manually, therefore the branching factor is 1\.

### 

### Graph 2 {#graph-2}

### 

Correct paths maintain higher similarity, suggesting consistency in reasoning. Incorrect paths diverge more, reflecting erratic decision-making. Once again, the first step has perfect similarity, since it’s always the same. SentenceTransformer is used to embed the reasoning steps in both experiments.

### 

## **links**

* Colab: [KianKyarsMATS.ipynb](https://colab.research.google.com/drive/1iEMNwrRTidxH32ZUuA50NOo7LG6zXyv0)  
* [🤗 Dataset I created for prompt intervention](https://huggingface.co/datasets/kyars/CoTIntervention)

[^1]:  As worded by Neel Nanda