import tkinter,math,random
from tkinter import ttk,messagebox
from datetime import datetime
window=tkinter.Tk(className="Симуляция перекрёстка")
current_phase=0
phases_delays=[1,10,1,1,2]
phases_current_delays=phases_delays.copy()
blinking=False
blinking_delay=0.5
phases_colors=("#000","#0F0","#FF0","#F00","#F80")
cars=[]
cars_colors=("#000","#800","#D11","#090","#3A1","#005","#12C","#981")
cars_spawn_min_delays=[1.5,1.5,1.5,1.5]
cars_spawn_max_delays=[4,4,4,4]
cars_spawn_delays=[random.uniform(cars_spawn_min_delays[direction],cars_spawn_max_delays[direction]) for direction in range(4)]
relative_directions_probabilities=[[50 for _ in range(4)] for _ in range(4)]
last_cars_from=[None for _ in range(4)]




def change_current_phase(phase):#СМЕНА ФАЗ СВЕТОФОРОВ
    global current_phase,blinking
    current_phase=phase
    canvas.itemconfigure("light",fill="#000")
    index=phase%5+1*(phase>=5)
    
  
    if phase==0:
        blinking=False
    elif phase==1:
        blinking=False
        blinking_delay=0
        canvas.itemconfigure("0green",fill="#0F0")
        canvas.itemconfigure("1red",fill="#F00")
    elif phase==2:
        canvas.itemconfigure("0yellow",fill="#FF0")
        canvas.itemconfigure("1red",fill="#F00")
    elif phase==3 or phase==7:
        canvas.itemconfigure("0red",fill="#F00")
        canvas.itemconfigure("1red",fill="#F00")
    elif phase==4:
        canvas.itemconfigure("0red",fill="#F00")
        canvas.itemconfigure("1red",fill="#F00")
        canvas.itemconfigure("1yellow",fill="#FF0")
    elif phase==5:
        blinking=False
        blinking_delay=0
        canvas.itemconfigure("0red",fill="#F00")
        canvas.itemconfigure("1green",fill="#0F0")
    elif phase==6:
        canvas.itemconfigure("0red",fill="#F00")
        canvas.itemconfigure("1yellow",fill="#FF0")
    elif phase==8:
        canvas.itemconfigure("0red",fill="#F00")
        canvas.itemconfigure("0yellow",fill="#FF0")
        canvas.itemconfigure("1red",fill="#F00")



def traffic_lights_update(dt):#ОБНОВЛЕНИЕ СОСТОЯНИЯ СВЕТОФОРОВ
    global current_phase,blinking,blinking_delay
    index=current_phase%5+1*(current_phase>=5)
    phases_current_delays[index]-=dt
    if phases_current_delays[index]<=0:
        phases_current_delays[index]=phases_delays[index]
        if current_phase:
            change_current_phase((current_phase+1)%9+(current_phase==8))
        else:
            blinking=not blinking
            if blinking:
                canvas.itemconfigure("0yellow",fill="#FF0")
                canvas.itemconfigure("1yellow",fill="#FF0")
            else:
                canvas.itemconfigure("0yellow",fill="#000")
                canvas.itemconfigure("1yellow",fill="#000")
    if current_phase:
        
        if (current_phase==1 or current_phase==5) and phases_current_delays[index]<=3:
            blinking_delay-=dt
            if blinking_delay<=0:
                blinking_delay=0.5
                blinking=not blinking
                if current_phase==1:
                    tag="0green"
                else:
                    tag="1green"
                if blinking:#Мигаем
                    canvas.itemconfigure(tag,fill="#000")
                else:
                    canvas.itemconfigure(tag,fill="#0F0")



class Car:
    max_length,min_length,max_width,min_width=50,40,30,20
    max_speed=80
    def __init__(self,from_direction,to_direction,speed):
        self.from_direction,self.to_direction=from_direction,to_direction
        self.turn=(self.to_direction-self.from_direction)
        if from_direction==0:
            self.x=canvas_width/2-25
            self.y=-50
            self.rotation=0.5*math.pi
        elif from_direction==1:
            self.x=canvas_width+50
            self.y=canvas_height/2-25
            self.rotation=math.pi
        elif from_direction==2:
            self.x=canvas_width/2+25
            self.y=canvas_height+50
            self.rotation=1.5*math.pi
        else:
            self.x=-50
            self.y=canvas_height/2+25
            self.rotation=0
        self.speed=speed
        self.acceleration=0
        self.next_car=last_cars_from[from_direction]
        self.prev_car=None
        last_cars_from[from_direction]=self
        if self.next_car:
            self.next_car.prev_car=self
        self.length=random.randint(self.min_length,self.max_length)
        self.width=random.randint(self.min_width,self.max_width)
        self.color=random.choice(cars_colors)
        self.phase=0
    def move(self,dt):#Метод перемещения
        self.speed=max(0,min(self.speed+self.acceleration*dt,self.max_speed))
        self.x+=self.speed*dt*math.cos(self.rotation)
        self.y+=self.speed*dt*math.sin(self.rotation)
    def update(self,dt):
        if self.phase==0:
            if self.next_car:
                if self.from_direction==0:
                    rast=self.next_car.y-self.next_car.length/2-self.y-self.length/2
                elif self.from_direction==1:
                    rast=self.x-self.length/2-self.next_car.x-self.next_car.length/2
                elif self.from_direction==2:
                    rast=self.y-self.length/2-self.next_car.y-self.next_car.length/2
                else:
                    rast=self.next_car.x-self.next_car.length/2-self.x-self.length/2
        elif self.phase==1:
            self.acceleration=self.max_speed
        self.move(dt)
    def draw(self):
        canvas.create_polygon(self.x-self.length/2*math.cos(self.rotation)+self.width/2*math.sin(self.rotation),self.y-self.width/2*math.cos(self.rotation)-self.length/2*math.sin(self.rotation),self.x+self.length/2*math.cos(self.rotation)+self.width/2*math.sin(self.rotation),self.y-self.width/2*math.cos(self.rotation)+self.length/2*math.sin(self.rotation),self.x+self.length/2*math.cos(self.rotation)-self.width/2*math.sin(self.rotation),self.y+self.width/2*math.cos(self.rotation)+self.length/2*math.sin(self.rotation),self.x-self.length/2*math.cos(self.rotation)-self.width/2*math.sin(self.rotation),self.y+self.width/2*math.cos(self.rotation)-self.length/2*math.sin(self.rotation),fill=self.color,tags=("car"))#Создаём полигон по нужным координатам нужного цвета
menu=tkinter.Menu(window)#верхнее меню
def start_stop_pressed():#Функция запуска или остановки симуляции
    global current_phase,cars,last_cars_from
    if current_phase:
        window.resizable(True,True)
        change_current_phase(0)
        for car in cars:
            del car.next_car
            del car.prev_car
        cars=[]
        canvas.delete("car")
        menu.entryconfigure(1,label="Запустить симуляцию")
    else:
        window.resizable(False,False)
        change_current_phase(random.randint(1,6))
        menu.entryconfigure(1,label="Сбросить симуляцию")
menu.add_command(label="Запустить симуляцию",command=start_stop_pressed)
def help_pressed():
    help_window=tkinter.Toplevel(window)
    help_window.title("Помощь")
    tkinter.Label(help_window,padx=5,pady=10,text="Здесь будет инструкция по работе с приложением.").pack(fill="y")
menu.add_command(label="Помощь",command=help_pressed)
def about_pressed():
    about_window=tkinter.Toplevel(window)
    about_window.title("О программе")
    tkinter.Label(about_window,padx=10,pady=5,text="Эта программа позволяет смоделировать движение на перекрестке. \nПерекрёсток является регулируемым. Автомобили могут двигаться во всех возможных направлениях.").pack(fill="x")
menu.add_command(label="О программе",command=about_pressed)
window.config(menu=menu)


canvas=tkinter.Canvas(window,width=500,height=500,bg="gray")
canvas.pack(side=tkinter.RIGHT,fill="both",expand=True)
canvas_width,canvas_height=0,0


def resize_canvas(event): #Окно основное
    global canvas_width,canvas_height
    canvas.delete("all")
    x_center=event.width/2
    y_center=event.height/2
    canvas.create_line(0,y_center,event.width,y_center,width=100,fill="#666666")
    canvas.create_line(0,y_center,event.width,y_center,width=5,fill="#FFFFFF")
    canvas.create_line(x_center,0,x_center,event.height,width=100,fill="#666666")
    canvas.create_line(x_center,0,x_center,event.height,width=5,fill="#FFFFFF")
    canvas.create_rectangle(x_center-50,y_center-50,x_center+50,y_center+50,fill="#666666",width=0)
    canvas.create_rectangle(x_center-75,y_center-115,x_center-55,y_center-55,fill="#444444")
    canvas.create_oval(x_center-73,y_center-113,x_center-57,y_center-97,fill="#000000",tags=("0green","light"))
    canvas.create_oval(x_center-73,y_center-93,x_center-57,y_center-77,fill="#000000",tags=("0yellow","light"))
    canvas.create_oval(x_center-73,y_center-73,x_center-57,y_center-57,fill="#000000",tags=("0red","light"))
    canvas.create_rectangle(x_center+55,y_center-75,x_center+115,y_center-55,fill="#444444")
    canvas.create_oval(x_center+57,y_center-73,x_center+73,y_center-57,fill="#000000",tags=("1red","light"))
    canvas.create_oval(x_center+77,y_center-73,x_center+93,y_center-57,fill="#000000",tags=("1yellow","light"))
    canvas.create_oval(x_center+97,y_center-73,x_center+113,y_center-57,fill="#000000",tags=("1green","light"))
    canvas.create_rectangle(x_center+55,y_center+55,x_center+75,y_center+115,fill="#444444")
    canvas.create_oval(x_center+57,y_center+57,x_center+73,y_center+73,fill="#000000",tags=("0red","light"))
    canvas.create_oval(x_center+57,y_center+77,x_center+73,y_center+93,fill="#000000",tags=("0yellow","light"))
    canvas.create_oval(x_center+57,y_center+97,x_center+73,y_center+113,fill="#000000",tags=("0green","light"))
    canvas.create_rectangle(x_center-115,y_center+55,x_center-55,y_center+75,fill="#444444")
    canvas.create_oval(x_center-113,y_center+57,x_center-97,y_center+73,fill="#000000",tags=("1green","light"))
    canvas.create_oval(x_center-93,y_center+57,x_center-77,y_center+73,fill="#000000",tags=("1yellow","light"))
    canvas.create_oval(x_center-73,y_center+57,x_center-57,y_center+73,fill="#000000",tags=("1red","light"))
    change_current_phase(current_phase)
    for car in cars:
        car.x+=(event.width-canvas_width)/2
        car.y+=(event.height-canvas_height)/2
    canvas_width,canvas_height=event.width,event.height
canvas.bind("<Configure>",resize_canvas)
window.update()

#анимация
window.minsize(window.winfo_width(),window.winfo_height())
last_update=datetime.now()
while True:
    now=datetime.now()
    dt=(now-last_update).total_seconds()
    last_update=now
    traffic_lights_update(dt)
    if current_phase:
        for direction in range(4):
            cars_spawn_delays[direction]-=dt
            if cars_spawn_delays[direction]<=0:
                cars_spawn_delays[direction]=random.uniform(cars_spawn_min_delays[direction],cars_spawn_max_delays[direction])
                if (not last_cars_from[direction]) or (direction==0 and last_cars_from[direction].y-last_cars_from[direction].length/2>-50+Car.max_length/2+5) or (direction==1 and last_cars_from[direction].x+last_cars_from[direction].length/2<canvas_width+50-Car.max_length/2-5) or (direction==2 and last_cars_from[direction].y+last_cars_from[direction].length/2<canvas_height+50-Car.max_length/2-5) or (direction==3 and last_cars_from[direction].x-last_cars_from[direction].length/2>-50+Car.max_length/2+5):
                    total=sum(relative_directions_probabilities[direction])
                    if total:
                        destinations_probabilities=[]
                        for destination in range(4):
                                 destinations_probabilities.append(relative_directions_probabilities[direction][destination]/total)
                        choice=random.random()
                        for side in range(4):
                            if choice<=destinations_probabilities[side]:
                                destination=side
                                break
                            else:
                                choice-=destinations_probabilities[side]
                    else:
                        destination=random.choice(range(4))
                    if last_cars_from[direction]:
                        speed=last_cars_from[direction].speed
                    else:
                        speed=Car.max_speed
                    cars.append(Car(direction,destination,speed))
        canvas.delete("car")
        for car in cars:
            car.update(dt)
        for car in cars:
            car.draw()
    window.update()
