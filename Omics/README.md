# Omics💥

```txt
Created Date: Thursday, September 5th 2019, 11:00:53 am
Author: ZeFeng Zhu👨‍💻
```

## Course

### Reference Couse🌎

**MIT 7.91J Foundations of Computational and Systems Biology** [🎡](https://www.youtube.com/playlist?list=PLUl4u3cNGP63uK-oWiLgO7LLJV6ZCWXac) 

> list=PLUl4u3cNGP63uK-oWiLgO7LLJV6ZCWXac

### Undergraduate Courses🌏

* 基因组信息学
* 转录组学
* 表观组学
* 代谢组学
* 蛋白组学
* 计算机辅助药物设计
* 临床基因组学

## 5. Library Complexity and Short Read Alignment (Mapping)

* [📺 Thread](https://www.youtube.com/watch?v=P3ORBMon8aw)

## 6. Genome Assembly

* [📺 Thread](https://www.youtube.com/watch?v=ZYW2AeDE6wU)

<iframe width="699" height="393" src="https://www.youtube.com/embed/ZYW2AeDE6wU?list=PLUl4u3cNGP63uK-oWiLgO7LLJV6ZCWXac" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## 7. ChIP-seq Analysis; DNA-protein Interactions

* [📺 Before class](https://www.youtube.com/watch?v=nkWGmaYRues "StatQuest: A gentle introduction to ChIP-Seq")
* [📺 Thread](https://www.youtube.com/watch?v=Ob9xGBPvr_s)

### ChIP-seq Protocol

***Indentifies the locations in the genome bound by proteins***

#### Experiment Protocol

> The essential idea is that you have a collection of cells (i.e 10 million cells to get robust signals). Another essential idea is that you take a flash photography picture of the cells while it's alive and you add a cross-linking agent and that cross-links proteins and create bonds between the proteins and the DNA where those proteins are sitting. Then you isolate the chromatin material and you wind up with pieces of DNA with protein occupying them (so far are non-selectively cross-linked to the genome, just all the proteins). And you can take them extracted and fragmented. Typically you fragment it by using sonication which is mechanical energy which causes the DNA to break at random locations. Then you can immunopurify with an antibody to the protein of interest. So one condition of using this technology is either A: you have a good antibody to a protein that you care about as regulatory, or B: you have tagged this protein such that it has a flag tag, myc tag or some other epitope on it which allows you to use an antibody or other purification methodology for that specific tag.

1. Crosslink proteins to binding sites in living cells
   * Fix with formaldehyde(or something like it) 
2. Harvest cells and fragment DNA (Sonication/DNA fragmentation)
3. **Experimental group🌝 & Control group🌚** (Input: Only sonicated DNA)
   * [🌝] Enrich for protein-bound DNA fragments with antibody (Purification of ChIP-DNA)
   * [🌚] Do Nothing
4. **Experimental group🌝 & Control group🌚**
   * [🌝] Sequence ChIP-DNA (Quantification of ChIP-DNA)
     * Prepare a sequencing library by adding sequencing adapters to both end of the DNA fragments
     * PCR amplify the library
     * Check the library concentration
     * Sequence
     * Filter out garbage reads
     * Align the high quality reads to genome (NEXT STEP)
   * [🌚] Sequence whole cell extract(WCE) DNA
     * same

> One problem with tags on proteins is that they can render the proteins nonfunctional. If thet're nonfunctional , then, of course, they are not going to bind where they should bind. 

> After you have purified the protein of interest, you can **reverse** the cross-linking, have a collection of fragments that you then sequence using a high throughput sequencing instruments. Since the fragmentation is random, you are going to sequencing both ends of these molecules which gives you a sequence tag that is **near** where the event occurred, but not exactly at it. And we are going to take these tags and align the reads to the genome and try to discern from those aligned reads where the original proteins were binding. Now, our job is to do the best possible alignment or discovery of where the proteins are binding, given this evidence. The other thing we will do is that we will take the original population of molecules and do the WCE as control.

#### Data Processing Protocol

> Target: genome wide and figure every place that the target protein is binding to the genome. One way to approach the question would be simply say, where are the peaks and where is the middle of the peak?(peak finding)

1. Alignment
2. Peak finding(signal construction)
    * It just works fine when a peak represents a single binding event
    * As two peaks come closer, instead of having two peaks, we are going to wind up having one broad peak.
    * So we need to be able to take these sorts of envents that occur underneath a single enrichment, or single peak into separate binding events
    * The spatial distribution of reads can be used to improve spatial resolution of prediction and de-convolve joint binding events
3. Peak calling?
    * We Use control track to verify that a high concentration of reads in the Chip-seq track is due to a protein binding there and not because a lost of reads mapped to a repetitive region.
4. Next step
   * compare peaks for the same protein in different cell types
   * Motif finding
   * determine the functional role of the target protein by looking at where it binds relative to the genes

> i.e _A binding event produces a distribution of reads around its site._ There are _two binding events_.
> One of the reasons this addtive property works is that we are working with a large population of cells, and regulators don't always occupy a site. And thus, what we are looking at in terms of the reads are the sum of all of the evidence from all of the cells. And so even though the proteins are close to one other, we often can find an additive effect between that proximal binding.
> ...

## 8. RNA-sequence Analysis: Expression, Isoforms

* [📺 Before class](https://www.youtube.com/watch?v=tlf6wYJrwKY "StatQuest: A gentle introduction to RNA-seq")
* [📺 Thread](https://www.youtube.com/watch?v=MniYgsZSp30)
* [📺 After class](https://www.youtube.com/watch?v=gKnfP2_Xdpo "StatQuest: RNA-seq - the problem with technical replicates")

## 9. Modeling and Discovery of Sequence Motifs

* [📺 Thread](https://www.youtube.com/watch?v=1EMonM7qAU8)

## 10. Markov and Hidden Markov Models of Genomic and Protein Features

* [📺 Thread](https://www.youtube.com/watch?v=d5NMrA2HkG4)

## 14. Predicting Protein Interactions

* [📺 Thread](https://www.youtube.com/watch?v=C95294_vvQY)

## 15. Gene Regulatory Networks

* [📺 Thread](https://www.youtube.com/watch?v=So6MK_FcP4E)

## 16. Protein Interaction Networks

* [📺 Thread](https://www.youtube.com/watch?v=RBPcKbEvK3U)