#!/bin/bash

# apitoken should be 1st argument
API_TOKEN=$1

# samplefiles dir should be 2nd argument
FILESDIR=$2

# hard-code files to datasets. only sampledata, after all.
# i started with an associative array, but, eh.

# record of american democracy

curl -H "X-Dataverse-key:$API_TOKEN" -X POST -F 'file=@keyal (1).tsv' -F 'jsonData={"description":"Tab delimited data","categories":["Key Data File - Alabama"], "restrict":"false"}' "http://localhost:8080/api/datasets/44747/add"
sleep 3
curl -H "X-Dataverse-key:$API_TOKEN" -X POST -F 'file=@keyal-1.por' -F 'jsonData={"description":"SPSS portable data file","categories":["Key Data File - Alabama"], "restrict":"false"}' "http://localhost:8080/api/datasets/44747/add"
sleep 3
curl -H "X-Dataverse-key:$API_TOKEN" -X POST -F 'file=@road_codebook' -F 'jsonData={"description":"codebook","categories":["Documentation"], "restrict":"false"}' "http://localhost:8080/api/datasets/44747/add"
sleep 3

# ubiquity press > jopd

curl -H "X-Dataverse-key:$API_TOKEN" -X POST -F 'file=@FE_1933_2006_data_subset.csv' -F 'jsonData={"description":"Data","categories":[""], "restrict":"false"}' "http://localhost:8080/api/datasets/76232/add"
sleep 3
curl -H "X-Dataverse-key:$API_TOKEN" -X POST -F 'file=@FE_1933_2006_data_subset.sav' -F 'jsonData={"description":"Data","categories":[""], "restrict":"false"}' "http://localhost:8080/api/datasets/76232/add"
sleep 3
curl -H "X-Dataverse-key:$API_TOKEN" -X POST -F 'file=@bafacalo_dataset_subset.sav' -F 'jsonData={"description":"Dataset from the BAFACALO project: a 292x247 matrix containing the projectÃ¢ÂÂs primary data. Object: BAFACALO_DATASET","categories":[""], "restrict":"false"}' "http://localhost:8080/api/datasets/54486/add"
sleep 3

# king

curl -H "X-Dataverse-key:$API_TOKEN" -X POST -F 'file=@adjacency_subset_.sav' -F 'jsonData={"description":"Proximity Data File ","categories":["2y. Data: Additional Files"], "restrict":"false"}' "http://localhost:8080/api/datasets/88913/add"
sleep 3
curl -H "X-Dataverse-key:$API_TOKEN" -X POST -F 'file=@allc_subset.sav' -F 'jsonData={"description":"Number of deaths from All Causes","categories":["2b. Data: Cause of Death - All Causes"], "restrict":"false"}' "http://localhost:8080/api/datasets/88913/add"
