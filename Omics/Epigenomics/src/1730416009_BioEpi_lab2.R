# Filename: 1730416009_BioEpi_lab2.R
# Modified: Thursday, December 26th 2019, 10:25:00 am

#安装ChIPseeker相关包
BiocManager::install("ChIPseeker")
BiocManager::install("TxDb.Hsapiens.UCSC.hg19.lincRNAsTranscripts")

#载入相关包
library("ChIPseeker")
library(TxDb.Hsapiens.UCSC.hg19.knownGene)

#读入peak文件
setwd("/Users/lidingyang/Downloads/")
peak <- readPeakFile("test_peaks.bed")
txdb <- TxDb.Hsapiens.UCSC.hg19.knownGene

#输出注释信息文件peak.annotation.tsv
peakAnno <- annotatePeak(peak,tssRegion = c(-3000, 3000),TxDb = txdb,annoDb = "org.Hs.eg.db")
write.table(as.data.frame(peakAnno),"peak.annotation.tsv",sep="\t",row.names = F,quote = F)

#载入相关包
library("ChIPseeker")
library("org.Hs.eg.db")
library(clusterProfiler)
library(TxDb.Hsapiens.UCSC.hg19.knownGene)
library("TxDb.Hsapiens.UCSC.hg19.lincRNAsTranscripts")
#读入peak文件
txdb <- TxDb.Hsapiens.UCSC.hg19.knownGene
lincRNA_txdb=TxDb.Hsapiens.UCSC.hg19.lincRNAsTranscripts
treat <- readPeakFile("test_peaks.bed")
peaks <- list(treat=treat)
promoter <- getPromoters(TxDb=txdb, upstream=3000, downstream=3000)
tagMatrixList <- lapply(peaks, getTagMatrix, windows=promoter)
peakAnnoList <- lapply(peaks, annotatePeak, TxDb=txdb,tssRegion=c(-3000, 3000), verbose=FALSE,addFlankGeneInfo=TRUE, flankDistance=5000,annoDb="org.Hs.eg.db")
# Create a list with genes from each sample
gene = lapply(peakAnnoList, function(i) as.data.frame(i)$geneId)
# Run GO enrichment analysis 
ego <- enrichGO(gene = gene, 
                keytype = "ENTREZID",
                OrgDb = org.Hs.eg.db,
                ont = "BP", 
                pAdjustMethod = "BH", 
                qvalueCutoff = 0.05, 
                readable = TRUE)
# Dotplot visualization
dotplot(ego, showCategory=50)
# Multiple samples KEGG analysis
compKEGG <- compareCluster(geneCluster = gene, 
                           fun = "enrichKEGG",
                           organism = "human",
                           pvalueCutoff  = 0.05, 
                           pAdjustMethod = "BH")
dotplot(compKEGG, showCategory = 20, title = "KEGG Pathway Enrichment Analysis")
