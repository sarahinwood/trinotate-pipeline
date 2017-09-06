#!/usr/bin/env python3

import shutil
import subprocess
import pathlib


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


###########
# GLOBALS #
###########

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

########
# MAIN #
########

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
