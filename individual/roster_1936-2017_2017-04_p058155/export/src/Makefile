# -*- coding: utf-8 -*-

# Authors:	Roman Rivera (Invisible Institute)
# individual/roster_1936-2017_2017-04_p058155/export/src/Makefile

.PHONY: all clean
# Additional files created: export.log, export.yaml,
# roster_1936-2017_2017-04_profiles.csv.gz,

all: \
		output/roster_1936-2017_2017-04.csv.gz

output/roster_1936-2017_2017-04.csv.gz: \
		src/export.py \
		input/roster_1936-2017_2017-04.csv.gz \
		input/roster_1936-2017_2017-04_profiles.csv.gz
	python $<


clean:
	rm output/*


# done
