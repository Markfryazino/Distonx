def lag(data, index_cols, lag_cols, mode = "day"):
    
    shift_range = [1, 2, 3, 4, 5, 12]

    for shift in tqdm_notebook(shift_range):
        shifted_data = data[index_cols + lag_cols].copy()

        # pd.DateOffset(seconds = shift)
        # "-" for data from future
        shifted_data['date'] -= pd.DateOffset(days = 1)

        foo = lambda x: '{}_{}lag_{}'.format(x, mode, shift) if x in lag_cols else x
        shifted_data = shifted_data.rename(columns = foo)

        data = pd.merge(data, shifted_data, on = index_cols, how = 'left').fillna(0) # or other NaN value

    return data

def first_extremum(data, delta_list, value_column, mode = 'max'):
    # data must have "date"
    copy_data = data.copy()
    
    for delta in delta_list:
        for value_label in value_column:
            
            if mode == 'max':
                max_mask = (copy_data[value_label].rolling(1 + 2 * delta , center = True).max() ==\
                            copy_data[value_label])
                indexes = np.where(copy_data[value_label].rolling(1 + 2 * delta , center = True).max() ==\
                                   copy_data[value_label])[0]
            else:
                max_mask = (copy_data[value_label].rolling(1 + 2 * delta , center = True).min() ==\
                            copy_data[value_label])
                indexes = np.where(copy_data[value_label].rolling(1 + 2 * delta , center = True).min() ==\
                                   copy_data[value_label])[0]

            indexes_with_nan = np.concatenate([indexes, [None]])

            # fmxi is first max index (index of the first maximum)
            copy_data['{}_f{}i{}'.format(value_label, mode, 1 + 2 * delta)] =\
                indexes_with_nan[np.searchsorted(indexes, data.index, side='right')]

            # fmxr is first max range (range to the first maximum)
            copy_data['{}_f{}r{}'.format(value_label, mode, 1 + 2 * delta)] =\
                copy_data['{}_f{}i{}'.format(value_label, mode, 1 + 2 * delta)] - copy_data.index

            max_val = copy_data[max_mask][[value_label]]
            max_val = max_val.rename(columns = lambda x : "{}_{}{}".format(x, mode, 1 + 2 * delta))  

            copy_data = copy_data.join(max_val, how = 'left')

            # print(copy_data[value_label] == copy_data[value_label+"_max"])
            copy_data.loc[copy_data[value_label] == copy_data['{}_{}{}'.format(value_label, mode,  1 + 2 * delta)], 
                          '{}_f{}r{}'.format(value_label, mode, 1 + 2 * delta)] = 0

            copy_data.drop(['{}_f{}i{}'.format(value_label, mode, 1 + 2 * delta)], inplace = True, axis = 1)
            copy_data = copy_data[::-1]
            copy_data['{}_{}{}'.format(value_label, mode,  1 + 2 * delta)] = copy_data[
                '{}_{}{}'.format(value_label, mode,  1 + 2 * delta)].ffill()
            copy_data = copy_data[::-1]

    return copy_data


#lag(data, ["date"], ["brent_close", "brent_open"])
#       date	        brent_close	brent_open	brent_close_daylag_1	brent_open_daylag_1	brent_close_daylag_2	brent_open_daylag_2	brent_close_daylag_3	brent_open_daylag_3	brent_close_daylag_4	brent_open_daylag_4	brent_close_daylag_5	brent_open_daylag_5	brent_close_daylag_12	brent_open_daylag_12
#0	2002-07-01	25.64	25.50	25.75	25.61	25.75	25.61	25.75	25.61	25.75	25.61	25.75	25.61	25.75	25.61
#1	2002-07-02	25.75	25.61	25.84	25.73	25.84	25.73	25.84	25.73	25.84	25.73	25.84	25.73	25.84	25.73

#get_max(data, [2, 3], ['brent_close', 'brent_open'], 'min')
#       date	        brent_close	brent_open	brent_close_fminr5	brent_close_min5	brent_open_fminr5	brent_open_min5	brent_close_fminr7	brent_close_min7	brent_open_fminr7	brent_open_min7
#0	2002-07-01	25.64	25.50	5	25.08	6	25.1	5	25.08	6	25.1
#1	2002-07-02	25.75	25.61	4	25.08	5	25.1	4	25.08	5	25.1
