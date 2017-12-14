for ego in `cat egos_to_run` 
do
	t=cut `grep `time python main_enumeration.py $ego 4` real` -d '	' -f2
	echo $ego $t >> '../time_per_ego.csv'
done
