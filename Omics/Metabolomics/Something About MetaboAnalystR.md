# Something About MetaboAnalystR

```txt
Filename: Something About MetaboAnalystR.md
Created Date: Friday, December 27th 2019, 5:01:54 pm
Author: ZeFeng Zhu
```

## Platform

It is recommended that the following steps be performed on the `Rstudio`.

## Upgrade R to 3.6+

* Note: this step is unnecessary unless your R version is 3.5

About how to upgrade R:

* <https://www.jianshu.com/p/c8ed84a229df?from=timeline&isappinstalled=0>


```R
install.packages("installr")
require(installr)
updateR()
```

## Rtools (for windows)

> <https://cran.r-project.org/bin/windows/Rtools/>

Download `Rtools` from the link if you did not install `Rtools`

Note:

* During the installation, select both x32 and x64 version since both are useful.

## Install

```file
install.R
```

## Bugs

### First of all: Keep Update

```R
# Ensure that your windows-platform-computer has installed Rtools, if your operating system is MAC OS, ignore this comment
require('devtools')
update_packages("MetaboAnalystR")
```

* Note: Only update MetaboAnalystR, skip others
* `install_version("data.table", version="1.12.6")` to fix unexpected update

### `SetKEGG.PathLib`

Something wrong:

```R
mSet<-SetKEGG.PathLib(mSet, "hsa")
```

How to fix:

```R
mSet<-SetKEGG.PathLib(mSet, "hsa", "current")
```

### `PerformIntegGeneMapping`

There are currently errors in this function.
