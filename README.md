# gerrychain_redist_compare
repo with scripts for gerrychain and redist comparison project

Contains scripts & data files for running both Redist & Gerrychain. See package home pages for installation instructions and reference guides on these useful opensource ensemble simulation engines for creating sample legislative district plans: 
Redist & Redistmetrics available on cran
- https://cran.microsoft.com/snapshot/2022-07-18/web/packages/redist/index.html
- https://cran.r-project.org/web/packages/redistmetrics/index.html
modifications & adds to gerrychain software, 
- https://gerrychain.readthedocs.io/en/latest/user/install.html

Additional customizations/ modules for Gerrychain available & documented in this repo: https://github.com/dinosg/gerrychain

Redist routines:

pa_congressional.Rmd reads in base shapefile data for Pennsylvania and computes Redist SMC Congressional district plans.

pa_house.Rmd does the same, only for Redist merge-split plans. Code is basically similar and various options within are highlighted/ commented out.

Gerrychain routines:
chain_parallel_county_composite_muni_sumf.py creates parallel processing 'Recom' ensembles. It reads in an 'input template' - either PA_HDIST_lrc.py or PA_CD17_sumf.py that sets input parameters for either House or Congressional districts. These will be constrained for county and municipality splits (parameters set by input template)

chain_ppartonly_compsumf.py creates parallel random tree ensembles that are NOT constrained for county/muni splits


splice_assignment_fn.py 'splices in' a new district assignment from a csv/ text files and merges it to an existing geodataframe with state VTD shapes and election data, defines my_apportionment to be something new (reflecting what's in the file). Extremely useful for assessing test plans, or constructing new district mappings from intermediate stored results

conditional_dump.py tests a partition state against some condition - if it meets it, dumps out the VTD assignments to a text file. Uses routines in district_list.py for output

county splits & gerrychain modifications:


chain_xtended_muni.py needs to be included in sourcecode gerrychain directory along with  __init__.py and county_splits.py need to be included in sourcecode gerrychain/updaters directory



