# 20190327_Note of R language
Date: 20190327, By: ZeFengZhu
## Content
## matrix()
### Use

```R
> data <- c(c(1,2),c(3,4),c(56,66))
> mat <- matrix(data,3,2)
> mat
     [,1] [,2]
[1,]    1    4
[2,]    2   56
[3,]    3   66
> mat <- matrix(data,2,3)
> mat
     [,1] [,2] [,3]
[1,]    1    3   56
[2,]    2    4   66
> mat <- matrix(data,3,2,byrow=TRUE)
> mat
     [,1] [,2]
[1,]    1    2
[2,]    3    4
[3,]   56   66

```

## t()
### Use

```R
> t(mat)
     [,1] [,2] [,3]
[1,]    1    3   56
[2,]    2    4   66
```

## solve()
### Use

```R
> solve(mat)
Error in solve.default(mat) : 'a'(3 x 2)必需是正方形的
> b= matrix(c(1,3,534,66,34,4,6,63,5),3,3)
> solve(b)
              [,1]          [,2]          [,3]
[1,] -3.885453e-05 -0.0001449937  1.873547e-03
[2,]  1.593367e-02 -0.0015158005 -2.132261e-05
[3,] -8.597276e-03  0.0166979714 -7.770906e-05
```

## colnames(), rownames()
### USe

```R
> colnames(mat) <- c("E","F")
> rownames(mat) <- c("A","B","C")
> mat
   E  F
A  1  2
B  3  4
C 56 66
> mat[,"E"]
 A  B  C 
 1  3 56 
> mat["A",]
E F 
1 2 
> mat[,1]
 A  B  C 
 1  3 56 
> mat[1,]
E F 
1 2 
```

## sample()
### Use

```R
> hour <- sample(1:12, 6, replace=TRUE)
> min <- sample(0:59, 6, replace=TRUE)
> sec <- sample(0:59, 6, replace=TRUE)
> ampm <- sample(c("AM","PM"),6,TRUE)
> dim <- data.frame(H=hour,M=min,S=sec,AP=ampm)
> dim
   H  M  S AP
1  3  2 53 AM
2 12 45 55 PM
3 12  2 17 PM
4  9 33 47 AM
5  2  9  4 AM
6  1  7 13 PM
```

## data.frame()
### Use

```R
> suburbs <- data.frame(city="Chicago", county="Cook", 
+ state="IL",pop=2853114)
>  newRow <- data.frame(city="West Dundee", county="Kane", 
+ state="IL", pop=5428) 
>  suburbs <- rbind(suburbs, newRow) 
> suburbs
         city county state     pop
1     Chicago   Cook    IL 2853114
2 West Dundee   Kane    IL    5428
> suburbs[1]  # data.frame
         city
1     Chicago
2 West Dundee
> suburbs[[1]]  # factor
[1] Chicago     West Dundee
Levels: Chicago West Dundee
> suburbs["city"]  # data.frame
         city
1     Chicago
2 West Dundee
> suburbs[["city"]]  # factor
[1] Chicago     West Dundee
Levels: Chicago West Dundee
> suburbs$city  # factor
[1] Chicago     West Dundee
Levels: Chicago West Dundee
```

## subset()
### Use

```R
>  library(MASS) 
>  subset(Cars93, select=Model, subset=(MPG.city > 30)) 
     Model
31 Festiva
39   Metro
42   Civic
73  LeMans
80   Justy
83   Swift
84  Tercel

> subset(Cars93, select=c(Model,Min.Price,Max.Price), subset=(Cylinders == 4 & Origin == "USA")) 
           Model Min.Price Max.Price
6        Century      14.2      17.3
12      Cavalier       8.5      18.3
13       Corsica      11.4      11.4
15        Lumina      13.4      18.4
21       LeBaron      14.5      17.1
23          Colt       7.9      10.6
24        Shadow       8.4      14.2
25        Spirit      11.9      14.7
27       Dynasty      14.8      16.4
29        Summit       7.9      16.5
31       Festiva       6.9       7.9
32        Escort       8.4      11.9
33         Tempo      10.4      12.2
34       Mustang      10.8      21.0
35         Probe      12.8      15.2
60         Capri      13.3      15.0
68       Achieva      13.0      14.0
69 Cutlass_Ciera      14.2      18.4
72         Laser      11.4      17.4
73        LeMans       8.2       9.9
74       Sunbird       9.4      12.8
79            SL       9.2      12.9
```

Use the subset function with a negated argument for the select parameter to exclude a column from a data frame using its name:

```R
> subset(Cars93, select=c(-Model,-Min.Price,-Max.Price))
```

## na.omit()
Your data frame contains NA values, which is creating problems for you. 
### Use

```R
> x <- c(1, NA, 3, 4, 5) 
> y <- c(6, 7, NA, 9, 10) 
> dfrm <- data.frame(x, y) 
> dfrm <- data.frame(x, y) 
> cumsum(dfrm) # cannot get what you want 
   x  y
1  1  6
2 NA 13
3 NA NA
4 NA NA
5 NA NA
>  dfrm2 <- na.omit(dfrm) 
> cumsum(dfrm)
   x  y
1  1  6
2 NA 13
3 NA NA
4 NA NA
5 NA NA
```

## merge() with() par() plot() point() grid()
