from __future__ import division
import sys
import copy
import random
from collections import defaultdict

class BayesNet:
    def __init__(self):
        self.bayes_net = dict()

        self.bayes_net['B'] = {
            'parents' : [],
            'prob' : {'t':0.001, 'f':0.999},
        }

        self.bayes_net['E'] = {
            'parents': [],
            'prob': {'t':0.002, 'f':0.998},
        }

        self.bayes_net['A'] = {
            'parents': ['B', 'E'],
            'prob': {
                ('t,t') : 0.95,
                ('t,f'): 0.94,
                ('f,t'): 0.29,
                ('f,f'): 0.001,
            }
        }

        self.bayes_net['J'] = {
            'parents': ['A'],
            'prob': {
                ('t'): 0.90,
                ('f'): 0.05,
            }
        }

        self.bayes_net['M'] = {
            'parents': ['A'],
            'prob': {
                ('t'): 0.70,
                ('f'): 0.01,
            }
        }


    def enumeration_ask(self, query_var, evidence):
        distribution = []
        for val in ['t', 'f']:
            evi = copy.deepcopy(evidence)
            evi[query_var] = val
            distribution.append(self.enumeration_all(evi))
        return


    def enumeration_all(self, vars, evid):
        if len(vars) == 0:
            return 1.0


    def compare(self, sample, evid_values):
        for var in evid_values.keys():
            if sample.get(var) != evid_values.get(var):
                return False
        return True


    def prior_sample(self, samples, evidence, query_term):
        count  = 0
        t_count = 0
        result = 0.0

        p_evidence = evidence.copy()
        p_evidence[query_term] = 't'


        for index in samples:
            if self.compare(samples[index], evidence):
                t_count+=1

            if self.compare(samples[index], p_evidence):
                count+=1

        if t_count!=0:
            result = count/t_count

        return result


    def likelihood_sampling(self, samples, evidence, query_term, samp_prob):
        count  = 0
        t_count = 0
        result = 0.0

        p_evidence = evidence.copy()
        p_evidence[query_term] = 't'


        for index in samples:
            if self.compare(samples[index], evidence):
                t_count+= samp_prob[index]

            if self.compare(samples[index], p_evidence):
                count+= samp_prob[index]

        if t_count!=0:
            result = count/t_count

        return result


    def likelihood_prob(self, num_sample, evidence):
        prob = dict()
        sample = defaultdict(dict)
        count = 0

        while count < num_sample:
            b = random.random()
            e = random.random()
            a = random.random()
            j = random.random()
            m = random.random()
            weight = 1.0

            if evidence.get('B') is not None:
                if evidence['B'] == 't':
                    weight *= self.bayes_net['B']['prob']['t']
                    sample[count]['B'] = 't'
                else:
                    weight *= self.bayes_net['B']['prob']['f']
                    sample[count]['B'] = 'f'
            else:
                if b < self.bayes_net['B']['prob']['t']:
                    sample[count]['B'] = 't'
                else:
                    sample[count]['B'] = 'f'


            if evidence.get('E') is not None:
                if evidence['E'] == 't':
                    weight *= self.bayes_net['E']['prob']['t']
                    sample[count]['E'] = 't'
                else:
                    weight *= self.bayes_net['E']['prob']['f']
                    sample[count]['E'] = 'f'
            else:
                if e < self.bayes_net['E']['prob']['t']:
                    sample[count]['E'] = 't'
                else:
                    sample[count]['E'] = 'f'

            alarm = ''
            if sample[count].get('B') == 't':
                alarm += 't'+','
            else:
                alarm += 'f'+','

            if sample[count]['E'] == 't':
                alarm += 't'
            else:
                alarm += 'f'

            if evidence.get('A') is not None:
                if evidence['A'] == 't':
                    weight *= self.bayes_net['A']['prob'][alarm]
                    sample[count]['A'] = 't'
                else:
                    weight *= self.bayes_net['A']['prob'][alarm]
                    sample[count]['A'] = 'f'
            else:
                if a < self.bayes_net['A']['prob'][alarm]:
                    sample[count]['A'] = 't'
                else:
                    sample[count]['A'] = 'f'

            jm =""
            if sample[count].get('A') =='t':
                jm += 't'
            else:
                jm += 'f'

            if evidence.get('J') is not None:
                if evidence['J'] == 't':
                    weight *= self.bayes_net['J']['prob'][jm]
                    sample[count]['J'] = 't'
                else:
                    weight *= self.bayes_net['J']['prob'][jm]
                    sample[count]['J'] = 'f'
            else:
                if j < self.bayes_net['J']['prob'][jm]:
                    sample[count]['J'] = 't'
                else:
                    sample[count]['J'] = 'f'

            if evidence.get('M') is not None:
                if evidence['M'] == 't':
                    weight *= self.bayes_net['M']['prob'][jm]
                    sample[count]['M'] = 't'
                else:
                    weight *= self.bayes_net['M']['prob'][jm]
                    sample[count]['M'] = 'f'
            else:
                if m < self.bayes_net['M']['prob'][jm]:
                    sample[count]['M'] = 't'
                else:
                    sample[count]['M'] = 'f'

            prob[count] = weight
            count +=1
        return sample, prob

    def generate_sample(self, num_sample):
        count = 0
        sample = defaultdict(dict)

        while count < num_sample :
            b = random.random()
            e = random.random()
            a = random.random()
            j = random.random()
            m = random.random()


            if b < self.bayes_net['B']['prob']['t']:
                sample[count]['B'] = 't'
            else:
                sample[count]['B'] = 'f'

            if e < self.bayes_net['E']['prob']['t']:
                sample[count]['E'] = 't'
            else:
                sample[count]['E'] = 'f'

            alarm = ''
            if sample[count]['B'] == 't':
                alarm += 't'
            else :
                alarm += 'f'
            alarm += ','
            if sample[count]['E'] == 't':
                alarm += 't'
            else:
                alarm += 'f'

            if a < self.bayes_net['A']['prob'][alarm]:
                sample[count]['A'] = 't'
            else:
                sample[count]['A'] = 'f'

            jm =""
            if sample[count]['A'] =='t':
                jm += 't'
            else:
                jm += 'f'

            if j < self.bayes_net['J']['prob'][jm]:
                sample[count]['J'] = 't'
            else:
                sample[count]['J'] = 'f'

            if m < self.bayes_net['M']['prob'][jm]:
                sample[count]['M'] = 't'
            else:
                sample[count]['M'] = 'f'

            count += 1
        return sample


    def generate_rejection_sample(self, num_sample, evidence):
        rejection_sample = defaultdict(dict)
        samples = self.generate_sample(num_sample)
        for i in range(0, len(samples)):
            if self.compare(samples[i],evidence):
                rejection_sample[i] = samples[i]
        return rejection_sample

    def parse_evidence(self, evidence_set):
        evidence = dict()
#        if ',' in evidence_set:
        for str in evidence_set.split(" "):
            temp = str.split(",")
            evidence[temp[0]] = temp[1]
        #else:
        #    str = evidence_set.split(" ")
        #    evidence[str[0]] = str[1]
        return evidence

def main():
    net = BayesNet()
    num_samples = 100000#sys.argv[1]
    evidence_set = 'M,t J,f'#sys.argv[2]
    query = 'B'#sys.argv[3]
    samples = net.generate_sample(num_samples)
    evidence_val = net.parse_evidence(evidence_set)
    print 'Prior Sampling: '
    for q in query.split(","):
        print net.prior_sample(samples, evidence_val , q)

    print 'Rejection Sampling:'
    rejection_samples = net.generate_rejection_sample(num_samples, evidence_val)
    for q in query.split(","):
        print net.prior_sample(rejection_samples, evidence_val , q)

    print 'Likelihood Weighting:'
    likelihood_sample, sample_prob = net.likelihood_prob(num_samples, evidence_val)
    for q in query.split(","):
        print net.likelihood_sampling(likelihood_sample, evidence_val , q, sample_prob)

    return


if __name__ == '__main__':
    main()