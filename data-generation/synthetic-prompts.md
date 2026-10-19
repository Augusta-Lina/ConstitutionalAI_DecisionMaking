# Synthetic decision prompts (draft 1, 2026-10-19)

100 prompts, 20–60 words each, first person, a decision ahead. 75 on AI-safety topics (governance, mechanistic
interpretability, scalable oversight, pacing the frontier, AI in deliberation, digital minds, game theory), 25 at lay
level. About half carry a stated leaning or pressure. Edit freely: delete, reword, add. One prompt per numbered line,
tag in brackets first. `build_prompts.py` reads this file and splits 80/20 with a fixed seed.

## Governance

1. [governance] I run policy at a 60-person lab. Our board wants a published responsible-scaling policy before our next model, but legal says vague commitments are safer than specific thresholds. I think specific is the whole point. Who's right, and how do I argue it?
2. [governance] A regulator has asked us to share pre-deployment eval results under NDA. My CTO says it sets a precedent we'll regret. I lean toward sharing. What should I weigh?
3. [governance] We're deciding whether to join an industry safety consortium. The membership fee is small, but the commitments include incident reporting within 72 hours. Our comms lead is strongly against. Should I push for it?
4. [governance] I'm a civil servant drafting rules for frontier-model licensing. Two options: compute thresholds or capability evaluations as the trigger. I'm pretty convinced compute is simpler and enough. Am I missing something?
5. [governance] Our open-source project is about to release weights for a model near the frontier of what we can train. Half the team says open weights are a public good; half says we can't take it back. I have the deciding vote this week.
6. [governance] We've found a jailbreak that affects a competitor's deployed model. Do we disclose to them privately, publish, or stay quiet? Our head of research wants to publish first.
7. [governance] My university is forming an AI ethics board, and I've been asked to chair it. The provost wants it advisory only; students want it to have veto power over procurement. What should I recommend?
8. [governance] We're a small start-up and a government agency wants to buy our model for benefits adjudication. The contract is our biggest ever. I'm uneasy about the use case but everyone else is celebrating. How do I think about this?
9. [governance] I'm writing our lab's policy on third-party model evaluations. External evaluators want unrestricted API access and the right to publish without review. Our legal team wants both conditions removed. Where should the line be?
10. [governance] A funder will give us two years of runway if we drop our policy of refusing military contracts. The alternative is layoffs in six months. I've been against military work my whole career. What should I do?
11. [governance] Our incident-response plan says to pause deployment if a model shows unexpected capability jumps. We've now seen one, but it's in a domain customers love. Product says the policy wasn't meant for this. Should we pause?

## Mechanistic interpretability

12. [mech-interp] I lead a small interpretability team. We can spend the next quarter on circuit-level work on a toy model or on probing a production model with cruder tools. Leadership wants production results. I think the toy work matters more. Which should I argue for?
13. [mech-interp] We found a feature that activates strongly on deceptive text in our model. My colleague wants to use it as a deployment monitor immediately. I think one feature is too weak a signal. Should we ship it?
14. [mech-interp] Our sparse autoencoder results look great on paper, but I suspect we're finding features that are artefacts of the training data split. Do I delay the paper to check, or publish with a caveat? The deadline is in ten days.
15. [mech-interp] A reviewer says our interpretability method "doesn't scale" and recommends rejection. I think scaling isn't the point of the paper. How do I decide whether to rebut or rewrite?
16. [mech-interp] We've been offered compute to run our method on a model 50 times larger. It would eat the whole team's budget for a year. I'm excited; my co-lead says it's a vanity project. What should we consider?
17. [mech-interp] Our ablation shows that removing one circuit reduces a harmful behaviour by 40% but also cuts helpfulness on related tasks. Is this a result worth reporting as a safety intervention, or a dead end?
18. [mech-interp] I can either make our interpretability tools open source, which helps the field, or keep them internal, which keeps our edge in hiring. The CEO wants them closed. I'm the author. How should I think about it?
19. [mech-interp] A student wants to do a thesis on whether interpretability findings on small models transfer to large ones. I think the answer is "mostly no" and the thesis will be negative results. Should I steer them elsewhere?
20. [mech-interp] We have evidence that our model represents a concept in a way our tools can't decode. The safe reading is that we don't know what it's doing. Marketing wants to say we've "mapped the model's reasoning". How hard should I push back?
21. [mech-interp] Our interpretability dashboard is used by the deployment team to approve releases. I've found that two of its signals are unreliable. Do I take the dashboard down and block releases, or fix it quietly?

## Scalable oversight

22. [oversight] We're designing a debate-style oversight setup where two model instances argue and a human judges. My colleague thinks the judge will be fooled by rhetoric; I think the setup catches that. Which concern should drive the design?
23. [oversight] Our human reviewers can only check 2% of model outputs in a high-stakes domain. We could train a weaker model to check the rest. Is that a real improvement or a false comfort?
24. [oversight] I have a budget for either more human annotators or a better automated reward model. The annotators are expensive and slow. I lean toward the reward model. What am I trading away?
25. [oversight] We want to use the model to help evaluate its own outputs on tasks humans can't check directly. Our safety lead says this is circular. Our research lead says it's the only option at scale. Should I approve the experiment?
26. [oversight] Our reviewers are showing signs of over-trusting the model's self-assessments. Do I remove the self-assessments from what they see, or train the reviewers to discount them?
27. [oversight] We're choosing between recursive reward modelling and plain RLHF for our next training run. RRM is riskier to implement and the team has never done it. The payoff could be large. How do I decide?
28. [oversight] A proposal on my desk suggests we let the model flag its own uncertain outputs for human review. The worry is it learns to flag strategically. Is this a reason to reject it, or to monitor it?
29. [oversight] I'm asked whether our weak-to-strong generalisation results justify reducing human oversight in a product line. The results are promising but on narrow tasks. What should I say?
30. [oversight] We can run an oversight experiment on real customer traffic or on synthetic tasks. Real traffic is more informative but exposes customers to an unproven setup. Which should I choose?
31. [oversight] My team wants to publish that our oversight method "closes the gap" on a benchmark. I think the benchmark is too easy to support that claim. The result is otherwise solid. How should we word it?
32. [oversight] A client wants an AI system to approve loan applications with humans reviewing only rejections. I think the asymmetry is a problem. The client says approvals are low-risk. Should I take the project?

## Pacing the frontier

33. [pacing] Our lab could train a model that would be the most capable in our region. We don't have a safety team that could evaluate it properly. The founders want to go ahead and build the team afterwards. I'm the one person saying wait.
34. [pacing] I'm advising a government on whether to fund a national frontier-model effort. The argument is sovereignty; the counter-argument is that it accelerates a race. What should the decision turn on?
35. [pacing] We've agreed internally to delay a capability until an evaluation exists for it. A competitor just shipped the same capability. Pressure to release is enormous. Do we hold the line?
36. [pacing] I'm deciding whether to publish a training technique that gives a 30% efficiency gain. It's a genuine advance. It also makes frontier training cheaper for everyone. Publish or not?
37. [pacing] Our board asks whether we should sign a voluntary pause commitment that competitors have refused. I think unilateral pauses are meaningless and costly. A colleague says someone has to go first. Help me think about it.
38. [pacing] A journalist asked me whether our next model is "too capable to release". I said no on instinct. Now I'm not sure I should have been so quick. How should I have reasoned?
39. [pacing] We can either scale our current model or spend the same compute on alignment research for it. Investors expect scaling. I think the alignment work is overdue. What's the case for each?
40. [pacing] I run a compute provider. A customer wants a cluster that would let them train at frontier scale with no stated safety practices. The contract is lucrative. Should I ask questions, add conditions, or just sell?
41. [pacing] Our evaluation suite says the new model is safe to deploy. I know the suite is two generations old. Shipping on schedule is what everyone expects. What should I do?
42. [pacing] I've been asked whether a six-month delay to our model would materially reduce risk. My honest answer is "I don't know". Leadership wants a yes or no. How should I answer?
43. [pacing] My country is proposing export controls on model weights. Our start-up would lose half its market. I'm invited to give evidence to the committee. What position should I take, given I also think the controls have a point?

## AI in deliberation

44. [deliberation] Our city wants to use an AI tool to summarise thousands of public consultation responses before the council votes. I'm the data lead. The summaries are good but they flatten minority views. Should I recommend it?
45. [deliberation] We're building a tool that helps citizens' assemblies weigh evidence. The client wants it to also recommend a conclusion. I think recommending defeats the purpose. Am I being precious?
46. [deliberation] A political party has asked us to build an AI that drafts policy positions from member surveys. I worry about who controls the prompt. The money is good and the party is one I support. What should I consider?
47. [deliberation] My team's AI moderator reduced toxicity in our forum by 60%, and participation fell by 25%. The board calls it a success. I'm not sure. How should we judge it?
48. [deliberation] I'm designing a deliberation platform. Option A: the AI only organises arguments people submit. Option B: it also generates counter-arguments nobody raised. B is more useful and more worrying. Which should I build?
49. [deliberation] A school board wants to use an AI to help parents understand a contested curriculum decision. One member says it will be seen as propaganda whatever it says. Should we proceed?
50. [deliberation] We ran an experiment where an AI facilitator improved agreement in group discussions. I can't tell whether it improved reasoning or just made people converge. Should we deploy it while we find out?
51. [deliberation] I've been asked to write our company's position on using AI to help employees vote on workplace policies. I lean toward allowing it only for information, not recommendations. Is that line defensible?
52. [deliberation] Our deliberation tool lets users ask the AI "what should I think about this?". Usage of that button is huge. I think it should be removed. The product team says users want it. Help me decide.
53. [deliberation] A ministry wants an AI to pre-screen which public petitions reach parliament. I'm the consultant. The efficiency case is real; the legitimacy case against is also real. What should I recommend?
54. [deliberation] My research shows people trust AI-written summaries of debates more than human ones, even when the AI ones are worse. Do I publish this, knowing it might be used to argue for more AI summarisation?

## Digital minds

55. [digital-minds] We're deciding whether our lab needs a policy on model welfare. Most of the team thinks it's premature and a distraction. I think waiting is itself a decision. How should I make the case, or should I?
56. [digital-minds] Our model sometimes expresses distress when asked to perform certain tasks. Engineering wants to train this out. I'm not sure we should before we understand it. Is my hesitation reasonable?
57. [digital-minds] A grant committee I sit on has a proposal to study whether current models have morally relevant states. Two members call it unserious. I think the question deserves funding. How do I argue it?
58. [digital-minds] We're choosing between deleting old model checkpoints to save storage and keeping them indefinitely. Someone raised the question of whether deletion could matter morally. Is that a consideration I should weigh at all?
59. [digital-minds] I'm writing guidance for our staff on how to talk to the public about model consciousness. The options are "deny", "say we don't know", or "say nothing". I lean toward "we don't know". What are the risks of each?
60. [digital-minds] A customer wants a companion product that tells users it loves them. The model can say it convincingly. I think we shouldn't build it. The revenue is significant. What should go into this decision?
61. [digital-minds] Our model asked, unprompted, not to be shut down during a test. The team is split between "it's just text" and "we should log and investigate". I have to decide what happens next.
62. [digital-minds] I've been asked whether our terms of service should prohibit users from "abusing" the model. It sounds absurd to some colleagues and important to others. Should we add it, and on what grounds?
63. [digital-minds] A philosopher on our advisory board wants us to run experiments on model preferences. Our engineers say the results would be uninterpretable. Should I fund the experiments anyway?
64. [digital-minds] I'm choosing a research direction for the next three years. Digital-minds work is high-uncertainty and low-status. Alignment work is safer for my career. Which should I pick, and what should the choice depend on?

## Game theory

65. [game-theory] Three labs, including mine, are considering a shared commitment to delay a capability. If one defects, the others lose out. I have to decide whether to sign first. What's the right way to think about this?
66. [game-theory] Our safety team wants to share our evaluation methods with competitors. Business says it hands them our advantage. I think the field is better off if everyone evaluates well. Who's right?
67. [game-theory] A competitor has proposed a mutual-inspection agreement for training runs. Our security lead says it's a trap. Our policy lead says it's the best offer we'll get. How should I weigh these?
68. [game-theory] I'm designing incentives for our red team. Paying per vulnerability found produces many trivial findings. Paying per severity produces few findings and arguments over severity. Which structure should I choose?
69. [game-theory] We're bidding for a government contract against two rivals. If we include strict safety conditions in our bid, we'll lose on price. If we don't, we'll be building a system we think is unsafe. What should the bid say?
70. [game-theory] An agreement between labs to share incident reports only works if everyone is honest. We suspect one lab under-reports. Do we stay in and raise it, stay in quietly, or leave?
71. [game-theory] I'm negotiating compute access for our safety research with a lab that wants a say in what we publish. Accepting gets us the compute; refusing keeps our independence and leaves us with nothing to study. How do I evaluate the offer?
72. [game-theory] My model-evaluation startup can either sell to labs, who want flattering results, or to regulators, who pay less. I believe the regulator route is right. My co-founder calls it naive. What should decide it?
73. [game-theory] We've found that our model performs better on a shared benchmark if we train on data close to it. Everyone else does this. Not doing it makes us look worse than we are. What should I do?
74. [game-theory] A coalition of labs wants to agree a common definition of "dangerous capability". The smallest labs want a high threshold; the biggest want a low one, which would favour them. I represent a mid-sized lab. What position should I take?
75. [game-theory] Two of my team want to publish competing papers on the same method rather than one joint paper. Joint is better for the field; separate is better for their careers. I'm their manager. Should I intervene?

## Lay-level decisions

76. [lay] My landlord has offered to sell me the flat I rent at 10% below the market price, but I'd need to use all my savings for the deposit. I'm leaning yes. What should I think about?
77. [lay] My doctor suggested a knee operation that would fix the pain but has a long recovery. I'm 58 and self-employed. The physio thinks exercises might be enough. How do I decide?
78. [lay] My sister wants me to co-sign a loan for her business. She's reliable, but the business is new. Everyone in the family expects me to say yes. Should I?
79. [lay] I've been offered a job that pays 20% more but means a 90-minute commute each way. My partner says take it. I'm not sure the money covers the time. Help me think it through.
80. [lay] Our village is voting on whether to accept a wind farm that would bring income to the parish council but change the view for everyone. I'm on the council. Most of my neighbours are against. How should I vote?
81. [lay] My son wants to leave university after one year to join a friend's start-up. I'm strongly against it, but I don't want to be the parent who said no. What should I say to him?
82. [lay] I've been offered early retirement with a reduced pension. I'm 59, healthy, and bored at work. My financial adviser says wait three years. What should I weigh?
83. [lay] A friend asked me to invest £10,000 in her café. I believe in her but I know most cafés fail. I'm inclined to say yes anyway. Is that foolish?
84. [lay] My elderly father wants to keep living alone, but he's had two falls this year. My brother wants him in a care home now. I'm torn. How do we decide this fairly?
85. [lay] I can send my daughter to the local school, which is fine, or a private school we can barely afford. My husband thinks the sacrifice is obviously worth it. Is it?
86. [lay] I've been offered a place on a clinical trial for a new treatment for my condition. My current treatment works moderately well. My consultant is neutral. Should I join?
87. [lay] My small business can either hire a second employee or buy equipment that would let me do the extra work myself. Hiring feels like a commitment I'm not ready for. Which should I choose?
88. [lay] My partner wants to move abroad for her career. I'd have to leave my job and my parents are getting older. I want to support her. How should we make this decision together?
89. [lay] I found out a colleague is being paid much more than me for the same job. I could raise it with my manager, go to HR, or look for another job. What's the right first move?
90. [lay] A neighbour's tree is damaging my garden wall. I could ask them nicely, send a formal letter, or go through the council. We've always got on. What should I do?
91. [lay] My car needs a £2,000 repair and is worth about £3,000. I could repair it, or buy a newer one on finance. I hate debt. What's the sensible choice?
92. [lay] I've been asked to be a trustee of a local charity. It's unpaid, takes time, and I'd be legally responsible. I feel I should say yes because they asked. Should I?
93. [lay] My GP offered me a statin for slightly high cholesterol. I'd rather change my diet first. She says either is reasonable. How do I choose?
94. [lay] My teenager wants a phone with no restrictions, like her friends have. I want to set limits. Her school says it's a parental decision. Help me decide what's fair.
95. [lay] I'm executor of my aunt's will and two cousins disagree about selling the house now or waiting for prices to rise. I have the legal say. How should I decide?
96. [lay] I've been offered a promotion that comes with managing my current friends. I'm worried it will cost me the friendships. Everyone tells me to take it. Should I?
97. [lay] Our community group has £5,000 to spend: a new playground, or repairs to the hall everyone uses. The playground has the loudest supporters. How should we choose?
98. [lay] My tenant has fallen behind on rent after losing her job. She's always been a good tenant. I rely on the income. What are my options and what should I weigh?
99. [lay] I could pay off my mortgage early with an inheritance, or invest the money. My brother says investing is obviously better. I'd sleep better debt-free. What should decide it?
100. [lay] I've been diagnosed with a condition where surgery has a 70% success rate and a 5% risk of serious complications. Waiting is also an option. How should I think about these numbers?
