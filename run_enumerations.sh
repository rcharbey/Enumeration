TIMEFORMAT=%2U
for ego in `cat egos_to_run` 
do
	echo $ego >> '../time_per_ego.csv'
	{ time python main_enumeration.py $ego 4 ;} 2>> '../time_per_ego.csv'
done
