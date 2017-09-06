#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import shutil
import snakemake
import subprocess
import os
import pathlib
from pkg_resources import resource_filename


#############
# FUNCTIONS #
#############


def get_full_path(binary):
    which = shutil.which(binary)
    # check if the binary exists
    if not which:
        raise EnvironmentError(
            'Trinotate dependency {0} not found in $PATH'.format(binary))
    # get the full path to binary
    binary_path = pathlib.Path(which).resolve()
    return str(binary_path)


def check_binary_version(binary_path, version_suffix):
    version_output = subprocess.check_output([binary_path, version_suffix])
    version_string = version_output.decode().rstrip('\n')
    return version_string.replace('\n', ' ')


def check_r_package(r_package):
    r_expression = ('x = "{}";'
                    'if (!requireNamespace(x, quietly = TRUE))'
                    '{{quit(status = "1")}}').format(r_package)
    try:
        subprocess.check_call(['Rscript', '-e', r_expression])
    except:
        raise EnvironmentError(
            'R package {} not installed'.format(r_package))


###########
# GLOBALS #
###########

snakefile = resource_filename(__name__, 'Snakefile')

binary_to_version_suffix = {
    'TransDecoder.LongOrfs': None,
    'TransDecoder.Predict': None,
    'blastp': '-version',
    'blastx': '-version',
    'hmmscan': None,
    'RnammerTranscriptome.pl': None,
    'get_Trinity_gene_to_trans_map.pl': None,
    'tmhmm': None,
    'rnammer': '-v',
    'signalp': '-V',
    'Trinotate': None
}

r_packages = [
    'data.table',
    'rtracklayer'
]

########
# MAIN #
########

def main():
    # parse arguments
    parser = argparse.ArgumentParser(
        prog='trinotate_pipeline')
    parser.add_argument(
        '--trinity_fasta',
        required=True,
        help='Trinity.fasta file to annotate',
        type=str,
        dest='trinity_fasta')
    parser.add_argument(
        '--blast_db',
        required=True,
        help='Uniprot database for BLAST searches, e.g. uniprot_sprot.pep',
        type=str,
        dest='blast_db')
    parser.add_argument(
        '--hmmer_db',
        required=True,
        help='Pfam database for use with hmmscan, e.g. Pfam-A.hmm',
        type=str,
        dest='hmmer_db')
    parser.add_argument(
        '--sqlite_db',
        required=True,
        help='Boilerplate Trinotate SQLite database, e.g. Trinotate.sqlite',
        type=str,
        dest='sqlite_db')
    parser.add_argument(
        '--outdir',
        required=True,
        help='Output directory',
        type=str,
        dest='outdir')
    default_threads = min(os.cpu_count() // 2, 50)
    parser.add_argument(
        '--threads',
        help=('Number of threads. Default: %i' % default_threads),
        type=int,
        dest='threads',
        default=default_threads)
    args = vars(parser.parse_args())

    # get a dict of full paths to pass to snakemake
    binary_to_full_path = {}
    for binary in binary_to_version_suffix:
        # check binary is in path
        full_path = get_full_path(binary)
        binary_to_full_path[binary] = full_path
        # print full path
        pref = 'Using {}'.format(binary)
        print('{:>38}: {}'.format(pref, full_path))
        # if we know how to check the version, do so and print
        if binary_to_version_suffix[binary]:
            suffix = binary_to_version_suffix[binary]
            version = check_binary_version(full_path, suffix)
            pref = '{} version'.format(binary)
            print('{:>38}: {}'.format(pref, version))

    # add the binaries to args
    for binary in binary_to_full_path:
        args[binary] = binary_to_full_path[binary]

    # check if the required R packages are installed
    for x in r_packages:
        check_r_package(x)

    # run the pipeline
    snakemake.snakemake(
        snakefile=snakefile,
        config=args,
        cores=args['threads'],
        timestamp=True)


if __name__ == '__main__':
    main()
