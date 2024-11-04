import os
import pickle


#文件类
class FileStatus(object):
    def save(self):
        fpath = input("请输入保存路径：")
        file = open(fpath, 'wb')
        pickle.dump(self.file)
        file.close()

    def load(self):
        fpath = open('请输入棋盘路径：')
        if os.access(fpath, os.F_OK):
            file = open(fpath, 'rb+')
            status = pickle.load(file)
            file.close()
            return status
        else:
            print('输入路径错误！')
#文件类

#玩家类
class Player():
    number=0
    def __init__(self,name=''):
        if not name:
            Player.number+=1
            if Player.number==1:
                name = '白方下子'
            else:
                name = '黑方下子'
            #name='Play%d'%Player.number
        self.name=name
    def play(self):
        t=input("请输入落子点(X,Y)，现在由"+self.name +":")
        return t
#玩家类


#棋盘类
class Board():
    class Status(object):#棋位状态
        NONE = 0
        WHITE = 1
        BLACK = 2

    def __init__(self,maxx=10,maxy=10):
        self.maxx=maxx
        self.maxy=maxy
        self.Checkboard=[[0]*maxy for i in range(maxx)]
    def hasChessman(self,xPoint,yPoint):
        return self.Checkboard[xPoint][yPoint]!=Board.Status.NONE
    def downPawn(self,xPoint,yPoint,who):
        if self.hasChessman(xPoint,yPoint):
            print("该点已落子，请重下：")
            return False
        else:
            self.Checkboard[xPoint][yPoint]=Board.Status.BLACK if who else Board.Status.WHITE
            return True
    def inRange(self,xPoint,yPoint):
        return ((xPoint < self.maxx and xPoint >= 0) and (yPoint < self.maxy and yPoint >= 0))


    def checkFiverow(self,xPoint,yPoint,xDir,yDir):
        count = 0
        t = self.Checkboard[xPoint][yPoint]
        x, y = xPoint, yPoint
        while self.inRange(x, y) and t == self.Checkboard[x][y]:
            count += 1
            x -= xDir
            y -= yDir
        x, y = xPoint, yPoint
        while self.inRange(x, y) and t == self.Checkboard[x][y]:
            count += 1
            x += xDir
            y += yDir
        if count >= 5:
            return True
        else:
            return False

    def isWin(self,xPoint,yPoint):
        Result1 = self.checkFiverow(xPoint, yPoint, 1, 0)
        Result2 = self.checkFiverow(xPoint, yPoint, 0, 1)
        Result3 = self.checkFiverow(xPoint, yPoint, 1, 1)
        Result4 = self.checkFiverow(xPoint, yPoint, 1, -1)
        if (Result1 or Result2 or Result3 or Result4):
            return True
#棋盘类


    #显示棋盘
    def PrintCheckboard(self):
        print("            五子棋        ")
        print("   零 一 二 三 四 五 六 七 八 九       ")
        qiType=["空","黑","白"]
        for i in range(self.maxx):
            print(i,end='')
            print(' '.join(qiType[x] for x in self.Checkboard[i]))
    #显示棋盘

#游戏类
class Gobang(FileStatus):
    def __init__(self,checkboard,white,black):
        self.Checkboard=checkboard
        self.white=white
        self.black=black
        self.who=True
    def start(self):
        os.system('cls')
        self.PrintCheckboard()

        while True:
            t=(self.black if self.who else self.white).play()
            if t[0]=='S':
                self.save()
                continue
            if t[0]=='L':
                self.load()
                self.PrintCheckboard()
                continue
            t=t.split(',')
            if len(t)==2:
                x=int(t[0])
                y=int(t[1])
                if self.Checkboard.downPawn(x,y,self.who):
                    os.system('cls')
                    self.PrintCheckboard()
                    if self.Checkboard.isWin(x,y):
                        print(self.black.name if self.who else self.white.name)+'赢！'
                        break
                    self.who = not self.who
        os.system('pause')
    def PrintCheckboard(self):
        self.Checkboard.PrintCheckboard()
        print()
#游戏类


if __name__=='__main__':
    t=Gobang(Board(),Player(),Player())
    t.start()
