def flatten_lists(iterable):
    it = iter(iterable)
    for e in it:
        if isinstance(e, (list, tuple)):
            for f in flatten_lists(e):
                yield f
        else:
            yield e


def followers(file_name):
    follow = open(file_name, 'r')
    for follower in follow:
        follower_list = []
        follower_list.append(follower.strip('\n'))
        for element in flatten_lists(follower_list):
            yield element