# @Date:   2019-06-05T11:25:07+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Project: M_Rlanguage
# @Last modified time: 2019-06-05T12:21:56+08:00


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
get_Ttest_Result <- function(dfrm, groupVector_a, groupVector_b){
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
dfrm <- read.csv('./GSE5056_series_matrix.txt',
                header = TRUE, sep='\t', row.names=1)
dfrm_new <- na.omit(get_Ttest_Result(dfrm, 1:18, 19:44)) # Handel the NA value


# ------------------------------------------------------------------------------
# Set the cutoff and add tage to the data
# ------------------------------------------------------------------------------
co_p <- 2 # cutoff of p_value: 0.01 (-log10(0.01) = 2)
co_f <- 0.35 # cutoff of fold_change: +-1.274561(log2(cutoff) = +-0.35)
dfrm_new$Expression = "Normal"
dfrm_new[(dfrm_new$fold_change > 2^co_f) & (dfrm_new$p_value < 10^-co_p),]['Expression']='Up'
dfrm_new[(dfrm_new$fold_change < 2^-co_f) & (dfrm_new$p_value < 10^-co_p),]['Expression']='Down'


# ------------------------------------------------------------------------------
# Start to Plot the Data
# ------------------------------------------------------------------------------
pdf("Boxplot_Plot_of_GSE5056_zzf_0605.pdf")
# Set the margin, background-color, character-size
par(mfrow=c(1,2), mar=c(8,9,6,3), bg="#FFFFF0", tcl=0, cex.axis=0.5, mex=0.24)
# Draw the boxplot of Up Expression
boxplot(log2(dfrm_new[dfrm_new$Expression == "Up",][,1:44])+1,
        horizontal=TRUE, las=2, # Let the plot and tage horizontal
        col=topo.colors(44), border="#708090", pch=16, cex=0.5,# make it pretty
        xlab="log2(Up Expression)+1", yaxt = "n", ylab="Example")
# Draw the boxplot of Down Expression
boxplot(log2(dfrm_new[dfrm_new$Expression == "Down",][,1:44])+1,
        horizontal=TRUE, las=2,
        col=topo.colors(44), border="#708090", pch=16, cex=0.5,
        xlab="log2(Down Expression)+1")
# Set the title using mtext()
mtext("BoxPlot of Expression", side = 3, line = -4, outer = TRUE)
dev.off()
