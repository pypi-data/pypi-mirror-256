#!/usr/bin/env python3

import argparse
import os
import re
import subprocess
from datetime import datetime
from shutil import move

import somaticseq.utilities.dockered_pipelines.container_option as container
import somaticseq.utilities.split_Bed_into_equal_regions as split_bed
from somaticseq._version import __version__ as VERSION

timestamp = re.sub(r"[:-]", ".", datetime.now().isoformat())


def run():

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # INPUT FILES and Global Options
    parser.add_argument(
        "-outdir",
        "--output-directory",
        type=str,
        help="Absolute path for output directory",
        default=os.getcwd(),
    )
    parser.add_argument(
        "-somaticDir",
        "--somaticseq-directory",
        type=str,
        help="SomaticSeq directory output name",
        default="SomaticSeq",
    )
    parser.add_argument(
        "-tbam", "--tumor-bam", type=str, help="tumor bam file", required=True
    )
    parser.add_argument(
        "-nbam", "--normal-bam", type=str, help="normal bam file", required=True
    )
    parser.add_argument(
        "-tname",
        "--tumor-sample-name",
        type=str,
        help="tumor sample name",
        default="TUMOR",
    )
    parser.add_argument(
        "-nname",
        "--normal-sample-name",
        type=str,
        help="normal sample name",
        default="NORMAL",
    )
    parser.add_argument(
        "-ref",
        "--genome-reference",
        type=str,
        help="reference fasta file",
        required=True,
    )
    parser.add_argument(
        "-include",
        "--inclusion-region",
        type=str,
        help="inclusion bed file",
    )
    parser.add_argument(
        "-exclude",
        "--exclusion-region",
        type=str,
        help="exclusion bed file",
    )
    parser.add_argument(
        "-dbsnp",
        "--dbsnp-vcf",
        type=str,
        help="dbSNP vcf file, also requires .idx, .gz, and .gz.tbi files",
        required=True,
    )
    parser.add_argument("-cosmic", "--cosmic-vcf", type=str, help="cosmic vcf file")
    parser.add_argument(
        "-minVAF",
        "--minimum-VAF",
        type=float,
        help="minimum VAF to look for",
        default=0.05,
    )
    parser.add_argument(
        "-action",
        "--action",
        type=str,
        help="action for each mutation caller' run script",
        default="echo",
    )
    parser.add_argument(
        "-somaticAct",
        "--somaticseq-action",
        type=str,
        help="action for each somaticseq.cmd",
        default="echo",
    )
    parser.add_argument(
        "-tech",
        "--container-tech",
        type=str,
        help="docker or singularity",
        default="docker",
        choices=("ada", "xgboost", "ada.R"),
    )
    parser.add_argument(
        "-dockerargs",
        "--extra-docker-options",
        type=str,
        help="extra arguments to pass onto docker run",
        default="",
    )

    # RUN TOOLS
    parser.add_argument(
        "-mutect2", "--run-mutect2", action="store_true", help="Run MuTect2"
    )
    parser.add_argument(
        "-varscan2", "--run-varscan2", action="store_true", help="Run VarScan2"
    )
    parser.add_argument(
        "-jsm", "--run-jointsnvmix2", action="store_true", help="Run JointSNVMix2"
    )
    parser.add_argument(
        "-sniper", "--run-somaticsniper", action="store_true", help="Run SomaticSniper"
    )
    parser.add_argument(
        "-vardict", "--run-vardict", action="store_true", help="Run VarDict"
    )
    parser.add_argument("-muse", "--run-muse", action="store_true", help="Run MuSE")
    parser.add_argument(
        "-lofreq", "--run-lofreq", action="store_true", help="Run LoFreq"
    )
    parser.add_argument(
        "-scalpel", "--run-scalpel", action="store_true", help="Run Scalpel"
    )
    parser.add_argument(
        "-strelka2", "--run-strelka2", action="store_true", help="Run Strelka2"
    )
    parser.add_argument(
        "-somaticseq", "--run-somaticseq", action="store_true", help="Run SomaticSeq"
    )

    ## SomaticSeq Train or Classify
    parser.add_argument(
        "-train",
        "--train-somaticseq",
        action="store_true",
        help="SomaticSeq training mode for classifiers",
    )
    parser.add_argument("-trueSnv", "--truth-snv", type=str, help="VCF of true hits")
    parser.add_argument(
        "-trueIndel", "--truth-indel", type=str, help="VCF of true hits"
    )
    parser.add_argument(
        "-snvClassifier", "--snv-classifier", type=str, help="action for each .cmd"
    )
    parser.add_argument(
        "-indelClassifier",
        "--indel-classifier",
        type=str,
        help="action for each somaticseq.cmd",
    )

    # EXTRA ARGUMENTS TO PASS ONTO TOOLS
    parser.add_argument(
        "-exome",
        "--exome-setting",
        action="store_true",
        help="Invokes exome setting in Strelka2 and MuSE",
    )

    parser.add_argument(
        "--mutect2-arguments", type=str, help="extra parameters for Mutect2", default=""
    )
    parser.add_argument(
        "--mutect2-filter-arguments",
        type=str,
        help="extra parameters for FilterMutectCalls step",
        default="",
    )

    parser.add_argument(
        "--varscan-arguments",
        type=str,
        help="extra parameters for VarScan2",
        default="",
    )
    parser.add_argument(
        "--varscan-pileup-arguments",
        type=str,
        help="extra parameters for mpileup used for VarScan2",
        default="",
    )

    parser.add_argument(
        "--jsm-train-arguments",
        type=str,
        help="extra parameters for JointSNVMix2 train",
        default="",
    )
    parser.add_argument(
        "--jsm-classify-arguments",
        type=str,
        help="extra parameters for JointSNVMix2 classify",
        default="",
    )

    parser.add_argument(
        "--somaticsniper-arguments",
        type=str,
        help="extra parameters for SomaticSniper",
        default="",
    )

    parser.add_argument(
        "--vardict-arguments", type=str, help="extra parameters for VarDict", default=""
    )

    parser.add_argument(
        "--muse-arguments", type=str, help="extra parameters", default=""
    )

    parser.add_argument(
        "--lofreq-arguments", type=str, help="extra parameters for LoFreq", default=""
    )

    parser.add_argument(
        "--scalpel-discovery-arguments",
        type=str,
        help="extra parameters for Scalpel discovery",
        default="",
    )
    parser.add_argument(
        "--scalpel-export-arguments",
        type=str,
        help="extra parameters for Scalpel export",
        default="",
    )
    parser.add_argument(
        "--scalpel-two-pass",
        action="store_true",
        help="Invokes two-pass setting in scalpel",
    )

    parser.add_argument(
        "--strelka-config-arguments",
        type=str,
        help="extra parameters for Strelka2 config",
        default="",
    )
    parser.add_argument(
        "--strelka-run-arguments",
        type=str,
        help="extra parameters for Strelka2 run",
        default="",
    )

    parser.add_argument(
        "--somaticseq-arguments",
        type=str,
        help="extra parameters for SomaticSeq",
        default="",
    )
    parser.add_argument(
        "--somaticseq-algorithm",
        type=str,
        help="either ada or xgboost",
        default="xgboost",
    )

    parser.add_argument(
        "-nt",
        "--threads",
        type=int,
        help="Split the input regions into this many threads",
        default=1,
    )

    # Parse the arguments:
    args = parser.parse_args()
    workflowArguments = vars(args)

    workflowArguments["reference_dict"] = (
        re.sub(r"\.[a-zA-Z]+$", "", workflowArguments["genome_reference"]) + ".dict"
    )

    return args, workflowArguments


def run_SomaticSeq(input_parameters, tech="docker"):

    DEFAULT_PARAMS = {
        "MEM": "4G",
        "genome_reference": None,
        "inclusion_region": None,
        "exclusion_region": None,
        "output_directory": os.curdir,
        "somaticseq_directory": "SomaticSeq",
        "action": "echo",
        "dbsnp_vcf": None,
        "cosmic_vcf": None,
        "snv_classifier": None,
        "indel_classifier": None,
        "truth_snv": None,
        "truth_indel": None,
        "somaticseq_arguments": "",
        "train_somaticseq": False,
        "somaticseq_algorithm": "xgboost",
    }

    for param_i in DEFAULT_PARAMS:
        if param_i not in input_parameters:
            input_parameters[param_i] = DEFAULT_PARAMS[param_i]

    all_paths = []
    for path_i in (
        input_parameters["normal_bam"],
        input_parameters["tumor_bam"],
        input_parameters["genome_reference"],
        input_parameters["output_directory"],
        input_parameters["inclusion_region"],
        input_parameters["exclusion_region"],
        input_parameters["dbsnp_vcf"],
        input_parameters["cosmic_vcf"],
        input_parameters["snv_classifier"],
        input_parameters["indel_classifier"],
        input_parameters["truth_snv"],
        input_parameters["truth_indel"],
    ):
        if path_i:
            all_paths.append(path_i)

    container_line, fileDict = container.container_params(
        f"lethalfang/somaticseq:{VERSION}",
        tech=tech,
        files=all_paths,
        extra_args=input_parameters["extra_docker_options"],
    )

    # Mounted paths for all the input files and output directory:
    mounted_genome_reference = fileDict[input_parameters["genome_reference"]][
        "mount_path"
    ]
    mounted_tumor_bam = fileDict[input_parameters["tumor_bam"]]["mount_path"]
    mounted_normal_bam = fileDict[input_parameters["normal_bam"]]["mount_path"]
    mounted_outdir = fileDict[input_parameters["output_directory"]]["mount_path"]

    outdir = os.path.join(
        input_parameters["output_directory"], input_parameters["somaticseq_directory"]
    )
    logdir = os.path.join(outdir, "logs")
    outfile = os.path.join(logdir, input_parameters["script"])

    mutect2 = "{}/MuTect2.vcf".format(mounted_outdir)
    varscan_snv = "{}/VarScan2.snp.vcf".format(mounted_outdir)
    varscan_indel = "{}/VarScan2.indel.vcf".format(mounted_outdir)
    jsm2 = "{}/JointSNVMix2.vcf".format(mounted_outdir)
    sniper = "{}/SomaticSniper.vcf".format(mounted_outdir)
    vardict = "{}/VarDict.vcf".format(mounted_outdir)
    muse = "{}/MuSE.vcf".format(mounted_outdir)
    lofreq_snv = "{}/LoFreq.somatic_final.snvs.vcf.gz".format(mounted_outdir)
    lofreq_indel = "{}/LoFreq.somatic_final.indels.vcf.gz".format(mounted_outdir)
    scalpel = "{}/Scalpel.vcf".format(mounted_outdir)
    strelka_snv = "{}/Strelka/results/variants/somatic.snvs.vcf.gz".format(
        mounted_outdir
    )
    strelka_indel = "{}/Strelka/results/variants/somatic.indels.vcf.gz".format(
        mounted_outdir
    )

    os.makedirs(logdir, exist_ok=True)
    with open(outfile, "w") as out:

        out.write("#!/bin/bash\n\n")

        out.write(f"#$ -o {logdir}\n")
        out.write(f"#$ -e {logdir}\n")
        out.write("#$ -S /bin/bash\n")
        out.write("#$ -l h_vmem={}\n".format(input_parameters["MEM"]))
        out.write("set -e\n\n")

        out.write('echo -e "Start at `date +"%Y/%m/%d %H:%M:%S"`" 1>&2\n\n')

        # out.write( 'docker pull lethalfang/somaticseq:{} \n\n'.format(VERSION) )

        out.write(f"{container_line} \\\n")
        out.write("run_somaticseq.py \\\n")

        if input_parameters["train_somaticseq"] and input_parameters["threads"] == 1:
            out.write(
                "--somaticseq-train --algorithm {} \\\n".format(
                    input_parameters["somaticseq_algorithm"]
                )
            )

        out.write(
            "--output-directory {} \\\n".format(
                os.path.join(mounted_outdir, input_parameters["somaticseq_directory"])
            )
        )
        out.write("--genome-reference {} \\\n".format(mounted_genome_reference))

        if input_parameters["inclusion_region"]:
            mounted_inclusion = fileDict[input_parameters["inclusion_region"]][
                "mount_path"
            ]
            out.write("--inclusion-region {} \\\n".format(mounted_inclusion))

        if input_parameters["exclusion_region"]:
            mounted_exclusion = fileDict[input_parameters["exclusion_region"]][
                "mount_path"
            ]
            out.write("--exclusion-region {} \\\n".format(mounted_exclusion))

        if input_parameters["cosmic_vcf"]:
            mounted_cosmic = fileDict[input_parameters["cosmic_vcf"]]["mount_path"]
            out.write("--cosmic-vcf {} \\\n".format(mounted_cosmic))

        if input_parameters["dbsnp_vcf"]:
            mounted_dbsnp = fileDict[input_parameters["dbsnp_vcf"]]["mount_path"]
            out.write("--dbsnp-vcf {} \\\n".format(mounted_dbsnp))

        if input_parameters["snv_classifier"] or input_parameters["indel_classifier"]:
            out.write(
                "--algorithm {} \\\n".format(input_parameters["somaticseq_algorithm"])
            )

            if input_parameters["snv_classifier"]:
                out.write(
                    "--classifier-snv {} \\\n".format(
                        fileDict[input_parameters["snv_classifier"]]["mount_path"]
                    )
                )

            if input_parameters["indel_classifier"]:
                out.write(
                    "--classifier-indel {} \\\n".format(
                        fileDict[input_parameters["indel_classifier"]]["mount_path"]
                    )
                )

        if input_parameters["truth_snv"]:
            out.write(
                "--truth-snv {} \\\n".format(
                    fileDict[input_parameters["truth_snv"]]["mount_path"]
                )
            )

        if input_parameters["truth_indel"]:
            out.write(
                "--truth-indel {} \\\n".format(
                    fileDict[input_parameters["truth_indel"]]["mount_path"]
                )
            )

        if input_parameters["somaticseq_algorithm"]:
            out.write(
                "--algorithm {} \\\n".format(input_parameters["somaticseq_algorithm"])
            )

        if input_parameters["somaticseq_arguments"]:
            out.write("{} \\\n".format(input_parameters["somaticseq_arguments"]))

        out.write("paired \\\n")
        out.write("--tumor-bam-file {} \\\n".format(mounted_tumor_bam))
        out.write("--normal-bam-file {} \\\n".format(mounted_normal_bam))

        if input_parameters["run_mutect2"]:
            out.write("--mutect2-vcf {} \\\n".format(mutect2))

        if input_parameters["run_varscan2"]:
            out.write("--varscan-snv {} \\\n".format(varscan_snv))
            out.write("--varscan-indel {} \\\n".format(varscan_indel))

        if input_parameters["run_jointsnvmix2"]:
            out.write("--jsm-vcf {} \\\n".format(jsm2))

        if input_parameters["run_somaticsniper"]:
            out.write("--somaticsniper-vcf {} \\\n".format(sniper))

        if input_parameters["run_vardict"]:
            out.write("--vardict-vcf {} \\\n".format(vardict))

        if input_parameters["run_muse"]:
            out.write("--muse-vcf {} \\\n".format(muse))

        if input_parameters["run_lofreq"]:
            out.write("--lofreq-snv {} \\\n".format(lofreq_snv))
            out.write("--lofreq-indel {} \\\n".format(lofreq_indel))

        if input_parameters["run_scalpel"]:
            out.write("--scalpel-vcf {} \\\n".format(scalpel))

        if input_parameters["run_strelka2"]:
            out.write("--strelka-snv {} \\\n".format(strelka_snv))
            out.write("--strelka-indel {}\n".format(strelka_indel))

        out.write('\necho -e "Done at `date +"%Y/%m/%d %H:%M:%S"`" 1>&2\n')

    # "Run" the script that was generated
    command_line = "{} {}".format(input_parameters["action"], outfile)
    returnCode = subprocess.call(command_line, shell=True)

    return outfile


def merge_results(input_parameters, tech="docker"):

    DEFAULT_PARAMS = {
        "MEM": "4G",
        "output_directory": os.curdir,
        "somaticseq_directory": "SomaticSeq",
        "action": "echo",
        "script": "mergeResults.{}.cmd".format(timestamp),
        "snv_classifier": None,
        "indel_classifier": None,
        "truth_snv": None,
        "truth_indel": None,
        "somaticseq_arguments": "",
        "train_somaticseq": False,
        "somaticseq_algorithm": "xgboost",
    }
    for param_i in DEFAULT_PARAMS:
        if param_i not in input_parameters:
            input_parameters[param_i] = DEFAULT_PARAMS[param_i]

    all_paths = []
    for path_i in (
        input_parameters["genome_reference"],
        input_parameters["output_directory"],
        input_parameters["snv_classifier"],
        input_parameters["indel_classifier"],
        input_parameters["truth_snv"],
        input_parameters["truth_indel"],
    ):
        if path_i:
            all_paths.append(path_i)

    container_line, fileDict = container.container_params(
        f"lethalfang/somaticseq:{VERSION}",
        tech=tech,
        files=all_paths,
        extra_args=input_parameters["extra_docker_options"],
    )

    # Mounted paths for all the input files and output directory:
    mounted_outdir = fileDict[input_parameters["output_directory"]]["mount_path"]
    prjdir = input_parameters["output_directory"]
    logdir = os.path.join(prjdir, "logs")
    outfile = os.path.join(logdir, input_parameters["script"])
    mutect2 = mounted_outdir + "/{}/MuTect2.vcf"
    varscan_snv = mounted_outdir + "/{}/VarScan2.snp.vcf"
    varscan_indel = mounted_outdir + "/{}/VarScan2.indel.vcf"
    vardict = mounted_outdir + "/{}/VarDict.vcf"
    muse = mounted_outdir + "/{}/MuSE.vcf"
    lofreq_snv = mounted_outdir + "/{}/LoFreq.somatic_final.snvs.vcf.gz"
    lofreq_indel = mounted_outdir + "/{}/LoFreq.somatic_final.indels.vcf.gz"
    scalpel = mounted_outdir + "/{}/Scalpel.vcf"
    strelka_snv = mounted_outdir + "/{}/Strelka/results/variants/somatic.snvs.vcf.gz"
    strelka_indel = (
        mounted_outdir + "/{}/Strelka/results/variants/somatic.indels.vcf.gz"
    )
    somaticdir = input_parameters["somaticseq_directory"]
    os.makedirs(logdir, exist_ok=True)

    with open(outfile, "w") as out:

        out.write("#!/bin/bash\n\n")
        out.write(f"#$ -o {logdir}\n")
        out.write(f"#$ -e {logdir}\n")
        out.write("#$ -S /bin/bash\n")
        out.write("#$ -l h_vmem={}\n".format(input_parameters["MEM"]))
        out.write("set -e\n\n")
        out.write('echo -e "Start at `date +"%Y/%m/%d %H:%M:%S"`" 1>&2\n\n')

        if input_parameters["run_mutect2"]:
            out.write(f"{container_line} \\\n")
            out.write("concat.py --bgzip-output -infiles \\\n")

            for i in range(1, input_parameters["threads"] + 1):
                out.write(mutect2.format(i) + " ")

            out.write("\\\n")
            out.write("-outfile {}/MuTect2.vcf\n\n".format(mounted_outdir))

        if input_parameters["run_varscan2"]:
            out.write(f"{container_line} \\\n")
            out.write("concat.py --bgzip-output -infiles \\\n")

            for i in range(1, input_parameters["threads"] + 1):
                out.write(varscan_snv.format(i) + " ")

            out.write("\\\n")
            out.write("-outfile {}/VarScan2.snv.vcf\n\n".format(mounted_outdir))
            out.write(f"{container_line} \\\n")
            out.write("concat.py --bgzip-output -infiles \\\n")

            for i in range(1, input_parameters["threads"] + 1):
                out.write(varscan_indel.format(i) + " ")

            out.write("\\\n")
            out.write("-outfile {}/VarScan2.indel.vcf\n\n".format(mounted_outdir))

        if input_parameters["run_vardict"]:
            out.write(f"{container_line} \\\n")
            out.write("concat.py --bgzip-output -infiles \\\n")

            for i in range(1, input_parameters["threads"] + 1):
                out.write(vardict.format(i) + " ")

            out.write("\\\n")
            out.write("-outfile {}/VarDict.vcf\n\n".format(mounted_outdir))

        if input_parameters["run_muse"]:
            out.write(f"{container_line} \\\n")
            out.write("concat.py --bgzip-output -infiles \\\n")

            for i in range(1, input_parameters["threads"] + 1):
                out.write(muse.format(i) + " ")

            out.write("\\\n")
            out.write("-outfile {}/MuSE.vcf\n\n".format(mounted_outdir))

        if input_parameters["run_lofreq"]:
            out.write(f"{container_line} \\\n")
            out.write("concat.py --bgzip-output -infiles \\\n")

            for i in range(1, input_parameters["threads"] + 1):
                out.write(lofreq_snv.format(i) + " ")

            out.write("\\\n")
            out.write("-outfile {}/LoFreq.snv.vcf\n\n".format(mounted_outdir))
            out.write(f"{container_line} \\\n")
            out.write("concat.py --bgzip-output -infiles \\\n")

            for i in range(1, input_parameters["threads"] + 1):
                out.write(lofreq_indel.format(i) + " ")

            out.write("\\\n")
            out.write("-outfile {}/LoFreq.indel.vcf\n\n".format(mounted_outdir))

        if input_parameters["run_scalpel"]:
            out.write(f"{container_line} \\\n")
            out.write("concat.py --bgzip-output -infiles \\\n")

            for i in range(1, input_parameters["threads"] + 1):
                out.write(scalpel.format(i) + " ")

            out.write("\\\n")
            out.write("-outfile {}/Scalpel.vcf\n\n".format(mounted_outdir))

        if input_parameters["run_strelka2"]:
            out.write(f"{container_line} \\\n")
            out.write("concat.py --bgzip-output -infiles \\\n")

            for i in range(1, input_parameters["threads"] + 1):
                out.write(strelka_snv.format(i) + " ")

            out.write("\\\n")
            out.write("-outfile {}/Strelka.snv.vcf\n\n".format(mounted_outdir))

            out.write(f"{container_line} \\\n")
            out.write("concat.py --bgzip-output -infiles \\\n")

            for i in range(1, input_parameters["threads"] + 1):
                out.write(strelka_indel.format(i) + " ")

            out.write("\\\n")
            out.write("-outfile {}/Strelka.indel.vcf\n\n".format(mounted_outdir))

        ###### SomaticSeq #####
        if input_parameters["run_somaticseq"]:

            # Ensemble.sSNV.tsv
            out.write(f"{container_line} \\\n")
            out.write("concat.py -infiles \\\n")

            for i in range(1, input_parameters["threads"] + 1):
                out.write(
                    "{}/{}/{}/Ensemble.sSNV.tsv".format(mounted_outdir, i, somaticdir)
                    + " "
                )
            out.write("\\\n")
            out.write("-outfile {}/Ensemble.sSNV.tsv\n\n".format(mounted_outdir))

            # Ensemble.sINDEL.tsv
            out.write(f"{container_line} \\\n")
            out.write("concat.py -infiles \\\n")

            for i in range(1, input_parameters["threads"] + 1):
                out.write(
                    "{}/{}/{}/Ensemble.sINDEL.tsv".format(mounted_outdir, i, somaticdir)
                    + " "
                )

            out.write("\\\n")
            out.write("-outfile {}/Ensemble.sINDEL.tsv\n\n".format(mounted_outdir))

            # If asked to create classifier, do it here when TSV files are combined
            if input_parameters["train_somaticseq"] and input_parameters["truth_snv"]:
                out.write(f"{container_line} \\\n")
                if input_parameters["somaticseq_algorithm"] == "ada":
                    out.write(
                        "ada_model_builder_ntChange.R {}/Ensemble.sSNV.tsv\n\n".format(
                            mounted_outdir
                        )
                    )
                else:
                    out.write(
                        "somatic_xgboost.py train -threads {} -tsvs {}/Ensemble.sSNV.tsv\n\n".format(
                            input_parameters["threads"], mounted_outdir
                        )
                    )

            if input_parameters["train_somaticseq"] and input_parameters["truth_indel"]:
                out.write(f"{container_line} \\\n")
                if input_parameters["somaticseq_algorithm"] == "ada":
                    out.write(
                        "ada_model_builder_ntChange.R {}/Ensemble.sINDEL.tsv\n\n".format(
                            mounted_outdir
                        )
                    )
                else:
                    out.write(
                        "somatic_xgboost.py train -threads {} -tsvs {}/Ensemble.sINDEL.tsv\n\n".format(
                            input_parameters["threads"], mounted_outdir
                        )
                    )

            # If in prediction mode, combine SSeq.Classified.sSNV.vcf, else Consensus.sSNV.vcf
            if input_parameters["snv_classifier"]:

                out.write(f"{container_line} \\\n")
                out.write("concat.py --bgzip-output -infiles \\\n")

                for i in range(1, input_parameters["threads"] + 1):
                    out.write(
                        "{}/{}/{}/SSeq.Classified.sSNV.vcf".format(
                            mounted_outdir, i, somaticdir
                        )
                        + " "
                    )

                out.write("\\\n")
                out.write(
                    "-outfile {}/SSeq.Classified.sSNV.vcf\n\n".format(mounted_outdir)
                )
                # SSeq.Classified.sSNV.tsv
                out.write(f"{container_line} \\\n")
                out.write("concat.py --bgzip-output -infiles \\\n")

                for i in range(1, input_parameters["threads"] + 1):
                    out.write(
                        "{}/{}/{}/SSeq.Classified.sSNV.tsv".format(
                            mounted_outdir, i, somaticdir
                        )
                        + " "
                    )
                out.write("\\\n")
                out.write(
                    "-outfile {}/SSeq.Classified.sSNV.tsv\n\n".format(mounted_outdir)
                )
            # Consensus mode: Consensus.sSNV.vcf
            else:
                out.write(f"{container_line} \\\n")
                out.write("concat.py --bgzip-output -infiles \\\n")

                for i in range(1, input_parameters["threads"] + 1):
                    out.write(
                        "{}/{}/{}/Consensus.sSNV.vcf".format(
                            mounted_outdir, i, somaticdir
                        )
                        + " "
                    )
                out.write("\\\n")
                out.write("-outfile {}/Consensus.sSNV.vcf\n\n".format(mounted_outdir))

            # If in prediction mode, combine SSeq.Classified.sINDEL.vcf, else Consensus.sINDEL.vcf
            if input_parameters["indel_classifier"]:

                out.write(f"{container_line} \\\n")
                out.write("concat.py --bgzip-output -infiles \\\n")
                for i in range(1, input_parameters["threads"] + 1):
                    out.write(
                        "{}/{}/{}/SSeq.Classified.sINDEL.vcf".format(
                            mounted_outdir, i, somaticdir
                        )
                        + " "
                    )
                out.write("\\\n")
                out.write(
                    "-outfile {}/SSeq.Classified.sINDEL.vcf\n\n".format(mounted_outdir)
                )
                # SSeq.Classified.sINDEL.tsv
                out.write(f"{container_line} \\\n")
                out.write("concat.py --bgzip-output -infiles \\\n")

                for i in range(1, input_parameters["threads"] + 1):
                    out.write(
                        "{}/{}/{}/SSeq.Classified.sINDEL.tsv".format(
                            mounted_outdir, i, somaticdir
                        )
                        + " "
                    )
                out.write("\\\n")
                out.write(
                    "-outfile {}/SSeq.Classified.sINDEL.tsv\n\n".format(mounted_outdir)
                )

            # Consensus mode: Consensus.sINDEL.vcf
            else:
                out.write(f"{container_line} \\\n")
                out.write("concat.py --bgzip-output -infiles \\\n")

                for i in range(1, input_parameters["threads"] + 1):
                    out.write(
                        "{}/{}/{}/Consensus.sINDEL.vcf".format(
                            mounted_outdir, i, somaticdir
                        )
                        + " "
                    )
                out.write("\\\n")
                out.write("-outfile {}/Consensus.sINDEL.vcf\n\n".format(mounted_outdir))

        out.write('\necho -e "Done at `date +"%Y/%m/%d %H:%M:%S"`" 1>&2\n')

    command_line = "{} {}".format(input_parameters["action"], outfile)
    returnCode = subprocess.call(command_line, shell=True)

    return outfile
