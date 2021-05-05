"""
The template of the script for the machine learning process in game pingpong
"""
import random
class MLPlay:
	def __init__(self, side):
		"""
		Constructor

		@param side A string "1P" or "2P" indicates that the `MLPlay` is used by
			   which side.
		"""
		self.ball_served = False
		self.side = side
		self.count = 0
		self.lastbox= 0
		self.m = 16
	def update(self, scene_info):
		"""
		Generate the command according to the received scene information
		"""

		# print(scene_info["blocker"][0],scene_info["blocker"][1])
		xp = scene_info["platform_1P"][0] + 20        
		yp = scene_info["platform_2P"][0] + 20
		xs = scene_info["ball_speed"][0]
		ys = scene_info["ball_speed"][1]
		x = scene_info["ball"][0]
		y = scene_info["ball"][1]
		box = scene_info["blocker"][0] + 15
		# print(x,y)
		boxspeed = box - self.lastbox
		# print(boxspeed)
		# print(box,boxspeed)
		if scene_info["status"] != "GAME_ALIVE":
			self.m = random.randint(1,16)
			print(xs,ys)
			return "RESET"
		if not self.ball_served :
			if self.m % 2 == 1:
				if self.count <= self.m:
					self.count += 1
					return "MOVE_RIGHT"
				else:
					self.ball_served = True
					return "SERVE_TO_LEFT"
			elif self.m % 2 == 0:
				if self.count <= self.m:
					self.count += 1
					return "MOVE_LEFT"
				else:
					self.ball_served = True
					return "SERVE_TO_LEFT"

		else :
			self.lastbox = box
			if ys > 0 :
				n = 415 - y
				trueexpect = x + n * (xs / ys)
				# print("------------")
				# print(expect)
				expect = realexpect(trueexpect)  
				# print("trueexpect",trueexpect)
				# print("expect",expect) 		
				# print(expect)
				# print("------------")
				if y < 235:
					a = 235 - y 
					l = 265 - y
					m = 250 - y
					leave_time = l /abs(ys)
					arrive_time = a / abs(ys)
					mid_time = m / abs(ys)
					arrive_expect = x + a * (xs / ys)
					leave_expect = x + l * (xs / ys)
					mid_expect = x + m * (xs / ys)
					arrive_expect = realexpect(arrive_expect)
					leave_expect = realexpect(leave_expect)	
					mid_expect = realexpect(mid_expect)			
					arrive_block = arrive_time * boxspeed + box
					leave_block = leave_time * boxspeed + box	
					arrive_block = realbox(arrive_block)
					leave_block = realbox(leave_block)
					# print("expect:",mid_expect)
					reexpect = mid_expect + (mid_expect - trueexpect)					
					reexpect = realexpect(reexpect)
					if hitbox(arrive_expect,arrive_block) == 0 and hitbox(leave_expect,leave_block):
						# print("blue hit")
						expect = (expect + reexpect) / 2
				# print(expect)
				if self.side == "1P":
					if xp - 5> expect : 
						return "MOVE_LEFT"
					elif xp + 5< expect:
						return "MOVE_RIGHT"
					else:return "NONE"
				elif self.side == "2P":
					if y > 235 :                    
						if yp - 5> 100 : 
							return "MOVE_LEFT"
						elif yp + 5< 100:
							return "MOVE_RIGHT"
						else:return "NONE"
					else: 
						m = 235 - y 
						reflect = x +  (m + 155) * (xs / ys)
						reflect = realexpect(reflect)
						# print(reflect)
						if yp - 10> reflect : 
							return "MOVE_LEFT"
						elif yp + 10< reflect:
							return "MOVE_RIGHT"
						else:return "NONE"
			elif ys < 0:
				n = y - 80
				trueexpect = x - n * (xs / ys)
				# print("------------")
				expect = realexpect(trueexpect)
				# print("trueexpect",trueexpect)
				# print("expect",expect)

				if y > 265:
					a = y - 265
					l = y - 235
					m = y - 250
					leave_time = l / abs(ys)
					arrive_time = a / abs(ys)
					mid_time = m / abs(ys)
					arrive_expect = x - a * (xs / ys)
					leave_expect = x - l * (xs / ys)
					mid_expect = x - m * (xs / ys)
					arrive_expect = realexpect(arrive_expect)
					leave_expect = realexpect(leave_expect)					
					mid_expect = realexpect(mid_expect)	
					arrive_block = arrive_time * boxspeed + box
					leave_block = leave_time * boxspeed + box
					arrive_block = realbox(arrive_block)
					leave_block = realbox(leave_block)
					# print("expect:",mid_expect)	
					# if hitbox(arrive_expect,arrive_block) or hitbox(leave_expect,leave_block):
						# print("red hit")
					reexpect = mid_expect + (mid_expect - trueexpect)					
					reexpect = realexpect(reexpect)
					if hitbox(arrive_expect,arrive_block) == 0 and hitbox(leave_expect,leave_block):
						# print("red hit")
						expect = (expect + reexpect) / 2
				# print(expect)
				# print("------------")
				if self.side == "2P":
					if yp - 5> expect : 
						return "MOVE_LEFT"
					elif yp + 5< expect:
						return "MOVE_RIGHT"
					else:return "NONE"
				elif self.side == "1P":
					if y < 265 :  
						if xp - 5 > 100 : 
							return "MOVE_LEFT"
						elif xp + 5 < 100:
							return "MOVE_RIGHT"
						else:return "NONE"
					else : 
						m = y - 265
						reflect = x - (m + 155) * (xs / ys)
						reflect = realexpect(reflect)
						# print(reflect)
						if xp - 10> reflect : 
							return "MOVE_LEFT"
						elif xp + 10< reflect:
							return "MOVE_RIGHT"
						else:return "NONE"
			self.lastbox = box
	def reset(self):
		"""
		Reset the status
		"""
		self.ball_served = False
def realexpect(n):
	if n < 0:
		n = abs(n)
	if n > 390 :
		n -= 390
	elif n > 195:
		n = 390 - n
	return n
def realbox(n):
	if n > 185:
		n = 370 -n
	if  n < 0:
		n = abs(n)
	return n
def hitbox(ball,box):
	if ball >= box - 15 and ball <= box + 15:
		return True
	return False
