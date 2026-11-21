# Exam toolkit

The practice exam is a Moodle quiz of 26 questions, each worth 1 mark, in about 70 to 80 minutes. Almost every question has 4 options (a to d), and a few say "Select one or more" (3 in the practice exam). There is no coding: it is small calculations on a basic calculator, plus short theory questions (name the method, spot the false statement). The wrong numeric options sit very close to the right one (0.4706 against 0.4715, 0.4721, 0.4701), so the arithmetic must be exact, not roughly right. This guide is the short version of the week-by-week notes: for each type of question, a recipe you can follow, one worked example with every intermediate number, and the slips that produce the wrong options. Q-numbers (Q3, Q21 ...) refer to the questions of the released practice exam.

## How to approach the exam

- **Time.** 26 questions in 75 minutes is about 3 minutes each. Calculation questions deserve 2 to 3 minutes, theory questions 1 minute. Bank the minutes you save on theory for the long calculations.
- **Write the numbers down.** Copy the given numbers from the stem onto scratch paper before you touch the calculator. Most wrong answers are a mis-copied number, not a wrong idea.
- **Keep full precision, round once at the end.** Do not round intermediate values to 2 decimals. The options differ in the 3rd or 4th decimal, and early rounding can land you on the neighbour option.
- **Look at all four options before you start.** The options tell you the form of the answer (a fraction, a percentage, bits, a vector) and often reveal the slip each wrong option stands for. If your answer matches none, you have made a slip, and the closest option usually shows which one.
- **Compare close options by checking one more digit.** If your answer is 0.4706 and the options are 0.4706 and 0.4701, you are fine. If you got 0.4703, redo the arithmetic: that value is not an option for a reason.
- **Trap list to run through before you click.** Posterior or likelihood? Which log base (entropy base 2, AdaBoost and likelihood natural)? Weighted or unweighted? Which class is "positive"? Denominator = predicted positives (precision) or actual positives (recall)? Similarity or distance?
- **Multi-select.** If the stem says "Select one or more", judge every option on its own as true or false, then tick exactly the true ones. Do not stop at the first true option. In the practice exam these were Q10, Q21 and Q26.
- **Units and rounding.** Check whether the answer is a probability (0 to 1) or a percentage, and whether the stem says "natural log" or "bits". Quote to the number of decimals the options use.
- **When to skip.** If a diagram question (a ReLU network) will take more than 4 minutes, flag it and come back. Do not leave a single-answer question blank unless the exam instructions say wrong answers lose marks (check them, the practice exam does not say): with 4 options a guess has a 25% chance, and eliminating two options makes it 50%. A blind guess on a "select one or more" question is much worse than 25%, because you must get the whole set right.
- **Theory statements.** "Always" and "never" are a warning sign: look for a counter-example before you tick (but some are true, for example information gain is never negative). Precise claims such as "reduces variance", "needs labels" or "assumes independence given the class" are more often true, but still check them against the cheat-sheet.

## The question types, with recipes

### 1. Bayes' rule with a prior and a test

In plain words: you see an outcome (a lost bet, a blue ball, a positive test) and ask which cause is more likely. Each cause gets a score = how likely the cause was to start with × how likely it was to produce the outcome. Your answer is that cause's share of the total score.

**Looks like.** Two slot machines with win rates 10% and 20%, you lose once, probability you picked machine B (Q3). Two jars and a biased coin, you drew blue, probability it came from jar A (Q23).

**Recipe.**
1. List the causes with their priors (P(B) = 0.5, P(A) = 0.5).
2. For each cause write the likelihood of what you saw (P(lose | B) = 0.8, P(lose | A) = 0.9).
3. Multiply prior × likelihood for each cause (the "joint" scores: 0.4 and 0.45).
4. Add the scores. This is the evidence, by total probability: P(lose) = 0.4 + 0.45 = 0.85.
5. Divide the score of the cause you want by the evidence.

**Natural-frequency table method** (same answer, no formula). Imagine 1000 plays. 500 on B and 500 on A. B loses 80% of 500 = 400 times, A loses 90% of 500 = 450 times. Of the 850 lost plays, 400 were on B.

**Worked example (Q3).** P(B | lose) = (0.5 × 0.8) / (0.5 × 0.8 + 0.5 × 0.9) = 0.4 / 0.85 = 0.4706. Answer a.

Second example (Q23). The coin sends you to jar A with probability 0.8, to jar B with 0.2. Jar A is 50% blue, jar B is 40% blue. Score A = 0.8 × 0.5 = 0.4. Score B = 0.2 × 0.4 = 0.08. Evidence = 0.48. P(A | blue) = 0.4 / 0.48 = 0.8333.

**Traps.**
- Answering with the likelihood (0.8) instead of the posterior: P(lose | B) is not P(B | lose).
- Using the wrong colour or outcome: the jar question was about blue, not red. Use the likelihood of what you actually saw.
- Dividing by one score instead of the sum (the evidence must add all causes).
- Forgetting the prior when the prior is not 50/50 (the coin was 0.8/0.2).
- A rare cause keeps a low posterior even after a positive result. Always weigh by the prior.

### 2. Conditional probability from a given distribution

In plain words: first make the weights into real probabilities (they must add to 1), then throw away the outcomes that the condition excludes and ask what share the wanted outcome has of what remains.

**Looks like.** A die twice as likely to show an even face as an odd face: P(X = 3 | X > 2) (Q18).

**Recipe.**
1. Turn the description into weights: odd faces weigh 1, even faces weigh 2.
2. Normalise: total weight 3 × 1 + 3 × 2 = 9, so odd faces have probability 1/9 and even faces 2/9.
3. Add the probabilities of the outcomes allowed by the condition (the denominator).
4. Divide the probability of the wanted outcome by that sum: P(A | B) = P(A and B) / P(B).

**Worked example (Q18).** X > 2 allows faces 3, 4, 5, 6: 1/9 + 2/9 + 1/9 + 2/9 = 6/9. Wanted: face 3 = 1/9. P(X = 3 | X > 2) = (1/9) / (6/9) = 1/6 = 0.1667. Answer c.

**Traps.**
- Using 1/9 (the unconditional P(X = 3)): it is 0.1111, which is close to the option 0.1121 but is not it. Neither is the answer.
- Using 1/6 as the face probability (a fair die) gives 1/4 after restricting. Normalise first.
- Picking an even face by mistake: P(X = 4 | X > 2) = (2/9)/(6/9) = 0.3333, and 2/9 = 0.2222 is the unconditional P(even face). Both are options.
- Dividing by 1 or by the whole die instead of by P(X > 2).

### 3. Naive Bayes by counting

In plain words: for each class, multiply how common the class is by how common each feature value is inside that class. The biggest product wins. Treating the features as separate factors is the "naive" part.

**Looks like.** Mushroom table, 3 Yes and 4 No rows. P(y = Yes) and P(white, spotted | Yes) given conditional independence (Q21). Statements about Naive Bayes (Q6).

**Recipe.**
1. Prior = rows of the class ÷ all rows.
2. For each feature, conditional = rows with that value AND that class ÷ rows of that class. Count inside the class only.
3. Multiply the prior by all the conditionals: this is the (unnormalised) score of the class.
4. To get a probability, divide a class's score by the sum of the class scores.
5. Laplace smoothing for categorical features: (count + 1) ÷ (class count + number of values the feature can take). The extra term differs from feature to feature.

**Worked example (Q21).** P(Yes) = 3/7. Among the 3 Yes rows: white = 1 of 3, spotted = yes in 2 of 3. Under independence, P(white, yes | Yes) = (1/3)(2/3) = 2/9. Statements a and d are correct. The raw count 1/3 (rows that are white and yes among the Yes rows) is the joint count, not the Naive Bayes product, so it is wrong under the stated assumption.

Classify a new mushroom (white, spotted): score Yes = 3/7 × 1/3 × 2/3 = 0.0952. Among the 4 No rows, white = 2/4, spotted = 1/4, so score No = 4/7 × 1/2 × 1/4 = 0.0714. Posterior of Yes = 0.0952 / (0.0952 + 0.0714) = 4/7 = 0.5714. Predict Yes.

Smoothing: colour has 3 values, spotted has 2. P(white | Yes) = (1 + 1)/(3 + 3) = 1/3, P(spotted | Yes) = (2 + 1)/(3 + 2) = 3/5. P(light brown | Yes) was 0/3 and becomes (0 + 1)/(3 + 3) = 1/6, so one unseen value no longer zeros the whole product.

**Traps.**
- Quoting the raw joint count (1/3) when the stem says to assume conditional independence: you must multiply the separate conditionals.
- Counting among all rows instead of inside the class (denominator 7 instead of 3).
- Unnormalised scores like 0.0952 are not probabilities. Normalise when the stem asks for a probability.
- Laplace: add the number of values of that feature to the denominator, not a fixed 2 (Bernoulli word models add 2: (docs with word + 1)/(docs in class + 2); multinomial adds the vocabulary size). The Lab 3 code and formula have errors here: follow the slides and the arithmetic above.
- Statements about Naive Bayes: see the theory cheat-sheet. Features are independent given the class, not "dependent given the class" (that was the wrong statement in Q6).

### 4. Likelihood and log-likelihood

In plain words: likelihood = how probable the observed data is, viewed as a function of the parameter. For independent examples the probabilities multiply, and a log turns the product into a sum, which is easier to differentiate. The maximum likelihood estimate (MLE) is the parameter value where the (log-)likelihood is highest.

**Looks like.** Exponential density p(x) = λ e^(−λx), i.i.d. data x1 ... xm, log-probability of the data (Q24).

**Recipe.**
1. Product over the examples: L(λ) = Π p(xi).
2. Take ln: each factor's ln becomes a term, and the sum has m terms. Constants that appear in each term are multiplied by m.
3. Simplify each term: ln(λ e^(−λ xi)) = ln λ − λ xi.
4. Sum over i: ℓ(λ) = m ln λ − λ Σ xi.
5. For the MLE, set the derivative to zero. You only need the results, listed below, not the derivation.

**Results the course uses.**

| Model | Log-likelihood or MLE |
|---|---|
| Exponential | ℓ = m ln λ − λ Σ xi, λ̂ = m / Σ xi = 1 / (sample mean) |
| Bernoulli (p = P(1)) | ℓ = k ln p + (m − k) ln(1 − p), p̂ = k / m (share of ones) |
| Gaussian | μ̂ = sample mean, σ̂² = (1/n) Σ (xi − x̄)² (divides by n, so it is biased; the unbiased s² divides by n − 1) |
| Gaussian noise regression | maximising the likelihood = minimising the sum of squared errors |

**Worked example (Q24 with numbers).** Data 2, 1, 3: m = 3, Σ xi = 6. λ̂ = 3/6 = 0.5. ℓ(0.5) = 3 ln 0.5 − 0.5 × 6 = −2.0794 − 3 = −5.0794. In Q24 the option with m log λ − λ Σ xi is the answer (c): the other options keep one log λ, or keep the product.

Gaussian check: data 1, 2, 3, 6 have mean 3, squared deviations 4, 1, 0, 9 (sum 14). MLE variance = 14/4 = 3.5. Unbiased variance = 14/3 = 4.667.

**Traps.**
- Writing log λ instead of m log λ: every example contributes one ln λ.
- A product left in the answer (Π) when the question asks for the log-probability.
- The argmax of ℓ equals the argmax of L, but the maximum values differ.
- The MLE of the variance divides by n, the sample variance by n − 1. (The course's Naive Bayes notes use n − 1 for a per-class variance, scikit-learn's GaussianNB uses n: follow the formula the stem gives.)
- The likelihood is a function of the parameter with the data fixed: it is not a probability distribution over the parameter.

### 5. Logistic regression

In plain words: compute one score z = β · x (a weighted sum), then squash it into a probability with the sigmoid. Score 0 means 50%, large positive means near 1, large negative means near 0.

**Looks like.** β = (−ln 2, ln 5, −ln 7), x* = (1, −1, −1), find P(y = 0 | x*) (Q11). A statement on what logistic regression assumes (Q9).

**Recipe.**
1. z = β1 x1 + β2 x2 + ... (add the bias term if the stem has one).
2. P(y = 1) = 1 / (1 + e^(−z)).
3. Read what the question asks for. P(y = 0) = 1 − P(y = 1).
4. Shortcut when z is a log (z = ln a): e^z = a, so P(y = 1) = a / (1 + a) and P(y = 0) = 1 / (1 + a).

**Worked example (Q11).** z = (−ln 2)(1) + (ln 5)(−1) + (−ln 7)(−1) = −ln 2 − ln 5 + ln 7 = ln(7/10) = ln 0.7 = −0.3567. P(y = 1) = 0.7/1.7 = 0.4118. P(y = 0) = 1/1.7 = 0.5882. Answer d.

**Odds and log-odds.** odds = p / (1 − p). The logit = ln(odds). Logistic regression assumes the logit is a linear function of the features: ln(P(y=1)/P(y=0)) = β · x. So the correct form is "a linear relationship between the features and the logit of the outcome" (Q9, d). Not a linear relationship with the probability, not a logit of the features. Odds of 3 mean p = 0.75; odds of 0.7 mean p = 0.7/1.7 = 0.4118.

**Traps.**
- Giving P(y = 1) (0.4118) when asked for P(y = 0).
- Sign errors with negative inputs: (−ln 7)(−1) = +ln 7.
- Solving z = 0.5 for the boundary: the boundary is z = 0 (probability 0.5).
- Calling it non-linear: the sigmoid is non-linear but the decision boundary β · x = 0 is linear.

### 6. Evaluation metrics from counts

In plain words: all of them are "right ÷ some total". The skill is choosing the total.

| Metric | Formula | Denominator is |
|---|---|---|
| Accuracy | (TP + TN) / all | every example |
| Precision | TP / (TP + FP) | everything predicted positive |
| Recall (sensitivity, TPR) | TP / (TP + FN) | everything actually positive |
| Specificity | TN / (TN + FP) | everything actually negative |
| FPR | FP / (FP + TN) | everything actually negative (= 1 − specificity) |
| F1 | 2 P R / (P + R) = 2 TP / (2 TP + FP + FN) | harmonic mean of P and R, ignores TN |

**Looks like.** A home test given to 100 individuals known to have the virus returns 72 positive results: which is it (Q8, Q13)?

**Recipe.**
1. Fill the 2 × 2 table (TP, FP, FN, TN) from the stem. Say which class is "positive".
2. Pick the metric, write its denominator in words, then count.
3. Check the denominator is non-zero and the answer is between 0 and 1.

**Worked example 1 (Q8, Q13).** All 100 people truly have the virus, so there are no true negatives or false positives: TP = 72, FN = 28, FP = 0. Recall = 72/(72 + 28) = 72%. Precision = 72/(72 + 0) = 100%. Answer: recall 72% (28% is the miss rate). 

**Worked example 2.** TP = 30, FP = 10, FN = 20, TN = 40 (100 examples). Accuracy = 70/100 = 0.70. Precision = 30/40 = 0.75. Recall = 30/50 = 0.60. Specificity = 40/50 = 0.80. F1 = 2 × 0.75 × 0.6 / 1.35 = 0.6667 (check: 60/90). The arithmetic mean of 0.75 and 0.6 is 0.675: that is not F1.

**Traps.**
- "100 known positives" means no FP and no TN exist. Do not invent negatives.
- Swapping precision and recall (the denominators differ: predicted vs actual positives).
- F1 is a harmonic mean (never the plain average) and it ignores TN.
- Accuracy is misleading on unbalanced data: 95 negatives and 5 positives with an "always negative" classifier gives 95% accuracy and recall 0.
- Reading a 28% as a recall when it is 1 − recall.

### 7. k-NN

In plain words: rank the training points by closeness to the new point, take the k closest, and let them vote.

**Looks like.** Six documents with a "cosine distance (the higher the value, the closer)" to a new document d, class for k = 3 and k = 5 (Q12).

**Recipe.**
1. Check the direction: is the number a distance (smaller is closer) or a similarity (larger is closer, like cosine similarity)? The stem will say.
2. Sort the points from closest to farthest in that direction.
3. Take the first k points and count the classes.
4. Majority wins. With 2 classes use an odd k to avoid ties. If a tie is unavoidable, the stem must give a tie-break (nearest first, or the larger class).
5. Redo steps 3 and 4 for each k asked: the answer can change.

**Worked example (Q12).** Higher = closer, so the order is 1 (A, 1.00), 2 (B, 0.95), 3 (B, 0.94), 4 (A, 0.45), 5 (A, 0.40), 6 (B, 0.39).
k = 3: A, B, B, so B. k = 5: A, B, B, A, A, so 3 A against 2 B, giving A. Answer d (B for k = 3 and A for k = 5). If you wrongly sort ascending you get A for k = 3.

Cosine similarity = (u · v) / (‖u‖ ‖v‖), from −1 to 1, and it ignores the length of the vectors: u and 3u have similarity 1. Example: u = (1, 2, 0), v = (2, 1, 1): u · v = 4, ‖u‖ = √5, ‖v‖ = √6, similarity = 4 / √30 = 0.7303.

**Traps.**
- Sorting a similarity ascending (or a distance descending).
- Taking the k nearest of the wrong list: sort first, then count.
- k = 1 always gives zero training error when the points are distinct, because each training point is its own nearest neighbour. That says nothing about test error. The weighted vote course formula uses 1 / distance².
- Large k means a smoother, simpler, higher-bias model. k = n predicts the majority class everywhere. Normalise features first (distances depend on scale).

### 8. Entropy and information gain

In plain words: entropy measures how mixed a column is. Pure column = 0 bits, an even split of 2 values = 1 bit, 4 equal values = 2 bits.

**Looks like.** Entropy of the columns X, Y, Z of a 6-row table (Q16), and of the computed column XY/(Z + 1) (Q20).

**Recipe.**
1. If the question uses a derived column, compute it row by row first (apply the formula to each row).
2. Count how often each distinct value occurs; probabilities p = count / rows.
3. H = −Σ p log2 p, base 2 unless told otherwise.
4. Information gain of a split: H(parent) − Σ (branch size / parent size) × H(branch). Use the size-weighted average, never the plain average.
5. Gini = 1 − Σ p². Pure = 0.

**Worked example 1 (Q16).** X has Jack, Amy, Sam twice each: H = log2 3 = 1.585. Y has 0 and 1 three times each: H = 1. Z has A twice and B four times: H = −(1/3) log2(1/3) − (2/3) log2(2/3) = 0.5283 + 0.3900 = 0.9183. Answer b.

**Worked example 2 (Q20).** The column XY/(Z + 1) has the rows (0,0,0), (0,1,1), (1,0,0), (1,1,1), (2,0,1), (2,1,1), which give 0, 0, 0, 0.5, 0, 1. Values: 0 appears 4 times, 0.5 once, 1 once: p = 4/6, 1/6, 1/6.
H = −(2/3) log2(2/3) − 2 × (1/6) log2(1/6) = 0.3900 + 2 × 0.4308 = 1.2516. Answer c. (If you skip the division by Z + 1 or the product, you count different groups and land on a different option.)

**Worked example 3 (information gain).** Mushroom classes: 3 Yes, 4 No: H = 0.9852 (Gini = 1 − (9 + 16)/49 = 0.4898). Split on "spotted": spotted = yes has 3 rows (2 Yes, 1 No) with H = 0.9183, spotted = no has 4 rows (1 Yes, 3 No) with H = 0.8113. Weighted: 3/7 × 0.9183 + 4/7 × 0.8113 = 0.8571. Gain = 0.9852 − 0.8571 = 0.1281.

**Traps.**
- Using ln instead of log2: the answer then comes out as "too small" (it is in nats).
- Entropy can exceed 1 when there are more than 2 values (log2 3 = 1.585). Maximum is log2 of the number of values.
- Entropy depends on the counts of the values, not on the values themselves, so one value that appears twice counts as one group of 2.
- Gain uses the size-weighted children, not their average, and the gain is never negative.
- A pure child has entropy 0: it does not make the gain 0, it makes it large.
- Compute the derived column before counting. Check division by zero (an option "undefined" is usually a distractor).

### 9. Choosing from train and validation error

In plain words: training error keeps falling (or stays level) as the tree gets deeper, so it cannot choose the depth. The validation error is the honest estimate: its lowest point is the choice.

**Looks like.** Depths 3, 4, 5, 6 with training and validation error: which depth for the final model (Q1)?

**Recipe.**
1. Ignore the training error column for the choice.
2. Find the lowest validation error.
3. If two depths tie, take the simpler (shallower) one. Check if any option makes this decision for you.
4. Read the pattern: training and validation both high = underfitting (high bias); training low, validation much higher = overfitting (high variance).

**Worked example (Q1).** Validation errors 35%, 30%, 30%, 35% at depths 3, 4, 5, 6. Lowest is 30%, shared by depths 4 and 5. The usual rule is to prefer the simpler tree, which gives depth 4. Be careful: this is a genuine tie, the exam's own key for Q1 is unknown (the student ticked 5), so this guide does not claim 4 is the marked answer. What is safe: the training error is irrelevant, depths 3 and 6 are out, and the choice is between 4 and 5 only. In your own practice, avoid exact ties. Depth 6 has the lowest training error (15%) but a high validation error, so it overfits. Depth 3 has a high training error, so it underfits.

**Traps.**
- Picking the lowest training error (the deepest tree).
- Ties: the usual rule is the simplest model among the equally good ones, but the marked answer for a real tie (Q1) is unknown, so do not rely on it. In a question without a tie, there is no issue.
- Choosing on the test error and then quoting it: that is optimistic. The test set is only for the final number.

### 10. Ensembles

In plain words: many models vote. The question is how the models were made, and which kind of error the combination reduces.

**Looks like.** Name the method from a procedure (Q5, Q7), true/false statements on bagging (Q10), AdaBoost weighted vote with a threshold (Q4).

**Name the method from the procedure.**

| Procedure | Method |
|---|---|
| Resample the examples with replacement, train one model on each, majority vote | Bagging (bootstrap aggregating) |
| Bagging with trees, and also each tree sees a random subset of the features (columns) | Random forest |
| Train models one after another, each focusing on the previous mistakes, weighted vote | Boosting (AdaBoost) |
| Just the resampling step, with no models or vote | Bootstrapping |

Q5 (resampled images, 100 logistic models, vote) is bagging. Q7 (the same with trees plus a random sample of 40 pixels per subset) is a random forest.

**Facts.**
- Bagging reduces variance. It trains the models independently, so in parallel. It does not reduce bias, so it does not rescue a high-bias model. The bootstrap samples examples (rows), not features.
- Boosting is sequential (cannot be parallel) and mainly reduces bias. It can overfit very noisy data.
- Random forest: bagging plus a random feature subset, which makes the trees less alike.

**AdaBoost recipe.**
1. Model weight α = ½ ln((1 − ε) / ε) with the weighted error ε (natural log). Smaller error = larger α. ε = 0.5 gives α = 0.
2. Turn each base model's output into ±1 using the stated threshold (above the threshold means +1).
3. Compute the weighted sum Σ αj × prediction j.
4. The sign of the sum is the class.

**Worked example (Q4).** Errors 0.3, 0.25, 0.41. α1 = ½ ln(0.7/0.3) = 0.4236, α2 = ½ ln(0.75/0.25) = 0.5493, α3 = ½ ln(0.59/0.41) = 0.1820. Outputs 0.4, 0.86, 0.56 with threshold 0.6 become −1, +1, −1. Sum = −0.4236 + 0.5493 − 0.1820 = −0.0563 < 0, so the prediction is −1. Answer d. With threshold 0.5 the third output turns to +1 and the sum becomes +0.3076: the threshold matters.

**Traps.**
- Dropping the ½ (gives ln(0.7/0.3) = 0.8473), inverting the ratio, or using log10.
- Forgetting to threshold first (using the raw outputs 0.4, 0.86, 0.56).
- Using an unweighted vote: the weighted sum can disagree with the plain majority, and a strong model can outvote two weak ones.
- Bagging "reduces bias" is false. Bagging "samples features" is false (a random forest does). Bootstrap sampling is with replacement.
- A random forest's feature subset is chosen once per tree in the course's definition (sklearn picks features at each split). Read what the stem describes.

### 11. Kernels

In plain words: a kernel k(x, y) is a dot product φ(x) · φ(y) in a new feature space. To find φ, split the kernel into a sum of terms, and write each term as (something of x) × (the same something of y). Each term becomes one entry of φ.

**Looks like.** Which φ matches k(x, y) = e^(x1+y1) + e^(x2+y2) + 0.25 x1² y1² + log(x1) log(y1) + log(x2) log(y2)? (Q2, Q19). The RBF kernel's behaviour (Q15).

**Recipe.**
1. Split k into its sum terms. Each term is one entry of φ.
2. Make each term a product of the same function of x and of y: e^(x1+y1) = e^(x1) × e^(y1), so the entry is e^(x1).
3. A coefficient c is shared between the two sides: c = (√c)(√c), so the entry carries √c. Coefficient 0.25 means 0.5 in the map entry, coefficient 2 means √2.
4. Terms that are separate in k stay separate entries (log x1 log y1 and log x2 log y2 are two entries, not one entry log x1 + log x2).
5. Count the terms: that is the number of entries of φ.

**Worked example 1 (Q2).** Terms: e^(x1) e^(y1), e^(x2) e^(y2), (0.5 x1²)(0.5 y1²) = 0.25 x1² y1², (log x1)(log y1), (log x2)(log y2). So φ = (e^(x1), e^(x2), 0.5 x1², log x1, log x2). Answer d. The option with 0.25 x1² would give 0.0625 x1² y1².

**Worked example 2 (Q19).** k = e^(x1x2 + y1y2) + 2 (x1 y1) / (x2 y2) + 0.25 x1³ y1³. Terms: e^(x1x2) · e^(y1y2); (√2 x1/x2)(√2 y1/y2); (0.5 x1³)(0.5 y1³). φ = (e^(x1x2), √2 x1/x2, 0.5 x1³). Answer b.

**Valid kernels and counts.**
- A valid kernel is symmetric with a Gram matrix that is positive semi-definite. Sums, positive multiples and products of valid kernels are valid. k(x, x) cannot be negative.
- Polynomial kernel (x · y)^2 in 2D: φ = (x1², x2², √2 x1x2), 3 entries. (1 + x · y)² in 2D: φ = (1, x1², x2², √2 x1, √2 x2, √2 x1x2), 6 entries. The number of features of the degree-p polynomial kernel (with constant) in d dimensions is C(d + p, p): d = 2, p = 2 gives 6; d = 10, p = 2 gives 66. Without the constant (degree exactly p) it is C(d + p − 1, p).
- RBF kernel k = exp(−‖x − y‖² / (2σ²)): equals 1 for identical points, near 1 for points close together, near 0 for far points, always between 0 and 1. ‖x − y‖² = 2, σ = 1 gives e^(−1) = 0.3679. ‖x − y‖² = 8 gives e^(−4) = 0.0183. Smaller σ means "close" is stricter. So for Q15: close point near 1, far point near 0 (statement A).

**Traps.**
- Forgetting the square root of the coefficient (0.25 → 0.5, 2 → √2).
- Merging two separate terms into one entry: (log x1 + log x2)(log y1 + log y2) also has cross terms such as log x1 log y2, which k does not contain.
- RBF: the exponent is −d² / (2σ²), a negative number, so the kernel is never above 1 or below 0.

### 12. Linear separability and feature transformations

In plain words: a linear model draws a straight line (or plane). If one class sits between the other in 1-D, no threshold separates them, but adding or changing a feature may.

**Looks like.** Which feature map makes 1-D data separable (Q22). Which models cannot reach zero training error on every linearly separable dataset (Q26).

**Recipe.**
1. Compute each candidate feature for every data point, one line per point.
2. Plot the points mentally in the (x, feature) plane, positives against negatives.
3. Ask: does one straight line split the two classes? A quick test: is a negative point on the line segment between two positive points? If so, no line works.
4. Pick the transformation(s) where the answer is yes (there can be more than one). If the stem is single-answer and two options both work, nothing in the maths separates them: say so to yourself, and pick the one you can justify.

**Worked example (Q22).** x = −π, −π/2, 0, π/2, π with y = +, −, −, −, +. cos x = −1, 0, 1, 0, −1: the positives have the lowest cos, so the line cos x = −0.5 separates them: separable. cos(0.5x) = 0, 0.707, 1, 0.707, 0: the positives have the lowest value again: separable. sin x = 0, −1, 0, 1, 0: the middle negative (0, 0) lies between the two positives (−π, 0) and (π, 0): not separable. sin(0.5x) = −1, −0.707, 0, 0.707, 1: the middle negative (0, 0) is the midpoint of the two positives (−π, −1) and (π, 1): not separable. So A (cos x) and C (cos 0.5x) work, B and D do not. Caution: Q22 was shown as a single-answer question (radio buttons) and A and C both work, so the question itself is ambiguous. The exam's key is unknown (the student ticked A). This guide does not claim which one is marked correct; only the maths above is certain. In 1-D toy data, with + at −2 and 2 and − at −0.5, 0, 0.5, shifting or scaling x does not help, while x² does.

**Facts for the true/false.**
- Perceptron: converges to a separating line if the data are linearly separable (any one of them, depends on the order of examples), never if they are not. Hard-margin SVM: needs separable data, finds the unique widest-margin line. Both reach zero training error on separable data.
- An unpruned decision tree and 1-NN can reach zero training error whenever points with different labels are distinct. k-NN with large k cannot always (15-NN can outvote a lone point surrounded by 14 others): this was Q26, answer a.
- SVM margin: when w is scaled so the closest point has |w · x − t| = 1, the distance from the boundary to the closest point is 1 / ‖w‖ (the two margin lines are 2 / ‖w‖ apart). Some sources call 2 / ‖w‖ "the margin": if an option is off by a factor of 2, check which one the stem means. Smaller ‖w‖ means a wider margin. Distance of a point to the line w · x = t is |w · x − t| / ‖w‖. Example: w = (3, 4), t = 5, point (3, 2): |17 − 5| / 5 = 2.4.
- Perceptron update on a mistake (y w · x ≤ 0): w ← w + y x. Starting from w = 0 the first example is always a mistake.

**Traps.**
- Two of the four transformations can work. Test all four.
- Linear in the features is not linear in x: a linear model on (x, cos x) gives a curved boundary in x.
- Scaling or shifting a single feature never creates separability.

### 13. Neural network arithmetic

In plain words: each unit takes a weighted sum of its inputs plus a bias, then applies an activation. ReLU keeps positive values and zeroes negatives, the sigmoid squashes to (0, 1), softmax turns a score list into probabilities.

**Looks like.** Parameters of an MLP with biases, 5 inputs, 20 hidden, 3 outputs (Q14). The value of a hidden unit after ReLU for given inputs (Q17, Q25).

**Recipe.**
1. Parameters: per layer (inputs × outputs) weights + (outputs) biases. Add the layers.
2. Forward pass: for each unit compute bias + Σ weight × input. Do all hidden units, then the output.
3. Apply the activation: ReLU(a) = max(0, a), sigmoid(a) = 1 / (1 + e^(−a)).
4. Softmax of scores s: e^(si) / Σ e^(sj). Cross-entropy with the true class c is −ln(softmax probability of c).

**Worked example 1 (Q14).** 5 × 20 + 20 = 120 for the first layer, 20 × 3 + 3 = 63 for the second, total 183. Answer c. Forgetting the biases gives 100 + 60 = 160, forgetting only the output biases gives 180.

**Worked example 2 (forward pass).** Inputs x = (1, 2). Hidden units ReLU, weights as (bias, w1, w2):

| Unit | bias | w1 | w2 | pre-activation | after ReLU |
|---|---|---|---|---|---|
| h1 | 0.5 | 1 | −1 | 0.5 + 1 − 2 = −0.5 | 0 |
| h2 | −1 | 2 | 0.5 | −1 + 2 + 1 = 2 | 2 |
| h3 | 0 | −1 | 1 | −1 + 2 = 1 | 1 |

Output is a sigmoid unit with bias −1 and weights (1, 0.5, −2) on (h1, h2, h3): z = −1 + 1 × 0 + 0.5 × 2 − 2 × 1 = −2, output = 1 / (1 + e^2) = 0.1192. (Skipping the ReLU on h1 gives z = −2.5, output 0.0759: a typical wrong option.) Count of parameters: 2 × 3 + 3 + 3 × 1 + 1 = 13.

**Worked example 3 (softmax).** Scores (2, 1, 0): exponentials 7.389, 2.718, 1, sum 11.107. Probabilities 0.6652, 0.2447, 0.0900 (sum 1). If the true class is the first, the cross-entropy is −ln 0.6652 = 0.4076. If it is the last, −ln 0.0900 = 2.4076.

**Traps.**
- Forgetting the bias of the output layer or the hidden layer.
- Forgetting to apply ReLU before the next layer (negative values must become 0).
- Using the network input instead of the hidden outputs in the output layer.
- A sigmoid unit has a non-linear output but a linear decision boundary. Stacking linear layers without an activation is still linear.

### 14. Lighter topics (not in the practice exam)

**k-means, one iteration.** Assign every point to its nearest centre, then move each centre to the mean of its points. Points (1,1), (2,1), (4,3), (5,4), centres (1,1) and (5,4). Distances for (4,3): to (1,1) √13 = 3.606, to (5,4) √2 = 1.414, so it joins the second centre. Assignment: first two points to centre 1, last two to centre 2. New centres: (1.5, 1) and (4.5, 3.5). It uses squared distance, and the result depends on the starting centres (local minimum).

**Hierarchical linkage.** Clusters {1, 2} and {6, 9} in 1-D. Pair distances: 5, 8, 4, 7. Single linkage = minimum = 4. Complete linkage = maximum = 8. Average linkage = mean = 6. Single uses the closest pair, complete the farthest pair.

**PCA.** Centre the data first. The proportion of variance kept by the first component = its eigenvalue ÷ the sum of all eigenvalues (the sum equals the trace of the covariance matrix). Eigenvalues 4 and 1: first component keeps 4/5 = 80%. Covariance [[3, 1], [1, 3]] has eigenvalues 4 and 2: 4/6 = 0.6667. PCA directions maximise variance and ignore labels.

**Regularisation.** Ridge adds λ‖θ‖² and shrinks coefficients towards 0 without making them exactly 0. Lasso adds λ Σ|θi| and can set coefficients exactly to 0. Larger λ means a simpler model (more bias, less variance) and a higher training error. 1-D ridge without intercept: slope = Σ xy / (Σ x² + λ): for x = (1, 2, 3), y = (2, 4, 6), λ = 1: 28/15 = 1.8667 instead of 2.

**PAC bound.** For a finite hypothesis class and a consistent learner, m ≥ (1/ε)(ln|H| + ln(1/δ)), natural logs, round up. |H| = 1000, ε = 0.1, δ = 0.05: ln 1000 = 6.9078, ln 20 = 2.9957, sum 9.9035, × 10 = 99.04, so m = 100. Confidence 95% means δ = 0.05. These bounds say "m examples are enough", not "m are needed". The VC-based bound uses log2.

**VC dimension.** A set is shattered if every labelling can be realised. Lines in the plane (d = 2 features) have VC dimension d + 1 = 3: any 3 points not on a line can be shattered, no 4 points can. VC dimension is finite if and only if the class is PAC-learnable.

## Theory cheat-sheet

Each bullet is a statement you may see as true or false. The words in bold are what the exam hides in a wrong option.

**Probability and Bayes**
- P(D | T) is not P(T | D). A rare condition keeps the posterior low after a positive test.
- MAP uses the prior, ML ignores it (equal priors make them agree).
- Naive Bayes is generative (models P(x | class) and P(class)). Logistic regression is discriminative.

**Naive Bayes**
- Assumes features are **conditionally independent given the class** (not independent in general, and not dependent).
- Features can be nominal (counts) or numeric (a Gaussian per class and per feature). Missing values: leave that feature out of the product.
- It is often a good classifier but a poor probability estimator (over-confident).
- Needs few data, is fast, and trains by counting. Smoothing pulls estimates towards uniform and removes zero products.
- In Q6, "features are equally important" was not the incorrect statement: Naive Bayes multiplies the feature factors alike, with no feature weights.

**Logistic regression**
- Linear decision boundary, probability from a sigmoid, trained by maximising the likelihood (minimising cross-entropy) with gradient descent. The cost is convex with no closed form. It assumes the logit is linear in the features.

**Evaluation**
- Precision = of predicted positives, how many are real. Recall = of real positives, how many were found. F1 is a harmonic mean. Never tune on the test set.

**k-NN**
- Lazy (stores the data, no training). Small k: low bias, high variance, complex. Large k: smoother, higher bias. Sensitive to scaling and to irrelevant features. Slow at prediction time. A distance-weighted vote uses 1 / distance².

**Decision trees**
- Greedy top-down splitting, so not guaranteed to be the best tree. High variance. Deeper trees fit the training data better and generalise worse past a point. Pruning limits overfitting. A discrete attribute is used at most once on a path. Training error need not be 0 if identical inputs have different labels.

**Ensembles**
- Bagging: bootstrap rows, parallel, reduces variance, good for high-variance models (deep trees), not for high-bias ones.
- Random forest: bagging + random features. Boosting: sequential, reweights mistakes, reduces bias, can overfit noise. A weak learner only needs to beat chance (ε < 0.5, so α > 0).

**SVM, perceptron, kernels**
- Perceptron: mistake-driven, only converges if separable, result depends on order. Hard-margin SVM: maximum margin, unique solution, depends only on the support vectors (points with α > 0). Soft margin: large C means narrow margin and few errors (close to hard margin), small C means wide margin and more errors.
- The kernel trick computes φ(x) · φ(y) without building φ. A kernel lets a linear method draw a curved boundary in the original space. The RBF kernel has an infinite-dimensional feature space.

**Neural networks**
- A single sigmoid unit = logistic regression. Without non-linear activations a deep network is still linear. Backpropagation reaches a local minimum, not necessarily the global one. Cross-entropy goes with softmax. Dropout is only used while training.

**Bias and variance, regularisation**
- Training error falls with complexity, validation error is U-shaped. Overfitting = low bias, high variance. Underfitting = high bias, low variance. Ridge shrinks, lasso zeroes. Bigger λ means simpler. Choose the hyper-parameters on validation data.

**Clustering, PCA, learning theory**
- k-means: hard assignments, local minimum, needs k, uses squared distance. EM for mixtures: soft assignments, local maximum of the likelihood. PCA: unsupervised, centre first, linear.
- PAC: probably (confidence 1 − δ) approximately (error ≤ ε) correct. Zero training error does not mean zero true error.

## Numbers worth remembering

**Logs.**

| x | 2 | 3 | 5 | 6 | 7 | 9 | 10 |
|---|---|---|---|---|---|---|---|
| log2 x | 1 | 1.585 | 2.3219 | 2.585 | 2.8074 | 3.1699 | 3.3219 |
| ln x | 0.6931 | 1.0986 | 1.6094 | 1.7918 | 1.9459 | 2.1972 | 2.3026 |

Rules: ln(a/b) = ln a − ln b, ln(ab) = ln a + ln b, ln(1/a) = −ln a, log2 x = ln x / 0.6931.

**e and the sigmoid.**

| Value | Number |
|---|---|
| e | 2.7183 |
| e², e³ | 7.3891, 20.0855 |
| e^(−0.5), e^(−1), e^(−2), e^(−3), e^(−4) | 0.6065, 0.3679, 0.1353, 0.0498, 0.0183 |
| sigmoid(−1), (0), (1), (2), (3) | 0.2689, 0.5, 0.7311, 0.8808, 0.9526 |
| sigmoid(ln a) | a / (1 + a): ln 3 gives 0.75, ln 0.7 gives 0.4118 |

**Fractions.** 1/3 = 0.3333, 2/3 = 0.6667, 1/6 = 0.1667, 5/6 = 0.8333, 1/7 = 0.1429, 3/7 = 0.4286, 4/7 = 0.5714, 1/9 = 0.1111, 1/11 = 0.0909. Roots: √2 = 1.4142, √3 = 1.7321, √5 = 2.2361.

**Entropy in bits for common splits.**

| Class shares | Entropy |
|---|---|
| 1/2, 1/2 | 1 |
| 1/3, 2/3 | 0.9183 |
| 1/4, 3/4 | 0.8113 |
| 0.4, 0.6 | 0.9710 |
| 0.3, 0.7 | 0.8813 |
| 1/5, 4/5 | 0.7219 |
| 1/6, 5/6 | 0.6500 |
| 1/10, 9/10 | 0.4690 |
| 1/2, 1/4, 1/4 | 1.5 |
| 3 equal shares | 1.585 |
| 4 equal shares | 2 |
| 8 equal shares | 3 |

The terms −p log2 p for single probabilities: p = 1/2 gives 0.5, 1/3 gives 0.5283, 2/3 gives 0.3900, 1/4 gives 0.5, 3/4 gives 0.3113, 1/6 gives 0.4308.

**AdaBoost weights α = ½ ln((1 − ε)/ε).**

| ε | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 |
|---|---|---|---|---|---|
| α | 1.0986 | 0.6931 | 0.4236 | 0.2027 | 0 |

An error above 0.5 gives a negative α.

**Others.** π = 3.1416, π/2 = 1.5708. A bootstrap sample of size m leaves out about e^(−1) = 36.8% of the examples. Parameters of a layer: inputs × outputs + outputs.

## Check yourself

Can you ...

1. compute a posterior from a prior and a test (formula and a table of 1000 imaginary cases), and a conditional probability by normalising the weights and restricting to the allowed outcomes?
2. compute a Naive Bayes score from a small table, and say why the raw joint count is a different thing?
3. write the log-likelihood of i.i.d. exponential data, and give the MLE of λ, of a Bernoulli p, and of a Gaussian variance (and say which divides by n)?
4. compute P(y = 0) from a weight vector, and say what "the logit is linear in the features" means?
5. get precision, recall, specificity and F1 from a 2 × 2 table, and say what each denominator is (including the "100 known positives" case)?
6. run k-NN for two values of k on a sorted list, and say whether a similarity is sorted up or down?
7. compute the entropy of a column (also a computed one), the information gain of a split, and a Gini value?
8. pick a depth from a train and validation table, and say what you do with a tie?
9. name bagging, random forest and boosting from a procedure, and compute an AdaBoost vote with a threshold?
10. find φ from a kernel (with the square root of each coefficient), test which transformation makes 1-D data separable, and count the parameters of a small network with biases?
