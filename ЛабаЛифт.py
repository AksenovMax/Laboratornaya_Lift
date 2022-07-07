from tkinter import *
import telebot
from threading import Thread

TOKEN = "5180806406:AAFWKuw_9kJItZWXEQWGvbAip-ip5q0lA-s"

bott = telebot.TeleBot(TOKEN)


def lift_control():
    @bott.message_handler(commands=['start'])
    def start(message):
        bott.send_message(message.chat.id, text="Какой этаж")

    @bott.message_handler(content_types=['text'])
    def etaj(message):
        if message.text == '4':
            click_btn4_cabina()
        if message.text == '3':
            click_btn3_cabina()
        if message.text == '2':
            click_btn2_cabina()
        if message.text == '1':
            click_btn1_cabina()

    class lift:
        def __init__(self):
            self.position = 0
            self.min_position = 0
            self.max_position = 500
            self.size = 110
            self.Kdn = 0
            self.Kup = 0
            self.sq1 = 0
            self.sq2 = 0
            self.sq3 = 0
            self.sq4 = 0
            self.b1_cabina = 0
            self.b2_cabina = 0
            self.b3_cabina = 0
            self.b4_cabina = 0
            self.bstop_cabina = 0
            self.b1_wall = 0
            self.b2_wall = 0
            self.b3_wall = 0
            self.b4_wall = 0
            self.lift_image = canvas.create_rectangle(0, self.position, 300,  self.position + self.size, width=2,fill="grey")
            self.sq1_image = canvas.create_rectangle(200, 105, 250, 115, width=2, fill="black")
            self.sq2_image = canvas.create_rectangle(200, 205, 250, 215, width=2, fill="black")
            self.sq3_image = canvas.create_rectangle(200, 305, 250, 315, width=2, fill="black")
            self.sq4_image = canvas.create_rectangle(200, 405, 250, 415, width=2, fill="black")

        def __lift_work__(self):
           if (self.Kdn == 1):
               self.position = self.position - 1
           if (self.Kup == 1):
               self.position = self.position + 1

           if (self.position < self.min_position):
               self.position = self.min_position
           if (self.position > self.max_position):
               self.position = self.max_position

           if (self.position >90)&((self.position <110)):
               self.sq1 = 1; canvas.itemconfig(self.sq1_image,fill = "red")
           else:
               self.sq1 = 0;canvas.itemconfig(self.sq1_image, fill="black")

           if (self.position >190)&((self.position <210)):
               self.sq2 = 1
               canvas.itemconfig(self.sq2_image, fill="red")
           else:
               self.sq2 = 0
               canvas.itemconfig(self.sq2_image, fill="black")

           if (self.position >290)&((self.position <310)):
               self.sq3 = 1
               canvas.itemconfig(self.sq3_image, fill="red")
           else:
               self.sq3 = 0
               canvas.itemconfig(self.sq3_image, fill="black")

           if (self.position >390) & ((self.position < 410)):
               self.sq4 = 1
               canvas.itemconfig(self.sq4_image, fill="red")
           else:
               self.sq4 = 0
               canvas.itemconfig(self.sq4_image, fill="black")

           canvas.delete(self.lift_image)
           self.lift_image = canvas.create_rectangle(0, self.position, 200, self.position + self.size, width=2,fill="grey")

    class door:
        def __init__(self):
            self.sq_open = 0
            self.sq_close = 0
            self.Kopen = 0
            self.Kclose = 0
            self.position = 100
            self.max_position = 100
            self.vert_position = 0
            self.high = 90 #высота двери
            self.width = self.max_position / 2
            self.left_door_image = canvas.create_rectangle(0, self.vert_position,
                                                           self.position,self.vert_position+self.high,
                                                           width=2, fill="brown")
            self.right_door_image = canvas.create_rectangle(self.max_position - self.position, self.vert_position,
                                                            self.max_position, self.vert_position + self.high,
                                                            width=2, fill="brown")

        def __door_work__(self):
            if self.Kopen == 1:
                self.position = self.position - 1
            if self.Kclose == 1:
                self.position = self.position + 1

            self.sq_close = 0
            self.sq_open = 0

            if self.position >= self.max_position:
                self.position = self.max_position
                self.sq_close = 1

            if self.position <=0:
                self.position = 0
                self.sq_open = 1


            canvas.delete(self.left_door_image)
            canvas.delete(self.right_door_image)
            self.left_door_image = canvas.create_rectangle(0, self.vert_position, self.position,
                                                           self.vert_position + self.high, width=2,
                                                           fill="brown")
            self.right_door_image = canvas.create_rectangle(self.max_position*2 - self.position, self.vert_position,
                                                           self.max_position*2,
                                                           self.vert_position + self.high, width=2,
                                                           fill="brown")

    def lift_control():
        nonlocal state_lift
        nonlocal state_door
        nonlocal stall_timer
# состояние ОСТАНОВЛЕНО
        stall_timer = stall_timer + 1
        if (state_lift == 1):
            stall_timer = 0
            lift.Kdn = 0
            lift.Kup = 0

            if (lift.b1_wall == 1)|(lift.b1_cabina == 1):
                if lift.sq1 == 0:
                    if state_door == 1:
                        state_lift = 2

            if (lift.b2_wall == 1)|(lift.b2_cabina == 1):
                if lift.sq2 == 0 and lift.position < 190:
                    if state_door == 1:
                        state_lift = 3

            if (lift.b2_wall == 1)|(lift.b2_cabina == 1):
                if lift.sq2 == 0 and lift.position > 210:
                    if state_door == 1:
                        state_lift = 7

            if (lift.b3_wall == 1)|(lift.b3_cabina == 1):
                if lift.sq3 == 0 and lift.position < 290:
                    if state_door == 1:
                        state_lift = 4

            if (lift.b3_wall == 1)|(lift.b3_cabina == 1):
                if lift.sq3 == 0 and lift.position > 310:
                    if state_door == 1:
                        state_lift = 6

            if (lift.b4_wall == 1)|(lift.b4_cabina == 1):
                if lift.sq4 == 0:
                    if state_door == 1:
                        state_lift = 5

            if lift.bstop_cabina == 1:
                state_lift = 1

################################### 1 этаж
        if (state_lift == 2):
            lift.Kdn = 1
            lift.Kup = 0

            if lift.sq1 == 1:
               state_lift = 1
               state_door = 2
            if lift.bstop_cabina == 1:
                state_lift = 1

            if (stall_timer>500):
                state_lift = 1



################################ 2 этаж
        if (state_lift == 3):
            lift.Kdn = 0
            lift.Kup = 1

            if lift.sq2 == 1:
                state_lift = 1
                state_door = 2
            if lift.bstop_cabina == 1:
                state_lift = 1

            if (stall_timer>500):
                state_lift = 1

        if (state_lift == 7):
            lift.Kdn = 1
            lift.Kup = 0

            if lift.sq2 == 1:
                state_lift = 1
                state_door = 2
            if lift.bstop_cabina == 1:
                state_lift = 1

            if (stall_timer>500):
                state_lift = 1
##################################### 3 этаж
        if (state_lift == 4):
            lift.Kdn = 0
            lift.Kup = 1

            if lift.sq3 == 1:
                state_lift = 1
                state_door = 2
            if lift.bstop_cabina == 1:
                state_lift = 1

            if (stall_timer>500):
                state_lift = 1

        if (state_lift == 6):
            lift.Kdn = 1
            lift.Kup = 0

            if lift.sq3 == 1:
                state_lift = 1
                state_door = 2
            if lift.bstop_cabina == 1:
                state_lift = 1

            if (stall_timer>500):
                state_lift = 1

###################################### 4 этаж
        if (state_lift == 5):
            lift.Kdn = 0
            lift.Kup = 1

            if lift.sq4 == 1:
                state_lift = 1
                state_door = 2
            if lift.bstop_cabina == 1:
                state_lift = 1

            if (stall_timer>500):
                state_lift = 1


    def door_control():
        nonlocal  state_door
        nonlocal  state_lift
        nonlocal  timer
        if state_door == 1:
            door.Kclose = 0
            door.Kopen = 0
            if lift.b1_wall ==1:
                state_door = 2
            if lift.b2_wall ==1:
                state_door = 2
            if lift.b3_wall ==1:
                state_door = 2
            if lift.b4_wall ==1:
                state_door = 2
            if state_lift>1:
                state_door = 1

        if state_door == 2:
            door.Kclose = 0
            door.Kopen = 1
            timer = 0
            if door.sq_open == 1:
                state_door = 3

        if state_door == 3:
            door.Kclose = 0
            door.Kopen = 0
            timer = timer + 1
            if timer > 10:
                state_door = 4

        if state_door == 4:
            door.Kclose = 1
            door.Kopen = 0
            if door.sq_close == 1:
                state_door = 1


    def work():
        lift.__lift_work__()
        door.vert_position = lift.position
        door.__door_work__()

        lift_control()
        door_control()

        #print("лифт = ",state_lift, " b1wall=",lift.b1_wall," b2wall=",lift.b2_wall, " door=",state_door)

        lift.b1_cabina = lift.b1_wall = lift.b2_cabina = lift.b2_wall =lift.b3_cabina = lift.b3_wall= lift.b4_cabina = lift.b4_wall= 0
        lift.bstop_cabina = 0
        root.after(10, work)

    def click_btn1_cabina():
        lift.b1_cabina = 1

    def click_btn2_cabina():
        lift.b2_cabina = 1

    def click_btn3_cabina():
        lift.b3_cabina = 1

    def click_btn4_cabina():
        lift.b4_cabina = 1

    def click_btnstop_cabina():
        lift.bstop_cabina = 1

    def click_btn1_wall():
        lift.b1_wall = 1

    def click_btn2_wall():
        lift.b2_wall = 1

    def click_btn3_wall():
        lift.b3_wall = 1

    def click_btn4_wall():
        lift.b4_wall = 1

    WallMaxY = 500
    WallMaxX = 1000
    mode = 0

    state_lift = 1
    state_door = 1
    timer = 0
    stall_timer = 0

    root = Tk()
    root.geometry("1000x500")
    root.title("LIFT STATION CONTROL")
    canvas=Canvas(root,height=WallMaxY, width = WallMaxX)
    canvas.place(x=0,y=0)
    canvas.create_rectangle(0,0,WallMaxX,WallMaxY,width = 10 )
    canvas.create_rectangle(700, 0, WallMaxX, WallMaxY, width=10,fill = "grey")
    lift = lift()
    door = door()
    work()

    btn1_cabina = Button(canvas, background = "#555",padx = 20,pady = 20, text = "Кабина Этаж 1",command = click_btn1_cabina)
    btn1_cabina.place(x=800,y=20)
    btn2_cabina = Button(canvas, background = "#555", padx=20, pady=20, text="Кабина Этаж 2", command=click_btn2_cabina)
    btn2_cabina.place(x=800, y=120)
    btn3_cabina = Button(canvas, background = "#555", padx=20, pady=20, text="Кабина Этаж 3", command=click_btn3_cabina)
    btn3_cabina.place(x=800, y=220)
    btn3_cabina = Button(canvas, background = "#555", padx=20, pady=20, text="Кабина Этаж 4", command=click_btn4_cabina)
    btn3_cabina.place(x=800, y=320)
    btnstop_cabina = Button(canvas, background = "#555", padx=20, pady=20, text="Кабина СТОП", command=click_btnstop_cabina)
    btnstop_cabina.place(x=800, y=420)

    btn1_wall = Button(canvas, background="#955", padx=20, pady=20, text="Стена Этаж 1", command=click_btn1_wall)
    btn1_wall.place(x=300, y=120)
    btn2_wall = Button(canvas, background="#955", padx=20, pady=20, text="Стена Этаж 2", command=click_btn2_wall)
    btn2_wall.place(x=300, y=220)
    btn3_wall = Button(canvas, background="#955", padx=20, pady=20, text="Стена Этаж 3", command=click_btn3_wall)
    btn3_wall.place(x=300, y=320)
    btn3_wall = Button(canvas, background="#955", padx=20, pady=20, text="Стена Этаж 4", command=click_btn4_wall)
    btn3_wall.place(x=300, y=420)

    root.mainloop()


if __name__ == "__main__":
    def botty():
        bott.polling(none_stop=True)

    def tkntr():
        lift_control()

    def threading():
        t1 = Thread(target=botty)
        t2 = Thread(target=tkntr)
        t2.start()
        t1.start()

    threading()