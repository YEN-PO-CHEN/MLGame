$.ML_PONG:
	python MLGame.py -i ml_play.py -i ml_play.py pingpong HARD
$.Test_PONG:
	python MLGame.py -f 180 -i ml_play_template.py pingpong HARD
$.Test_PONG_5:
	python MLGame.py -f 180 -i ml_play_template_5.py pingpong HARD
$.Test_PONG_RECORD:
	python MLGame.py -f -r -i ml_play_template.py pingpong HARD 200
$.Stu:
	python MLGame.py -f 150 -r -i ml_STU.py pingpong HARD 100
$.Test_snake:
	python MLGame.py -i ml_play_template.py snake
$.ML_snake:
	python MLGame.py -i ml_play.py -i ml_play.py snake