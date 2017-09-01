#!/usr/bin/env python3

import os

#data file
trinity_fasta="data/Trinity.fasta"

#results files
transdecoder_results="output/transdecoder/Trinity.fasta.transdecoder.pep"
blastp_results="output/blastp/blastp.outfmt6"
blast_db="bin/trinotate/db/uniprot_sprot.pep"
blastx_results="output/blastx/blastx.outfmt6"
hmmer_results="output/hmmer/TrinotatePFAM.out"
rnammer_results="output/rnammer/Trinity.fasta.rnammer.gff"
tmhmm_results="output/tmhmm/tmhmm.out"
renamed_transdecoder="output/signalp/renamed_transdecoder_results.fasta"
signalp_results="output/signalp/signalp.out"
signalp_gff="output/signalp/signalp.gff"
signalp_renamed_gff="output/signalp/renamed_signalp_gff.gff2"
trinotate_database="output/trinotate/Trinotate.sqlite"
trinity_gene_trans_map="output/trinotate/Trinity.fasta.gene_trans_map"
trinotate_annotation_report="output/trinotate/trinotate_annotation_report.txt"

#intermediate files
transdecoder_directory=os.path.split(transdecoder_results)[0]
log_directory="output/logs"

#rules
rule run_transdecoder:
	input:
		trinity_fasta=trinity_fasta
	output:
		transdecoder_results,
		td_fasta=temp(os.path.join(transdecoder_directory,'Trinity.fasta')),
		w_dir=transdecoder_directory
	threads:
		1
	shell:
		'cp {input.trinity_fasta} {output.td_fasta} ; '
		'cd {output.w_dir} ; '
		'TransDecoder.LongOrfs -t Trinity.fasta -S ; '
		'TransDecoder.Predict -t Trinity.fasta'

rule run_blastp:
	input:
		transdecoder_results=transdecoder_results,
		db=blast_db
	output:
		blastp_results
	threads:
		50
	log:
		os.path.join(log_directory, 'blastp.log')
	shell:
		'blastp '
		'-db {input.db} '
		'-query {input.transdecoder_results} '
		'-num_threads {threads} '
		'-max_target_seqs 1 '
		'-outfmt 6 > {output} '
		'2> {log}'

rule run_blastx:
	input:
		trinity_fasta=trinity_fasta,
		db=blast_db
	output:
		blastx_results
	threads:
		50
	log:
		os.path.join(log_directory, 'blastx.log')
	shell:
		'blastx '
		'-db {input.db} '
		'-query {input.trinity_fasta} '
		'-num_threads {threads} '
		'-max_target_seqs 1 '
		'-outfmt 6 > {output} '
		'2> {log}'

rule run_hmmer:
	input:
		transdecoder_results
	output:
		touch(hmmer_results)
	shell:
		'printf "input:\t%s\noutput\t%s\n" {input} {output}'

rule run_rnammer:
	input:
		trinity_fasta
	output:
		touch(rnammer_results)
	shell:
		'printf "input:\t%s\noutput\t%s\n" {input} {output}'

rule run_tmhmm:
	input:
		transdecoder_results
	output:
		touch(tmhmm_results)
	shell:
		'printf "input:\t%s\noutput\t%s\n" {input} {output}'

rule run_rename_transdecoder:
	input:
		transdecoder_results
	output:
		touch(renamed_transdecoder)
	shell:
		'printf "input:\t%s\noutput\t%s\n" {input} {output}'

rule run_signalp:
	input:
		renamed_transdecoder
	output:
		touch(signalp_results),
		touch(signalp_gff)
	shell:
		'printf "input:\t%s\noutput\t%s\n" {input} {output}'

rule run_rename_signalp_gff:
	input:
		signalp_gff
	output:
		touch(signalp_renamed_gff)
	shell:
		'printf "input:\t%s\noutput\t%s\n" {input} {output}'

rule run_gene_to_trans_map:
	input:
		trinity_fasta
	output:
		touch(trinity_gene_trans_map)
	shell:
		'printf "input:\t%s\noutput\t%s\n" {input} {output}'

rule run_load_trinotate_results:
	input:
		trinity_fasta,
		trinity_gene_trans_map,
		transdecoder_results,
		blastx_results,
		blastp_results,
		hmmer_results,
		signalp_renamed_gff,
		tmhmm_results,
		rnammer_results
	output:
		touch(trinotate_database)
	shell:
		'printf "input:\t%s\noutput\t%s\n" {input} {output}'

rule run_trinotate_report:
	input:
		trinotate_database
	output:
		touch(trinotate_annotation_report)
	shell:
		'printf "input:\t%s\noutput\t%s\n" {input} {output}'









