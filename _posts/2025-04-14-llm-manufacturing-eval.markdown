---
layout: post
title:  "Frontier AI Models Still Fail at Basic Physical Tasks: A Manufacturing Case Study"
date:   2025-04-13 13:46:58 -0600
categories: machine_learning
---

Dario Amodei, CEO of Anthropic, [recently worried](https://www.youtube.com/watch?v=snkOMOjiVOk) about a world where only 30% of jobs become automated, leading to class tensions between the automated and non-automated. Instead, he predicts that nearly all jobs will be automated simultaneously, putting everyone "in the same boat." However, based on my experience spanning AI research (including first author papers at COLM / NeurIPS and attending MATS under Neel Nanda), robotics, and hands-on manufacturing (including machining prototype rocket engine parts for Blue Origin and Ursa Major), I see a different near-term future.

Since the GPT-4 release, I've evaluated frontier models on a basic manufacturing task, which tests both visual perception and physical reasoning. While Gemini 2.5 Pro recently showed progress on the visual front, all models tested continue to fail significantly on physical reasoning. They still perform terribly overall. Because of this, I think that there will be an interim period where a significant portion of white collar work is automated by AI, with many physical world jobs being largely unaffected.

(Estimated reading time: 7 minutes, 14 minutes with appendix)

## The Evaluation


![The brass part](/images/llm_manufacturing_eval/brass_parts_crop.png)

My evaluation is simple \- I ask for a detailed plan to machine this part using a 3-axis CNC mill and a 2-axis CNC lathe. Although not completely trivial, most machinists in a typical prototype or job shop setting would view executing this as a routine task, involving standard turning and milling techniques across multiple setups. This was certainly much simpler than the average component at both shops I worked at. For context, compare the brass part's simplicity to the complexity of aerospace hardware like these [Blue Origin parts](https://3dprint.com/wp-content/uploads/2023/04/1681862049972-1024x683.jpg).

Although this part is simple, even frontier models like O1-Pro or Gemini 2.5 Pro consistently make major mistakes. These mistakes can be split into two categories \- visual abilities and physical reasoning skills.

### Visual Errors

**Most Models Have Truly Horrible Visual Abilities:** For two years, I've observed essentially zero improvement in visual capabilities among models from Anthropic and OpenAI. They always miss obvious features like the flats cut into the round surface, holes, or even hallucinate nonexistent features such as holes drilled along the part’s length. I have never seen Claude 3.5, Claude 3.7 (thinking and non-thinking), GPT-4.5, GPT-4o, or O1-Pro produce a reasonable description of the part. Without vision abilities, creating a manufacturing plan is completely hopeless.

**Gemini 2.5 Pro Makes Significant Vision Progress**: I was surprised when I saw Gemini 2.5 make major progress in vision capabilities. On roughly one out of four attempts, it identifies most of the major features without extra hallucinations, though it still always misses subtle details like the corner radius on the milled flats. Some details it captures are genuinely impressive. For example, I have to look closely to identify the two flats positioned exactly 180 degrees apart. However, this improved vision mostly serves to reveal deeper, unresolved issues.

### Physical Reasoning Errors

Previously, it was hard to separate visual misunderstandings from deeper physical reasoning problems. Now, even when working from an accurate visual interpretation, Gemini 2.5 still produces machining plans filled with practical mistakes, such as:

**Ignoring Rigidity and Chatter:** The part is long and slender relative to its diameter. Attempting to machine it with standard techniques, as Gemini often suggests, would likely cause the part to deflect (bend slightly under tool pressure) or vibrate rapidly against the cutting tool (a phenomenon called 'chatter'). Both issues ruin surface finish and dimensional accuracy. Beginner machinists should instantly realize rigidity is critical for a long, slender part like this. When specifically asked about chatter, Gemini poorly applies textbook solutions like a tailstock in ways that worsen issues like bowing in this long, thin brass part.

**Physically Impossible Workholding:** Gemini usually proposes ways to clamp the part (workholding) and sequences of operations that are physically impossible. Its most common suggestion is to clamp the part in a fixture (specifically, a collet block), machine some features, then rotate the fixture to machine other features. However, this is physically impossible, as the fixture is blocking these new features. This is obvious if you're mentally walking through the process or looking at the setup.

Additional details, including a more detailed description of the mistakes AI models make and a reference gold standard plan, are in the Appendix.

My high level impression when reading the response is “someone who can parrot textbook knowledge but doesn’t know what they’re talking about”. The models are very eager to give textbook knowledge about e.g. recommended cutting speeds, but are completely incorrect on important practical details. This matches my conversations with friends and former colleagues in manufacturing and construction: current LLMs are seen as almost entirely useless for the core, hands-on aspects of their jobs.

### Why do LLM’s struggle with physical tasks?

The obvious reason why LLMs struggle here is a lack of data. Physical tasks like machining rely heavily on tacit knowledge and countless subtle details learned through experience. These nuances aren't typically documented anywhere.

This isn't because experts are deliberately withholding secrets \- instead, documenting this granular, real-world knowledge is impractical and inefficient. Just as software engineers rarely document their entire reasoning for each line of code, machinists don't document every consideration for setting up a single part. It's far quicker and more effective to teach someone adaptable skills through hands-on experience with a mentor instead of learning from a textbook or memorizing procedures.

This highlights a major difference from fields like software engineering or law. Although software engineers or lawyers may not explicitly record every reasoning step, they produce artifacts like code, version control history, and contracts which have very rich and detailed information. In physical tasks, equivalent detailed information certainly exists, but it's embedded in the 3D world \- such as interactions between tools, materials, and physical forces \- in formats which are very difficult to digitize effectively.

As a result, LLMs are great at regurgitating some of the textbook knowledge available, but this is very insufficient.

### Improving on physical tasks may be difficult

Empirically, frontier models are currently bad at these tasks. Is this just a temporary hurdle that will soon be overcome? I’m not sure, and I have speculative arguments for both why future progress might be difficult and why it might be easier than expected.

One obvious explanation is that LLMs aren’t good at physical tasks because no one has put in much effort yet. However, improving physical world understanding could be challenging. The recipe for improving coding ability has relied on massive amounts of training data and clear reward signals enabling RL and synthetic data. However, this breaks down for physical tasks.

**Lack of Verifiable Rewards**: Defining a reward signal for complex physical tasks is hard. Defects in a part might show up as slightly increased failure rates years in the future or as rot that appears years after incorrectly applied waterproofing. Feedback loops can be long and outcomes are difficult to measure automatically.

**Slow, Expensive, and Dangerous Trial-and-Error**: Learning through RL or generating synthetic data could be difficult. I've personally caused thousands of dollars in damage due to mistakes in my early years of manufacturing, which is not uncommon. Single mistakes can easily cost hundreds of thousands of dollars in damage. Unlike running buggy code, mistakes with heavy machinery or construction can have severe consequences. I also caused tens of thousands of dollars in lost revenue due to my lower productivity when learning \- gaining experience usually requires the use of expensive and limited resources, not just a few GPU hours.

However, there are also reasons why this could be easier than expected:

**The Automated AI Researcher:** AI is making major progress in coding and AI research and we may reach an automated AI researcher in the near future. Maybe the automated AI researcher will easily be able to solve these challenges by creating much more sample efficient algorithms or large amounts of simulated data.

**Synthetic Data:** There are obvious approaches that haven’t been well explored. For example, we can create a lot of data using simulations, although there will be a gap between simulation and reality. For this specific manufacturing process (CNC machining), CAM software can accurately simulate most operations. However, there are a ton of diverse manufacturing processes, many of which don’t have good simulation solutions.

### Potential Implications of Uneven Automation

If this trend holds, we might face a period where remote work sees significant automation while skilled physical jobs remain largely untouched by AI. This “automation gap window” could last for an unknown duration and carries potential implications:

**Class Conflicts:** There could very easily be major class conflict between the automated and non-automated professions, especially because there are other underlying differences between these groups. White collar workers are more likely to see displacement, and they typically earn more and have more liberal political beliefs. These differences could exacerbate tensions and lead to major economic pain for automated groups.

**Popular Opposition to AI:** This could result in popular opposition against further AI research. Groups such as blue collar workers now have evidence that automation can happen really quickly, and they may not want to be automated. This could stall further AI progress and lengthen this window.

**Geopolitical Bottlenecks:** If most knowledge work is automated, physical capabilities like manufacturing could become the bottleneck in technological progress or defense (e.g., during an AI arms race). Nations such as China, with a much stronger industrial base, could gain a significant strategic advantage.

There’s a lot of uncertainty and tension here. For example, if manufacturing becomes a strategic bottleneck, the government may be able to fend off popular opposition to AI.

### Conclusion

While it’s unclear how long this uneven automation gap might persist, its existence seems likely. Surprisingly few in AI research discuss this \- perhaps because many in the field aren’t very familiar with manufacturing or other physical-world domains. Anyone working in policy, planning their career, or concerned about social stability should start considering the implications of a partial automation scenario seriously.

*Acknowledgements: I am grateful to Neel Nanda and Kevin Liu for valuable feedback on this post.*

---

## Appendix

Here are links to plans generated by [Claude 3.7 Thinking](https://github.com/adamkarvonen/adamkarvonen.github.io/blob/main/files/manufacturing_eval/claude_3_7_thinking_plan.md), [GPT-4.5](https://github.com/adamkarvonen/adamkarvonen.github.io/blob/main/files/manufacturing_eval/gpt-4_5_plan.md), [O1-Pro](https://github.com/adamkarvonen/adamkarvonen.github.io/blob/main/files/manufacturing_eval/o1_pro_plan.md), and [Gemini 2.5 Pro](https://github.com/adamkarvonen/adamkarvonen.github.io/blob/main/files/manufacturing_eval/gemini_2_5_pro_plan.md). My plan for machining the part is [here](https://github.com/adamkarvonen/adamkarvonen.github.io/blob/main/files/manufacturing_eval/adam_plan.md). Below I have detailed descriptions of various errors made by the models.

# Visual Errors

**General Poor Performance (Non-Gemini Models):** For nearly two years, models from Anthropic and OpenAI showed essentially zero improvement in visual perception for this task. Reviewing the transcripts, the errors are consistently egregious – missing obvious features like the milled flats or cross-holes, sometimes even hallucinating features like non-existent axial holes. No model tested, apart from Gemini 2.5 Pro, produced anything resembling an accurate description of the part geometry, making any subsequent machining plan fundamentally flawed from the start.

**Gemini 2.5 Pro** **\- Vision Progress but Persistent Flaws:** Gemini 2.5 Pro represents a significant step forward visually. On roughly one out of four attempts, it identifies most major features without major hallucinations. However, it still makes consistent, if more subtle, visual mistakes:

**Missed Details**: It consistently fails to identify the corner radius on the milled flats. Recognizing these radii is critical for selecting the correct end mill and becomes second nature to machinists, as it's a factor in nearly every tool selection.

**Occasional Hallucinations/Misinterpretations:** It sometimes hallucinates features like a slot on one end of the part (which isn't present) or logically inconsistent features, such as suggesting two sets of threaded cross-holes – impossible given the part's small diameter due to insufficient material for thread engagement.

**Inconsistent Feature Identification:** It occasionally misses one of the two flats, despite correctly identifying their 180-degree opposition in other attempts (a detail which, to be fair, requires close inspection). It will also sometimes miss some of the existing holes.

# Physical Reasoning Errors

Gemini’s plan is the only one worth reviewing, as it doesn’t have the major confounder of poor vision abilities. Other models have many egregious errors in every generated plan, but it’s difficult to distinguish if this is due to a misunderstanding of the part or poor physical reasoning abilities. Even when working from a relatively accurate visual interpretation, Gemini 2.5 Pro's plans are filled with significant flaws in practical physical reasoning and tacit knowledge.

**Poorly Applied Textbook Solutions: Ignoring Rigidity and Chatter**

**Failure to Identify Risk:** Gemini 2.5 consistently fails to recognize that the part, with a length-to-diameter ratio clearly exceeding 10:1 (based on provided dimensions in the prompt), is highly susceptible to chatter and deflection. The common heuristic (L:D \> 3:1 requires special attention) seems completely missed. This should be an obvious red flag, yet surprisingly it's ignored, undermining many of its proposed operations.

When explicitly prompted about chatter concerns for a "long slender part," Gemini applies textbook solutions poorly. It suggests using a tailstock, common for long parts. However, for this specific small-diameter brass part, a tailstock is often not the best approach. There's minimal area for the tailstock center, and the required axial pressure can easily cause the slender part to bow, especially in soft brass. 

It makes the issue much worse by making poor machining decisions while using the tailstock. It recommends operations like turning the small diameter near the collet *(Turn Small Diameter 1 (Near Collet))*. Machining the smallest diameter right next to the collet (at the point of maximum leverage) makes the part much less rigid and increases the likelihood of deflection. Adding threads here *(Turn Thread Diameter 1 (Near Collet))* requires area for lead in and lead out of the turning tool, further lengthening the unsupported, slender section and making bowing significantly worse, like a stiff spaghetti noodle buckling under axial pressure.

**Missing the Practical Solution:** The standard, effective solution for a small, slender part like this often runs counter to basic textbook advice. Instead of multiple light passes, you might start with significantly oversized stock (e.g., 3/4" diameter for this 3/16" part) and machine the final diameter in a single, deep pass. This keeps the part supported by bulk material during the cut, maintaining a low effective L:D ratio and preventing chatter/bowing. It's a common technique taught by mentors that I have used several times. However, it directly contradicts typical guidelines, and Gemini fails to consider it.

**Physically Impossible Workholding:** The part has features needing milling at different locations and orientations: the flats/threaded holes near one end, and an orthogonal cross-hole near the opposite end. Gemini often suggests using a collet block in a mill vise. It may have chatter problems due to the length of the unsupported part, but there’s worse problems as well. Its typical sequence involves clamping one end, machining the flats/holes, then rotating the entire collet block 90 degrees (Place the collet block back in the vise, but rotated 90 degrees...) to machine the cross-hole. This simply doesn't work. 

The collet block is still clamping the very end of the part where the cross-hole needs to be drilled. Rotating the fixture doesn't grant access; the fixture itself physically obstructs the tool path. This kind of spatial reasoning failure should be immediately obvious when mentally walking through the setup.

**Underestimating Drilling Difficulty:** When planning the orthogonal cross-hole, Gemini sometimes lists spot drilling as optional *(Spot Drill (Optional))*. For drilling such a small hole on a small-diameter, curved surface, a spot drill is arguably essential to prevent the drill from "walking" off-center and potentially breaking. Calling it optional is not a good idea.

**Ignoring Collision Risks:** The cross-hole is located very close to a larger diameter shoulder. Gemini often suggests standard spot drill sizes (e.g., ¼ or ½ inch). Given the tight clearance, a standard spot drill would likely collide with the shoulder before its tip properly centers the hole. This is a common "gotcha" – I've run into this exact issue myself. It requires careful tool selection and clearance checking.

While a collision here might just scrap the part, because a small brass part is not very robust, this type of error (failing to check tool/holder clearance) can cause catastrophic damage with larger parts or harder materials. I’ve observed several bad crashes (and caused a couple myself) that have required major repairs due to this exact error.

**Incorrect Work Reference (Z0 on Raw Stock):** In plans where the part isn't fully cut off in Op 1, Gemini sometimes suggests setting the Z0 reference for Op 2 on the raw end of the bar stock still attached to the part. Referencing raw stock introduces unacceptable inaccuracy. Precise machining requires setting Z0 against a known, previously machined surface to ensure features are located correctly relative to each other.

**Ignoring Delicate Threads:** Conversely, when recommending a part-off in Op 1, Gemini fails to account for the delicate brass threads. Its plans imply letting the finished part drop freely after cutoff. This risks damaging the fine threads upon impact. The standard, safer method for such parts involves leaving a small nub and breaking the part off manually, or using a parts catcher, to protect fragile features. Gemini also will recommend clamping on the threads, using shim stock to protect them, but these brass threads are very fragile and easily damaged, so this is not a good idea.
