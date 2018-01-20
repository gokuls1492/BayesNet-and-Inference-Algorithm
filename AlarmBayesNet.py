from __future__ import division
import copy
import random
from collections import defaultdict


class Node:
    def _init_(self):
        self.name = ""
        self.cpt = []
        self.value = None


class BayesNet:

    def init(self):
        global b, e, a, m, j
        b = Node()
        e = Node()
        a = Node()
        m = Node()
        j = Node()

        b.name = "B"
        b.cpt = [{"B": True, "value": 0.001},
                 {"B": False, "value": 0.999}]
        b.value = None

        e.name = "E"
        e.cpt = [{"E": True, "value": 0.002},
                 {"E": False, "value": 0.998}]
        e.value = None

        a.name = "A"
        a.cpt = [{"A": True, "B": True, "E": True, "value": 0.95},
                 {"A": True, "B": True, "E": False, "value": 0.94},
                 {"A": True, "B": False, "E": True, "value": 0.29},
                 {"A": True, "B": False, "E": False, "value": 0.001},
                 {"A": False, "B": True, "E": True, "value": 0.05},
                 {"A": False, "B": True, "E": False, "value": 0.06},
                 {"A": False, "B": False, "E": True, "value": 0.71},
                 {"A": False, "B": False, "E": False, "value": 0.999}]
        a.value = None

        j.name = "J"
        j.cpt = [{"A": True, "J": True, "value": 0.9},
                 {"A": True, "J": False, "value": 0.1},
                 {"A": False, "J": True, "value": 0.05},
                 {"A": False, "J": False, "value": 0.95}]
        j.value = None

        m.name = "M"
        m.cpt = [{"A": True, "M": True, "value": 0.7},
                 {"A": True, "M": False, "value": 0.3},
                 {"A": False, "M": True, "value": 0.01},
                 {"A": False, "M": False, "value": 0.99}]
        m.value = None


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
        p_evidence[query_term] = True
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
        p_evidence[query_term] = True
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
            b_ran = random.random()
            e_ran = random.random()
            a_ran = random.random()
            j_ran = random.random()
            m_ran = random.random()
            weight = 1.0
            if evidence.get('B') is not None:
                if evidence['B'] == True:
                    weight *= self.get_CPT_Value(b.cpt, True, None, None, None, None)
                    sample[count]['B'] = True
                else:
                    weight *= self.get_CPT_Value(b.cpt, False, None, None, None, None)
                    sample[count]['B'] = False
            else:
                if b_ran < self.get_CPT_Value(b.cpt, True, None, None, None, None):
                    sample[count]['B'] = True
                else:
                    sample[count]['B'] = False


            if evidence.get('E') is not None:
                if evidence['E'] == True:
                    weight *= self.get_CPT_Value(e.cpt, None, True, None, None, None)
                    sample[count]['E'] = True
                else:
                    weight *= self.get_CPT_Value(e.cpt, None, False, None, None, None)#self.bayes_net['E']['prob']['f']
                    sample[count]['E'] = False
            else:
                if e_ran < self.get_CPT_Value(e.cpt, None, True, None, None, None):#self.bayes_net['E']['prob']['t']:
                    sample[count]['E'] = True
                else:
                    sample[count]['E'] = False

            if sample[count]['B'] == True:
                burg_val = True#alarm += 't'
            else :
                burg_val = False#alarm += 'f'

            if sample[count]['E'] == True:
                earthq_val = True
            else:
                earthq_val = False

            if evidence.get('A') is not None:
                if evidence['A'] == True:
                    weight *= self.get_CPT_Value(a.cpt, burg_val, earthq_val, True, None, None)#self.bayes_net['A']['prob'][alarm]
                    sample[count]['A'] = True
                else:
                    weight *= self.get_CPT_Value(a.cpt, burg_val, earthq_val, False, None, None)#self.bayes_net['A']['prob'][alarm]
                    sample[count]['A'] = False
            else:
                if a_ran < self.get_CPT_Value(a.cpt, burg_val, earthq_val, True, None, None):#self.bayes_net['A']['prob'][alarm]:
                    sample[count]['A'] = True
                else:
                    sample[count]['A'] = False

            if sample[count]['A'] ==True:
                alarm_val= True
            else:
                alarm_val = False

            if evidence.get('J') is not None:
                if evidence['J'] == True:
                    weight *= self.get_CPT_Value(j.cpt, None, None, alarm_val, True, None)
                    sample[count]['J'] = True
                else:
                    weight *= self.get_CPT_Value(j.cpt, None, None, alarm_val, False, None)
                    sample[count]['J'] = False
            else:
                if j_ran < self.get_CPT_Value(j.cpt, None, None, alarm_val, True, None):
                    sample[count]['J'] = True
                else:
                    sample[count]['J'] = False

            if evidence.get('M') is not None:
                if evidence['M'] == True:
                    weight *= self.get_CPT_Value(m.cpt, None, None, alarm_val, None, True)#self.bayes_net['M']['prob'][jm]
                    sample[count]['M'] = True
                else:
                    weight *= self.get_CPT_Value(m.cpt, None, None, alarm_val, None, False)#self.bayes_net['M']['prob'][jm]
                    sample[count]['M'] = False
            else:
                if m_ran < self.get_CPT_Value(m.cpt, None, None, alarm_val, None, True):#self.bayes_net['M']['prob'][jm]:
                    sample[count]['M'] = True
                else:
                    sample[count]['M'] = False

            prob[count] = weight
            count +=1
        return sample, prob

    def generate_sample(self, num_sample):

        count = 0
        sample = defaultdict(dict)

        while count < num_sample :
            b_ran = random.random()
            e_ran = random.random()
            a_ran = random.random()
            j_ran = random.random()
            m_ran = random.random()

            if b_ran < self.get_CPT_Value(b.cpt, True, None, None, None, None):#self.bayes_net['B']['prob']['t']:
                sample[count]['B'] = True
            else:
                sample[count]['B'] = False

            if e_ran < self.get_CPT_Value(e.cpt, None, True, None, None, None):#self.bayes_net['E']['prob']['t']:
                sample[count]['E'] = True
            else:
                sample[count]['E'] = False

            #alarm = ''
            if sample[count]['B'] == True:
                burg_val = True#alarm += 't'
            else :
                burg_val = False#alarm += 'f'
            #alarm += ','
            if sample[count]['E'] == True:
                earthq_val = True
            else:
                earthq_val = False

            if a_ran < self.get_CPT_Value(a.cpt, burg_val, earthq_val, True, None, None):#self.bayes_net['A']['prob'][alarm]:
                sample[count]['A'] = True
            else:
                sample[count]['A'] = False

            #jm =""
            if sample[count]['A'] ==True:
                alarm_val= True
            else:
                alarm_val = False

            if j_ran < self.get_CPT_Value(j.cpt, None, None, alarm_val, True, None):#self.bayes_net['J']['prob'][jm]:
                sample[count]['J'] = True
            else:
                sample[count]['J'] = False

            if m_ran < self.get_CPT_Value(m.cpt, None, None, alarm_val, None, True):#self.bayes_net['M']['prob'][jm]:
                sample[count]['M'] = True
            else:
                sample[count]['M'] = False

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
        # evidence[str[0]] = str[1]
        for key in evidence.keys():
            if evidence[key] == 't':
                evidence[key] = True
            else:
                evidence[key] = False
        return evidence

    def parseEvidence(self, evidence):
        split = evidence.split(" ")
        evidence = []
        for each in split:
            eachSplit = each.split(",")
            if (len(eachSplit) == 2):
                obj = Node()
                if (eachSplit[0].lower() == 'a'):
                    obj = a
                elif (eachSplit[0].lower() == 'm'):
                    obj = m
                elif (eachSplit[0].lower() == 'j'):
                    obj = j
                elif (eachSplit[0].lower() == 'e'):
                    obj = e
                elif (eachSplit[0].lower() == 'b'):
                    obj = b
                obj.value = True if eachSplit[1].lower() == 't' else False
                evidence.append(obj)
        evidence = [i for i in evidence if i]
        return evidence

    def parseQuery(self, query):
        global b, e, a, m, j
        if (query.lower() == 'j'):
            return j
        elif (query.lower() == 'm'):
            return m
        elif (query.lower() == 'a'):
            return a
        elif (query.lower() == 'b'):
            return b
        elif (query.lower() == 'e'):
            return e

    def enumerate(self):
        global b, e, a, m, j
        res = 0
        for burg in b.cpt:
            if b.value is None or burg["B"] == b.value:
                for earth in e.cpt:
                    if e.value is None or (earth["E"] == e.value):
                        for al in a.cpt:
                            if (a.value is None or al["A"] == a.value) and (
                                    al["B"] == burg["B"] and al["E"] == earth["E"]):
                                for john in j.cpt:
                                    if (j.value is None or john["J"] == j.value) and (john["A"] == al["A"]):
                                        for mary in m.cpt:
                                            if (m.value is None or mary["M"] == m.value) and (mary["A"] == al["A"]):
                                                res += (
                                                burg["value"] * earth["value"] * al["value"] * mary["value"] * john[
                                                    "value"])
        return res

    def enumeration_ask(self, query, evidence_set):
        sum = 0
        result = 0
        self.parseEvidence(evidence_set)
        for value in [True, False]:
            isNone = query.value is None
            if (isNone):
                query.value = value
                result = self.enumerate()
                sum += result
                if (isNone):
                    query.value = None
                    prob = (sum - result) / sum
        return str(prob)

    def get_CPT_Value(self, cpt, b_val, e_val, a_val, j_val, m_val):
        for entry in cpt:
            if (entry.get("B")==b_val or entry.get("B")== None) and (entry.get("E") == e_val or entry.get("E") == None) and (entry.get("A")==a_val or entry.get("A")== None)  and (entry.get("J")==j_val or entry.get("J")== None) and (entry.get("M")==m_val or entry.get("M")== None):
                return entry.get("value")
        return None

def main():
    net = BayesNet()
    net.init()
    num_samples = 1000#sys.argv[1]
    evidence_set = 'J,t E,f'#sys.argv[2]
    query = 'M'#sys.argv[3]
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

    queryEnum = net.parseQuery(query)
    res = 'Enumeration of [' + query + ' | ' + evidence_set + '] is :'
    print res, net.enumeration_ask(queryEnum, evidence_set)

    return


if __name__ == '__main__':
    main()