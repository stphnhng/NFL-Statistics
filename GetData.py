import nflgame
import re

games = nflgame.games(2017)


# Code to find 1 or 2 point conversion percentages
def conversionPercentage():
    onePointAttempt = 0
    onePointSucceed = 0

    twoPointAttempt = 0
    twoPointSucceed = 0

    plays = nflgame.combine_plays(games)
    for key in plays:
        playString = str(key)
        if "two-point conversion" in playString.lower():
            twoPointAttempt+=1
            if("attempt succeeds" in playString.lower()):
                twoPointSucceed+=1
        if "extra point" in playString.lower():
            onePointAttempt+=1
            if("good" in playString.lower()):
                onePointSucceed+=1

    print("---- one point conversion ----")
    print("success = ", onePointSucceed, " twoPointAttempt = ",onePointAttempt)
    print("success rate = ", float(onePointSucceed/onePointAttempt))

    print("---- two point conversion ----")
    print("success = ", twoPointSucceed, " twoPointAttempt = ",twoPointAttempt)
    print("success rate = ", float(twoPointSucceed/twoPointAttempt))

def conversionPerGame():
    
    twoPointTotalAttempt = 0
    twoPointTotalSucceed = 0
    onePointTotalAttempt = 0
    onePointTotalSucceed = 0

    twoPointWinner = 0

    for game in games:
        onePointAttempt = 0
        onePointSucceed = 0

        twoPointAttempt = 0
        twoPointSucceed = 0

        homeScore = 0
        awayScore = 0

        twoPointAttemptHome = 0
        twoPointAttemptAway = 0

        scoreArr = {}
        scoreTracker = {}
        scoreTracker[game.home] = 0
        scoreTracker[game.away] = 0


        # TODO: 
        #  - keep track of when teams attempt 1/2 point conversions while behind or ahead and how far is the gap.


        # COMPLETE:
        #  - print out score before every 2 point conversion.
        #     - use eids somehow(?) maybe link up score to EID and check eid b4 2point conversion.
        

        #print("\n ---------")
        #print("GAME: ",game, " eid: ", game.eid)
        for score in game.scores:
            scoreStringArr = score.split(" ")
            scoringTeam = scoreStringArr[0]
            otherTeam = game.home
            if(game.home == scoringTeam):
                otherTeam = game.away
            playEid = scoreStringArr[-1]
            if("TD" in score):
                scoreArr[playEid] = ([scoringTeam, 6, otherTeam])
            elif("FG" in score):
                scoreArr[playEid] = ([scoringTeam, 3, otherTeam])
            #print("\t",score)
        previousPlayEid = 0
        for play in game.drives.plays():
            playString = str(play)
            eid = str(play.playid)
            playStringArr = re.findall(r"[\w']+",playString)
            if str(eid) in scoreArr:
                scoreTracker[scoreArr[eid][0]] += scoreArr[eid][1]
            scoringTeam = playStringArr[0]
            otherTeam = game.home
            if(playStringArr[0] == game.home):
                otherTeam = game.away
            if "two-point conversion" in playString.lower():
                #print(playString)
                if(scoreTracker[scoringTeam] < scoreTracker[otherTeam]): 
                    print(scoringTeam, scoreTracker[scoringTeam], " vs. ", otherTeam, scoreTracker[otherTeam])
                    twoPointAttempt+=1
                    if(scoringTeam == game.home):
                        twoPointAttemptHome+=1
                    else:
                        twoPointAttemptAway+=1
                    if("attempt succeeds" in playString.lower()):
                        twoPointSucceed+=1
                if("attempt succeeds" in playString.lower()):
                    scoreTracker[scoringTeam]+=2
            if "extra point" in playString.lower():
                #print("----")
                #print("Score: {}: {} vs. {}:{} ".format(game.home,scoreTracker[game.home],game.away,scoreTracker[game.away]) )
                #print("Currently attempting 1-point conversion is: ",playString[1:3])
                #print(playString)
                if(scoreTracker[scoringTeam] < scoreTracker[otherTeam]): 
                    print(scoringTeam, scoreTracker[scoringTeam], " vs. ", otherTeam, scoreTracker[otherTeam])
                    onePointAttempt+=1
                    if("good" in playString.lower()):
                        onePointSucceed+=1
                if("good" in playString.lower()):
                    scoreTracker[playStringArr[0]] +=1
                    #print("Score: {}: {} vs. {}:{} ".format(game.home,scoreTracker[game.home],game.away,scoreTracker[game.away]) )
                #print("----")
            previousPlayEid = eid
        twoPointTotalSucceed += twoPointSucceed
        twoPointTotalAttempt += twoPointAttempt
        onePointTotalSucceed += onePointSucceed
        onePointTotalAttempt += onePointAttempt
        if(False):
            # code for finding percentages when one/two point conversion were attempted with and without each other.
            global twoPointOnlyAttempt
            global twoPointOnlyScore
            global onePointOnlyAttempt
            global onePointOnlyScore
            if(twoPointAttempt == 0):
                twoPointOnlyAttempt+= twoPointAttempt
                onePointOnlyAttempt+= onePointAttempt
                onePointOnlyScore+= onePointSucceed
                if(twoPointSucceed >= 1):
                    twoPointOnlyScore+= twoPointSucceed
            twoAttempted = False
            if(twoPointAttempt != 0):
                twoAttempted = True



            if onePointAttempt == 0:
                onePointAttempt = 1
            if twoPointAttempt == 0:
                twoPointAttempt = 1

        if(twoPointAttempt > 120):
            print("---- one point conversion ----")
            print("success = ", onePointSucceed, " twoPointAttempt = ",onePointAttempt)
            print("success rate = ", float(onePointSucceed/onePointAttempt))

            print("---- two point conversion ----")
            print("success = ", twoPointSucceed, " twoPointAttempt = ",twoPointAttempt)
            print("success rate = ", float(twoPointSucceed/twoPointAttempt))
            print("\n")
        if(game.score_home > game.score_away):
            if(twoPointAttemptHome >= 1):
                twoPointWinner+=1
        else:
            if(twoPointAttemptAway>=1):
                twoPointWinner+=1
    print("winner ratio: ", twoPointWinner, len(games), float(twoPointWinner/len(games)))
    print("one:", onePointTotalSucceed, onePointTotalAttempt, float(onePointTotalSucceed/onePointTotalAttempt))
    print("two:",twoPointTotalSucceed, twoPointTotalAttempt, float(twoPointTotalSucceed/twoPointTotalAttempt))

def getTimeConversion():
    # If a team attempts 2-point conversions earlier in the game (before Q3)
    # is there a higher chance that they will win?

    twoAttempted = 0
    conversionWin = 0

    for game in games:
        teamAttemptedTwo = {}
        teamAttemptedTwo[game.home] = False
        teamAttemptedTwo[game.away] = False
        for play in game.drives.plays():
            playArr = re.findall(r"[\w']+",str(play))
            quarterIndex = getFirstOccurrenceArr(playArr,'Q')
            if(quarterIndex != -1):
                if (int(playArr[quarterIndex][1]) >= 3) and ("two-point conversion" in str(play).lower()):
                    teamAttemptedTwo[playArr[0]] = True
                    twoAttempted+=1

        if(teamAttemptedTwo[highestScoreHalfTime(game)]):
            conversionWin+=1

    print("Number of times attempted a 2-point conversion before Q3: ", twoAttempted)
    print("% of teams that were winning when attempting before Q3: ",float(conversionWin/len(games)))

def highestScoreHalfTime(game):
    # Given game.scores, find the winning team at halftime (before Q3)
    winningTeam = game.home
    scoreTracker = {}
    scoreTracker[game.home.lower()] = 0
    scoreTracker[game.away.lower()] = 0
    for score in game.scores:
        splitStringArr = re.findall(r"[\w']+",str(score).lower())
        if int(splitStringArr[1][1]) < 3:
            if(splitStringArr[2] == "td"):
                scoreTracker[splitStringArr[0]]+=6
            elif(splitStringArr[2] == "fg"):
                scoreTracker[splitStringArr[0]]+=3

    for play in game.drives.plays():
        playStr = str(play).lower()
        splitStringArr = re.findall(r"[\w']+",playStr)
        if ("two-point conversion" in playStr) and ("attempt succeeds" in playStr):
            if (int(splitStringArr[getFirstOccurrenceArr(splitStringArr,'q')][1]) < 3):
                scoreTracker[splitStringArr[0]]+=2
        if ("extra point" in playStr) and ("good" in playStr):
            if (int(splitStringArr[getFirstOccurrenceArr(splitStringArr,'q')][1]) < 3):
                scoreTracker[splitStringArr[0]]+=1
    if(scoreTracker[game.home.lower()] < scoreTracker[game.away.lower()]):
        winningTeam = game.away

    return winningTeam

def getFirstOccurrenceArr(arr, char):
    for index in range(0,len(arr)):
        if(len(arr[index]) == 2):
            if(arr[index][0] == char) and (arr[index][1].isdigit()):
                return index
    return -1

# percentage of games where a 2-point conversion was attempted.
def percentageConversionAttempted():
    conversionAttempted = 0
    stopTracking = False
    for game in games:
        for play in game.drives.plays():
            if ("two-point conversion" in str(play).lower()) and ( not stopTracking):
                conversionAttempted+=1
                stopTracking = True
        stopTracking = False
    print("number of games with a two-point conversion:",conversionAttempted)
    print("percentage of games where two-point conversion attempted: ", float(conversionAttempted/len(games)))



twoPointOnlyAttempt = 0
twoPointOnlyScore = 0

onePointOnlyAttempt = 0
onePointOnlyScore = 0

percentageConversionAttempted()

#getTimeConversion()

#conversionPerGame()

# If the scoring team is behind in score
# 289 294 0.9829931972789115 (289 one-point scored, 294 attempted, 98.3% chance of success)
# 19 44 0.4318181818181818 (19 two-point scored, 44 attempted, 43.2% chance of success)

# If the scoring team is = or above in score
# 755 764 0.9882198952879581 (755 one-point scored, 764 attempted, 98.82% chance of success)
# 15 33 0.45454545454545453  (15 two-point score, 33 attempted, 45.45% chance of success)


# Two Point Conversion never attempted
# 822 830 0.9903614457831326

# Two Point Conversion Attempted Once
# 169 175 0.9657142857142857    (one pointer stats)
# 24 42 0.5714285714285714 score, attempt, percentage of success (only one two pointer in whole game)

# Two Point Conversion Attempted more than once
# 53 53 1.0  (one pointer stats)
# 10 35 0.2857142857142857  ''        (more than two attempted two point conversions)

# Total two point conversion attempted stats
# 222 228 0.9736842105
#print("one point:", onePointOnlyScore,onePointOnlyAttempt, float(onePointOnlyScore/onePointOnlyAttempt))
#print("two point:", twoPointOnlyScore,twoPointOnlyAttempt, float(twoPointOnlyScore/twoPointOnlyAttempt))


#conversionPercentage()

