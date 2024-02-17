from geoformat.conversion.geolayer_conversion import create_geolayer_from_i_feat_list
from geoformat.conf.error_messages import field_missing


####
#
# CLAUSE
#
# The CLAUSE functions return a directly a list of i_feat or a dict with a list associates to each key of i_feat
###

def clause_where(geolayer, field_name, predicate, values):
    """
    This function return an i_feat list from a geolayer that match with a predicate and given value.

    :param geolayer: layer on which we want to apply the where clause
    :param field_name: name of field on which is made the where clause
    :param predicate: predicate used in this list : '=','<', '>', '<>', 'LIKE', 'BETWEEN', 'IS', 'IS NOT'
    :param values: value that we want match or unmatch

    :return: i_feat_list
    """
    if field_name not in geolayer['metadata']['fields']:
        raise Exception(field_missing.format(field_name=field_name))

    # transform values to iterate variable
    if not isinstance(values, (list, tuple)):
        if isinstance(values, tuple):
            values = list(values)
        else:
            values = [values]

    # init result list
    i_feat_list = []

    # loop on geolayer
    for i_feat in geolayer['features']:
        feature = geolayer['features'][i_feat]
        feature_value = feature.get('attributes', {}).get(field_name)

        # save feature_value in list by default
        if isinstance(feature_value, (list, tuple, set)):
            feature_value_list = feature_value
        else:
            feature_value_list = [feature_value]

        save_i_feat = False
        # loop on feature_value_list
        for feature_value in feature_value_list:

            if '=' in predicate or 'IN' in predicate or predicate == 'LIKE' or predicate == 'BETWEEN':
                if feature_value in values:
                    save_i_feat = True
                    break

            if '>' in predicate or '<' in predicate or predicate == 'BETWEEN':
                if predicate == '<>':
                    if feature_value not in values:
                        save_i_feat = True
                else:
                    if feature_value is not None:
                        if '>' in predicate and feature_value > values[0]:
                            save_i_feat = True
                        if '<' in predicate and feature_value < values[-1]:
                            save_i_feat = True
                        if predicate == 'BETWEEN':
                            if values[0] < feature_value < values[-1]:
                                save_i_feat = True

            if 'IS' in predicate:
                if feature_value in values:
                    save_i_feat = True

                if 'NOT' in predicate:
                    save_i_feat = not save_i_feat

        if save_i_feat:
            i_feat_list.append(i_feat)

    return i_feat_list


def clause_group_by(geolayer, field_name_list):
    """
    Return a dictionnary with field name list as key and i_feat list from geolayer
    """

    if isinstance(field_name_list, str):
        field_name_list = [field_name_list]

    result_dico = {}
    for i_feat in geolayer['features']:
        feature = geolayer['features'][i_feat]

        # if feature is serialized
        if 'feature_serialize' in geolayer['metadata']:
            if geolayer['metadata']['feature_serialize']:
                feature = eval(feature)

        field_value_tuple = tuple(
            [feature['attributes'][field_name] if field_name in feature['attributes'] else None for field_name in
             field_name_list])

        # convert list value to tuple (if exists) very rare
        field_value_tuple = tuple([tuple(value) if isinstance(value, list) else value for value in field_value_tuple])

        if field_value_tuple in result_dico:
            result_dico[field_value_tuple].append(i_feat)
        else:
            result_dico[field_value_tuple] = [i_feat]

    return result_dico


def clause_order_by(geolayer, order_parameters):
    """
    Send i_feat list in order define in order_parameters

    order_parameters format : 3 poosibilities :
        order_parameters = 'field_name' (order by default is ASC)
        order_parameters = ('field_name', 'ASC' or 'DESC')
        order_parameter = [('field_name_a', 'ASC' or 'DESC'), ('field_name_b', 'ASC' or 'DESC'), ..., ('field_name_n', 'ASC' or 'DESC'
    """

    def insert_in_order_list_by_split(value, i_feat_list, order_by_list):
        # try to insert at extremity of list
        # value is lower of last value in order_by_list
        if value <= order_by_list[0][0]:
            if value == order_by_list[0][0]:
                order_by_list[0][1] = order_by_list[0][0] + i_feat_list
            else:
                order_by_list = [(value, i_feat_list)] + order_by_list
            return order_by_list
        # value is upper of last value in order_by_list
        elif value >= order_by_list[-1][0]:
            if value == order_by_list[-1][0]:
                order_by_list[-1][1] = order_by_list[-1][0] + i_feat_list
            else:
                order_by_list = order_by_list + [(value, i_feat_list)]
            return order_by_list

        # if no insertion we have to split in two
        list_cuter_idx = int(len(order_by_list) / 2)
        if value <= order_by_list[list_cuter_idx - 1][0]:
            if value == order_by_list[list_cuter_idx - 1][0]:
                order_by_list[list_cuter_idx - 1][1] += i_feat_list
                return order_by_list
            else:
                order_by_list_splited = order_by_list[:list_cuter_idx]
                result = insert_in_order_list_by_split(value, i_feat_list, order_by_list_splited)
                return result + order_by_list[list_cuter_idx:]

        if value >= order_by_list[list_cuter_idx][0]:
            if value == order_by_list[list_cuter_idx][0]:
                order_by_list[list_cuter_idx][1] += i_feat_list
                return order_by_list
            else:
                order_by_list_splited = order_by_list[list_cuter_idx:]
                result = insert_in_order_list_by_split(value, i_feat_list, order_by_list_splited)
                return order_by_list[:list_cuter_idx] + result

        return order_by_list[:list_cuter_idx] + [(value, i_feat_list)] + order_by_list[list_cuter_idx:]

    def order_values(dico_value, field_order):
        """
            This function ordered value in function of field order
        """
        order_by_list = None
        none_value_i_feat = []
        for value in dico_value:
            i_feat_list = dico_value[value]
            if None in value:
                none_value_i_feat += i_feat_list
            else:
                # first iteration
                if not order_by_list:
                    order_by_list = [(value, i_feat_list)]
                else:
                    order_by_list = insert_in_order_list_by_split(value, i_feat_list, order_by_list)

        # reverse order if we are DESC
        if field_order.upper() == 'DESC' and order_by_list:
            order_by_list = sorted(order_by_list, reverse=True)

        # add none value (if exists) in function of order_fields
        if len(none_value_i_feat) > 0:
            if order_by_list:
                if field_order.upper() == 'ASC':
                    order_by_list += [((None,), none_value_i_feat)]
                else:
                    order_by_list = [((None,), none_value_i_feat)] + order_by_list
            else:
                order_by_list = [(None, none_value_i_feat)]

        return order_by_list

    def field_group_by_then_order(geolayer, order_parameters):
        """
        This function is used to realise first a group by and reorder result
        Then it recall it if there is an other field_order_paramenters
        """
        (field_name, field_order) = order_parameters[0]
        gb_field_name = clause_group_by(geolayer, field_name)
        gb_field_name_ordered = order_values(gb_field_name, field_order)
        result_i_feat_list = []
        for value, i_feat_list in gb_field_name_ordered:
            if len(i_feat_list) > 1:
                if len(order_parameters) > 1:
                    new_order_parameters = order_parameters[1:]
                    new_geolayer = create_geolayer_from_i_feat_list(geolayer, i_feat_list, reset_i_feat=False)
                    result_i_feat_list += field_group_by_then_order(new_geolayer, new_order_parameters)
                else:
                    result_i_feat_list += i_feat_list
            else:
                result_i_feat_list += i_feat_list

        return result_i_feat_list

    # verification enters parameters
    if isinstance(order_parameters, (list, tuple)):
        authorised_order_value = set(['ASC', 'DESC'])
        for i_field, field in enumerate(order_parameters):
            if len(field) == 1:
                order_parameters[i_field] = (field, 'ASC')
            elif len(field) == 2:
                if field[1].upper() not in authorised_order_value:
                    raise Exception('error you must add "ASC" or "DESC" key in second position')
            else:
                raise Exception('error order_paramaters variable format is not correct')
    elif isinstance(order_parameters, str):
        order_parameters = [(order_parameters, 'ASC')]
    else:
        raise Exception("error: order_parameters must be a list / tuple or str value")

    for (field_name, order_value) in order_parameters:
        if field_name not in geolayer['metadata']['fields']:
            raise Exception(field_missing.format(field_name=field_name))

    return field_group_by_then_order(geolayer, order_parameters)

