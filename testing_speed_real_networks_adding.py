# Comparing the rate of contagion in the original and network with added edges.

assert False, \
    "This file is obsolete use measuring_spread_time_real_networks.py ," \
    " dump_spreading_data.py, and plot_spread_time_histograms.py instead."

from models import *

size_of_dataset = 200

percent_more_edges_list = [5, 10, 15, 20, 25]

if __name__ == '__main__':

    if data_dump:
        try:
            df = pd.read_csv(output_directory_address + network_group + 'spreading_data_dump.csv')
        except FileNotFoundError:
            df = pd.DataFrame(dtype='float')
            print('New ' + network_group + 'spreading_data_dump file will be generated.')

    for percent_more_edges in percent_more_edges_list:
        for network_id in network_id_list:

            print(network_id)

            #  load in the network and extract preliminary data

            fh = open(edgelist_directory_address + network_group + network_id + '.txt', 'rb')

            G = NX.read_edgelist(fh, delimiter=DELIMITER)

            print('original size ', len(G.nodes()))

            #  get the largest connected component:
            if not NX.is_connected(G):
                G = max(NX.connected_component_subgraphs(G), key=len)
                print('largest connected component extracted with size ', len(G.nodes()))

            #  remove self loops:
            if len(list(G.selfloop_edges())) > 0:
                print('warning the graph has ' + str(len(list(G.selfloop_edges()))) + ' self-loops that will be removed')
                print('number of edges before self loop removal: ', G.size())
                G.remove_edges_from(G.selfloop_edges())
                print('number of edges before self loop removal: ', G.size())

            network_size = NX.number_of_nodes(G)

            # number_edges = G.number_of_edges()

            # original_average_clustering = NX.average_clustering(G)

            if do_computations:

                initial_seeds = 2

                params_add_random = {
                    'network': G,
                    'size': network_size,
                    'add_edges': True,
                    'edge_addition_mode': 'random',
                    'number_of_edges_to_be_added': int(np.floor(0.01*percent_more_edges * G.number_of_edges())),
                    # 'initial_states': [1] * initial_seeds + [0] * (network_size - initial_seeds),
                    'initialization_mode': 'fixed_number_initial_infection',
                    'initial_infection_number': number_initial_seeds,
                    'delta': 0.0000000000000001,  # recoveryProb,  # np.random.beta(5, 2, None), # recovery probability
                    'fixed_prob_high': fixed_prob_high,
                    'fixed_prob': fixed_prob_low,
                    'alpha': alpha,
                    'gamma': gamma,
                    'theta': 2,
                    'rewire': False,
                }

                dynamics_add_random = DeterministicLinear(params_add_random)

                speed_add_random, std_add_random, _, _, speed_samples_add_random = \
                    dynamics_add_random.avg_speed_of_spread(
                        dataset_size=size_of_dataset,
                        cap=0.9,
                        mode='max')

                print(speed_add_random, std_add_random)

                print(speed_samples_add_random)

                params_add_triad = {
                    'network': G,
                    'size': network_size,
                    'add_edges': True,
                    'edge_addition_mode': 'triadic_closures',
                    'number_of_edges_to_be_added': int(np.floor(0.01 * percent_more_edges * G.number_of_edges())),
                    # 'initial_states': [1] * initial_seeds + [0] * (network_size - initial_seeds),
                    'initialization_mode': 'fixed_number_initial_infection',
                    'initial_infection_number': number_initial_seeds,
                    'delta': 0.0000000000000001,
                    'fixed_prob_high': fixed_prob_high,
                    'fixed_prob': fixed_prob_low,
                    'alpha': alpha,
                    'gamma': gamma,
                    'theta': 2,
                    'rewire': False,
                }

                dynamics_add_triad = DeterministicLinear(params_add_triad)

                speed_add_triad, std_add_triad, _, _, speed_samples_add_triad = \
                    dynamics_add_triad.avg_speed_of_spread(
                        dataset_size=size_of_dataset,
                        cap=0.9,
                        mode='max')

                print(speed_add_triad, std_add_triad)

                print(speed_samples_add_triad)

                print(NX.is_connected(G))

            if save_computations:

                pickle.dump(speed_samples_add_random, open(spreading_pickled_samples_directory_address + 'speed_samples_'
                                                           + str(percent_more_edges) + '_percent_' + 'add_random_'
                                                           + network_group + network_id
                                                           + model_id + '.pkl', 'wb'))
                pickle.dump(speed_samples_add_triad, open(spreading_pickled_samples_directory_address + 'speed_samples_'
                                                          + str(percent_more_edges) + '_percent_' + 'add_triad_'
                                                          + network_group + network_id
                                                          + model_id + '.pkl', 'wb'))

            if load_computations:

                speed_samples_add_random = pickle.load(open(spreading_pickled_samples_directory_address + 'speed_samples_'
                                                            + str(percent_more_edges) + '_percent_' + 'add_random_'
                                                            + network_group + network_id
                                                            + model_id + '.pkl', 'rb'))
                speed_samples_add_triad = pickle.load(open(spreading_pickled_samples_directory_address + 'speed_samples_'
                                                           + str(percent_more_edges) + '_percent_' + 'add_triad_'
                                                           + network_group + network_id
                                                           + model_id + '.pkl', 'rb'))

                speed_add_triad = np.mean(speed_samples_add_triad)

                speed_add_random = np.mean(speed_samples_add_random)

                std_add_triad = np.std(speed_samples_add_triad)

                std_add_random = np.std(speed_samples_add_random)

            if do_plots:

                plt.figure()

                plt.hist([speed_samples_add_random, speed_samples_add_triad], label=['random', 'triads'])

                plt.ylabel('Frequency')
                plt.xlabel('Time to Spread')
                plt.title('\centering The mean spread times are '
                          + str(Decimal(speed_add_random).quantize(TWOPLACES))
                          + '(SD=' + str(Decimal(std_add_random).quantize(TWOPLACES)) + ')'
                          + ' and '
                          + str(Decimal(speed_add_triad).quantize(TWOPLACES))
                          + '(SD=' + str(Decimal(std_add_triad).quantize(TWOPLACES)) + '),'
                          + '\\vspace{-10pt}  \\begin{center}  in the two networks with ' + str(percent_more_edges)
                          + '\% additional random or triad closing edges. \\end{center}')
                plt.legend()
                if show_plots:
                    plt.show()

                if save_plots:
                    plt.savefig(output_directory_address + 'speed_samples_histogram_'
                                + str(percent_more_edges) + '_edge_additions_'
                                + network_group + network_id
                                + model_id + '.png')
            if data_dump:

                print('we are in data_dump mode')

                df_common_part_add_random = pd.DataFrame(data=[[network_group, network_id, network_size,
                                                                'random_addition', percent_more_edges,
                                                                MODEL]] * len(speed_samples_add_random),
                                                       columns=['network_group', 'network_id', 'network_size',
                                                                'intervention_type',
                                                                'intervention_size', 'model'])

                df_sample_ids_add_random = pd.Series(list(range(len(speed_samples_add_random))), name='sample_id')

                df_time_to_spreads_add_random = pd.Series(speed_samples_add_random, name='time_to_spread')

                new_df_add_random = pd.concat([df_common_part_add_random, df_sample_ids_add_random,
                                               df_time_to_spreads_add_random],
                                              axis=1)

                df_common_part_add_triad = pd.DataFrame(data=[[network_group, network_id, network_size,
                                                               'triad_addition', percent_more_edges,
                                                               MODEL]] * len(speed_samples_add_triad),
                                                        columns=['network_group', 'network_id', 'network_size',
                                                                 'intervention_type',
                                                                 'intervention_size', 'model'])

                df_sample_ids_add_triad = pd.Series(list(range(len(speed_samples_add_triad))), name='sample_id')

                df_time_to_spreads_add_triad = pd.Series(speed_samples_add_triad, name='time_to_spread')

                new_df_add_triad = pd.concat([df_common_part_add_triad, df_sample_ids_add_triad,
                                              df_time_to_spreads_add_triad],
                                             axis=1)

                print(new_df_add_triad)

                extended_frame = [df, new_df_add_random, new_df_add_triad]

                df = pd.concat(extended_frame, ignore_index=True, verify_integrity=False)#.drop_duplicates().reset_index(drop=True)

    if data_dump:
        df.to_csv(output_directory_address + network_group + 'spreading_data_dump.csv', index=False)#  , index=False
