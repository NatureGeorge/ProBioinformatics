
# Different Apply Function in R language
## Content
* lapply()
* sapply()
* apply()
* tapply()
* mapply()

## lapply() &  sapply()
> Input: __list, fun__; Output: ***lapply*** always returns the results in ***list*** whereas ***sapply*** returns the results in a ***vector*** if that is possible

```R
lst <- lapply(lst, fun)
vec <- sapply(lst, fun)
# Special (e.g, fun is range)
mat <- sapply(lst, fun)
```

## apply()
> Input: ___matrix|dataframe, 1|2, fun___; Output: ***vector|matrix***

Applying a Function to Every Row (1)

Applying a Function to Every Column (2)

## tapply() & by()
> Input: ___dataframe|.., groupingFactor, fun___; Output: 

Applying a Function to Groups of Data

## mapply()
> Input: ___f, vecs,___; Output: ***vector***

Applying a Function to Parallel Vectors or Lists
