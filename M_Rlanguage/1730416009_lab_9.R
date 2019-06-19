# @Date:   2019-06-15T14:05:55+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Project: M_Rlanguage
# @Last modified time: 2019-06-15T14:57:59+08:00
# ------------------------------------------------------------------------------
# Preparation for the packages
# ------------------------------------------------------------------------------
require(ggplot2)
require(gridExtra)


# ------------------------------------------------------------------------------
## [Description]
### This function calculates the fold-change and p-value of two groups.
## [Input]
### dataframe -> the grouped data; groupVector_a/b --> a vector of groupA that represent the column index;
## [Output]
### returns the input dataframe with two additional(new) columns: 'fold_change', 'p_value'
## [Details]
### When calculating the p-value, this function use apply() to get the results
## [Notes]
### This function is faster than get_Ttest_Result_2()
# ------------------------------------------------------------------------------
get_Ttest_Result_2 <- function(dfrm, groupVector_a, groupVector_b){
    # Get the average value of sample group A (non-smokers) & group B (smokers)
    non_smoker_mean <- apply(dfrm[, groupVector_a], 1, mean)
    smoker_mean <- apply(dfrm[, groupVector_b], 1, mean)
    # Calculate the fold-change
    fold_change <- smoker_mean / non_smoker_mean
    fold_change_dfrm <- as.data.frame(fold_change)

    # Use apply() to apply t.test and get results of p-value
    ## Use tempFunction to get p-value
    p_value <- apply(dfrm[1:(dim(dfrm)[1]-1),], 1, function(x) t.test(as.numeric(x[groupVector_a]),as.numeric(x[groupVector_b]))$p.value)
    p_value <- append(p_value, NA) # Handle the NA value
    p_value_dfrm <- as.data.frame(p_value)

    # Add two new columns to the input dfrm
    dfrm <- cbind(dfrm, fold_change_dfrm, p_value_dfrm)
    # Return Value
    return(dfrm)
}


# ------------------------------------------------------------------------------
# Get the Data
# ------------------------------------------------------------------------------
dfrm <- read.csv('C:\\Users\\Nature\\Desktop\\M_RLanguage\\Lab_6\\GSE5056_series_matrix.txt',
                header = TRUE, sep='\t', row.names=1)
dfrm_new <- na.omit(get_Ttest_Result_2(dfrm, 1:18, 19:44))


# ------------------------------------------------------------------------------
# Select 4 genes with lowest p-value
# ------------------------------------------------------------------------------
most <- dfrm_new[order(dfrm_new$p_value),,drop=FALSE][1:4,1:44]
# Get the data of smokers
x1 <- stack((log2(data.frame(t(most[,1:18])))+1))
x1$var1 <- c('smoker')
# Get the data of non-smokers
x2 <- stack((log2(data.frame(t(most[,19:44])))+1))
x2$var1 <- c('non-smoker')
# Combine the data of smokers and non-smokers
x3 <- rbind(x1,x2)
colnames(x3) <- c('values', 'gene', 'var')


# ------------------------------------------------------------------------------
# Plot the data with ggplot2
# ------------------------------------------------------------------------------
# Set the theme of the plot
setTheme <- theme(legend.position = "top",
                  legend.text=element_text(size=3.8),
                  axis.text=element_text(size=7),
                  axis.title=element_text(size=10, face="bold"))
# First Plot: Different expression of smokers and non-smokers in each gene
s1 <- ggplot(data=x3, aes(x=gene, y=values, fill=var)) +
  geom_boxplot() + setTheme
# Second Plot: Different expression of genes in each group of people
s2 <- ggplot(data=x3, aes(x=var, y=values, fill=gene)) +
  geom_boxplot() + setTheme

# Save the Plot
ggsave(grid.arrange(s2,s1,ncol = 2), filename = "C:/Users/Nature/Desktop/M_RLanguage/homeWork/17生信_lab_9/1730416009_朱泽峰/1730416009_lab9_0612.pdf")
