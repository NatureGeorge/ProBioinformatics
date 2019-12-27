x <- c(0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.2,0.21,0.23)
y <- c(42,43.5,45,45.5,45,47.5,49,53,50,55,55,60)
lm.sol <- lm(y ~ 1+x)
summary(lm.sol)
# OutPut
#
#Call:
#lm(formula = y ~ 1 + x)
#
#Residuals:
#    Min      1Q  Median      3Q     Max
#-2.0431 -0.7056  0.1694  0.6633  2.2653                                        <- 残差分布
#
#Coefficients:                                                                  <- 回归系数/参数beta0,beta1的最小二乘估计值、标准差、显著性检验之t检验结果(t-value,p-value?)
#            Estimate Std. Error t value Pr(>|t|)
#(Intercept)   28.493      1.580   18.04 5.88e-09 ***
#x            130.835      9.683   13.51 9.50e-08 ***
#---
#Signif. codes:
#0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
#
#Residual standard error: 1.319 on 10 degrees of freedom                        <- 残差标准差
#Multiple R-squared:  0.9481,	Adjusted R-squared:  0.9429                       <- 回归方程的检验之相关系数检验法
#F-statistic: 182.6 on 1 and 10 DF,  p-value: 9.505e-08                         <- 回归方程的检验之F检验法
#

beta.int <- function(fm, alpha=0.05){
  # A function that extract the estimated interval
  A <- summary(fm)$coefficients
  df <- fm$df.residual
  mid <- A[, 2] * qt(1-alpha/2, df)
  left <- A[, 1] - mid
  right <- A[, 1] + mid
  rowname <- dimnames(A)[[1]]
  colname <- c("Estimate", "Left", "Right")
  matrix(c(A[,1], left, right), ncol=3, dimnames=list(rowname, colname))
}
# OutPut
#
#> beta.int(lm.sol)
#             Estimate      Left     Right
#(Intercept)  28.49282  24.97279  32.01285
#x           130.83483 109.25892 152.41074
#

# ------------------------------------------------------------------------------

X <- matrix(c(194.5, 20.79, 1.3179, 131.79, 194.3, 20.79, 1.3179, 131.79, 197.9,
  22.4, 1.3502, 135.02, 198.4, 22.67, 1.3555, 135.55, 199.4, 23.15, 1.3646, 136.46,
  199.9, 23.35, 1.3683, 136.83, 200.9, 23.89, 1.3782, 137.82, 201.1, 23.99, 1.38,
  138, 201.4, 24.02, 1.3806, 138.06, 201.3, 24.01, 1.3805, 138.05, 203.6, 25.14,
  1.4004, 140.04, 204.6, 26.57, 1.4244, 142.44, 209.5, 28.49, 1.4547, 145.47, 208.6,
  27.76, 1.4434, 144.34, 210.7, 29.04, 1.463, 146.3, 211.9, 29.88, 1.4754, 147.54,
  212.2, 30.06, 1.478, 147.8), ncol = 4, byrow = T, dimnames = list(1:17, c("F",
  "h", "log", "log100")))
forbes<-as.data.frame(X)
lm.sol <- lm(log100 ~ F, data=forbes)
summary(lm.sol)
# OutPut
#Call:
#lm(formula = log100 ~ F, data = forbes)
#
#Residuals:
#     Min       1Q   Median       3Q      Max
#-0.32261 -0.14530 -0.06750  0.02111  1.35924
#
#Coefficients:
#             Estimate Std. Error t value Pr(>|t|)
#(Intercept) -42.13087    3.33895  -12.62 2.17e-09 ***
#F             0.89546    0.01645   54.45  < 2e-16 ***
#---
#Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
#
#Residual standard error: 0.3789 on 15 degrees of freedom
#Multiple R-squared:  0.995,	Adjusted R-squared:  0.9946
#F-statistic:  2965 on 1 and 15 DF,  p-value: < 2.2e-16
#
y.res<-residuals(lm.sol);plot(y.res)
text(12,y.res[12], labels=12,adj=1.2)
i<-1:17; forbes12<-as.data.frame(X[i!=12, ])
lm12<-lm(log100~F, data=forbes12)
summary(lm12)
# OutPut
# Call:
# lm(formula = log100 ~ F, data = forbes12)
#
#Residuals:
#     Min       1Q   Median       3Q      Max
#-0.21175 -0.06194  0.01590  0.09077  0.13042
#
#Coefficients:
#             Estimate Std. Error t value Pr(>|t|)
#(Intercept) -41.30180    1.00038  -41.29 5.01e-16 ***                          <- Improved Std. Error
#F             0.89096    0.00493  180.73  < 2e-16 ***
#---
#Signif. codes:
#0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
#
#Residual standard error: 0.1133 on 14 degrees of freedom                       <- Improved Residual standard error
#Multiple R-squared:  0.9996,	Adjusted R-squared:  0.9995                       <- Improved R2
#F-statistic: 3.266e+04 on 1 and 14 DF,  p-value: < 2.2e-16
#

toothpaste<-data.frame(
  X1=c(-0.05, 0.25,0.60,0, 0.25,0.20, 0.15,0.05,-0.15, 0.15, 0.20, 0.10,0.40,0.45,0.35,0.30, 0.50,0.50, 0.40,-0.05, -0.05,-0.10,0.20,0.10,0.50,0.60,-0.05,0, 0.05, 0.55),
  X2=c( 5.50,6.75,7.25,5.50,7.00,6.50,6.75,5.25,5.25,6.00, 6.50,6.25,7.00,6.90,6.80,6.80,7.10,7.00,6.80,6.50, 6.25,6.00,6.50,7.00,6.80,6.80,6.50,5.75,5.80,6.80),
  Y =c( 7.38,8.51,9.52,7.50,9.33,8.28,8.75,7.87,7.10,8.00, 7.89,8.15,9.10,8.86,8.90,8.87,9.26,9.00,8.75,7.95, 7.65,7.27,8.00,8.50,8.75,9.21,8.27,7.67,7.93,9.26)
)
lm.sol<-lm(Y~X1+X2, data=toothpaste)
summary(lm.sol)
