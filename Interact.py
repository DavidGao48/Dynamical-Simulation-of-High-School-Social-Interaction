from tkinter import *
import random

class Student():

    colors = ['#000000', '#FF0000', '#00FF00', '#0000FF', '#999900', '#FF00FF', '#00FFFF', '#6CFFBB', '#6CBBFF', '#FF6CBB', '#FFBB6C', '#BBFF6C', '#BB6CFF']
    eta = 3
    listStudents = []  # This is where I store coordinates, directions of movements, and lists of friends

    def __init__(self, campus, number, pos, v, ethnicity, boarding, gender, year):
        '''
            :param campus: the canvas to draw on
            :param x:x coordinate of the circle
            :param y:y coordinate of the circle
            '''

        self.campus = campus
        self.studentID = number
        self.pos = pos
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.v = v
        self.friends = []

        self.ethnicity = ethnicity
        self.boarding = boarding
        self.gender = gender
        self.year = year

        self.k = 0.1
        self.alpha = 0.1
        self.beta = 0.1
        self.base = 1.1
        self.pSevere = 0.001

        self.distanceOrderK = 0

        self.id = self.campus.create_oval(pos[0], pos[1], pos[0] + 10, pos[1] + 10, outline = Student.colors[self.ethnicity], fill = Student.colors[self.ethnicity])


        return

    def frame(self):

        self.campus.move(self.id, self.v[0], self.v[1])

        for s in self.friends:

            if random.random()<self.pSevere:

                self.severeF(s)

        self.pos = [self.pos[0]+self.v[0], self.pos[1]+self.v[1]]
        self.x = self.pos[0]
        self.y = self.pos[1]

        return

    def p(self):

        '''
                Assigns a probability distribution of the direction the student can move in
                :param identity: the student number
                :return: the probability distribution list
                '''

        '''
        Note: This is the function that needs research in sociology to back up
        This will be the focus of my Capstone project next year.

        u (Utility) is an important matrix. We manipulate this matrix: essentially, if we want to
        increase the chance of a student moving in a certain direction, we just increase the value of this direction
        in this list.

        The most primitive functionality of this list is to ensure that students don't move outside of the campus.
        Thus, when we declare the list below, we start with the factor for moving in each direction equal to the
        distance from the edge in that direction.
        '''

        mu = [0,0]

        for s1 in Student.listStudents:

            if s1.studentID!=self.studentID:

                f1 = 0

                if s1.ethnicity==self.ethnicity: f1+=self.alpha
                else: f1-=self.beta
                if s1 in self.friends: f1+=self.k

                dx = s1.x-self.x
                dy = s1.y-self.y

                if dx!=0 and dy!=0:

                    fVecX = f1*dx/((dx**2+dy**2) ** (0.5 - self.distanceOrderK))
                    fVecY = f1*dy/((dx**2+dy**2) ** (0.5 - self.distanceOrderK))

                    mu[0]+=fVecX
                    mu[1]+=fVecY
        '''
        now we turn the distribution factor list into a probability distribution.
        we simply divide each factor by the sum of all factors,
        such that the ratio between each factor remains the same,
        while the sum becomes 1.
        '''


        pX = [1-1/(1+self.base**mu[0]), 1/(1+self.base**mu[0])]
        pY = [1-1/(1+self.base**mu[1]), 1/(1+self.base**mu[1])]

        for i in range(0, 2):

            if 1200 * i + ((-1) ** (i)) * self.x <= 20:
                pX[i] = 1
                pX[(i-1)**2] = 0

            if 500 * i + ((-1) ** (i)) * self.y <= 20:
                pY[i] = 1
                pY[(i - 1) ** 2] = 0

        return [pX,pY]

    def assignV(self, pX, pY):

        v = [0,0]

        seed = random.random()
        if seed<pX[0]: v[0] = 10
        else: v[0] = -10

        seed = random.random()
        if seed<pY[0]: v[1] = 10
        else: v[1] = -10

        self.v = v
        return

    def severeF(self, s1):

        for i in range(0,len(self.friends)-1):

            if self.friends[i].studentID==s1.studentID:

                self.friends.pop(i)

        for i in range(0,len(s1.friends)-1):

            if s1.friends[i].studentID==self.studentID:

                s1.friends.pop(i)


        for i in range(0,len(Friendships.listFriendships)-1):

            if (Friendships.listFriendships[i].s1.studentID==self.studentID and Friendships.listFriendships[i].s2.studentID==s1.studentID) or (Friendships.listFriendships[i].s2.studentID==self.studentID and Friendships.listFriendships[i].s1.studentID==s1.studentID):

                self.campus.delete(Friendships.listFriendships[i].id)
                Friendships.listFriendships.pop(i)

class Friendships():

    listFriendships = []
    drawlines = False

    def __init__(self, campus, s1, s2):

        self.campus = campus

        self.s1 = s1
        self.s2 = s2

        if Friendships.drawlines:
            self.id = self.campus.create_line(s1.pos[0]+5, s1.pos[1]+5, s2.pos[0]+5, s2.pos[1]+5, fill = "grey")

        else:
            self.id = self.campus.create_line(s1.pos[0] + 5, s1.pos[1] + 5, s2.pos[0] + 5, s2.pos[1] + 5, fill="grey", state = "hidden")

    def update(self):

        if Friendships.drawlines:
            self.campus.delete(self.id)
            self.id = self.campus.create_line(self.s1.pos[0]+5, self.s1.pos[1]+5, self.s2.pos[0]+5, self.s2.pos[1]+5, fill = "grey")

        return

class Graphics():

    def __init__(self):

        self.root = Tk()

        self.campus = Canvas(self.root, width=1200, height=600, background="white")
        self.campus.place(x=10, y=10)


        for i in range(0, 100):
            self.newStudent(i)


        # self.animate()

        self.button = Button(self.root, width=15, text="animate", command=self.animate)
        self.button.place(x=1210, y=200)

        self.button = Button(self.root, width=15, text="admission", command=self.admission)
        self.button.place(x=800, y=700)

        self.button = Button(self.root, width=15, text="lineSwitch", command=self.lineSwitch)
        self.button.place(x=1210, y=400)

        self.t = 0
        self.tag = self.campus.create_text(100,550,font=15, text = "t = "+str(self.t/100))

        k = Student.listStudents[0].k
        alpha = Student.listStudents[0].alpha
        beta = Student.listStudents[0].beta
        base = Student.listStudents[0].base
        eta = Student.eta
        pSevere = Student.listStudents[0].pSevere

        self.inf = self.campus.create_text(500,550,font=15, text = "k = "+str(k)+" alpha = "+str(alpha)+" beta = "+str(beta)+" base = "+str(base)+" eta = "+str(eta)+" pSevere = "+str(pSevere))

        if Friendships.drawlines == True:
            lineOnOff = "on"
        else:
            lineOnOff = "off"
        self.displayFriendship = self.campus.create_text(1000,550,font = 15, text = "displayFriendship = "+lineOnOff)

        mainloop()


    def newStudent(self,num):
        '''
        Creates a new student number, and stores the characteristics of this student in the listIdentity
        :return: void
        '''

        pos = [random.randint(50, 1150), random.randint(50, 450)]

        v = [random.randint(-1,1),random.randint(-1,1)]

        Student.listStudents.append(Student(self.campus, num,pos,v,ethnicity=random.randint(0,Student.eta-1),boarding=0,gender=0,year=0))

        return

    def animate(self):

        '''
        Starts the circles moving. Recursive.
        :return: void
        '''

        for x in range(0, len(Student.listStudents)):
            Student.listStudents[x].frame()
            Student.listStudents[x].assignV(Student.listStudents[x].p()[0], Student.listStudents[x].p()[1])

        self.friendsUpdate()

        for x in range(0, len(Friendships.listFriendships)):
            Friendships.listFriendships[x].update()

        self.t+=1
        self.campus.itemconfig(self.tag, text = "t = "+str(self.t/100))

        if Friendships.drawlines == True:
            lineOnOff = "on"
        else:
            lineOnOff = "off"
        self.campus.itemconfig(self.displayFriendship, text="displayFriendship = " + lineOnOff)

        self.campus.after(1, self.animate)

    def friendsUpdate(self):

        for i in range(0, len(Student.listStudents)):

            for j in range(i + 1, len(Student.listStudents)):

                s1 = Student.listStudents[i]
                s2 = Student.listStudents[j]

                if (not s1 in s2.friends) and (not s2 in s1.friends) and (((s1.pos[0] - s2.pos[0]) ** 2 + (s1.pos[1] - s2.pos[1]) ** 2) <= 200):
                    s1.friends.append(s2)
                    s2.friends.append(s1)
                    Friendships.listFriendships.append(Friendships(self.campus,s1,s2))

        return

        # End of Graphics

    def admission(self):


        for i in range(0,10):
            pos = [random.randint(50, 1150), random.randint(50, 450)]

            v = [random.randint(-1, 1), random.randint(-1, 1)]

            Student.listStudents.append(
                Student(self.campus, len(Student.listStudents), pos, v, ethnicity=random.randint(0, Student.eta-1), boarding=0, gender=0, year=0))


    def lineSwitch(self):

        if Friendships.drawlines==True:

            Friendships.drawlines = False

            for i in range(0,len(Friendships.listFriendships)):

                self.campus.delete(Friendships.listFriendships[i].id)

        else:

            Friendships.drawlines = True

Graphics()