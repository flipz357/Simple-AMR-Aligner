# Simple and unsupervised AMR-to-text alignment based on Wasserstein Weisfeiler Leman

The repository contains python code for Wasserstein based AMR to text alignment. This is the key assumption:

**Every token has some correspondence in the AMR, and every AMR part has some correspondence in the sentence**

Note that this differs from other AMR alignment conceptualizations, e.g., where nodes/tokens can remain unaligned.


## Requirements

Install the following python packages (with pip or conda):

```
numpy (tested: 1.19.4)
scipy (tested: 1.1.0) 
networkx (tested: 2.5)
gensim (tested: 3.8.3)
penman (tested: 1.1.0)
pyemd (tested: 0.5.1)
spacy (tested: 3.4.1)
```

## Computing AMR-text alignment (AMR Nodes to token(offsets))

Recommended command:

```
cd src
python wasser_align.py -a test.amr \
		       -output_type score_alignment \ 
                       -stability_level 15 -k 10
```

Here's how such a file may look on the inside:

```
# ::id 1
# ::snt A cat runs
(r / run-01
	:arg0 (c / cat))

# ::id 2
...
```

The method 

1. uses spacy to project dependency graphs
2. uses 10 Weisfeiler-Leman iterations to project AMR and Dep graph into a similar space
3. Calculate Wasserstein distance, using calculated transport plan
4. return transport plan as alignment


## Interesting variation: additionally align dependency edges to AMR edges

We can also align full relation triples (e.g., `x arg0 y` VS `x nsubj y`), by raising edge labels to nodes (obtaining unlabeled graph).

This can be achieved by setting an additional parameter:

Recommended command:

```
cd src
python wasser_align.py -a test.amr \
		       -output_type score_alignment \
                       -stability_level 15 -k 10 \
		       --edge_to_node_transform 
```

## Interpreting output

For each sentence-amr pair a json dictionary is returned:


- score: wasserstein similarity between dependency tree and amr
- alignment: Wasserstein transport plan, keys are amr nodes, values are dictionaries where keys are offset_lemmas and values are flow, cost transportation


E.g.:

```
{"score": 0.684, "alignment": {"r": {"0_a": [0.166666, 0.42018861671278135], "6_run": [0.333333, 0.301206603576575]}, "c": {"0_a": [0.166667, 0.41607656600109755], "2_cat": [0.333333, 0.22984406628413767]}}}
```
Which means that

```
AMR node "r"(run) is projected to token "runs" with flow = 0.3333
AMR node "r"(run) is also projected to token "a" with flow = 0.167
AMR node "c"(cat) is projected to token "cat" ith flow 0.3333
AMR node "c"(cat) is also projected to token "a" with flow 0.167
```

the word "a" is distributed over two nodes, since 3 words need to be aligned to 2 AMR nodes in the example.

### Important Options

Some options that can be set according to use-case

- `-w2v_uri <string>`: use different word embeddings (FastText, word2vec, etc.). Current default: `glove-wiki-gigaword-100`.
- `-k <int>`: Use an int to specify the maximum contextualization level. E.g., If k=5, a node will receive info from nbs that are up to 5 hops away.
- `-stability_level <int>`: Consider two graphs with a few random parameters. We calculate the expected node distance matrix by sampling parameters `<int>` times. This increases stability of results but also increases runtime. A good trade-off may be 10 or 20. 
- `-communication_direction <string>`: There are three options. Consider (x, :arg0, y), where :arg0 is directed. Option `fromin` means y receives from x. Option `fromout` means that x receives from y. `both` (default value) means `fromin` *and* `fromout`.
- `--edge_to_node_transform`: This flag transforms the edge-labeled AMR graph into an (equivalent) graph with unlabeled edges. E.g., (1, arg1, 2), (1, arg2, 3) --> (1, 4), (1, 5), (4, 2), (5, 3), where 4 has label arg1 and 5 has label arg2.


More options can be checked out:

```
cd src
python wasser_align.py --help
```

## Citation

This repo is a derivative from our work below:

```
@article{10.1162/tacl_a_00435,
    author = {Opitz, Juri and Daza, Angel and Frank, Anette},
    title = "{Weisfeiler-Leman in the Bamboo: Novel AMR Graph Metrics and a Benchmark for AMR Graph Similarity}",
    journal = {Transactions of the Association for Computational Linguistics},
    volume = {9},
    pages = {1425-1441},
    year = {2021},
    month = {12},
    abstract = "{Several metrics have been proposed for assessing the similarity of (abstract) meaning representations (AMRs), but little is known about how they relate to human similarity ratings. Moreover, the current metrics have complementary strengths and weaknesses: Some emphasize speed, while others make the alignment of graph structures explicit, at the price of a costly alignment step.In this work we propose new Weisfeiler-Leman AMR similarity metrics that unify the strengths of previous metrics, while mitigating their weaknesses. Specifically, our new metrics are able to match contextualized substructures and induce n:m alignments between their nodes. Furthermore, we introduce a Benchmark for AMR Metrics based on Overt Objectives (Bamboo), the first benchmark to support empirical assessment of graph-based MR similarity metrics. Bamboo maximizes the interpretability of results by defining multiple overt objectives that range from sentence similarity objectives to stress tests that probe a metric’s robustness against meaning-altering and meaning- preserving graph transformations. We show the benefits of Bamboo by profiling previous metrics and our own metrics. Results indicate that our novel metrics may serve as a strong baseline for future work.}",
    issn = {2307-387X},
    doi = {10.1162/tacl_a_00435},
    url = {https://doi.org/10.1162/tacl\_a\_00435},
    eprint = {https://direct.mit.edu/tacl/article-pdf/doi/10.1162/tacl\_a\_00435/1979290/tacl\_a\_00435.pdf},
}

``` 
