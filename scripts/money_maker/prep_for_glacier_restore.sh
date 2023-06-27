#!/bin/bash

if [[ -z $1 ]]; then
    echo "Please provide a command line argument:"
    read argument
    # Validate the input here if needed
else
    argument=$1
fi


aws s3 ls s3://svz-master-pictures-new/raw-photos/$argument --recursive | sed "s/^[^ ]* [^ ]* *[0-9]* //" | tr '\n' '\0' | xargs  -t -0 -L 1 -I {} aws s3api restore-object --restore-request '{"Days":90,"GlacierJobParameters":{"Tier":"Bulk"}}' --bucket svz-master-pictures-new --key "{}"

