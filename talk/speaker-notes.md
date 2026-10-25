# Research with AI Agents: speaker notes

Each slide's notes are split by build step: **[k]** is what to say once click k has brought in its part; **[k–m]** covers several clicks.

## 1. Open-ended research with AI agents
Hi everyone, I'm Amir. Today's models are smart enough to do real research, but using them on open questions is surprisingly hard: they produce far more than we can check, and their mistakes are silent. What comes out is a haystack, and somewhere in it there may be a gem. This talk is about finding that gem: the practical habits I developed to use these models on open questions without losing control. It isn't a principled framework, just what worked for me, mostly in theoretical research, and everything is in a repo linked at the end. Let me start with the problem.

## 2. Smart models fail beautifully.
**[0]** Let's start with where we are today.

**[1]** We're in the middle of a fundamental transition: from writing every line of code, paper and theory ourselves, to delegating much more research to very capable models.

**[2]** The transition is hard, because in research, agents fail silently, and the smarter they get, the harder those failures are to catch. The text looks flawless, the figures look great, even the math looks great at a glance. But the real failure is hidden on page 12, in some assumption that quietly absorbs all the complexity.

**[3]** On top of that, they produce code, theory and papers far faster than we can read. So we end up with a pile of results that may contain some gems, but finding them takes an enormous amount of time: a gem in a haystack. And noise isn't only mistakes: a result can be correct but irrelevant. You lose so much control that it can defeat the purpose of using them at all.

## 3. → How do we find the gem?
So how do we find the gem?

## 4. The strategy at a glance.
**[0]** Here's the strategy at a glance, and it answers both questions. Start from one open-ended research question.

**[1]** We organize it into research thrusts: separate lines of exploration, each pushed forward.

**[2]** Most go step by step; now and then one splits, and some stop.

**[3]** And with some lag, the parts that are fully audited and relevant form the established core.

**[4]** The thrusts keep pushing out,

**[5]** and the core follows, always in one piece.

**[6]** The explored region's shore is where the uncharted waters begin.

**[7]** Instead of reading everything, you read the core: that's the signal-to-noise ratio, and that's how you stay in control.

**[8]** Finally, a part of the core is carved out and audited again, for novelty and significance: is it scientifically worthy? That's the paper, and that's the gem in the haystack. That's the map, the global strategy.

**[9]** But look at one thrust at the edge,

**[10]** pushing out into uncharted waters.

## 5. → How do we make each push succeed?
Let's zoom in. This is the frontier, and it's hard, even for a very capable model. How do we make each push succeed?

## 6. The multi-agent engine behind every thrust.
**[0]** The answer is a multi-agent engine: many agents, organized well, are what make a push into the research frontier feasible. It has four parts.

**[1]** First, why not one long thread? It accumulates everything: every dead end, every earlier claim, every sentiment.

**[2]** Once it makes an early mistake,

**[3]** everything after it is anchored to it, and telling it to be unbiased can't undo that.

**[4]** Independent agents start fresh, isolated, from different angles. The first one misses the flaw.

**[5]** So does the second.

**[6]** And the third.

**[7]** The fourth catches it, and one catch is all you need. That's how the skills run parallel proof routes and independent reviews.

**[8]** Agents can also work against each other. An author makes a claim.

**[9]** A critic objects.

**[10]** The author repairs it.

**[11]** And the critic checks again, round after round, until the objections are resolved. A single thread can't argue with itself like that.

**[12]** And it has to be cost-effective. Think of it as a pyramid. You're at the top: judgment and approval. Just below you, the most capable and most expensive models, for what's mission-critical: reviews, final checks, the hardest steps. Below them, capable models for drafting and derivations; at the base, cheaper models for code and routine runs.

**[13]** The pyramid is built so that a failure at a lower level gets caught by the audits above it.

**[14]** And at the base, the cheapest layer of all: computation. Whatever can run mechanically on a CPU or GPU, a test, a simulation, a small case, costs far less than generating tokens: a short script can refute a false claim in seconds.

## 7. → How do we do this in practice?
So how do we do this in practice?

## 8. Three foundations that make it practical.
**[0]** You can simply ask the main thread to start agents. What makes it practical are three foundations.

**[1]** Context: a coding agent, not a chat, on one always-on workstation. Then the theory, the LaTeX, the code, the results and the figures are all in reach. Agents work overnight, and even if you dispatch jobs elsewhere, the results come back.

**[2]** Persistence: everything under version control, and everything in the same place, theory included. Every snapshot holds the theory, the code, the audits and the paper together, so when an agent's refactor goes wrong, or you change your mind, you roll all of it back.

**[3]** Reuse. A project is just a folder with a file every agent in it reads, so the project's rules load by default. Prompts you type again and again become skills, which load by name or when a task matches them, and they're plain files, so they move with you to another model.

## 9. → Everything from here is a skill.
Everything from here is a skill. Here are the five.

## 10. Five skills: from open-ended question to paper.
**[0]** So the strategy rests on those foundations, and it's implemented as five skills. Here they are at a glance, from an open-ended research question to a paper.

**[1]** organize-research-project is the main one: it organizes a whole project, one big open question, into many separate thrusts, and builds the established core.

**[2]** Inside each thrust, formulate-problem pins down its question,

**[3]** solve-problem solves it, with every step checked,

**[4]** and teach-material makes sure you understand the result.

**[5]** Finally, review-paper audits the part of the core that becomes a paper, and its findings can start the next round. Let's start with the main one.

## 11. Organize: isolated thrusts, a gated core.
**[0]** The main one is the architecture: organize-research-project. A project is one big open question, and the skill rests on two ideas.

**[1–5]** From the research question, studies branch out, and the first idea is isolation: each study has its own question, inputs and folder, and by default it doesn't see the others' work. With your approval, one study can build on another.

**[6]** That way, an agent stuck on one failed idea can't drag the others into it, and you get the widest exploration. Inside each study, the agents formulate, solve and learn.

**[7]** The second idea is the established core: the studies that pass a promotion gate. A result enters only if it's correct, by an independent review; coherent, in notation, interfaces and tests; and relevant, which means your approval.

**[8–10]** These pass, and the core grows with each one.

**[11–12]** These fail and stay outside, with their evidence kept.

**[13]** So whatever is in the core is worth your time: that's the signal-to-noise ratio.

**[14]** And you build on the core:

**[15]** new studies can rely on promoted results,

**[16]** and they can be promoted in turn, so the core keeps growing. That's the organization, and it already has a lot of value.

**[17]** But let's zoom in on one thrust. Each one is a hard research question, a push into the unknown. How do we push through?

## 12. → First, what exactly is the question?
Here's one thrust: from something we already know to the next result. But look at the target: it isn't a sharp question at all. It's vague, with fuzzy boundaries, and an agent will happily answer an easier one. So first: what exactly is the question?

## 13. Formulate the steelman, then freeze it.
**[0]** Here's one thrust. In reality, the target isn't a sharp node at all. It's a vague question, and a lot of time goes into pinning down what we even want. The danger is that a vague question leaves room for answers to an easier question, and an agent will happily take them. The goal is the steelman, not the straw man: the strongest version that stays faithful to what you meant. So formulate-problem writes a research contract, and each field rules something out.

**[1]** The question itself is pinned down, so an easier target doesn't count.

**[2]** The definitions are fixed, so they can't drift halfway through.

**[3]** The quantifiers keep their order, so 'for all' can't quietly become 'there exists'.

**[4]** The evidence standard says what counts, so a proxy metric doesn't.

**[5]** And the scope is explicit, so one example can't stand in for a whole class. Notice that the vague boundary couldn't tell us whether any of these were in or out.

**[6]** Once they're ruled out, the true boundary emerges: one precise conjecture, with a sharp edge.

**[7]** Then it's frozen. A material change needs your say, and results for a changed question never count as answers to the original. Now we know exactly where the arrow points.

## 14. → Now, how do we solve it?
Now we have a frozen conjecture, and from what we know to it, a dashed arrow: the proof we still need. Now, how do we solve it?

## 15. Solve by many routes, then audit the proof.
**[0]** Solving is the second hard push, and it starts from the frozen contract.

**[1]** With your go-ahead, the proof search runs as parallel agents, one per route, and each route uses a genuinely different mechanism: duality, induction, an extremal argument. They all get the same contract, and none is told which strategy to favor, so they stay independent. After every round, a registry keeps score.

**[2]** Two routes that turn out to use the same idea are merged. A route that needs a lemma as hard as the theorem itself is marked blocked, but its valid lemmas are kept.

**[3]** Mature routes can borrow from each other: here duality supplies the missing lemma, and induction becomes a candidate proof.

**[4]** But a candidate isn't a proof yet. Separate checks rebuild every implication from the contract, check each cited theorem and its hypotheses, and hunt for counterexamples at the boundary and in degenerate cases.

**[5]** Only what survives gets written up by solve-problem: the plan first, every nontrivial step derived, no 'clearly' in place of a reason, and an answer to exactly the question in the contract.

## 16. → Solved. Do we understand it?
Solved, most likely: the arrow is solid. But understanding is still the key: to judge the result, and to build on it, we have to understand it. Do we understand it?

## 17. Learn the idea first, then every step.
**[0]** A correct proof you don't understand isn't worth much. Here's the kind of line an agent, or a paper, might hand you: private symbols everywhere. teach-material, together with explain-canonically, teaches it in layers.

**[1]** First, notation. It translates into the symbols the field already uses: the parameters theta, the loss L, its gradient. Only a few global symbols, each defined with its type before it's used.

**[2]** Then the idea, before any detail: every step goes downhill, and if the slope can't change too fast, each step lowers the loss by a definite amount. That's also the plan of the proof.

**[3]** Then a toy example that keeps the real structure: a one-dimensional quadratic, where you can see exactly when the iterates shrink to zero.

**[4]** And only then the details. When the argument invokes a theorem, it's stated right there, in the exact form needed, with its hypothesis checked and its conclusion spelled out for our objects. And if you're confused at any point, it rewrites the whole block rather than patching a sentence. Once you understand it, you can judge whether it joins the core. And that completes the loop for one thrust.

## 18. → Carved out of the core: is it a paper?
So far, results enter the core when they're correct, coherent and relevant. Now we take one compact part of the core, the part that tells a story, and carve it out as a paper. But correct isn't enough for a paper: it also needs novelty and significance, and it has to stand against the literature. Is it a paper?

## 19. Audit every claim against its evidence.
**[0]** review-paper reads the full submission, code included.

**[1]** It lifts out the three to five claims that matter most, into a ledger. Then it checks each one against its evidence.

**[2]** It re-derives the key proofs: here, the key lemma's proof fails.

**[3]** It retrieves the cited papers and checks that each citation is used correctly: one holds, and one source can't be verified.

**[4]** It audits the code: these baselines are unfair.

**[5]** It rates how plausible each conclusion is separately from how sound its argument is.

**[6]** Each flaw gets a severity: fatal, major or minor.

**[7]** And a fatal flaw cascades to every claim that depends on it: the main theorem falls with the lemma.

**[8]** The verdict says whether the central message stands, and the confidence reflects only what was actually checked. And its findings can start the next round of the project.

## 20. → Putting it all together.
Let's put it all together.

## 21. From the haystack to the core to the gem.
**[0]** Now that we've seen every piece: we start from one open-ended question.

**[1]** organize-research-project turns it into research thrusts, and inside each one, formulate, solve and learn.

**[2]** The explored region grows fast, and its shore is where the uncharted waters begin.

**[3]** Behind it, with some lag, the core grows through the promotion gate, always in one piece.

**[4–6]** That's the balance between exploration and exploitation: fresh, independent exploration out at the edge, and a core you can build on.

**[7]** And every step raises the signal-to-noise ratio: agents in adversarial positions audit each other, keep the spirit of the question, solve it without much help from us, and help us understand the result, so we can judge it quickly.

**[8]** Then review-paper audits the carved-out part as a whole paper: the claims, the literature, the novelty. Only a small part of everything we explored becomes the paper. Reading all of it would have been an enormous effort; reading and digesting this part is not. That's the gem in the haystack.

**[9]** Here's how to use it. Clone the repo, link a skill into your agent's skills folder, or make it a project's default from its AGENTS.md or CLAUDE.md. The README has the details. So let me wrap up.

## 22. From one question to a gem, and what's next.
**[0]** So to wrap up.

**[1]** We started from one open-ended question, explored it in thrusts, built a core, and carved out a gem.

**[2]** Everything we discussed has one goal: raise the signal-to-noise ratio, and save your time in every possible way, so you get what you're really after. In my own project, that meant about two hundred and thirty-five studies in eleven weeks, and only a small fraction of them ever made it into the core.

**[3]** What's next? These skills are very theory-oriented, but there's no reason they can't be adapted to other domains, and I hope people do. Two things I'd have liked to add: evaluations for skills, because right now, when you change a skill, it's not clear whether it really improved; and what I'd call live skills: a process under the hood that watches your chats, adapts your skills, maybe even writes new ones, and uses those evaluations to check.

**[4]** And a last, more philosophical note. We've gone from delegating tiny tasks to delegating maybe ninety-five percent of the mechanical work. So where does it stop? Right now, what's missing seems to be taste: knowing which direction is relevant, which is a dead end, where to explore in uncharted waters and when to stop. The good old exploration-exploitation dilemma. Ask an agent to supervise the whole thing today and you'll get a paper, at enormous cost, maybe even correct, but rarely a great one. Could we one day give a machine one open question and come back two months later to something extraordinary? There's no reason to think not. But not today.

**[5]** Everything is in the repo. Thank you.
