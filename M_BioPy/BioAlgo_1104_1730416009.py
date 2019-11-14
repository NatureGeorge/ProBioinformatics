# @Date:   2019-11-10T21:06:27+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Filename: BioAlgo_1104_1730416009.py
# @Last modified time: 2019-11-10T21:27:49+08:00
import numpy as np


class HiddenMarkovModel:
    def __init__(self, init_probs, emission_probs, trans_prob):
        """
        Constructor based on five different attributes: initial,
        emission probabilities and transition probabilities matrices.
        States and symbols lists.
        """
        self.initstate_prob = init_probs
        self.emission_probs = emission_probs
        self.transition_probs = trans_prob
        self.states = self.emission_probs.keys()
        self.symbols = list(self.emission_probs[list(
            self.emission_probs.keys())[0]].keys())

    def get_init_prob(self, state):
        """Initial probability of a given state"""
        if state in self.states:
            return (self.initstate_prob[state])
        else:
            return 0

    def get_emission_prob(self, state, symbol):
        """Probability of a given state emit a symbol """
        if state in self.states and symbol in self.symbols:
            return (self.emission_probs[state][symbol])
        else:
            return 0

    def get_transition_prob(self, state_orig, state_dest):
        """Probability of transition from an origin state to destination state"""
        if state_orig in self.states and state_dest in self.states:
            return (self.transition_probs[state_orig][state_dest])
        else:
            return 0

    def joint_probability(self, sequence, path):
        """
        Given an observed sequence and a corresponding state path
        calculate the probability of the sequence given the path under the model
        """
        seq_len = len(sequence)
        if seq_len == 0:
            return None

        path_len = len(path)
        if seq_len != path_len:
            print("Observed sequence and state path of different lengths!")
            return None

        prob = self.get_init_prob(
            path[0]) * self.get_emission_prob(path[0], sequence[0])
        for i in range(1, len(sequence)):
            prob = prob * self.get_transition_prob(
                path[i - 1], path[i]) * self.get_emission_prob(path[i], sequence[i])

        return prob

    def forward(self, sequence):
        """
        Given an observed sequence calculate the list of forward probabilities of the sequence using the chain rules
        """
        seq_len = len(sequence)
        if seq_len == 0:
            return []
        # calculate the product of the initial probability of each state and the first symbol of the sequence
        prob_list = [{}]
        for state in self.states:
            prob_list[0][state] = self.get_init_prob(
                state) * self.get_emission_prob(state, sequence[0])

        # iterate through the sequence and for each state multiply by the transition
        # probability with any other of the possibles states; this corresponds to a jump to a new state
        # once in this new state multiply by the corresponding emission probability of the sequence symbol in that state
        for i in range(1, seq_len):
            prob_list.append({})
            for state_dest in self.states:
                prob = 0
                for state_orig in self.states:
                    prob += prob_list[i - 1][state_orig] * \
                        self.get_transition_prob(state_orig, state_dest)
                prob_list[i][state_dest] = prob * \
                    self.get_emission_prob(state_dest, sequence[i])
        return prob_list

    def backward(self, sequence):
        """
        Given an observed sequence calculate the list of backward probabilities of the sequence
        """
        seq_len = len(sequence)
        if seq_len == 0:
            return []
        beta = [{}]
        for state in self .states:
            beta[0][state] = 1
        for i in range(seq_len - 1, 0, -1):
            beta.insert(0, {})
        for state_orig in self .states:
            prob = 0
        for state_dest in self .states:
            prob += beta[1][state_dest] * self.get_transition_prob(
                state_orig, state_dest) * self.get_emission_prob(state_dest, sequence[i])
            beta[0][state_orig] = prob
        return beta

    def viterbi(self, sequence):
        """
        Viterbi algorithm calculates the most probable state path
        for an observed sequence.
        """
        seq_len = len(sequence)
        if seq_len == 0:
            return []
        viterbi = {}
        state_path = {}
        # Initialize the probabilities for the first symbol
        for state in self.states:
            viterbi[state] = abs((np.log2(self.get_init_prob(state)) + np.log2(self.get_emission_prob(state, sequence[0]))))
            # print(viterbi[state])
            state_path[state] = [state]
        # compute recursively until the last element
        for t in range(1, seq_len):
            new_state_path = {}
            new_path = {}
            viterbi_tmp = {}
            for state_dest in self.states:
                intermediate_probs = []
                for state_orig in self.states:
                    prob = viterbi[state_orig] + abs(np.log2(abs(self.get_transition_prob(state_orig, state_dest) + 0.0000001)))
                    # print(prob)
                    intermediate_probs.append((prob, state_orig))
                (max_prob, max_state) = min(intermediate_probs)
                prob = abs(np.log2(self.get_emission_prob(state_dest, sequence[t]))) + max_prob
                viterbi_tmp[state_dest] = prob
                new_state_path[state_dest] = max_state
                new_path[state_dest] = state_path[max_state] + [state_dest]
            viterbi = viterbi_tmp
            state_path = new_path  # just keep the optimal path
        max_state = None
        max_prob = float("inf")
        # among the last states find the best prob and the best path
        for state in self.states:
            if viterbi[state] < max_prob:
                max_prob = viterbi[state]
                max_state = state
        return (max_prob, state_path[max_state])


def test():
    seq = "ACTTTA"
    initialP = {"5": 0.8, "M": 0.15, "3": 0.05}
    emissionP = {"5": {"A": 0.20, "C": 0.30, "G": 0.30, "T": 0.20}, "M": {"A": 0.25, "C": 0.25,
                                                                          "G": 0.25, "T": 0.25}, "3": {"A": 0.35, "C": 0.15, "G": 0.15, "T": 0.35}}
    transitionP = {"5": {"5": 0.8, "M": 0.2, "3": 0.0}, "M": {
        "5": 0.0, "M": 0.9, "3": 0.1}, "3": {"5": 0.0, "M": 0.0, "3": 1.0}}
    HMM = HiddenMarkovModel(initialP, emissionP, transitionP)
    print(HMM.viterbi(seq))


if __name__ == "__main__":
    test()
