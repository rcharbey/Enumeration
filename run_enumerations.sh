for ego in `cat egos_to_run` 
do
	t=times python main_enumeration.py $ego 4
	echo $t
	echo $ego $t >> '../time_per_ego.csv'
done
