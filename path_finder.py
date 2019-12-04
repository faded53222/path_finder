import operator
class Node():
	def __init__(self,x,y):
		self.x=x
		self.y=y
		self.neighbors=[]
		self.explored=0
		self.explored2=0
		self.g=0
		self.h=0
		self.f=0
		self.path_from=''
		self.path_from2=''
		self.unexplored_neighbor_count=0
		self.g2=0
	def distance(self,another):
		return abs(self.x-another.x)+abs(self.y-another.y)
map_l=[]
node_dic={}
start_node=Node(0,0)
end_node=Node(0,0)
length=0
height=0
def load(map_f):
	global start_node
	global end_node
	global height
	global length
	with open(map_f,'r') as f:
		i=-1
		for each in f.readlines():
			temp_map=[]
			i+=1
			j=-1
			if i==0:
				length=len(each)-1
			for each2 in each:
				temp_map.append(each2)
				j+=1
				if not each2.isspace():
					if each2!='1':
						new_node=Node(i,j)
						node_dic[(i,j)]=new_node
						if (i-1,j) in node_dic.keys():
							node_dic[(i-1,j)].neighbors.append(node_dic[(i,j)])
							node_dic[(i,j)].neighbors.append(node_dic[(i-1,j)])
						if (i+1,j) in node_dic.keys():
							node_dic[(i+1,j)].neighbors.append(node_dic[(i,j)])
							node_dic[(i,j)].neighbors.append(node_dic[(i+1,j)])
						if (i,j-1) in node_dic.keys():
							node_dic[(i,j-1)].neighbors.append(node_dic[(i,j)])
							node_dic[(i,j)].neighbors.append(node_dic[(i,j-1)])
						if (i,j+1) in node_dic.keys():
							node_dic[(i,j+1)].neighbors.append(node_dic[(i,j)])
							node_dic[(i,j)].neighbors.append(node_dic[(i,j+1)])						
						if each2=='S':
							start_node=new_node
						elif each2=='E':
							end_node=new_node
			map_l.append(temp_map)
	height=i+1
s_list=[]
max_f=0
count_steps=0
def IDA():
	global count_steps
	global max_f
	start_node.h=start_node.distance(end_node)
	start_node.g=0
	max_f=start_node.distance(end_node)
	while max_f<height*length:
		count_steps=0
		value=deal(start_node)
		print('max_f:'+str(max_f))
		if value==1:
			return 1
		max_f+=1
	return 0
def deal(current_node):
	global count_steps
	count_steps+=1
	if current_node==end_node:
		current_node2=end_node
		while 1:
			if current_node2==start_node:
				break
			counti=0
			min_g=length*height
			keep_node=''
			for each in current_node2.neighbors:
				if each.explored==1:
					if each.g<min_g:
						min_g=each.g
						keep_node=each
			if keep_node!=current_node2.path_from:
				current_node2.path_from=keep_node
				current_node2=keep_node
			else:
				current_node2=current_node2.path_from
		current_node.explored=0
		return 1
	if current_node.f>max_f:
		current_node.explored=0
		return 0
	current_node.explored=1
	deal_list=[]
	for each in current_node.neighbors:
		if each.explored==0:
			each.h=each.distance(end_node)
			each.g=current_node.g+1
			each.f=each.h+each.g
			each.path_from=current_node
			deal_list.append(each)
	cmpfun = operator.attrgetter('f')
	deal_list.sort(key=cmpfun)
	for each in deal_list:
		value=deal(each)
		if value==1:
			current_node.explored=0
			return 1
	current_node.explored=0
	return 0
def blind_search():
	global count_steps
	global max_f
	cnode1=start_node
	cnode2=end_node
	max_f=start_node.distance(end_node)/2
	while max_f<height*length/2:
		for i in range(height):
			for j in range(length):
				if (i,j) in node_dic.keys():
					node_dic[(i,j)].explored=0
					node_dic[(i,j)].explored2=0
					node_dic[(i,j)].unexplored_neighbor_count=len(node_dic[(i,j)].neighbors)
					#print(node_dic[(i,j)].unexplored_neighbor_count,end='')
				#else:
				#	print('0',end='')
			#print('\n')
		count_steps=0
		value=deal2(cnode1,cnode2)
		print('max_f:'+str(max_f))
		if value==1:
			#print(contact_node.x,contact_node.y)
			#print(contact_node.path_from)
			#print(contact_node.path_from2)
			return 1
		max_f+=1
	return 0
contact_node=''
def deal2(cnode1,cnode2):
	global count_steps
	global max_f
	global contact_node
	#print("pos1:",cnode1.x,cnode1.y)
	#print("pos2:",cnode2.x,cnode2.y)
	if cnode1.explored==1 or cnode2.explored2==1:
		#print('end bacause calced this case')
		return 0
	#for i in range(height):
	#	for j in range(length):
	#		if (i,j) in node_dic.keys():
	#			print(node_dic[(i,j)].explored2,end='')
	#		else:
	#			print('0',end='')
	#	print('\n')	
	count_steps+=1
	lab1=0
	lab2=0
	while 1:
		cnode1.explored=1
		for each in cnode1.neighbors:
			each.unexplored_neighbor_count-=1
		if cnode1.explored2==1:
			lab1=1
			break
		if cnode1.g>max_f:
			#print('end beacuse node1 exceed')
			return 0
		if cnode1.unexplored_neighbor_count>1:
			break
		if cnode1.unexplored_neighbor_count==0:
			#print('end beacuse node1 run out')
			return 0
		if cnode1.unexplored_neighbor_count==1:
			for cc in cnode1.neighbors:
				if cc.explored==0:
					the_node=cc
					break
			the_node.g=cnode1.g+1
			the_node.path_from=cnode1
			cnode1=the_node
	if lab1==1:
		contact_node=cnode1
		return 1
	while 1:
		cnode2.explored2=1
		for each in cnode2.neighbors:
			each.unexplored_neighbor_count-=1
		if cnode2.explored==1:
			lab2=1
			break
		if cnode2.g>max_f:
			#print('end beacuse node2 exceed')
			return 0
		if cnode2.unexplored_neighbor_count>1:
			break
		if cnode2.unexplored_neighbor_count==0:
			#print('end beacuse node2 run out')
			return 0
		if cnode2.unexplored_neighbor_count==1:
			for cc in cnode2.neighbors:
				if cc.explored2==0:
					the_node=cc
					break
			the_node.g2=cnode2.g2+1
			the_node.path_from2=cnode2
			cnode2=the_node
	if lab2==1:
		contact_node=cnode2
		return 1
	deal_list=[]
	for each in cnode1.neighbors:
		for each2 in cnode2.neighbors:
			if each.explored==0 and each2.explored2==0:
				each.g=cnode1.g+1
				each2.g=cnode2.g+1
				each.path_from=cnode1
				each2.path_from2=cnode2
				deal_list.append((each,each2))
	deal_list=sorted(deal_list, key=lambda x:(x[0].distance(x[1])))
	for each in deal_list:
		value=deal2(each[0],each[1])
		if value==1:
			return 1
	return 0
def write(file_name,typ):
	if typ==1:
		current_node=end_node
		while 1:
			if current_node==end_node:
				print('(end)',end="")	
				print(current_node.x,current_node.y,'<-',end="")
			elif current_node==start_node:
				print(current_node.x,current_node.y,'(start)',end="")
				break
			else:
				print(current_node.x,current_node.y,'<-',end="")
				map_l[current_node.x][current_node.y]=2
			current_node=current_node.path_from
		print('\n')
	if typ==2:
		map_l[contact_node.x][contact_node.y]=2
		current_node=contact_node
		while 1:
			if current_node==start_node:	
				print(current_node.x,current_node.y,'(start)',end="")
				break
			elif current_node==contact_node:
				print(current_node.x,current_node.y,'(contact)<-',end="")
			else:
				print(current_node.x,current_node.y,'<-',end="")
				map_l[current_node.x][current_node.y]=2
			current_node=current_node.path_from		
		print('\n')
		current_node=contact_node
		while 1:
			if current_node==end_node:	
				print(current_node.x,current_node.y,'(end)',end="")
				break
			elif current_node==contact_node:
				print(current_node.x,current_node.y,'(contact)->',end="")
			else:
				print(current_node.x,current_node.y,'->',end="")
				map_l[current_node.x][current_node.y]=2
			current_node=current_node.path_from2
		print('\n')
	with open(file_name,'w') as f:
		for each in map_l:
			for each2 in each:
				f.write(str(each2))
if __name__ == "__main__":
	load("MazeData.txt")
	if (IDA()==1):
		print('program was solved with max_f and steps_of_calc as:',max_f,count_steps)
		write('IDA_result.txt',1)
	'''
	for i in range(height):
		for j in range(length):
			if (i,j) in node_dic.keys():
				print(node_dic[(i,j)].explored2,end='')
			else:
				print('0',end='')
		print('\n')
	print('\n')		
	for i in range(height):
		for j in range(length):
			if (i,j) in node_dic.keys():
				print(node_dic[(i,j)].explored,end='')
			else:
				print('0',end='')
		print('\n')
	'''
	if (blind_search()==1):
		print('program was solved with max_f and steps_of_calc as:(这里的step是对两者进行转弯抉择的总次数)',max_f,count_steps)
		write('blind_search.txt',2)		
