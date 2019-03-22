# @Date:   2019-03-22T13:39:20+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Project: R_language
# @Last modified time: 2019-03-22T14:46:38+08:00

# Find all the files in a particular route.
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## Assume that the relative path of the target folder is "./group"
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# setwd("")  # set the work path
files <- list.files("group")
dirs <- paste("./group/", files, sep="")
names <- c("groupA", "groupB", "groupC", "groupD")

## Method 1
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
for(i in 1:length(dirs))
{
  temp <- read.table(dirs[i])
  temp_df <- cbind(temp, rep(names[i], times=nrow(temp)))
  if(i == 1) {Dat1 <- temp_df}
  else {Dat1 <- rbind(Dat1, temp_df)}
}
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

## Method 2
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
file_list <- list()
for(i in dirs)
{
  temp <- read.table(dirs)
  file_list <- append(file_list, temp)
}
names(file_list) <- names
Dat1 <- stack(file_list)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
