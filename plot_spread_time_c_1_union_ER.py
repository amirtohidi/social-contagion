# plotting the computed spread times in computing_spread_time_c_1_union_ER

from settings import *
from computing_spread_time_c_1_union_ER import models_list, size_of_dataset, NET_SIZE


if __name__ == '__main__':

    assert do_plots and load_computations, "we should be in load_computations and do_plots mode!"

    assert simulation_type == 'c1_union_ER', \
        "we are not in the right simulation_type:" + simulation_type

    spread_time_stds = pickle.load(open(theory_simulation_pickle_address
                                        + simulation_type
                                        + '_spread_times_std.pkl', 'rb'))

    spread_time_avgs = pickle.load(open(theory_simulation_pickle_address
                                        + simulation_type
                                        + '_spread_time_avgs.pkl', 'rb'))

    qs = pickle.load(open(theory_simulation_pickle_address
                          + simulation_type
                          + '_qs.pkl', 'rb'))

    plt.figure()

    for model in models_list:
        model_index = models_list.index(model)
        plt.errorbar(qs[model_index],
                     spread_time_avgs[model_index],
                     yerr=[1.96*s/np.sqrt(size_of_dataset) for s in spread_time_stds[model_index]],
                     linewidth=1.5,
                     label=model)  # $\\sigma_n = 1/2\log(n^{\\alpha})$

    plt.plot(qs[models_list.index('Threshold')],
             [500]*len(qs[models_list.index('Threshold')]),
             color='c', linewidth=1,
             label='$\mathcal{C}_2$ benchmark')

    plt.xscale("log")
    plt.ylabel('time to spread', fontsize=15)
    plt.xlabel('probability of adoptions below threshold $(q)$', fontsize=15)
    # plt.title('\centering Complex Contagion over $\mathcal{C}_{1} \\cup \mathcal{G}_{n,2/n},n = '
    #           + str(NET_SIZE) + '$'
    #           '\\vspace{-10pt}  \\begin{center}  with Sub-threshold Adoptions \\end{center}', fontsize=18)
    plt.legend()
    plt.arrow(0.0074, 500, 0, -500, width=0.0001, head_width=0.0006,
              head_length=50, capstyle='projecting',
              length_includes_head=True, shape='full', joinstyle='round', fc='k', ec='k')
    plt.text(0.008, 10, '$0.0074$',
             fontweight='bold', fontdict=None, withdash=False)
    if show_plots:
        plt.show()
    if save_plots:
        plt.savefig(theory_simulation_output_address + simulation_type + '.png')