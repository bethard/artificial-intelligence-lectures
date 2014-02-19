from __future__ import division
import random

class Variable(object):

    def __init__(self, *parents):
        self.parents = parents
        self.children = []
        self.prob_table = {}
        for parent in self.parents:
            parent.children.append(self)

    def add_probability(self, prob, *parent_values):
        self.prob_table[parent_values] = prob

    def probability_of(self, value, *parent_values):
        prob = self.prob_table[parent_values]
        if value is True:
            return prob
        else:
            return 1 - prob

class BayesNet(object):

    def __init__(self, variables):
        self.variables = variables

    def __iter__(self):
        return iter(self.variables)

    def __len__(self):
        return len(self.variables)


B = Variable()
B.add_probability(0.001)
E = Variable()
E.add_probability(0.002)

A = Variable(B, E)
A.add_probability(0.95, True, True)
A.add_probability(0.94, True, False)
A.add_probability(0.29, False, True)
A.add_probability(0.001, False, False)

J = Variable(A)
J.add_probability(0.90, True)
J.add_probability(0.05, False)

M = Variable(A)
M.add_probability(0.70, True)
M.add_probability(0.01, False)

alarm_net = BayesNet([B, E, A, J, M])
alarm_args = B, {J: True, M: True}, alarm_net, 10000

C = Variable()
C.add_probability(0.5)

S = Variable(C)
S.add_probability(0.10, True)
S.add_probability(0.50, False)

R = Variable(C)
R.add_probability(0.80, True)
R.add_probability(0.20, False)

WG = Variable(S, R)
WG.add_probability(0.99, True, True)
WG.add_probability(0.90, True, False)
WG.add_probability(0.90, False, True)
WG.add_probability(0.00, False, False)

wet_net = BayesNet([C, S, R, WG])
wet_args = R, {S: True}, wet_net, 10000


def prior_sample(bayes_net):
    # generate a value for each variable in the network
    # variables are sorted from parents to children
    sample = {}
    for variable in bayes_net:
        # find the values assigned to the parents
        parent_values = [sample[parent] for parent in variable.parents]
        # find the probability for this assignment from the table
        probability = variable.probability_of(True, *parent_values)
        # add True or False according to the distribution
        sample[variable] = random.random() < probability
    # return the complete sample
    return sample


def rejection_sampling(query, evidence, bayes_net, samples):
    # generate a bunch of samples, counting query values
    counts = {False: 0, True: 0}
    for _ in range(samples):
        sample = prior_sample(bayes_net)
        # if the sample is consistent with the evidence, count it
        if all(sample[variable] == evidence[variable] for variable in evidence):
            counts[sample[query]] += 1
    # normalize the counts and return the probabilities
    return normalize(counts)


def normalize(counts):
    # divide all counts by the total
    total = sum(counts.values())
    for value in counts:
        counts[value] /= total
    return counts

print 'Rejection Sampling'
# actual answer: {False:0.716, True: 0.284}
print 'P(B|j,m)', rejection_sampling(*alarm_args)
# actual answer: {False:0.7, True: 0.3}
print 'P(R|s)', rejection_sampling(*wet_args)


def likelihood_weighting(query, evidence, bayes_net, samples):
    # generate samples, adding up weights for each query value
    counts = {False: 0, True: 0}
    for _ in range(samples):
        sample, weight = weighted_sample(bayes_net, evidence)
        counts[sample[query]] += weight
    # normalize the counts and return the probabilities
    return normalize(counts)


def weighted_sample(bayes_net, evidence):
    # generate a value for each variable, from parents to children
    sample, weight = {}, 1.0
    for variable in bayes_net:
        parent_values = [sample[parent] for parent in variable.parents]
        # if the value is given, add it and update the weight
        if variable in evidence:
            sample[variable] = value = evidence[variable]
            weight *= variable.probability_of(value, *parent_values)
        # otherwise, add True or False using the distribution
        else:
            probability = variable.probability_of(True, *parent_values)
            sample[variable] = random.random() < probability
    # return the weighted sample
    return sample, weight


print 'Likelihood Weighting'
# actual answer: {False:0.716, True: 0.284}
print 'P(B|j,m)', likelihood_weighting(*alarm_args)
# actual answer: {False:0.7, True: 0.3}
print 'P(R|s)', likelihood_weighting(*wet_args)


def gibbs_sampling(query, evidence, bayes_net, samples):
    # initialize the sample with random values for non-evidence
    sample = {}
    for variable in bayes_net:
        if variable in evidence:
            sample[variable] = evidence[variable]
        else:
            sample[variable] = random.random() < 0.5
    # generate samples by changing non-evidence values
    counts = {False:0, True:0}
    non_evidence = [var for var in bayes_net if var not in evidence]
    for _ in range(samples):
        for variable in non_evidence:
            # get the prob distribution given the markov blanket
            probability = markov_blanket_probability_of(variable, sample)
            # select a new value according to that distribution
            sample[variable] = random.random() < probability
            # increment the count for the current query value
            counts[sample[query]] += 1
    # normalize the counts and return the probabilities
    return normalize(counts)


def markov_blanket_probability_of(variable, sample):
    # get the probabilities for each value of the variable
    counts = {}
    for value in [True, False]:
        # change the variable's value in the sample
        sample[variable] = value
        # add the probability of the variable given its parents
        parent_values = [sample[parent] for parent in variable.parents]
        counts[value] = variable.probability_of(value, *parent_values)
        # times the probabilities of the children given their parents
        for child in variable.children:
            child_value = sample[child]
            parent_values = [sample[parent] for parent in child.parents]
            counts[value] *= child.probability_of(child_value, *parent_values)
    # normalize the counts and return the probability of True
    return normalize(counts)[True]


#print gibbs_sampling(R, {S: True}, wet_net, 10)

print 'Gibbs Sampling'
# actual answer: {False:0.716, True: 0.284}
print 'P(B|j,m)', gibbs_sampling(*alarm_args)
# actual answer: {False:0.7, True: 0.3}
print 'P(R|s)', gibbs_sampling(*wet_args)
