#!/bin/bash

DIR="giza-pp/GIZA++-v2"
MK="giza-pp/mkcls-v2"

./$DIR/plain2snt.out e.txt c.txt
./$DIR/snt2cooc.out c.vcb e.vcb c_e.snt > cooc.ce
./$DIR/snt2cooc.out e.vcb c.vcb e_c.snt > cooc.ec
./$MK/mkcls -m2 -c80 -pe.txt -Ve.vcb.classes opt 
./$MK/mkcls -m2 -c80 -pc.txt -Vc.vcb.classes opt 
./$DIR/GIZA++ -S c.vcb -T e.vcb -C c_e.snt -CoocurrenceFile cooc.ce -O c2e 
./$DIR/GIZA++ -S e.vcb -T c.vcb -C e_c.snt -CoocurrenceFile cooc.ec -O e2c 

