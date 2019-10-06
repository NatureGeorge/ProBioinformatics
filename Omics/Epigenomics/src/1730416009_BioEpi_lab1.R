# @Date:   2019-08-16T23:24:17+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Filename: 1730416009_BioEpi_lab1.R
# @Last modified time: 2019-10-05T15:50:36+08:00

# ------------------------------------------------------------------------------
# Read the Files
# ------------------------------------------------------------------------------
folder <- '../data/'
file_1 <- paste(folder, 'GSE122186_H3K27ac-Input.WT.EtOH_peaks.FDR_0.001.bed', sep="")
file_2 <- paste(folder, 'GSE122186_H3K27ac-Input.WT.Untreated_peaks.FDR_0.001.bed', sep="")
# Just Read the First 3 columns
tab5rows <- read.table(file_1, nrows = 5,sep='\t')
classes <- sapply(tab5rows, class)
classes[c(-1,-2,-3)] <- rep("NULL", length(classes)-3)
data1 <- read.table(file_1, colClasses = classes)
data2 <- read.table(file_2, colClasses = classes)
# Just Focus On the Chr1 Data
chr1_data1 <- data1[data1$V1 == "chr1",]
chr1_data2 <- data2[data2$V1 == "chr1",]
# start <- min(c(min(chr1_data1[, "V2"]),min(chr1_data2[, "V2"]))) # 3670399
# end <- max(c(max(chr1_data1[, "V3"]),max(chr1_data2[, "V3"]))) # 195241958


# ------------------------------------------------------------------------------
# Count the Overlap
# ------------------------------------------------------------------------------
i <- 1
j <- 1
record <- FALSE
count <- 0 # count the overlap-num in file1 aspect
ans_s <- c() # Record the start data of Overlap
ans_e <- c() # Record the end data of Overlap
# Go through all the data of file1 and file2 in one loop
while (i <= dim(chr1_data1)[1] && j <= dim(chr1_data2)[1]) {
    lo <- max(c(chr1_data1[i, "V2"], chr1_data2[j, "V2"]))
    hi <- min(c(chr1_data1[i, "V3"], chr1_data2[j, "V3"]))
    if (lo <= hi){
        ans_s <- append(ans_s, lo)
        ans_e <- append(ans_e, hi)
        record <- TRUE
    }
    if (chr1_data1[i, "V3"] < chr1_data2[j, "V3"]){
        i <- i+1
        if (record){
            count <- count + 1
            record <- FALSE
        }
    }
    else{
        j <- j+1
    }
}
# Save the overlap info
df <- as.data.frame(list(Start=ans_s,End=ans_e))
