# Something About MetaboAnalystR

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
