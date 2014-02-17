from __future__ import division
import random

class Node(object):

    def __init__(self, *parents):
        self.parents = parents
        self.children = []
        self.prob_table = {}
        for parent in self.parents:
            parent.children.append(self)

    def add_prob(self, prob, *parent_values):
        self.prob_table[parent_values] = prob

    def get_prob(self, value, *parent_values):
        prob = self.prob_table[parent_values]
        if value is True:
            return prob
        else:
            return 1 - prob

class BayesNet(object):

    def __init__(self, nodes):
        self.nodes = nodes
        for i, node in enumerate(nodes):
            node.index = i

    def __iter__(self):
        return iter(self.nodes)

    def __len__(self):
        return len(self.nodes)


B = Node()
B.add_prob(0.001)
E = Node()
E.add_prob(0.002)

A = Node(B, E)
A.add_prob(0.95, True, True)
A.add_prob(0.94, True, False)
A.add_prob(0.29, False, True)
A.add_prob(0.001, False, False)

J = Node(A)
J.add_prob(0.90, True)
J.add_prob(0.05, False)

M = Node(A)
M.add_prob(0.70, True)
M.add_prob(0.01, False)

alarm_net = BayesNet([B, E, A, J, M])
alarm_args = B, {J: True, M: True}, alarm_net, 10000

C = Node()
C.add_prob(0.5)

S = Node(C)
S.add_prob(0.10, True)
S.add_prob(0.50, False)

R = Node(C)
R.add_prob(0.80, True)
R.add_prob(0.20, False)

WG = Node(S, R)
WG.add_prob(0.99, True, True)
WG.add_prob(0.90, True, False)
WG.add_prob(0.90, False, True)
WG.add_prob(0.00, False, False)

wet_net = BayesNet([C, S, R, WG])
wet_args = R, {S: True}, wet_net, 10000


def prior_sample(bayes_net):
    # generate a value for each variable in the network
    # variables are sorted from parents to children
    sample = []
    for node in bayes_net:
        # find the values assigned to the parents
        parent_samples = [sample[p.index] for p in node.parents]
        # find the probability for this assignment from the table
        prob = node.get_prob(True, *parent_samples)
        # add True or False according to the distribution
        sample.append(random.random() < prob)
    # return the complete sample
    return sample


def rejection_sampling(query_var, evidence, bayes_net, samples):
    # generate a bunch of samples, counting query values
    counts = {False: 0, True: 0}
    for _ in range(samples):
        sample = prior_sample(bayes_net)
        # if the sample is consistent with the evidence, count it
        if all(sample[v.index] == evidence[v] for v in evidence):
            counts[sample[query_var.index]] += 1
    # normalize the counts and return the probabilities
    return normalize(counts)


def normalize(counts):
    # divide all counts by the total
    total = sum(counts.values())
    for value in counts:
        counts[value] /= total
    # return the probabilities
    return counts

print 'Rejection Sampling'
# actual answer: {False:0.716, True: 0.284}
print 'P(B|j,m)', rejection_sampling(*alarm_args)
# actual answer: {False:0.7, True: 0.3}
print 'P(R|s)', rejection_sampling(*wet_args)


def weighted_sample(bayes_net, evidence):
    # generate a value for each variable from roots to leaves
    sample, weight = [], 1.0
    for node in bayes_net:
        p_samples = [sample[p.index] for p in node.parents]
        # if the value is given, add it and update the weight
        if node in evidence:
            weight *= node.get_prob(evidence[node], *p_samples)
            sample.append(evidence[node])
        # otherwise, add True or False using the distribution
        else:
            prob = node.get_prob(True, *p_samples)
            sample.append(random.random() < prob)
    # return the weighted sample
    return sample, weight


def likelihood_weighting(query_var, evidence, bayes_net, samples):
    # generate samples, adding up weights for each query value
    counts = {False: 0, True: 0}
    for _ in range(samples):
        sample, weight = weighted_sample(bayes_net, evidence)
        counts[sample[query_var.index]] += weight
    # normalize the counts and return the probabilities
    return normalize(counts)

print 'Likelihood Weighting'
# actual answer: {False:0.716, True: 0.284}
print 'P(B|j,m)', likelihood_weighting(*alarm_args)
# actual answer: {False:0.7, True: 0.3}
print 'P(R|s)', likelihood_weighting(*wet_args)


def gibbs_sampling(query_var, evidence, bayes_net, samples):
    # initialize the sample with random values for non-evidence
    sample = []
    for node in bayes_net:
        if node in evidence:
            sample.append(evidence[node])
        else:
            sample.append(random.random() < 0.5)
    # generate samples by changing non-evidence values
    counts = {False:0, True:0}
    non_evidence = [n for n in bayes_net if n not in evidence]
    for i in range(samples):
        for node in non_evidence:
            # get the prob distribution given the markov blanket
            probs = get_probs_given_markov_blanket(node, sample)
            # select a new value according to that distribution
            sample[node.index] = random.random() < probs[True]
            # increment the count for the current query value
            counts[sample[query_var.index]] += 1
    # normalize the counts and return the probabilities
    return normalize(counts)


def get_probs_given_markov_blanket(node, sample):
    # get the probabilities for each value of the variable
    counts = {}
    for value in [True, False]:
        # change the node's value in the sample
        sample[node.index] = value
        # the probability of the node given its parents
        p_samples = [sample[p.index] for p in node.parents]
        counts[value] = node.get_prob(value, *p_samples)
        # times probabilities of children given their parents
        for child in node.children:
            c_sample = sample[child.index]
            p_samples = [sample[p.index] for p in child.parents]
            counts[value] *= child.get_prob(c_sample, *p_samples)
    # normalize the counts and return the probabilities
    return normalize(counts)


#print gibbs_sampling(R, {S: True}, wet_net, 10)

print 'Gibbs Sampling'
# actual answer: {False:0.716, True: 0.284}
print 'P(B|j,m)', gibbs_sampling(*alarm_args)
# actual answer: {False:0.7, True: 0.3}
print 'P(R|s)', gibbs_sampling(*wet_args)
