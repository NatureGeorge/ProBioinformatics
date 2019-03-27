# Something about the Matrix in R language
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

# 一些操作
## t()
> t(mat)
     [,1] [,2] [,3]
[1,]    1    3   56
[2,]    2    4   66

## solve()
> solve(mat)
Error in solve.default(mat) : 'a'(3 x 2)必需是正方形的
> b= matrix(c(1,3,534,66,34,4,6,63,5),3,3)
> solve(b)
              [,1]          [,2]          [,3]
[1,] -3.885453e-05 -0.0001449937  1.873547e-03
[2,]  1.593367e-02 -0.0015158005 -2.132261e-05
[3,] -8.597276e-03  0.0166979714 -7.770906e-05

## colnames(), rownames()
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
