for i in $(seq 0 7)
do
	python3 data_generator.py ./$i/data$i.txt
done
