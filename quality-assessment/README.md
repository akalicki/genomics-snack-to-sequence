## Ubiquitous Genomics Hackathon #1: Snack to Sequence

Group #3: The Minnows
 - Alex Kalicki (avk2116)
 - Boyu Wang (bw2387)
 - Lilly Wang (lfw2114)
 - Mike Curry (mjc2260)
 - Tia Zhao (tz2191)


### Question 1

As instructed, we calculated the number of 1D and 2D reads classified as
"passed" versus the number classified as "failed". We also calculated the
fraction of reads that were 2D called in both the "pass" and "fail" folders with
the following results:

Passed Reads:
 - 3819 1D reads
 - 3819 2D reads
 - 50.00% of the "passed" reads were 2D

Failed Reads:
 - 10396 1D reads
 - 2300 2D reads
 - 18.12% of the "failed" reads were 2D

### Question 2

- Average reads per channel: 64
- Channel with most reads: 468
- Number of reads in Channel 468: 264

### Question 3

The cumulative base pairs from "passed" and "failed" 2D reads are plotted below
as a function of time. To find the cumulative nucleotides, multiply the y-values
of the graph by 2 (as each base pair consists of 2 nucleotides).

Cumulative "passed" nucleotides:

![cumulative passed nucleotides](images/question3_pass.png)

Cumulative "failed" nucleotides:

![cumulative failed nucleotides](images/question3_fail.png)

### Question 4

Since the entire human genome contains about 3 billion base pairs, it would take
about 284.38 days or 6825.16 hours to sequence it once using a MinION.
The rate of sequence reading that we used in the calculation was based on the
total sequence length for 'passed' 2D reads and their total duration.

### Question 5

As described in the assignment, we calculated the base-calling quality mean
and standard deviation for 2D reads in both the "passed" and "failed"
directories. We then compared using the student t-test to get the following:

Passed Reads:
 - Number of bases: 2876390
 - Average base-calling quality: 10.17
 - Base-calling median: 10.00
 - Base-calling standard deviation: 1.62

Failed Reads:
 - Number of bases: 1375824
 - Average base-calling quality: 8.77
 - Base-calling median: 9.00
 - Base-calling standard deviation: 1.92

Our reads showed a disappointingly low quality score on a scale from 1-30. Based
off previous successes in MinION sequencing read quality scores, we believe our
poor result to come from a bad sample or experimental practice. However, we can
see that the average base-calling quality in the failed reads is consistently
below the average base-calling quality of the passed reads.

The student t-test for these results yielded a value of 786, which allows us to
reject the null-hypothesis with any reasonable confidence level.

After isolating the first and last hour reads from the rest of the data, we
received the following results:

First Hour "Passed" 2D read median base-quality: 4.12
Last Hours "Passed" 2D read median base-quality: 4.12

The fact that the median base-quality values for the first and last hour match
up so precisely is a good sign, as it suggests that the quality of the
sequencing from the MinION Nanopores is not degrading over time running.



### Question 6

The following histograms depict the length distributions of 1D and 2D reads in
the failed and passed folders.

1D Reads

![seq length vs time](images/1D-Pass.png)

![seq length vs time](images/1D-Fail.png)

2D Reads

![seq length vs time](images/2D-Pass.png)

![seq length vs time](images/2D-Fail.png)

### Question 7

The following table shows the longest reads for each type of read in the passed
folder.

| Type       | Longest Read (nucleotides) |
|------------|----------------------------|
| Template   | 5032                       |
| Complement | 5167                       |
| 2D         | 6222                       |

### Question 8

The obtained sequence length over time for 2D reads is plotted below for both
"passed" and "failed" reads.

![seq length vs time](images/q8_plot.png)

The linear regression had a coefficient of 0.02, an intercept of -29574731.57,
and an R value of 0.025. There thus appears to be little correlation between
the two variables.

### Question 9

The pace of the strand sequencing (sequence length per duration in pore) is
plotted below for both "passed" and "failed" reads. For each plot, we attempted
to find the best linear fit to the data. Note that outliers beyond the range of
the plotted graphs significantly skewed the predicted linear fit for the
"failed" 2D reads.

Pacing for "passed" reads:

![passed read pacing](images/question9_pass.png)

Pacing for "failed" reads:

![failed read pacing](images/question9_fail.png)

### Question 10

|   | Pass       | Fail       |
|---|------------|------------|
| A | 27.132035% | 25.866463% |
| C | 22.518428% | 23.350443% |
| T | 27.072690% | 26.145277% |
| G | 23.276846% | 24.637817% |

### Question 11

We performed linear regression of sequencing duration against sequence
length for the passed 2D reads. We found a coefficient of 0.0091, an
intercept of -0.649, and an R^2 of 0.679. Experiments with features
consisting of frequency of nucleotides in the read only slightly
improved the R^2 for a linear model (probably just a result of more
degrees of freedom). Use of boosted trees brought the R^2 up to more
than .80 on the training set, but this was likely just the result of
overfitting.
