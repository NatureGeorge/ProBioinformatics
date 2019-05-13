# @Date:   2019-04-24T010:13:33+08:00
# @Email:  1730416009@stu.suda.edu.cn
# @Project: M_R_language
# @Last modified time: 2019-04-24T10:48:43+08:00
# ------------------------------------------------------------------------------
# O(n^2) Exponential Algorithm
# ------------------------------------------------------------------------------
fibonacci <- function(num){
    # Def the subFunction that get the final result of each inputNum
    unit <- function(num){
        # Deal with the basic situation + set the break point for the iteration
        if(num == 1){return(1)}
        # Deal with the incorrect input and nosence calculation + set the break point for the iteration
        else if(num <= 0){return(0)}
        # Use recursion to get the result of the sequence
        else {return(unit(num-1)+unit(num-2))}
    }
    # Declare the varible that store the answer of each recursion
    record <- c()
    # Use iteration to get the sequence
    for(i in 1:num){record <- append(record, unit(i))}
    return(record)
}
# ------------------------------------------------------------------------------
# O(n) Linear Algorithm
# Since the first two elements of the fibonacci sequence are '1' and the follow
# -ing elements are the result of the sum of previous two element, we can calcul
# -ate the sequence by iteration and performing two replacement.
# ------------------------------------------------------------------------------
fibonacci <- function(num){
    # Set the initial parameter
    sum <- 1  # Sum the result
    first <- 1 # F(n-2)
    second <- 1 # F(n-1)
    count <- 3  # the order of the sequence
    record <- c(1,1) # store the result of each order
    while(count <= num){
        sum <- first + second
        first <- second  # update
        second <- sum  # update
        count <- count + 1  # update
        record <- append(record, sum)
    }
    if(num <= 0){num <- 1}
    else if(num > 3){num <- 3}
    switch(num,return(c(1)),return(record),return(record))
}
