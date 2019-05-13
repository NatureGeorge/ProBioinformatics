# @Date:   2019-04-26T13:36:22+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Project: R_language
# @Last modified time: 2019-04-19T14:36:38+08:00

getStockPlot <- function(stockList, fileSavePath){
    # Load the package that needed for clooecting data
    library("tseries")
    # Prepare for printing a pdf-format plot
    pdf(fileSavePath)
    #---------------------------------------------------------------------------
    ## Set the arrangement of plot
    par(mfrow=c(2,2))
    opar <- par(no.readonly = TRUE)
    ## Declare Variables
    col_v <- 1:length(stockList)
    dataList <-  list()
    xlab <- "Year"
    ylab <- "Prices($)"
    ## Collect the stock data via [tseries] and store the data in a list
    for(com in stockList){
        dataList <- c(dataList,list(get.hist.quote(instrument = com)))
    }
    ## Find the best data to plot at first
    maxIndex <- 1
    for(i in col_v){
        if (max(dataList[[i]][,"High"]) >= max(dataList[[maxIndex]][,"High"])){
            maxIndex <- i
        }
    }
    ## Plot subFig
    for(tage in c("Open", "High", "Low", "Close")){
      plot(
          dataList[[maxIndex]][,tage],
          main=paste("the ",tage," price",sep = "", collapse = ""),
          xlab=xlab, ylab=ylab, type='n')

      for(i in col_v){
          legend("topleft", legend=stockList, lwd=2, col=col_v+1)
          points(dataList[[i]][,tage],type="l",col=i+1)}
    }
    mtext(text="The stock price of google,baidu and alibaba",side = 3,outer=TRUE,line=-1)
    #---------------------------------------------------------------------------
    dev.off()
    # Reset
    par(opar)
}

# Input
comList <- c("GOOG","BABA","BIDU")
pdfSavePath <- "1730416009.pdf"
getStockPlot(comList, pdfSavePath)
