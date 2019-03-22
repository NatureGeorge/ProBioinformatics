# @Date:   2019-03-20T10:16:22+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Project: R_language
# @Last modified time: 2019-03-20T14:36:38+08:00

# Read the Data
# setwd("C:\\Users\\Nature\\Desktop\\M_RLanguage\\Lab1 data\\Lab1 data")
fileIn_A <- read.table("group/groupA.txt")
fileIn_B <- read.table("group/groupB.txt")
fileIn_C <- read.table("group/groupC.txt")
fileIn_D <- read.table("group/groupD.txt")
## First Question Method[1]
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
### Pseudocode
#### 1>Using the while() and cbind() to combine each dataFrame with its group information.
#### 2>As soon as the cind() is finished for one file, use rbind() to combind the current dataFrame with last one.
#### 3>In the end, get the complete dataFrame(Dat1).
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# use list() to ensure the correct order of dataFrame and the group information that will be attach to it.
files <- list(fileIn_A, fileIn_B, fileIn_C, fileIn_D)
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


## First Question Method[2]
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
### Pseudocode
#### 1>stack() can indicate where each observation originated.
#### 2>Use $V1 to generate a factor.
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
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


# second Question
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
### Pseudocode
#### 1>read files and correct the "try" file into the manageable form that merge() can handle
#### 2>Use merge() to combine data.
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
height <- read.table("height.txt")
weight <- read.table("weight.txt")
try <- read.table("try.txt")
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


# Third Question
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Use complete.cases() to handle the NA value
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
mean_height <- mean(Dat2$Height)
max_weight <- max(Dat2$Weight)
min_i <- as.vector(Dat2$Try)
min_try <- min(min_i[complete.cases(min_i)])
cat("mean_height:", mean_height, "\n")
cat("max_weight:", max_weight, "\n")
cat("min_try:", min_try, "\n")
### Result: mean_height=168.8604 max_weight=107 min_try=1


# Fourth Question
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
groupInfo <- read.table("group.txt")
names(groupInfo) <- c("name","Group")
Dat4 <- merge(Dat2, groupInfo, by=1)
print(Dat4)
pdf("1730416009_output_boxplot.pdf")
boxplot(Weight ~ Group, Dat4, col=rainbow(4), main = "Weight Data of Three Groups", xlab = "Group Info", ylab = "Weight / kg")
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
### Result: The pdf is sorted in the same file.
