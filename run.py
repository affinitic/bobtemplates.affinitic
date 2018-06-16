# encoding: utf-8


def add_dependcy(policy, core, theme):
    f = open("{0}/setup.py".format(policy), "r")
    contents = f.readlines()
    f.close()
    index_to_add = 0
    for index, line in enumerate(contents):
        if index_to_add != 0:
            break
        if '],' in line:
            for index2, line2 in enumerate(contents):
                if 'install_requires=[' in line2:
                    index_to_add = index
                    break
                if index2 == index:
                    break

    contents.insert(index_to_add, "        '{0}',\n        '{1}',\n".format(core, theme))

    f = open("{0}/setup.py".format(policy), "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='config setup from policy')
    parser.add_argument(
            '-p',
            '--policy',
            dest='policy',
    )
    parser.add_argument(
            '-c',
            '--core',
            dest='core',
    )
    parser.add_argument(
            '-t',
            '--theme',
            dest='theme',
    )
    args = parser.parse_args()
    add_dependcy(args.policy, args.core, args.theme)
