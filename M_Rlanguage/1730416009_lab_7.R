# @Date:   2019-05-15T11:24:07+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Project: R_language
# @Last modified time: 2019-05-15T11:31:11+08:00

# ------------------------------------------------------------------------------
## [Description]
### This function calculates the fold-change and p-value of two groups.
## [Input]
### dataframe -> the grouped data; groupVector_a/b --> a vector of groupA that represent the column index;
## [Output]
### returns the input dataframe with two additional(new) columns: 'fold_change', 'p_value'
## [Details]
### When calculating the p-value, this function use for-loop to get the results
# ------------------------------------------------------------------------------
get_Ttest_Result_1 <- function(dfrm, groupVector_a, groupVector_b){
    # Get the average value of sample group A (non-smokers) & group B (smokers)
    non_smoker_mean <- apply(dfrm[, groupVector_a], 1, mean)
    smoker_mean <- apply(dfrm[, groupVector_b], 1, mean)
    # Calculate the fold-change
    fold_change <- smoker_mean / non_smoker_mean
    fold_change_dfrm <- as.data.frame(fold_change)

    # Use for-loop to apply t.test and get results of p-value
    p_value <- c()
    for(i in 1:(dim(dfrm)[1]-1)){ # Ignore the NA value
        p_value <- append(p_value, t.test(dfrm[i, groupVector_a], dfrm[i, groupVector_b])$p.value)
    }
    p_value <- append(p_value, NA) # Handle the NA value
    p_value_dfrm <- as.data.frame(p_value)

    # Add two new columns to the input dfrm
    dfrm <- cbind(dfrm, fold_change_dfrm, p_value_dfrm)
    # Return Value
    return(dfrm)
}


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


# Main()
dfrm <- read.csv('./GSE5056_series_matrix.txt',
                header = TRUE, sep='\t')
# dfrm_1 <- get_Ttest_Result_1(dfrm, 2:19, 20:45) # Slower
dfrm_2 <- get_Ttest_Result_2(dfrm, 2:19, 20:45) # Faster

# Plot()
pdf("Volcano_Plot_of_GSE5056_0515.pdf")
# Prepare for the Basic plot
plot(log2(dfrm_2$fold_change), -log10(dfrm_2$p_value), type='n', main="Volcano Plot of GSE5056",xlab="log2(fold_change)", ylab="-log10(p_value)")
grid()
# Set the Cutoff
co_p <- 2 # cutoff of p_value: 0.01 (-log10(0.01) = 2)
co_f <- 0.35 # cutoff of fold_change: +-1.274561(log2(cutoff) = +-0.35)
col_p <- rgb(0,206,209,maxColorValue=255)
# Get the SubSet data aaccording to the cutoff
var <- subset(dfrm_2, (fold_change > 2^co_f | fold_change < 2^-co_f) & p_value < 10^-co_p) # differential expression
nor <- subset(dfrm_2, (fold_change <= 2^co_f & fold_change >= 2^-co_f) | p_value >= 10^-co_p)
# Plot the points of different SubSet
points(log2(var$fold_change), -log10(var$p_value), col=col_p, pch = 19)
points(log2(nor$fold_change), -log10(nor$p_value), col = rgb(0, 0, 0, 35, maxColorValue=255))
# plot the lines of cutoff using abline()
abline(h=co_p, col=rgb(176,196,222,maxColorValue=255), lty=2)
abline(v=co_f, col=rgb(0,139,139,maxColorValue=255), lty=2)
abline(v=-co_f, col=rgb(0,139,139,maxColorValue=255), lty=2)
# Add the legend
legend("topleft", pch=c(19,1), , col=c(col_p,rgb(0,0,0)), legend=c('Differential expression','Normal expression'))

dev.off()
