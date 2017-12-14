TIMEFORMAT=%2U
for ego in `cat egos_to_run` 
do
	t=time { {
		python main_enumeration.py $ego 4;
	} 2>&1; }

	echo $ego $t >> '../time_per_ego.csv'
done
