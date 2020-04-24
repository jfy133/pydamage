#!/usr/bin/env python3

import pysam
from pydamage.parse_ct import ct_al
from pydamage.vuong import vuong_closeness
from pydamage import models
import numpy as np

class al_to_ct():

    def __init__(self, reference, al_handle):
        """Constructor of the class

        Args:
            al_handle(pysam.AlignmentFile)
            mode (str): opening mode (r, rb, rc)
            reference (string): a reference from the indexed bam file 
        """
        self.alignments = al_handle.fetch(reference)

        # self.alignments = al_file

    # def __repr__(self):
    #     return(f"Reference {reference}")

    def get_ct(self, wlen, show_al):
        """Compute CtoT substitutions

        Args:
            wlen (int): window length
            show_al(bool): print alignments representations
        """

        all_ct = []
        for al in self.alignments:
            if al.is_reverse == False and al.is_unmapped == False:
                cigar = al.cigartuples
                ref = al.get_reference_sequence()
                quer = al.query_sequence

                all_ct += ct_al(reference=ref,
                                query=quer,
                                cigartuple=cigar,
                                wlen=wlen,
                                show_al=show_al)
        return(all_ct)


def avg_coverage(pysam_cov):
    A = np.array(pysam_cov[0], dtype=int)
    C = np.array(pysam_cov[1], dtype=int)
    G = np.array(pysam_cov[2], dtype=int)
    T = np.array(pysam_cov[3], dtype=int)
    cov_all_bases = A + C + G + T
    cov = np.mean(cov_all_bases)
    return(cov)

def test_ct(ref, bam, mode, wlen, show_al, min_al, min_cov, process, verbose):
    al_handle = pysam.AlignmentFile(bam, mode=mode, threads=process)
    try:
        cov = avg_coverage(al_handle.count_coverage(contig=ref))
        nb_reads_aligned = al_handle.count(contig=ref)
        
        if nb_reads_aligned >= min_al or cov >= min_cov:
            al = al_to_ct(reference=ref, al_handle=al_handle)
            ct_data = al.get_ct(wlen=wlen, show_al=show_al)
            if ct_data:
                model_A = models.unif_mod()
                model_B = models.geom_mod()
                test_res = vuong_closeness(ref=ref, 
                                           model_A=model_A, 
                                           model_B=model_B, 
                                           data=ct_data, 
                                           wlen=wlen, 
                                           verbose=verbose)
                test_res['reference'] = ref
                test_res['nb_reads_aligned'] = nb_reads_aligned
                return(test_res)
        else:
            pass
    except ValueError:
        print(f"Could not fit a model for {ref} because of too few reads aligned ({nb_reads_aligned})")
        pass
