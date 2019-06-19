# @Date:   2019-06-15T14:05:55+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Project: M_Rlanguage
# @Last modified time: 2019-06-15T14:57:59+08:00
# ------------------------------------------------------------------------------
# Preparation for the packages
# ------------------------------------------------------------------------------
library(RColorBrewer)
library(MASS)

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
# Plot the Data
# ------------------------------------------------------------------------------
# Preparate the the data
da_x <- log2(apply(dfrm_new[,1:18], 1, mean)+1) # Smokers
da_y <- log2(apply(dfrm_new[,19:44], 1, mean)+1) # Non-smokers
# Start to Plot
pdf("Scatter_Plot_of_GSE5056_zzf_0619.pdf")
# Use smoothScatter() to visualize the density of points
smoothScatter(da_x, da_y,
              # Set the points
              pch=19,cex=.1,col = rgb(25, 25, 112, 20, maxColorValue=255),
              main="Scatter Plot of GSE5056",xlab="log2(smokers+1)", ylab="log2(nonSmokers+1)"
             )
# Drow the Points to maintian the origin form
points(da_x, da_y,
       pch=19,cex=.1,col = rgb(0, 0, 255, 20, maxColorValue=255))
# Use contour() to draw the colored contour lines
contour(kde2d(da_x, da_y, n=300), # compute 2D kernel density
        drawlabels=FALSE, nlevels=11, # Set the level of contour
        col=rev(brewer.pal(11, "RdYlBu")), # Set the color
        add=TRUE, lwd=1)
# End the Plot
dev.off()
