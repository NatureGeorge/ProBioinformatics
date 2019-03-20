# @Date:   2019-03-20T10:16:22+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Project: R_language
# @Last modified time: 2019-03-20T14:36:38+08:00

# warning: the file route has to be reset!
# First
fileIn_A <- read.table("./group/groupA.txt")
fileIn_B <- read.table("./group/groupB.txt")
fileIn_C <- read.table("./group/groupC.txt")
fileIn_D <- read.table("./group/groupD.txt")
## First [1]
### Pseudocode
#### 1>Using the while() and cbind() to combine each dataFrame with its group information.
#### 2>As soon as the cind() is finished for one file, use rbind() to combind the current dataFrame with last one.
#### 3>In the end, get the complete dataFrame(Dat1).
files <- list(fileIn_A, fileIn_B, fileIn_C, fileIn_D)  # use list() to ensure the correct order of dataFrame and the group information that will be attach to it.
names <- list("groupA", "groupB", "groupC", "groupD")
new_files <- list()  # state for appending new dataFrame
index <- 1
while(index <= length(files))
{
  new_fileIn <- cbind(files[[index]], rep(names[[index]], times=nrow(files[[index]])))
  new_files[[index]] <- new_fileIn
  if(index == 1) {Dat1 <- new_files[[index]]}
  else {Dat1 <- rbind(Dat1, new_files[[index]])}
  index <- index + 1
}
names(Dat1) <- c("Data", "Group")
print(Dat1)
### Result:
###    Data  Group
### 1    40 groupA
### 2    40 groupA
### 3    50 groupA
### 4    60 groupA
### 5    65 groupA
### 6    72 groupA
### 7    79 groupA
### 8    86 groupA
### 9    93 groupA
### 10  100 groupA
### 11  107 groupA
### 12   43 groupA
### 13   34 groupA
### 14   55 groupA
### 15   66 groupA
### 16   34 groupB
### 17   55 groupB
### 18   66 groupB
### 19   40 groupB
### 20   40 groupB
### 21   50 groupB
### 22   60 groupB
### 23   65 groupB
### 24   72 groupB
### 25   79 groupB
### 26   49 groupB
### 27   39 groupB
### 28   67 groupB
### 29   60 groupC
### 30   65 groupC
### 31   72 groupC
### 32   79 groupC
### 33   49 groupC
### 34   39 groupC
### 35   67 groupC
### 36  100 groupC
### 37  107 groupC
### 38   43 groupC
### 39   34 groupC
### 40   55 groupC
### 41   66 groupC
### 42   40 groupC
### 43   40 groupC
### 44   50 groupC
### 45   60 groupC
### 46   84 groupC
### 47   34 groupC
### 48   56 groupC
### 49   45 groupC
### 50   67 groupC
### 51   80 groupC
### 52   78 groupC
### 53   76 groupC
### 54   72 groupD
### 55   79 groupD
### 56   86 groupD
### 57   93 groupD
### 58  100 groupD
### 59  107 groupD
### 60   43 groupD
### 61   34 groupD
### 62   55 groupD
### 63   66 groupD
### 64   40 groupD
### 65   40 groupD
### 66   50 groupD
### 67   60 groupD
### 68   65 groupD
### 69   72 groupD
### 70   79 groupD
### 71   49 groupD
### 72   39 groupD
### 73   67 groupD
### 74  100 groupD
### 75  107 groupD
### 76   43 groupD
### 77   34 groupD
### 78   55 groupD
### 79   66 groupD
### 80   40 groupD
### 81   40 groupD
### 82   50 groupD
### 83   60 groupD
### 84   84 groupD
### 85   34 groupD
### 86   56 groupD
### 87   45 groupD
### 88   67 groupD
### 89   80 groupD
### 90   78 groupD
### 91   76 groupD
### 92   69 groupD

## First [2]
### Pseudocode
#### 1>stack() can indicate where each observation originated.
#### 2>Use $V1 to generate a factor.
Dat1 <- stack(list(groupA=fileIn_A$V1,groupB=fileIn_B$V1,groupC=fileIn_C$V1,groupD=fileIn_D$V1))
print(Dat1)
### Result:
###    values    ind
### 1      40 groupA
### 2      40 groupA
### 3      50 groupA
### 4      60 groupA
### 5      65 groupA
### 6      72 groupA
### 7      79 groupA
### 8      86 groupA
### 9      93 groupA
### 10    100 groupA
### 11    107 groupA
### 12     43 groupA
### 13     34 groupA
### 14     55 groupA
### 15     66 groupA
### 16     34 groupB
### 17     55 groupB
### 18     66 groupB
### 19     40 groupB
### 20     40 groupB
### 21     50 groupB
### 22     60 groupB
### 23     65 groupB
### 24     72 groupB
### 25     79 groupB
### 26     49 groupB
### 27     39 groupB
### 28     67 groupB
### 29     60 groupC
### 30     65 groupC
### 31     72 groupC
### 32     79 groupC
### 33     49 groupC
### 34     39 groupC
### 35     67 groupC
### 36    100 groupC
### 37    107 groupC
### 38     43 groupC
### 39     34 groupC
### 40     55 groupC
### 41     66 groupC
### 42     40 groupC
### 43     40 groupC
### 44     50 groupC
### 45     60 groupC
### 46     84 groupC
### 47     34 groupC
### 48     56 groupC
### 49     45 groupC
### 50     67 groupC
### 51     80 groupC
### 52     78 groupC
### 53     76 groupC
### 54     72 groupD
### 55     79 groupD
### 56     86 groupD
### 57     93 groupD
### 58    100 groupD
### 59    107 groupD
### 60     43 groupD
### 61     34 groupD
### 62     55 groupD
### 63     66 groupD
### 64     40 groupD
### 65     40 groupD
### 66     50 groupD
### 67     60 groupD
### 68     65 groupD
### 69     72 groupD
### 70     79 groupD
### 71     49 groupD
### 72     39 groupD
### 73     67 groupD
### 74    100 groupD
### 75    107 groupD
### 76     43 groupD
### 77     34 groupD
### 78     55 groupD
### 79     66 groupD
### 80     40 groupD
### 81     40 groupD
### 82     50 groupD
### 83     60 groupD
### 84     84 groupD
### 85     34 groupD
### 86     56 groupD
### 87     45 groupD
### 88     67 groupD
### 89     80 groupD
### 90     78 groupD
### 91     76 groupD
### 92     69 groupD

# Second
### Pseudocode
#### 1>read files and correct the "try" file into the manageable form that merge() can handle
#### 2>Use merge() to combine data.
height <- read.table("./height.txt")
weight <- read.table("./weight.txt")
try <- read.table("./try.txt")
try <- as.data.frame(t(try))
Dat2 <- merge(height, weight, by=1)
Dat2 <- merge(Dat2, try, by=1)
names(Dat2) <- c("Name","Height","Weight","Try")
print(Dat2)
### Result:
###        Name   Height Weight  Try
### 1    Binbin 180.0000     49    3
### 2       Bob 174.2857     40    3
### 3     Cheng 176.0000    107    1
### 4   Cizhong 167.0000     43    7
### 5       Dan 171.0714     55    1
### 6     Danny 156.0000     86    7
### 7     Deyin 173.2143     56    7
### 8   Dongmei 168.9286     50    3
### 9      Ella 178.5714     72    7
### 10      Eva 179.6429     79    4
### 11      Fei 174.2857     45    4
### 12 Gaochuan 172.1429     34    7
### 13   Haiyun 167.8571     40    9
### 14   Hanson 175.3571     50    2
### 15     Jack 176.4286     60    1
### 16    Jason 140.0000     60    6
### 17      Jim 170.0000     40    5
### 18     Juan 170.0000     34    2
### 19      Jun 135.0000    100    5
### 20     Kate 154.0000     40    4
### 21    Kevin 177.5000     65    6
### 22     Linc 167.0000     72    2
### 23  Lixiang 168.0000     69    1
### 24      Mac 167.0000     50    5
### 25   Mingbu 171.0714     84    5
### 26       Qi 160.0000     66    1
### 27     Qian 168.9286     43    5
### 28   Robert 175.0000     79    6
### 29     Rong 167.0000     39    6
### 30   Ruixin 156.0000     55    2
### 31   Shaliu 172.1429     66    1
### 32  Shirley 164.0000     67 <NA>
### 33   Steven 160.0000     93    4
### 34      Tom 180.0000     65    3
### 35 Xiaojing 171.0000     76    6
### 36   Xiaole 167.8571    107 <NA>
### 37 Xiaolong 174.0000     78    3
### 38 Xiaoming 188.0000     80    4
### 39  Xiaoyan 167.0000     40    9
### 40     Yang 173.2143     40    4
### 41     Yong 167.0000    100    9
### 42  Yunping 170.0000     60    8
### 43 Zhiqiang 175.3571     67    6
### 44   Zhiwei 163.0000     34    8

# Third
mean_height <- mean(Dat2$Height)
max_weight <- max(Dat2$Weight)
min_i <- as.vector(Dat2$Try)
min_try <- min(min_i[complete.cases(min_i)])  # Handle the NA value
cat("mean_height:", mean_height, "\n")
cat("max_weight:", max_weight, "\n")
cat("min_try:", min_try, "\n")
### Result: mean_height=168.8604 max_weight=107 min_try=1

# Fourth
groupInfo <- read.table("./group.txt")
names(groupInfo) <- c("name","Group")
Dat4 <- merge(Dat2, groupInfo, by=1)
print(Dat4)
pdf("./output_boxplot.pdf")
boxplot(Weight ~ Group, Dat4, col=rainbow(4))  # draw target columns to plot
dev.off()
### Result:
###        Name   Height Weight  Try  Group
### 1    Binbin 180.0000     49    3 GroupA
### 2       Bob 174.2857     40    3 GroupB
### 3     Cheng 176.0000    107    1 GroupB
### 4   Cizhong 167.0000     43    7 GroupC
### 5       Dan 171.0714     55    1 GroupC
### 6     Danny 156.0000     86    7 GroupB
### 7     Deyin 173.2143     56    7 GroupA
### 8   Dongmei 168.9286     50    3 GroupC
### 9      Ella 178.5714     72    7 GroupB
### 10      Eva 179.6429     79    4 GroupB
### 11      Fei 174.2857     45    4 GroupB
### 12 Gaochuan 172.1429     34    7 GroupC
### 13   Haiyun 167.8571     40    9 GroupB
### 14   Hanson 175.3571     50    2 GroupB
### 15     Jack 176.4286     60    1 GroupA
### 16    Jason 140.0000     60    6 GroupB
### 17      Jim 170.0000     40    5 GroupA
### 18     Juan 170.0000     34    2 GroupC
### 19      Jun 135.0000    100    5 GroupB
### 20     Kate 154.0000     40    4 GroupB
### 21    Kevin 177.5000     65    6 GroupA
### 22     Linc 167.0000     72    2 GroupC
### 23  Lixiang 168.0000     69    1 GroupB
### 24      Mac 167.0000     50    5 GroupC
### 25   Mingbu 171.0714     84    5 GroupC
### 26       Qi 160.0000     66    1 GroupB
### 27     Qian 168.9286     43    5 GroupC
### 28   Robert 175.0000     79    6 GroupA
### 29     Rong 167.0000     39    6 GroupB
### 30   Ruixin 156.0000     55    2 GroupB
### 31   Shaliu 172.1429     66    1 GroupC
### 32  Shirley 164.0000     67 <NA> GroupC
### 33   Steven 160.0000     93    4 GroupB
### 34      Tom 180.0000     65    3 GroupB
### 35 Xiaojing 171.0000     76    6 GroupB
### 36   Xiaole 167.8571    107 <NA> GroupB
### 37 Xiaolong 174.0000     78    3 GroupA
### 38 Xiaoming 188.0000     80    4 GroupA
### 39  Xiaoyan 167.0000     40    9 GroupA
### 40     Yang 173.2143     40    4 GroupA
### 41     Yong 167.0000    100    9 GroupA
### 42  Yunping 170.0000     60    8 GroupC
### 43 Zhiqiang 175.3571     67    6 GroupB
### 44   Zhiwei 163.0000     34    8 GroupA

### Result: The pdf is sorted in the same file.
