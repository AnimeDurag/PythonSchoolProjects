import random
class Character:
    '''
    Purpose:
        To be a base class for the Pretender and Crewperson classes
    Instance variables:
        self.name: name of the character
        self.color: string of what color the character is
        self.hat: string of what hat the character is wearing
        self.num_tasks: number of tasks that a character still has to complete
        self.status: boolean indicating whether the character is alive
        self.task_list: list of tasks with length num_tasks that need to be done
    Methods:
        __init__(self, name, color, hat, num_tasks): create instance variables
        for characters
        __repr__(self): returns a string containing the instance variables
        get_identity(self): returns the string 'Character'
    '''
    def __init__(self, name, color, hat, num_tasks):
        self.name = name
        self.color = color
        self.hat = hat
        self.num_tasks = num_tasks
        self.status = True
        given_tasks = ['Adjust engine output', 'Calibrate distributor',
        'Map course', 'Clear out O2 filter', 'Destroy asteroids',
        'Redirect power', 'Empty garbage', 'Secure wiring',
        'Fill engines tanks', 'Inspect laboratory', 'Move shields',
        'Steady steering','Initiate reactor', 'Submit personal info',
        'Sign in with ID', 'Enable manifolds', 'Sync data']
        self.task_list = []
        for i in range(num_tasks):
            task = random.choice(given_tasks)
            self.task_list.append(task)
            given_tasks.remove(task)

    def __repr__(self):
        if self.status == True:
            self.status = 'Alive'
        else:
            self.status = 'Ghost'
        return str(self.name) + ': ' + str(self.color) + ', wearing a ' + str(self.hat) + ' - Health status: ' + str(self.status)

    def get_identity(self):
        return 'Character'

class Crewperson(Character):
    '''
    Purpose:
        Specialization of Character class that is able to complete tasks
    Instance variables:
        See Character class documentation
    Methods:
        get_identity(self): returns the string 'Crewperson'
        complete_task(self): prints if a task or all tasks are completed and
        removes it unless it's an empty list
    '''
    def get_identity(self):
        return 'Crewperson'

    def complete_task(self):
        if self.task_list != []:
            print(self.name, 'completed the', self.task_list[0], 'task.')
            self.task_list.pop(0)
        else:
            print(self.name, 'has completed all their tasks.')

class Pretender(Character):
    '''
    Purpose:
        Specialization of Character class that allows them to eliminate other
        characters
    Instance variables:
        See Character class documentation
    Methods:
        get_identity(self): returns the string 'Pretender'
        eliminate(self, target): changes the health status of target and prints
        a string saying they were eliminated
    '''
    def get_identity(self):
        return 'Pretender'

    def eliminate(self, target):
        target.status = False
        print(self.name, 'eliminated', target.name + '.')

class Game:
    '''
    Purpose:
        Keep track of characters that are still alive and if either team has won
    Instance variables:
        self.player_list: contains a list of Crewperson and Pretender objects
    Methods:
        __init__(self, player_list): creates the player_list instance variable
        check_winner(self): Checks the status and numbers of each team and
        prints a statement of which team won or neither one does
        meeting(self):Characters that are alive vote for someone and either
        eliminates the most voted character or no one is voted off
        play_game(self): Until the game is won by either team, it simulates a
        full round of the game and checks the winner after each game method
    '''
    def __init__(self, player_list):
        self.player_list = player_list

    def check_winner(self):
        crew_alive = []
        pret_alive = []
        dead_crew = []
        dead_pret = []
        task_comp = []
        for player in self.player_list:
            if player.get_identity() == 'Crewperson':
                if player.status == False:
                    dead_crew.append(player)
                else:
                    crew_alive.append(player)
            elif player.get_identity() == 'Pretender':
                if player.status == False:
                    dead_pret.append(player)
                else:
                    pret_alive.append(player)
        for player in self.player_list:
            if (player.get_identity()=='Crewperson') and (player.task_list==[]):
                task_comp.append(player)

        if (len(task_comp) == (len(crew_alive) + len(dead_crew)) or
            pret_alive == []):
            print('Crewpersons win!')
            return 'C'
        elif len(pret_alive) >= len(crew_alive):
            print('Pretenders win!')
            return 'P'
        else:
            return '-'

    def meeting(self):
        meet_room = {}
        meet_keys = []
        for player in self.player_list:
            if player.status == True:
                meet_room[player] = 0
                meet_keys.append(player)
        for alive_ch in meet_keys:
            vote = random.choice(meet_keys)
            if vote == alive_ch:
                vote = random.choice(meet_keys)
                print(alive_ch.name, 'voted for', vote.name + '.')
                meet_room[vote] += 1
            else:
                print(alive_ch.name, 'voted for', vote.name + '.')
                meet_room[vote] += 1

        largest_vote = list(meet_room.values())
        for i in range(len(meet_keys)):
            if largest_vote.count(max(largest_vote)) > 1:
                print('Nobody was eliminated.')
                return None
            elif i == largest_vote.index(max(largest_vote)):
                print(meet_keys[i].name, 'was eliminated.')
                meet_keys[i].status == False
                return meet_keys[i].name

    def play_game(self):
        winning_key = '-'
        while winning_key == '-':
            for player in self.player_list:
                if player.get_identity() == 'Crewperson':
                    for i in range(random.randint(1,3)):
                        player.complete_task()
                elif player.get_identity() == 'Pretender' and player.status == True:
                    target = random.choice(self.player_list)
                    if target.get_identity()=='Crewperson' and target.status== True:
                        player.eliminate(target)
            winning_key = self.check_winner()
            if winning_key != '-':
                return winning_key
            self.meeting()
            winning_key = self.check_winner()
            if winning_key != '-':
                return winning_key
