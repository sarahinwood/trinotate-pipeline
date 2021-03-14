trinotate_pipeline
==================

A python3 wrapper for the Trinotate_ pipeline, using snakemake_.

.. image:: http://tomharrop.io/trinotate_pipeline/graph.svg

Requirements
------------

WRONG, USE SIF

The Trinotate_ dependencies must be installed and in ``$PATH``:

* ``TransDecoder``
* ``blastp`` and ``blastx``
* ``hmmscan``
* The ``Trinity`` script ``get_Trinity_gene_to_trans_map.pl``
* ``Trinotate`` and the ``Trinotate`` script ``RnammerTranscriptome.pl`` 
* ``tmhmm``
* ``rnammer``
* ``signalp``
* ``Trinotate``

Detailed installation instructions are available at the Trinotate_ website.

The following ``R`` packages are also required:

* ``data.table``
* ``rtracklayer``

Both may be installed from CRAN or Bioconductor.

Installation
------------

``pip3 install git+git://github.com/tomharrop/trinotate_pipeline.git``

Usage
-----

.. code::

    trinotate_pipeline [-h] --trinity_fasta Trinity.fasta --blast_db
                              uniprot_sprot.pep --hmmer_db Pfam-A.hmm --sqlite_db
                              Trinotate.sqlite --outdir outdir [--threads int]
                              [--targets Trinotate_report] [-n]

    optional arguments:
      -h, --help            show this help message and exit
      --trinity_fasta Trinity.fasta
                            Trinity fasta file to annotate
      --blast_db uniprot_sprot.pep
                            Uniprot database for BLAST searches
      --hmmer_db Pfam-A.hmm
                            Pfam database for use with hmmscan
      --sqlite_db Trinotate.sqlite
                            Boilerplate Trinotate SQLite database
      --outdir outdir       Output directory
      --threads int         Number of threads. Default: 50
      --targets Trinotate_report
                            list of target rules or file names. Default:
                            Trinotate_report
      -n                    Don't run the pipeline. Just print the DAG and quit.

.. _Trinotate: https://trinotate.github.io/
.. _snakemake: https://snakemake.readthedocs.io/en/stable/