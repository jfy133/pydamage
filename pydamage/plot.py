import matplotlib.pyplot as plt
from pydamage.models import geom_mod, unif_mod
import numpy as np
from os import makedirs


class damageplot():
    def __init__(self, damage_dict, wlen, outdir):
        """Class constructor getting damage dict
        
        Args:
            damage_dict(dict): pydamage result dictionary
            wlen(int): window length
            outdir(str): Pydamage result directory
        """        

        self.x = np.array(range(wlen))
        self.y = np.array([damage_dict[i] for i in self.x])
        self.unif_pmin = damage_dict['unif_pmin']
        self.unif_pmin_stdev = damage_dict['unif_pmin_stdev']
        self.geom_p = damage_dict['geom_p']
        self.geom_pmin = damage_dict['geom_pmin']
        self.geom_pmin_stdev = damage_dict['geom_pmin_stdev']
        self.geom_pmax = damage_dict['geom_pmax']
        self.geom_pmax_stdev = damage_dict['geom_pmax_stdev']
        self.contig = damage_dict['reference'] 
        self.outdir = outdir

    def makedir(self):
        self.plotdir = f"{self.outdir}/plots"
        makedirs(self.plotdir, exist_ok=True)

    def draw(self):
        """Draw pydamage plots
        """   

        unif = unif_mod()
        unif_pmin_low = max(unif.bounds[0][0], self.unif_pmin - 2*self.unif_pmin_stdev)
        unif_pmin_high = min(unif.bounds[1][0], self.unif_pmin + 2*self.unif_pmin_stdev)
        y_unif = unif.pmf(self.x, self.unif_pmin)
        y_unif_low = np.maximum(np.zeros(y_unif.shape[0]), unif.pmf(self.x, unif_pmin_low)) 
        y_unif_high = np.minimum(np.ones(y_unif.shape[0]), unif.pmf(self.x, unif_pmin_high))

        geom = geom_mod()
        geom_pmin_low = max(geom.bounds[0][1], self.geom_pmin - 2*self.geom_pmin_stdev)
        geom_pmin_high = min(geom.bounds[1][1], self.geom_pmin + 2*self.geom_pmin_stdev)
        geom_pmax_low = max(geom.bounds[0][2], self.geom_pmax - 2*self.geom_pmax_stdev)
        geom_pmax_high = min(geom.bounds[1][2], self.geom_pmax + 2*self.geom_pmax_stdev)

        y_geom = geom.pmf(self.x, self.geom_p, self.geom_pmin, self.geom_pmax)
        y_geom_low = np.maximum(np.zeros(y_geom.shape[0]), geom.pmf(self.x, self.geom_p, geom_pmin_low, geom_pmax_low))
        y_geom_high = np.minimum(np.ones(y_geom.shape[0]), geom.pmf(self.x, self.geom_p, geom_pmin_high, geom_pmax_high))

        fig = plt.figure(figsize=(12,8), dpi=100, facecolor='w', edgecolor='k')
        ax = fig.add_subplot(111)
        ax.xaxis.labelpad = 20
        ax.yaxis.labelpad = 20

        plt.plot(self.x, self.y,
                'o',
                label='Observed damage')
        # plt.hold(True)

        plt.plot(self.x, y_unif, 
            linewidth=2.5, 
            color = 'IndianRed',
            alpha = 0.8,
            label = 'Uniform model'
        )
        plt.fill_between(self.x, y_unif_low, y_unif_high,
            color='IndianRed',
            alpha=0.1,
            label = 'Uniform CI (2 sigma)'
        )

        plt.plot(self.x, y_geom,
                linewidth=2.5, 
                color = 'DarkOliveGreen',
                alpha = 0.8,
                label = 'Geometric model'
        )
        plt.fill_between(self.x, y_geom_low, y_geom_high,
            color='DarkOliveGreen',
            alpha=0.1,
            label = 'Geometric CI (2 sigma)'
        )
        plt.xlabel("Base from 5'", fontsize=20)
        plt.ylabel("Damage proportion", fontsize=20)
        plt.title(self.contig, fontsize=20)
        ax.legend(fontsize=18)
        ax.set_xticks(self.x)
        plt.savefig(f"{self.plotdir}/{self.contig}.png", dpi=200)