TIMEFORMAT=%2U
for ego in `cat egos_to_run` 
do
	echo $ego >> '../time_per_ego.csv'
	echo `$(time python main_enumeration.py $ego 4)` >> '../time_per_ego.csv'
done
