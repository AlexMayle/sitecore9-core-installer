# Sitecore9 Core Installer
A Python tool to create all the Solr collections needed for Sitecore 9 on linux. SIF provides no way to install Solr on a linux box, so here you go!

# Features
  - Easily create all of the collections needed for Sitecore 9, just the XP collections, just the xDB collections, or specific custom ones
  - Automatically applies the schema changes required for use with Sitecore 9, or custom configs can be provided
  - Specify any arguments accepted by the SolrCloud collections API
  - Supports creation of secondary collections
  - It's a simple python script, so running it remotely is a breeze

# Prerequisites
  - A running SolrCloud install
  -  Python 3
    
# Usage
Simply clone the repository onto any of the Solr servers participating in the cluster. There are two scripts `create_default_indexes.py` and `create_specific_indexes.py`. Run these from the root of the repo. The former script has no required arguments, the latter requires a space delimited list of collection names with the list wrapped in quotes. Other than that, the two scripts usages are the same. For full details use the `-h` or `--help` flag. 

### General
To see which commands will be executed, without executing them (dry run):
```
python3 create_default_indexes.py [OPTIONS]
```
Which will generate the following
```
/opt/solr/bin/solr create -c sitecore_master_index -d configsets/xp_config  && \
/opt/solr/bin/solr create -c sitecore_web_index -d configsets/xp_config  && \
/opt/solr/bin/solr create -c sitecore_marketingdefinitions_master -d configsets/xp_config  && \
/opt/solr/bin/solr create -c sitecore_marketingdefinitions_web -d configsets/xp_config  && \
/opt/solr/bin/solr create -c sitecore_marketing_asset_index_master -d configsets/xp_config  && \
/opt/solr/bin/solr create -c sitecore_marketing_asset_index_web -d configsets/xp_config  && \
/opt/solr/bin/solr create -c sitecore_testing_index -d configsets/xp_config  && \
/opt/solr/bin/solr create -c sitecore_suggested_test_index -d configsets/xp_config  && \
/opt/solr/bin/solr create -c sitecore_fxm_master_index -d configsets/xp_config  && \
/opt/solr/bin/solr create -c sitecore_fxm_web_index -d configsets/xp_config  && \
/opt/solr/bin/solr create -c xdb -d configsets/xdb_config  && \
/opt/solr/bin/solr create -c xdb_rebuild -d configsets/xdb_config
```
You'll notice that the default configs are `xp_config` and `xdb_Config`. These have all of the schema edits which the SIF framework applies for the XP and xDB collections, respectively.

To execute the commands generated against Solr
```
python3 create_default_indexes.py [OPTIONS] | exec
```

### Common Cases
To create and configure the default collections with a one-liner:
```
python3 create_default_indexes.py [OPTIONS] | exec
```
Create only the xDB collections
```
python create_default_indexes.py -xdb | exec
``` 

Create only the non-XDB collections
```
python create_default_indexes.py -xp | exec
```

### Advanced
To create specific collections:
```
python create_specific_indexes.py 'collection0 collection1 collection2'
```

Specify your own configuration:
```
python create_specific_indexes.pay 'collection0' --config /path/to/my/config --args '-n myconfigwillbecalledthisinzookeeper
```

By default, it assumes the Solr binary is at `/opt/solr/bin/solr` but this can be overriden like so:
```
python create_default_indexes.py -s /path/to/whatever/solr/binary
```

Provide arguments like shards, replication factor, name of the resulting config in zookeeper, etc:
```
python create_default_indexes.py -args `-rf 2 -s 3 -n myconfigname
```

###Testing
Tested on Sitecore 9.0.2. I'm unaware of any breaking changes on 9.1.x, so it will likely work there as well. 
