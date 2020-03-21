def split_to_pairs(dct):
    dict_of_pairs = dict()
    for key in dct:
        splited_key = key.split('_')
        if len(splited_key) > 1:
            pairname = splited_key[0]
            if pairname not in dict_of_pairs.keys():
                dict_of_pairs[pairname] = dict()
            if splited_key[1] == 'kline':
                dict_of_pairs[pairname]['_'.join(splited_key[1:])] = dct[key]
            elif splited_key[1] == 'asks':
                if splited_key[3] == 'price':
                    dict_of_pairs[pairname]['depth_ask_price_' + str(int(splited_key[-1]) + 1)] = dct[key]
                if splited_key[3] == 'quantity':
                    dict_of_pairs[pairname]['depth_ask_quantity_' + str(int(splited_key[-1]) + 1)] = dct[key]
            elif splited_key[1] == 'bids':
                if splited_key[3] == 'price':
                    dict_of_pairs[pairname]['depth_bid_price_' + str(int(splited_key[-1]) + 1)] = dct[key]
                if splited_key[3] == 'quantity':
                    dict_of_pairs[pairname]['depth_bid_quantity_' + str(int(splited_key[-1]) + 1)] = dct[key]
    return dict_of_pairs
