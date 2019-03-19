# @Date:   2019-03-18T10:15:28+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Project: FilterModel
# @Last modified time: 2019-03-18T11:17:31+08:00
# -*- coding:utf-8 -*-


# creact a dict which take aa as its keys
aa_list = ('A,K,D,F,G,N,M,L,R,T,P,S,I,E,Q,C,Y,H,W,V').split(',')
aa_dict = {}
for aa in aa_list:
    aa_dict[aa] = 0

# read file and write file
file_in = '1KP8_K'
file_out = '1KP8_K_fre_test.txt'
with open(file_in, 'rt') as input:
    with open(file_out, 'wt') as output:
        output.write('残基\t频数\t频率\n')
        # count the amount of a specific aa using dict
        aaSum = 0  # calculate the amount of all aa
        for line in input:
            if line[0] == '>':
                continue
            else:
                for i in range(len(line)-1):
                    aa_dict[line[i]] += 1
                    aaSum += 1
        # calculate the frequence of a specific aa using dict
        fre_dict = {}
        for i in aa_list:
            fre_dict[i] = aa_dict[i] / aaSum
        # output the result
        '''for i in aa_list:
            output.write(('%s\t%s\t%.2f\n') % (i, aa_dict[i], fre_dict[i]))'''

        # sort the frequence & output the result
        new_list = sorted(fre_dict.items(), key=lambda x: x[1], reverse=True)
        for i in new_list:
            output.write(('%s\t%s\t%.2f\n') % (i[0], aa_dict[i[0]], fre_dict[i[0]]))
