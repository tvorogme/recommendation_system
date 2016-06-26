def cosine_similarity(intersection_num, all_items_num,
                      first_set_len, second_set_len):
    """
    Count cosine similarity based on intersection data
    :param intersection_num: len of intersection of two sets
    :param all_items_num: num of all items, for example, sum of views
    :param first_set_len: len of first set, for example, views of first video
    :param second_set_len:
    :return:
    """
    intersection_probability = (intersection_num / all_items_num) ** 2
    first_set_probability = first_set_len / all_items_num
    second_set_probability = second_set_len / all_items_num
    cosine_similarity_value = (
        intersection_probability /
        (first_set_probability * second_set_probability)
    )
    return cosine_similarity_value
