import sys
import argparse

MODULE_DESCRIPTION = (
    "Generates Solr Collection API commands to install Solr on linux"
)

CREATE_CMD_FMT = "%s create -c %s -d %s %s"

XP_CONFIG_LOC = "configsets/xp_config"

COL_PREFIX = "sitecore"
SECONDARY_SUFFIX = "secondary"

XDB_PREFIX_HELP = (
    "The prefix for the xdb collections names.\n\nBe aware "
    "that providing this argument will require that the "
    "connection string are changed, as Sitecore defaults to "
    "'xdb' and 'xdb_rebuild' in the strings produced by the SIF "
    "framework.\n\nIf specific collection names are provided (-c) "
    "this argument is ignored and they will be prefixed with the "
    "provided -p argument, if any."
)

COLLECTION_NAME_HELP = (
   "A space delimited list of collections names. Wrap them in quotes." 
)

ADD_ARGS_HELP = (
    "A string of CREATECOLLECTION (Solr Collection API command) "
    "arguments to be included in the generated commands. Notable "
    "ones include the replication factor and the number of shards. "
    "(Default: 1 replica, 1 shard, no additional arguments.)"
)


parser = argparse.ArgumentParser(description=MODULE_DESCRIPTION)
parser.add_argument('collections',
                    default=None,
                    help=COLLECTION_NAME_HELP,
                    type=str,
                    action='append'
                   )

parser.add_argument('-solr',
                    default="/opt/solr/bin/solr",
                    help="Path to the solr binary",
                    type=str
                   )

parser.add_argument('-p,', '--prefix',
                    default=COL_PREFIX,
                    help="The prefix of the collection names.",
                    type=str
                   )

parser.add_argument('-args', '--additional-args',
                    default='',
                    help=ADD_ARGS_HELP,
                    type=str,
                   )

parser.add_argument('--secondary',
                    default=False,
                    help="Secondary indexes are created if provided.",
                    action='store_true',
                   )

parser.add_argument('--config',
                    default=XP_CONFIG_LOC,
                    help="Path to config file to use",
                    type=str
                   )


def add_prefix(prefix, collections):
    if prefix == '': return collections

    ret = map(lambda c: '_'.join((prefix, c)), collections)
    return list(ret)

def add_secondary_indexes(collections):
    ret = map(lambda c: '_'.join((c, SECONDARY_SUFFIX)), collections)
    return list(ret)

def create_commands(solr, collections, config, additional_arg_str):
    cmds = []
    for col in collections:
        cmds.append(CREATE_CMD_FMT % (solr, col, config, additional_arg_str))
    return cmds


if __name__ == '__main__':
    args = parser.parse_args()

    collection_names = add_prefix(args.prefix, args.collections)

    if args.secondary:
        collection_names += add_secondary_indexes(collection_names)

    commands = create_commands(args.solr,
                               collection_names,
                               args.config,
                               args.additional_args)

    print(' && \\\n'.join(commands))
