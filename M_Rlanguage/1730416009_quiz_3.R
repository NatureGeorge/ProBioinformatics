# @Date:   2019-05-22T10:15:11+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Project: M_Rlanguage
# @Last modified time: 2019-05-22T17:11:08+08:00


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

# ------------------------------------------------------------------------------
# Use the function defined before to get Data
# ------------------------------------------------------------------------------
dfrm <- read.csv('./GSE5056_series_matrix.txt',
                header = TRUE, sep='\t', row.names=1)
dfrm_2 <- get_Ttest_Result_2(dfrm, 1:18, 19:44)

# ------------------------------------------------------------------------------
# Prepare for the plotable data and plot-variables
## use annotation_col/row to check the result of clustering
# ------------------------------------------------------------------------------
dfrm_new = na.omit(dfrm_2) # Del the NA value
# Annotation [COLUMN]
annotation_col = data.frame(People = factor(rep(c("Non_Smoker", "Smoker"), c(18,26))))
rownames(annotation_col) = colnames(dfrm)
# Set the cutoff and add tage to the data
co_p <- 2 # cutoff of p_value: 0.01 (-log10(0.01) = 2)
co_f <- 0.35 # cutoff of fold_change: +-1.274561(log2(cutoff) = +-0.35)
dfrm_new$Expression = "Normal"
dfrm_new[(dfrm_new$fold_change > 2^co_f | dfrm_new$fold_change < 2^-co_f) &
         (dfrm_new$p_value < 10^-co_p),]['Expression']='Differential'
# Get the plotable data
dfrm_plot <- dfrm_new[dfrm_new$p_value < 10^-co_p,]
# Annotation [ROW]
annotation_row = data.frame(dfrm_plot['Expression'])
rownames(annotation_row) = rownames(dfrm_plot)
colnames(annotation_row) = c("Expression")

# ------------------------------------------------------------------------------
# Use pheatmap to draw a headmap plot
# ------------------------------------------------------------------------------
library("pheatmap")
pheatmap(dfrm_plot[, 1:44], scale = "row",
         main = "Expression heatmap",
         show_rownames=F,
         clustering_method = 'ward.D2',
         border=FALSE,
         fontsize=8.5,
         annotation_col = annotation_col, # Add annotation
         annotation_row = annotation_row, # Add annotation
         color = colorRampPalette(c("green", "black","red"))(500),
         annotation_colors = list(
            People = c(Non_Smoker = "#9370DB", Smoker = "#FFA500"),
            Expression = c(Differential = "#00CED1", Normal = "yellow")
          ),
         filename="quiz_3_zzf_0522.pdf" # Save the fig
        )
