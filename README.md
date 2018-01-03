# SuperHajusSudoku

## Technical description and startup

### In order to start the application
Starting with PyCharm, you should mark source directiory (where client, common, server... are located) as "Sources Root"

### Used libraries

Python 2.7

* TKinter - for building Graphical User Interface

## Program description

Program "SuperHajusSudoku" consists of three main modules:

Client- where all the client side of communication is located

Server- where all the server side of communication is located

Common- where all the common part of files are located, for server and client side both

## How to use the program

### First of all we have to start server side.

For that it's needed to open main program file **SuperHajusSudoku/server/main.py**

That will open the GUI, where it is needed to specify two parameters:

 1. Port number which is by default **7777**
 2. Server host number which is by default **127.0.0.1**, as a local ip address
 3. Then have to push the button **"Start server"**

![Server GUI](https://github.com/rennoraudmae/SuperHajusSudoku/blob/master/pictures/server.PNG)

It will create the Sudoku game server, in where, it is possible to start games


### Secondly must open the client side.

For that it's needed to open main program file **SuperHajusSudoku/client/main.py**

That will open the GUI, where it is needed to specify some parameters.

As it is multiplayer game, then that point can be done in two variations

**If there is only *one client*, then you must open the new game as well:**

1. Specify the same port number, as you added for server.
2. Insert the same ip address, as server has.
3. Insert the username - it can be chosen from right side of a program "Choose a nickname"
   or specified by user, but it must be at least 8 characters.
4. After that push the button {Connect to server}.

![Client GUI](https://github.com/rennoraudmae/SuperHajusSudoku/blob/master/pictures/client_1.PNG)


5. Then you have to fill the blanks:
   - (insert new game) where the new game name must be specified.
   - (insert the max players number) have to enter the number how many players can play current game.
6. And then create game button

![Client GUI create game](https://github.com/rennoraudmae/SuperHajusSudoku/blob/master/pictures/client_2.png)


6. Under Available games should appear: the name of the game.
7. In the blank - (insert game id) you have enter the name from list of Available games.

![Client GUI join game](https://github.com/rennoraudmae/SuperHajusSudoku/blob/master/pictures/client_3.PNG)

For example:

- create new game: new_sudoku
- max players: 3
- Available games: new_sudoku
- Join a game inserting id: new_sudoku

8. If all the blanks are filled then push the button {Join game}.
9. Finally the sudoku game_field will appear and you can start to play.
10. For playing, you must follow the rules of sudoku, if you didn't know yet how to play then just type into google search
    sudoku basics or something and then you can start to guess numbers. Server will send you feedback numbers on gamefield.

**Second Option to join the game, if game is already created**

Steps from 1.-4. are basically the same:

1. Specify the same port number, as you added for server.
2. Insert the same ip address, as server has.
3. Insert the username: By logically taken, this should be different from previous player to recognize different players.
4. After that push the button {Connect to server}.
5. In here we can specify new game as described above in point 5. or we can just join with the game which is already
   created. As under Available games should appear "new_sudoku", because previous player/client already made it.
   So we can just join with the available game.
6. If new_sudoku or whatever name of the game is inserted into blank "join a game inserting id" then we can start to play
   along by clicking {Join game}.
7. And again the sudoku game_field will appear and you can start to play.
8. For playing, you must follow the rules of sudoku, if you didn't know yet how to play then just type into google search
    sudoku basics or something and then you can start to guess numbers. Server will send you feedback numbers on gamefield.

![Client GUI gameplay](https://github.com/rennoraudmae/SuperHajusSudoku/blob/master/pictures/client_4.PNG)


**For leaving the game just push the button under game field "leave game"**





