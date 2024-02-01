.PHONY: export run debug clean

export:
	export FLASK_APP=main
	export FLASK_ENV=webapp
run:
	flask run
	
debug:
	flask --app main.py --debug run

clean:
	rm cmake -rf