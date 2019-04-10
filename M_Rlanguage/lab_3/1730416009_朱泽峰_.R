# @Date:   2019-04-10T11:00:45+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Project: R_language
# @Last modified time: 2019-04-09T11:17:12+08:00

# Read file in the target file
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
getData <- function(fileOpenPath, fileSavePath, plot_title, plot_xlab, plot_ylab){
    data <- read.table(fileOpenPath, head=T)
    pdf(fileSavePath)
    # Set the tages
    with(data, plot(speed, dist, main=plot_title, xlab=plot_xlab, ylab=plot_ylab, type='n'))
    # Set the legend
    with(data,legend(60, 60, as.character(levels(country)), pch=1:length(levels(country)), col=1:length(levels(country))))
    grid()
    # Points the data with different color
    with(data, points(data, pch=as.integer(country), col=as.integer(country)))
    # Draw regression line of different country
    subData_1 <- data[which(data$country=='China'),]
    subData_2 <- data[which(data$country=='Japan'),]
    with(subData_1, abline(lm(dist~speed)))
    with(subData_2, abline(lm(dist~speed), col='red'))
    dev.off()
}
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Main()
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
fileOpenPath <- 'C:\\Users\\Nature\\Desktop\\M_RLanguage\\Lab_3\\dataset.txt'
fileSavePath <- 'C:\\Users\\Nature\\Desktop\\M_RLanguage\\Lab_3\\1730416009_out.pdf'
plot_title <- 'Cars: Speed vs. Stopping Distance (1920)'
plot_xlab <- 'Speed (MPH)'
plot_ylab <- 'Stopping Distance (ft)'
getData(fileOpenPath, fileSavePath, plot_title, plot_xlab, plot_ylab)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
