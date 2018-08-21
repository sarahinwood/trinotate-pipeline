#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import io
import shutil
import snakemake
import subprocess
import sys
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


# graph printing
def print_graph(snakefile, config, targets, dag_prefix):
    # store old stdout
    stdout = sys.stdout
    # call snakemake api and capture output
    sys.stdout = io.StringIO()
    snakemake.snakemake(
        snakefile,
        config=config,
        targets=targets,
        dryrun=True,
        printdag=True)
    output = sys.stdout.getvalue()
    # restore sys.stdout
    sys.stdout = stdout
    # write output
    if shutil.which('dot'):
        svg_file = '{}.svg'.format(dag_prefix)
        # pipe the output to dot
        with open(svg_file, 'wb') as svg:
            dot_process = subprocess.Popen(
                ['dot', '-Tsvg'],
                stdin=subprocess.PIPE,
                stdout=svg)
        dot_process.communicate(input=output.encode())
    else:
        # just write the dag to file
        dag_file = '{}.dag'.format(dag_prefix)
        with open(dag_file, 'wt') as file:
            file.write(output)


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
        help='Trinity fasta file to annotate',
        metavar='Trinity.fasta',
        type=str,
        dest='trinity_fasta')
    parser.add_argument(
        '--blast_db',
        required=True,
        help='Uniprot database for BLAST searches',
        metavar='uniprot_sprot.pep',
        type=str,
        dest='blast_db')
    parser.add_argument(
        '--hmmer_db',
        required=True,
        help='Pfam database for use with hmmscan',
        metavar='Pfam-A.hmm',
        type=str,
        dest='hmmer_db')
    parser.add_argument(
        '--sqlite_db',
        required=True,
        help='Boilerplate Trinotate SQLite database',
        metavar='Trinotate.sqlite',
        type=str,
        dest='sqlite_db')
    parser.add_argument(
        '--outdir',
        required=True,
        help='Output directory',
        metavar='outdir',
        type=str,
        dest='outdir')
    default_threads = min(os.cpu_count() // 2, 50)
    parser.add_argument(
        '--threads',
        help=('Number of threads. Default: %i' % default_threads),
        metavar='int',
        type=int,
        dest='threads',
        default=default_threads)
    parser.add_argument(
        '--targets',
        help=('list of target rules '
              'or file names. Default: Trinotate_report'),
        metavar='Trinotate_report',
        type=str,
        dest='targets',
        default='Trinotate_report')
    parser.add_argument(
        '-n',
        help='Don\'t run the pipeline. Just print the DAG and quit.',
        dest='dry_run',
        action='store_true')

    args = vars(parser.parse_args())
    args['targets'] = [args['targets']]

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

    # print the dag
    log_directory = os.path.join(args['outdir'], 'logs')
    if not os.path.isdir(log_directory):
        os.makedirs(log_directory)
    print_graph(snakefile,
                args,
                args['targets'],
                os.path.join(log_directory, "graph"))

    # stop here if we're doing a dry run
    if args['dry_run']:
        return

    # check if the required R packages are installed
    for x in r_packages:
        check_r_package(x)

    # run the pipeline
    snakemake.snakemake(
        snakefile=snakefile,
        config=args,
        targets=args['targets'],
        cores=args['threads'],
        lock=False)


if __name__ == '__main__':
    main()
