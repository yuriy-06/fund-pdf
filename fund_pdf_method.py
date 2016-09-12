# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
# массив - марка - размер - х - у
from fpdf import FPDF

class fund_pdf():
	def __init__(self, fund_list):
		self.fund_list = fund_list
	
	def sizefn(self, mv):  # для переменных которые могут быть произвольно списком или float
		if type(mv) == list:
			v = max(mv)
		else:
			v = mv
		return v

	def sizefn_xy(self, mv):
		if type(mv) == list:
			v = mv
		else:
			v = [mv, mv]
		return v
	
	def print_pdf(self, path = "c:/base.pdf", font_size = 12):
		xm=[] # определим нулевые массивы координат
		ym=[]
		msize=[] # здесь будем хранить размеры фундаментов
		l = len(self.fund_list)
		for i in range(l):
		    size = self.sizefn(self.fund_list[i][1]); x = self.fund_list[i][2]; y = self.fund_list[i][3];
		    xm.append(x - size/2); xm.append(x + size/2) 
		    ym.append(y - size/2); ym.append(y + size/2); msize.append(size)
		
		xmin=min(xm);xmax=max(xm);
		ymin=min(ym);ymax=max(ym);
		max_size = max(msize)
		
		dx = xmax - xmin; dy = ymax - ymin;
		
		if dx>dy:
		    orientation = 'L'
		else:
		    orientation = 'P'
		print "orientation = ", orientation, '\n'
		
		# необходимо вычислить коэффициенты отображения расстояний
		field_size = 10  # в мм
		if orientation == 'L':
		    dxl = 297 - field_size*2; dyl = 210 - field_size*2
		else:
		    dxl = 210 - field_size*2; dyl = 297 - field_size*2
		dxk = dx/dxl; dyk = dy/dyl  # 
		
		k = max(dxk, dyk) # нашли общий коэффициент уменьшения
		##### вычислим поправку на вторую сторону -- TODO
		
		xm=[]; ym=[]  # очистим массивы и занесем туда координаты ц.т. фундаментов, а не их границы
		for i in range(l):
		    size = self.fund_list[i][1]; x = self.fund_list[i][2]; y = self.fund_list[i][3];
		    xm.append(x); 
		    ym.append(y);
		
		# найдем центр тяжести изображения
		
		xc = sum(xm)/l; yc = sum(ym)/l
		print "центр тяжести фундаментов xc/yc: ", xc, "/",yc, "\n"
		
		# приведем игреки так, чтобы цент тяжести прошел через ось
		ym = map(lambda y: y - yc, ym)
		# инвертируем игреки
		ym = map(lambda y: -y, ym)
		
		# отодвинем игреки на половину dy + половина размера фундамента
		ym = map(lambda y: y + dy/2 + max_size/2, ym)
		
		# приведем иксы к началу координат + половина размера фундамента
		xm = map(lambda x: x - xmin + max_size/2, xm)
		
		# смаштабируем координаты
		xm = map(lambda x: x/k, xm)
		ym = map(lambda y: y/k, ym)
		
		# отодвинем на величину поля
		xm = map(lambda x: x + field_size*2, xm)
		ym = map(lambda y: y + field_size*2, ym)
		
		title = ""
		heading = ""
		pdf = FPDF()
		pdf.add_page(orientation = orientation)
		pdf.set_font('Times', 'B', font_size)
		for i in range(l):
		    x = xm[i]; y = ym[i]
		    #fpdf.set_xy(x, x)
		    string1 = str(self.fund_list[i][0])
		    string2 = "size=" +str(self.fund_list[i][1]) + " m"
		    pdf.text(x, y, string1)  # выведем марку фундамента
		    pdf.text(x, y+font_size/2, string2)
		    size_x, size_y = self.sizefn_xy(self.fund_list[i][1])
		    pdf.line(x - size_x/2/k, y - size_y/2/k, x - size_x/2/k, y + size_y/2/k) # вверх из нижнего левого угла
		    pdf.line(x - size_x/2/k, y + size_y/2/k, x + size_x/2/k, y + size_y/2/k)  # вправо
		    pdf.line(x + size_x/2/k, y + size_y/2/k, x + size_x/2/k, y - size_y/2/k) # вниз
		    pdf.line(x + size_x/2/k, y - size_y/2/k, x - size_x/2/k, y - size_y/2/k)  # влево
		    
		pdf.output(name = path)

fund_list2 = [  
["fm1", 3.2, -33.775, -5.3],
["fm2", 3.2, -31.875, -0.5],
["fm3", 3.5, -27.975, -0.5],
["fm4", 3.1, -25.475, -5.3],
["fm5", [ 2.4, 3.2], -23.1, -9.95],
["fm6", [2.1, 4.2], -22.325, -13.2], 
["fm7", 0.9, -22.325, -15.3],
["fm8", 2.4, -18.225, -13.2],
["fm9", 2.4, -13.975, -13.2],
["fm10", 0.9, -13.975, -15.3],
["fm11", 4.1, -31.875, -9.95],
["fm12", 2.1, -30.725, -13.2],
["fm13", 2.3, -29.875, -15.3],
["fm14", 3.1, -28.675, -18.15],
["fm15", 2.5, -26.225, -18.4],
["fm16", 2.1, -23.775, -18.65],
["fm17", 1.9, -21.325, -18.9],
["fm18", 2.1, -18.875, -19.15],
["fm19", 1.9, -16.425, -19.4],
["fm20", 2.2, -13.975, -19.65],
["fm21", 2, -27.975, -12.05],
["fm22", [1.9, 2.1], -25.475, -10.95]
]
fund_list1=[
["fm1", 2.8, -33.775, -5.3],
["fm2", 2.9, -31.875, -0.5],
["fm3", 3, -27.975, -0.5],
["fm4", 2.9, -25.475, -5.3],
["fm5", [2.5, 2.8], -23.1, -9.95],
["fm6", [2, 3.3], -22.325, -13.2], 
["fm7", 0.9, -22.325, -15.3],
["fm8", 2.3, -18.225, -13.2],
["fm9", 2.3, -13.975, -13.2],
["fm10", 0.9, -13.975, -15.3],
["fm11", 2.9, -31.875, -9.95],
["fm12", [1.9, 2.2], -30.725, -13.2],
["fm13", [2, 2.3], -29.875, -15.3],
["fm14", 2.2, -28.675, -18.15],
["fm15", 2.3, -26.225, -18.4],
["fm16", 2, -23.775, -18.65],
["fm17", 1.9, -21.325, -18.9],
["fm18", 1.7, -18.875, -19.15],
["fm19", 1.8, -16.425, -19.4],
["fm20", 2, -13.975, -19.65],
["fm21", [2, 1.8], -27.975, -12.05],
["fm22", [1.9, 2], -25.475, -10.95]
 ]
fund_list3=[
["fm1", 2.8, -33.775, -5.3],
["fm2", 2.9, -31.875, -0.5],
["fm3", 3, -27.975, -0.5],
["fm4", 2.9, -25.475, -5.3],
["fm5", 2.8, -23.1, -9.95],
["fm6", 3.3, -22.325, -13.2], 
["fm7", 0.9, -22.325, -15.3],
["fm8", 2.3, -18.225, -13.2],
["fm9", 2.3, -13.975, -13.2],
["fm10", 0.9, -13.975, -15.3],
["fm11", 2.9, -31.875, -9.95],
["fm12",  2.2, -30.725, -13.2],
["fm13",  2.3, -29.875, -15.3],
["fm14", 2.2, -28.675, -18.15],
["fm15", 2.3, -26.225, -18.4],
["fm16", 2, -23.775, -18.65],
["fm17", 1.9, -21.325, -18.9],
["fm18", 1.7, -18.875, -19.15],
["fm19", 1.8, -16.425, -19.4],
["fm20", 2, -13.975, -19.65],
["fm21", 2, -27.975, -12.05],
["fm22",  2, -25.475, -10.95]
 ]

f = fund_pdf(fund_list3)
f.print_pdf(path = "c:/lisp/grunt/grunt-otriv/base.pdf")
