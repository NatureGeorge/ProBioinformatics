# @Date:   2019-04-19T13:36:22+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Project: R_language
# @Last modified time: 2019-04-19T14:36:38+08:00

# Handle the data into plotable format
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
getData <- function(df, year){
    i <- 2
    while(i <= 13)
    {
        temp <- df[,c(1,i)]
        temp$month <- i-1
        names(temp)[2]<- paste("data_",year,sep = "", collapse = "")
        if(i == 2){bindedDF <- temp}
        else{bindedDF <- rbind(bindedDF, temp)}
        i <- i + 1
    }
    return(bindedDF)
}
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Read the files and get Data
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
fileOpenPath_1 <- 'C:/Users/Nature/Desktop/M_RLanguage/R_Quiz_2/2015_tem_HK/tem_HK.txt'
fileOpenPath_2 <- 'C:/Users/Nature/Desktop/M_RLanguage/R_Quiz_2/2016_tem_HK/tem_HK.txt'
fileSavePath <- 's_plot.pdf'
data_1 <- read.csv(fileOpenPath_1, sep='\t')
data_2 <- read.csv(fileOpenPath_2, sep='\t')

df_1 <- getData(data_1,'2015')
df_2 <- getData(data_2,'2016')
## Deal with the NA value using merge()
df <- merge(df_1,df_2)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Set the Tage & Color
df$var <- df$data_2016-df$data_2015
df$col <- "grey"
df$col[df$var > 3] <- "red"
df$col[df$var < -3] <- "blue"
# Plot the data
pdf(fileSavePath)
plot(df$data_2015,df$data_2016,
     xlab="2015-temp(°C aka centigrade )",
     ylab="2016-temp(°C aka centigrade )",
     xlim=range(5,33),
     ylim=range(5,33),
     type="n",
     main="Everyday temp. in Hongkong in 2015 and 2016",
     cex=0.5)
grid()
with(df, points(data_2015,data_2016,pch=20,col=col))
with(df, abline(lm(data_2016~data_2015)))
legend("topleft", inset=.05, title="Temp Difference(2016-2015)", c("> 3°C","-3~3°C","< -3°C"), pch=16, col=c("red", "grey","blue"))
dev.off()
