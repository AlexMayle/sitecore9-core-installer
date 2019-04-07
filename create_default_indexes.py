import sys
import argparse

MODULE_DESCRIPTION = (
    "Generates Solr Collection API commands to install Solr on linux"
)

CREATE_CMD_FMT = "%s create -c %s -d %s %s"

XP_CONFIG_LOC = "configsets/xp_config"
XDB_CONFIG_LOC = "configsets/xdb_config"

COL_PREFIX = "sitecore"
SECONDARY_SUFFIX = "secondary"

COL_LIST = [
    "master_index",
    "web_index",
    "marketingdefinitions_master",
    "marketingdefinitions_web",
    "marketing_asset_index_master",
    "marketing_asset_index_web",
    "testing_index",
    "suggested_test_index",
    "fxm_master_index",
    "fxm_web_index"
]

XDB_COL_LIST = [
    "xdb",
    "xdb_rebuild"
]

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
    "The list of collection names. "
    "(Default: All standard collections installed by the SIF "
    "Framework.)"
)

ADD_ARGS_HELP = (
    "A string of CREATECOLLECTION (Solr Collection API command) "
    "arguments to be included in the generated commands. Notable "
    "ones include the replication factor and the number of shards. "
    "(Default: 1 replica, 1 shard, no additional arguments.)"
)


parser = argparse.ArgumentParser(description=MODULE_DESCRIPTION)

parser.add_argument('-solr',
                    default="/opt/solr/bin/solr",
                    help="Path to the solr binary",
                    type=str
                   )

parser.add_argument('-p,', '--prefix',
                    default=COL_PREFIX,
                    help="The prefix of the non-xdb collection names.",
                    type=str
                   )

parser.add_argument('--xdb-prefix',
                    default='',
                    help=XDB_PREFIX_HELP,
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
    print(args)
 
    xp_collections = add_prefix(args.prefix, COL_LIST)
    if args.secondary:
        xp_collections += add_secondary_indexes(xp_collections)
    commands = create_commands(args.solr,
                               xp_collections,
                               XP_CONFIG_LOC,
                               args.additional_args)

    xdb_collections = add_prefix(args.xdb_prefix, XDB_COL_LIST)
    commands += create_commands(args.solr,
                                xdb_collections,
                                XDB_CONFIG_LOC,
                                args.additional_args)

    print(' && \\\n'.join(commands))
