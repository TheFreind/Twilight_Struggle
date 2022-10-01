import random, math

currentPlayer = 1 # 0 - American player, 1 - Soviet player. Current player's turn
otherPlayer = 0 # Always opposite of currentPlayer. E.G. If it's the Soviet's turn, then otherPlayer = 0 to denote Americans.
phasingPlayer = 1 # Tracker of whose turn it is supposed to be. Culprit for DEFCON suicides.

warStage = "Early War"

FACTION = {
          0 : "U.S.A.",
          1 : "Soviet Union"
        }

OPERATIONS = 1 # Set to 4. Assume playing Nuclear Test Ban

VICTORYPOINTS = 0 # Soviets win at -20, Americans win at +20. 0 Indicates neutral.

DEFCON = 5 # 5 - Peace; 1 - Global thermonuclear war

# This tracks all things in space
# 0/1 (Currentplayer): [ "Name", Steps progressed so far, If spacing is available this turn (True - yes, False - no) ]
# "Space Track": [ "Name", Ops needed to space, Highest number rolled that succeeds, VPs as 1st or 2nd, Faction who reached it first ]
SPACE = {
        0 : [ "NASA", 0, True ],
        1 : [ "Roscosmos", 0, True ],
        "Space Track": [["Earth Satellite", 2, 3, [2, 1], "None"],
                        ["Animal in Space", 2, 4, [0, 0], "None"],
                        ["Man in Space", 2, 3, [2, 0], "None"],
                        ["Man in Earth Orbit", 2, 4, [0, 0], "None"],
                        ["Lunar Orbit", 3, 3, [3, 1], "None"],
                        ["Eagle/Bear has Landed", 3, 4, [0, 0], "None"],
                        ["Space Shuttle", 3, 3, [4, 2], "None"],
                        ["Space Station", 4, 2, [2, 0], "None"]]
    }

MILOPS = {
         0 : 0, # American Milops
         1 : 0  # Soviet Milops
    }

# All on-going event effects from both powers are tracked here.
# When they're in play, turn it on with "True". Faction whose event it belongs to. Permanent or expires on end of turn.
SITUATIONS = {
        # Early War
        "Vietnam Revolts":          [ False, "Soviet Union", "Temporary"],
        "De Gaulle Leads France":   [ False, "Soviet Union", "Permanent"],
        "Warsaw Pact Formed":       [ False, "Soviet Union", "Permanent"],
        "Containment":              [ False, "U.S.A.", "Temporary"],
        "Marshall Plan":            [ False, "U.S.A.", "Permanent"],
        "NATO":                     [ False, "U.S.A.", "Permanent"],
        "US/Japan Mutual Defense Pact": [ False, "U.S.A.", "Permanent"],
        "Formosan Resolution":      [ False, "U.S.A.", "Permanent"],
        "NORAD":                    [ False, "U.S.A.", "Permanent"],
        "Red Scare/Purge":          [ False, "None", "Temporary"],
        # Mid War
        "Breznev Doctrine":         [ False, "Soviet Union", "Temporary"],
        "'We Will Bury You'":       [ False, "Soviet Union", "Temporary"],
        "U2 Incident":              [ False, "Soviet Union", "Temporary"],
        "Flower Power":             [ False, "Soviet Union", "Permanent"],
        "Quagmire":                 [ False, "Soviet Union", "Permanent"],
        "Willy Brandt":             [ False, "Soviet Union", "Permanent"],
        "Nuclear Subs":             [ False, "U.S.A.", "Temporary"],
        "Bear Trap":                [ False, "U.S.A.", "Permanent"],
        "Shuttle Diplomacy":        [ False, "U.S.A.", "Permanent"],
        "Camp David Accords":       [ False, "U.S.A.", "Permanent"],
        "John Paul II Elected Pope":[ False, "U.S.A.", "Permanent"],
        "Cuban Missile Crisis":     [ False, "None", "Temporary"],
        "SALT Negotiations":        [ False, "None", "Temporary"],

        # Late War
        "AWACS Sale to Saudis":     [ False, "U.S.A.", "Permanent"],
        "North Sea Oil":            [ False, "U.S.A.", "Permanent"]
    }

# Countries in Twilight Struggle. Organized by region, where battlefields come first.
#   "Name" : [ [US, Soviet Influence], Stability, Battleground Boolean, Regions, Controller, [ Adjacent countries ] ]
COUNTRIES = {
        # Europe, then Western, then Eastern
        "Italy":[ [0,0], 2, True, ["Europe", "Western Europe"], "None", ["France","Greece","Spain/Portugal","Yugoslavia","Austria"] ],
        "France":[ [0,0], 3, True, ["Europe", "Western Europe"], "None", ["UK","Italy","Spain/Portugal","Algeria","West Germany"] ],
        "West Germany":[ [0,0], 4, True, ["Europe", "Western Europe"], "None", ["France","Benelux","Denmark","East Germany","Austria"] ],
        "East Germany":[ [0,3], 3, True, ["Europe", "Eastern Europe"], "None", ["Poland","West Germany","Czechoslovakia","Austria"] ],
        "Poland":[ [0,0], 3, True, ["Europe", "Eastern Europe"], "None", ["East Germany","Czechoslovakia","Soviet Union"] ],
        "Canada":[ [2,0], 4, False, ["Europe", "Western Europe"], "None", ["U.S.A.","UK"] ],
        "UK":[ [5,0], 5, False, ["Europe", "Western Europe"], "None", ["Canada","France","Norway","Benelux"] ],
        "Benelux":[ [0,0], 3, False, ["Europe", "Western Europe"], "None", ["UK","West Germany"] ],
        "Norway":[ [0,0], 4, False, ["Europe", "Western Europe"], "None", ["UK","Sweden"] ],
        "Denmark":[ [0,0], 3, False, ["Europe", "Western Europe"], "None", ["West Germany","Sweden"] ],
        "Sweden":[ [0,0], 4, False, ["Europe", "Western Europe"], "None", ["Norway","Denmark","Finland"] ],
        "Finland":[ [0,1], 4, False, ["Europe", "Western Europe", "Eastern Europe"], "None", ["Sweden","Soviet Union"] ],
        "Spain/Portugal":[ [0,0], 2, False, ["Europe", "Western Europe"], "None", ["France","Italy","Morocco"] ],
        "Greece":[ [0,0], 2, False, ["Europe", "Western Europe"], "None", ["Italy","Yugoslavia","Bulgaria","Turkey"] ],
        "Turkey":[ [0,0], 2, False, ["Europe", "Western Europe"], "None", ["Greece","Bulgaria","Romania","Syria"] ],
        "Austria":[ [0,0], 4, False, ["Europe", "Western Europe", "Eastern Europe"], "None", ["Italy","West Germany","East Germany","Hungary"] ],
        "Hungary":[ [0,0], 3, False, ["Europe", "Eastern Europe"], "None", ["Austria","Yugoslavia","Romania","Czechoslovakia"] ],
        "Czechoslovakia":[ [0,0], 3, False, ["Europe", "Eastern Europe"], "None", ["East Germany","Poland","Hungary"] ],
        "Romania":[ [0,0], 3, False, ["Europe", "Eastern Europe"], "None", ["Turkey","Yugoslavia","Soviet Union","Hungary"] ],
        "Bulgaria":[ [0,0], 3, False, ["Europe", "Eastern Europe"], "None", ["Turkey","Greece",] ],
        "Yugoslavia":[ [0,0], 3, False, ["Europe", "Eastern Europe"], "None", ["Italy","Hungary","Greece","Romania"] ],
        # Africa
        "Algeria":[ [0,0], 2, True, ["Africa"], "None", ["France","Morocco","Tunisia","Saharan States"] ],
        "Nigeria":[ [0,0], 1, True, ["Africa"], "None", ["Saharan States","Ivory Coast","Cameroon"] ],
        "Zaire":[ [0,0], 1, True, ["Africa"], "None", ["Angola","Zimbabwe","Cameroon"] ],
        "Angola":[ [0,0], 1, True, ["Africa"], "None", ["Zaire","South Africa","Botswana"] ],
        "South Africa":[ [1,0], 3, True, ["Africa"], "None", ["Angola","Botswana"] ],        
        "Morocco":[ [0,0], 3, False, ["Africa"], "None", ["Algeria","Spain/Portugal","West African States"] ],
        "Botswana":[ [0,0], 2, False, ["Africa"], "None", ["South Africa","Angola","Zimbabwe"] ],
        "Zimbabwe":[ [0,0], 1, False, ["Africa"], "None", ["Zaire","Botswana","SE African States"] ],
        "Cameroon":[ [0,0], 1, False, ["Africa"], "None", ["Zaire","Nigeria"] ],
        "Saharan States":[ [0,0], 1, False, ["Africa"], "None", ["Algeria","Nigeria"] ],
        "Ivory Coast":[ [0,0], 2, False, ["Africa"], "None", ["West African States","Nigeria"] ],
        "West African States":[ [0,0], 2, False, ["Africa"], "None", ["Ivory Coast","Morocco"] ],
        "Tunisia":[ [0,0], 2, False, ["Africa"], "None", ["Algeria","Libya"] ],
        "Sudan":[ [0,0], 1, False, ["Africa"], "None", ["Egypt","Ethiopia"] ],
        "Ethiopia":[ [0,0], 1, False, ["Africa"], "None", ["Sudan","Somalia"] ],
        "Somalia":[ [0,0], 2, False, ["Africa"], "None", ["Ethiopia","Kenya"] ],
        "Kenya":[ [0,0], 2, False, ["Africa"], "None", ["SE African States","Somalia"] ],
        "SE African States":[ [0,0], 1, False, ["Africa"], "None", ["Kenya","Zimbabwe"] ],
        # Middle East
        "Egypt":[ [0,0], 2, True, ["Middle East"], "None", ["Sudan","Libya","Israel"] ],
        "Libya":[ [0,0], 2, True, ["Middle East"], "None", ["Egypt","Tunisia"] ],
        "Israel":[ [1,0], 4, True, ["Middle East"], "None", ["Egypt","Lebanon","Jordan","Syria"] ],
        "Iran":[ [1,0], 2, True, ["Middle East"], "None", ["Iraq","Pakistan","Afghanistan"] ],
        "Iraq":[ [0,1], 3, True, ["Middle East"], "None", ["Iran","Saudi Arabia","Jordan","Gulf States"] ],
        "Saudi Arabia":[ [0,0], 3, True, ["Middle East"], "None", ["Iraq","Jordan","Gulf States"] ],
        "Lebanon":[ [0,0], 1, False, ["Middle East"], "None", ["Israel","Jordan","Syria"] ],
        "Syria":[ [0,1], 2, False, ["Middle East"], "None", ["Turkey","Lebanon","Israel"] ],
        "Jordan":[ [0,0], 2, False, ["Middle East"], "None", ["Iraq","Lebanon","Israel","Saudi Arabia"] ],
        "Gulf States":[ [0,0], 3, False, ["Middle East"], "None", ["Iraq","Saudi Arabia"] ],
        # Asia
        "Japan":[ [1,0], 4, True, ["Asia"], "None", ["U.S.A.","South Korea","Philippines","Taiwan"] ],
        "South Korea":[ [1,0], 3, True, ["Asia"], "None", ["Japan","North Korea","Taiwan"] ],
        "North Korea":[ [0,3], 3, True, ["Asia"], "None", ["South Korea","Soviet Union"] ],
        "Pakistan":[ [0,0], 2, True, ["Asia"], "None", ["Iran","Afghanistan","India"] ],
        "India":[ [0,0], 3, True, ["Asia"], "None", ["Burma","Pakistan"] ],
        "Thailand":[ [0,0], 2, True, ["Asia", "Southeast Asia"], "None", ["Vietnam","Laos/Cambodia","Malaysia"] ],
        "Afghanistan":[ [0,0], 2, False, ["Asia"], "None", ["Iran","Soviet Union","Pakistan"] ],
        "Burma":[ [0,0], 2, False, ["Asia", "Southeast Asia"], "None", ["India","Laos/Cambodia"] ],
        "Laos/Cambodia":[ [0,0], 1, False, ["Asia", "Southeast Asia"], "None", ["Burma","Thailand","Vietnam"] ],
        "Vietnam":[ [0,0], 1, False, ["Asia", "Southeast Asia"], "None", ["Laos/Cambodia","Thailand"] ],
        "Malaysia":[ [0,0], 2, False, ["Asia", "Southeast Asia"], "None", ["Indonesia","Thailand","Australia"] ],
        "Indonesia":[ [0,0], 1, False, ["Asia", "Southeast Asia"], "None", ["Malaysia","Philippines"] ],
        "Philippines":[ [1,0], 2, False, ["Asia", "Southeast Asia"], "None", ["Japan","Indonesia"] ],
        "Australia":[ [4,0], 4, False, ["Asia"], "None", ["Malaysia"] ],
        "Taiwan":[ [0,0], 3, False, ["Asia"], "None", ["Japan","South Korea"] ],
        # South America
        "Chile":[ [0,0], 3, True, ["South America"], "None", ["Peru","Argentina"] ],
        "Argentina":[ [0,0], 2, True, ["South America"], "None", ["Chile","Paraguay", "Uruguay"] ],
        "Brazil":[ [0,0], 2, True, ["South America"], "None", ["Venezuela", "Uruguay"] ],
        "Venezuela":[ [0,0], 2, True, ["South America"], "None", ["Brazil", "Colombia"] ],
        "Colombia":[ [0,0], 1, False, ["South America"], "None", ["Venezuela", "Ecuador"] ],
        "Ecuador":[ [0,0], 2, False, ["South America"], "None", ["Peru", "Colombia"] ],
        "Peru":[ [0,0], 2, False, ["South America"], "None", ["Ecuador", "Chile", "Bolivia"] ],
        "Bolivia":[ [0,0], 2, False, ["South America"], "None", ["Peru", "Paraguay"] ],
        "Paraguay":[ [0,0], 2, False, ["South America"], "None", ["Bolivia", "Argentina", "Uruguay"] ],
        "Uruguay":[ [0,0], 2, False, ["South America"], "None", ["Brazil", "Argentina", "Paraguay"] ],
        # Central America
        "Cuba":[ [0,0], 3, True, ["Central America"], "None", ["U.S.A.","Nicaragua", "Haiti"] ],
        "Panama":[ [1,0], 2, True, ["Central America"], "None", ["Costa Rica", "Colombia"] ],
        "Mexico":[ [0,0], 2, True, ["Central America"], "None", ["U.S.A.", "Guatemala"] ],
        "Guatemala":[ [0,0], 1, False, ["Central America"], "None", ["Mexico", "El Salvador", "Honduras"] ],
        "El Salvador":[ [0,0], 1, False, ["Central America"], "None", ["Honduras", "Guatemala"] ],
        "Honduras":[ [0,0], 2, False, ["Central America"], "None", ["El Salvador", "Guatemala", "Nicaragua", "Costa Rica"] ],
        "Costa Rica":[ [0,0], 3, False, ["Central America"], "None", ["Panama", "Nicaragua", "Honduras"] ],
        "Nicaragua":[ [0,0], 1, False, ["Central America"], "None", ["Cuba", "Honduras", "Costa Rica"] ],
        "Haiti":[ [0,0], 1, False, ["Central America"], "None", ["Honduras", "Dominican Rep"] ],
        "Dominican Rep":[ [0,0], 1, False, ["Central America"], "None", ["Haiti"] ],
    }

# All the playable cards in the game.
# "Name":["Event text", Operations, Faction affiliated, Removed after event boolean]
CARDS = {
    ## Soviet Early War - 15 cards ##
        "Nasser":["Add 2 USSR Influence to Egypt. The US removes half, rounded up, of its Influence from Egypt.",
                            1, "Soviet Union", True],
        "Romanian Abdication":["Remove all US Influence from Romania. The USSR adds sufficient Influence to Romania for Control.",
                            1, "Soviet Union", True],
        "Blockade":["Unless the US immediately discards a card with an Operations value of 3 or more, remove all US Influence from West Germany.",
                            1, "Soviet Union", True],
        "The Cambridge Five":["The US reveals all scoring cards in their hand of cards. The USSR player may add 1 USSR Influence to a single Region named on one of the revealed scoring cards.\
                            \n This card can not be played as an Event during the Late War.",
                            2, "Soviet Union", False],
        "Fidel":["Remove all US Influence from Cuba. USSR adds sufficient Influence in Cuba for Control.",
                            2, "Soviet Union", True],
        "Vietnam Revolts":["Add 2 USSR Influence to Vietnam. For the remainder of the turn, the USSR receives +1 Operations to the Operations value of a card that uses all its Operations in Southeast Asia.",
                            2, "Soviet Union", True],
        "Korean War":["North Korea invades South Korea. Roll a die and subtract (-1) from the die roll for every US controlled country adjacent to South Korea.\
                            \n On a modified die roll of 4-6, the USSR receives 2 VP and replaces all US Influence in South Korea with USSR Influence. The USSR adds 2 to its Military Operations Track.",
                            2, "Soviet Union", True],
        "Arab-Israeli War":["Pan-Arab Coalition invades Israel. Roll a die and subtract (-1) from the die roll for Israel, if it is US controlled, and for every US controlled country adjacent to Israel.\
                            \n On a modified die roll of 4-6, the USSR receives 2 VP and replaces all US Influence in Israel with USSR Influence. The USSR adds 2 to its Military Operations Track.\
                            \n This Event cannot be used after the “#65 – Camp David Accords” Event has been played.",
                            2, "Soviet Union", False],
        "Decolonization":["Add 1 USSR Influence to each of any 4 countries in Africa and/or Southeast Asia.",
                            2, "Soviet Union", False],
        "De-Stalinization":["The USSR may reallocate up to a total of 4 Influence from one or more countries to any non-US controlled countries (adding no more than 2 Influence per country).",
                            3, "Soviet Union", True],
        "Comecon":["Add 1 USSR Influence to each of 4 non-US controlled countries of Eastern Europe.",
                            3, "Soviet Union", True],
        "Suez Crisis":["Remove a total of 4 US Influence from France, the United Kingdom and Israel (removing no more than 2 Influence per country).",
                            3, "Soviet Union", True],
        "De Gaulle Leads France":["Remove 2 US Influence in France, add 1 USSR Influence.\nCancels effects of 'NATO' for France.",
                            3, "Soviet Union", True],
        "Warsaw Pact Formed":["Remove all US Influence from 4 countries in Eastern Europe, or add 5 USSR Influence in Eastern Europe. adding no more than 2 per country.\n'NATO' is allowed as an event.",
                            3, "Soviet Union", True],
        "Socialist Governments":["Remove a total of 3 US Influence from any countries in Western Europe (removing no more than 2 Influence per country).\
                            \n This Event cannot be used after the “#83 – The Iron Lady” Event has been played.",
                            3, "Soviet Union", False],
    ## U.S.A. Early War - 14 cards ##
        "C.I.A. Created":["U.S.S.R. reveals hand this turn.\nThen, the US may Conduct Operations as if they played a 1 Op card.",
                            1, "U.S.A.", True],
        "Truman Doctrine":["Remove all USSR Influence from a single uncontrolled country in Europe.",
                            1, "U.S.A.", True],
        "Independent Reds":["Add US Influence to either Yugoslavia, Romania, Bulgaria, Hungary, or Czechoslovakia so that it equals the USSR Influence in that country.",
                            2, "U.S.A.", True],
        "Formosan Resolution":["If this card’s Event is in effect, Taiwan will be treated as a Battleground country, for scoring purposes only, if Taiwan is US controlled when the Asia Scoring Card is played.\
                            \n This Event is cancelled after the US has played the “#6 – The China Card” card.",
                            2, "U.S.A.", True],
        "Defectors":["The US may play this card during the Headline Phase in order to cancel the USSR Headline Event (including a scoring card). The canceled card is placed into the discard pile.\
                            \n If this card is played by the USSR during its action round, the US gains 1 VP.",
                            2, "U.S.A.", False],
        "Special Relationship":["Add 1 US Influence to a single country adjacent to the U.K. if the U.K. is US-controlled but NATO is not in effect.\
                            \n Add 2 US Influence to a single country in Western Europe, and the US gains 2 VP, if the U.K. is US-controlled and NATO is in effect.",
                            2, "U.S.A.", False],
        "NORAD":["Add 1 US Influence to a single country containing US Influence, at the end of each Action Round, if Canada is US-controlled and the DEFCON level moved to 2 during that Action Round.\
                            \n This Event is canceled by the “#42 – Quagmire” Event.",
                            3, "U.S.A.", True],
        "East European Unrest":["Early or Mid War: Remove 1 USSR Influence from 3 countries in Eastern Europe. Late War: Remove 2 USSR Influence from 3 countries in Eastern Europe.",
                            3, "U.S.A.", False],
        "Five Year Plan":["The USSR must randomly discard a card. If the card has a US associated Event, the Event occurs immediately.\
                            \n If the card has a USSR associated Event or an Event applicable to both players, then the card must be discarded without triggering the Event.",
                            3, "U.S.A.", False],
        "Duck and Cover":["Degrade the DEFCON level by 1. The US receives VP equal to 5 minus the current DEFCON level.",
                            3, "U.S.A.", False],
        "Containment":["All Operations cards played by the US, for the remainder of this turn, receive +1 to their Operations value (to a maximum of 4 Operations per card).",
                            3, "U.S.A.", True],
        "US/Japan Mutual Defense Pact":["The US adds sufficient Influence to Japan for Control. The USSR cannot make Coup Attempts or Realignment rolls against Japan.",
                            4, "U.S.A.", True],
        "Marshall Plan":["Add 1 US Influence to each of any 7 non-USSR controlled countries in Western Europe.\n'NATO' is allowed as an event.",
                            4, "U.S.A.", True],
        "NATO":["The USSR cannot Coup, Realign, or 'Brush War' against any US controlled country in Europe.\nNATO event requires Marshall Plan or Warsaw Pact Formed to be in effect.",
                            4, "U.S.A.", True],
    ## Neutral and Scoring Early War - 10 cards ##
        "Asia Scoring":["Presence: 3; Domination: 7; Control: 9; +1 VP per controlled Battleground country in Region; +1 VP per country controlled that is adjacent to enemy superpower; MAY NOT BE HELD!",
                            0, "Neutral", False],
        "Europe Scoring":["Presence: 3; Domination: 7; Control: Automatic Victory; +1 VP per controlled Battleground country in Region; +1 VP per country controlled that is adjacent to enemy superpower; MAY NOT BE HELD!",
                            0, "Neutral", False],
        "Middle East Scoring":["Presence: 3; Domination: 5; Control: 7; +1 VP per controlled Battleground country in Region; MAY NOT BE HELD!",
                            0, "Neutral", False],        
        "Captured Nazi Scientists":["Move the Space Race Marker ahead by 1 space.",
                            1, "Neutral", True],
        "UN Intervention":["Play this card simultaneously with a card containing an opponent’s associated Event. The opponent’s associated Event is canceled but you may use the Operations value of the opponent’s card to conduct Operations. \
                            \n This Event cannot be played during the Headline Phase.",
                            1, "Neutral", False],
        "Olympic Games":["This player sponsors the Olympics. The opponent must either participate or boycott. If the opponent participates, each player rolls a die and the sponsor adds 2 to their roll. The player with the highest modified die roll receives 2 VP (reroll ties).\
                            \n If the opponent boycotts, degrade the DEFCON level by 1 and the sponsor may conduct Operations as if they played a 4 Ops card.",
                            2, "Neutral", False],    
        "Indo-Pakistani War":["India invades Pakistan or vice versa (player’s choice). Roll a die and subtract (-1) from the die roll for every enemy controlled country adjacent to the target of the invasion (India or Pakistan).\
                            \n On a modified die roll of 4-6, the player receives 2 VP and replaces all the opponent’s Influence in the target country with their Influence. The player adds 2 to its Military Operations Track.",
                            2, "Neutral", False],
        "The China Card":["This card begins the game with the USSR.\n When played, the player receives +1 Operations to the Operations value of this card if it uses all its Operations in Asia.\n It is passed to the opponent once played. \
                            \n A player receives 1 VP for holding this card at the end of Turn 10.",
                            4, "Neutral", "Soviet Union", True, False], # Index 3 represents who has ownership; index 4 is Available
        "Red Scare/Purge":["All Operations cards played by the opponent, for the remainder of this turn, receive -1 to their Operations value (to a minimum value of 1 Operations point).",
                            4, "Neutral", False],
        "Nuclear Test Ban":["The player receives VP equal to the current DEFCON level minus 2 then improves the DEFCON level by 2.",
                            4, "Neutral", False],
########################################
############# MID WAR CARDS ############
########################################
    ## Soviet Mid War - 15 cards ##
        "'We Will Bury You'":["Degrade the DEFCON level by 1. Unless UN Intervention card is played as an Event on the US’s next action round, the USSR receives 3 VP.",
                            4, "Soviet Union", True], 
        "Muslim Revolution":["Remove all US Influence from 2 of the following countries: Sudan, Iran, Iraq, Egypt, Libya, Saudi Arabia, Syria, Jordan. \nThis Event cannot be used after AWACS Sale to Saudis” Event has been played.",
                            4, "Soviet Union", False],   
        "Flower Power":["The USSR receives 2 VP for every US played “War” card (Arab-Israeli War, Korean War, Brush War, Indo-Pakistani War, Iran-Iraq War), used for Operations or an Event, after this card is played. \nThis Event is prevented / canceled by the 'An Evil Empire’ Event.",
                            4, "Soviet Union", True],
        "Quagmire":["On the US’s next action round, it must discard an Operations card with a value of 2 or more and roll 1-4 on a die to cancel this Event. Repeat this Event for each US action round until the US successfully rolls 1-4 on a die. \nIf the US is unable to discard an Operations card, it must play all of its scoring cards and then skip each action round for the rest of the turn. \nThis Event cancels NORAD.",
                            3, "Soviet Union", True],                                                    
        "Brezhnev Doctrine":["All Operations cards played by the USSR, for the remainder of this turn, receive +1 to their Operations value (to a maximum of 4 Operations per card).",
                            3, "Soviet Union", True],
        "U2 Incident":["The USSR receives 1 VP. If UN Intervention Event is played later this turn, either by the US or the USSR, the USSR receives an additional 1 VP..",
                            3, "Soviet Union", True],
        "Cultural Revolution":["If the US has the The China Card” card, the US must give the card to the USSR (face up and available to be played). If the USSR already has The China Card” card, the USSR receives 1 VP.",
                            3, "Soviet Union", True],
        "OPEC":["The USSR receives 1 VP for Control of each of the following countries: Egypt, Iran, Libya, Saudi Arabia, Iraq, Gulf States, Venezuela. \nThis Event cannot be used after the 'North Sea Oil' Event has been played.",
                            3, "Soviet Union", False],
        "Che":["The USSR may perform a Coup Attempt, using this card’s Operations value, against a non-Battleground country in Central America, South America or Africa. \
                \nThe USSR may perform a second Coup Attempt, against a different non-Battleground country in Central America, South America or Africa, if the first Coup Attempt removed any US Influence from the target country.",
                            3, "Soviet Union", False],                            
        "Portuguese Empire Crumbles":["Add 2 USSR Influence to Angola and the SE African States.",
                            2, "Soviet Union", True],
        "South African Unrest":["The USSR either adds 2 Influence to South Africa or adds 1 Influence to South Africa and 2 Influence to a single country adjacent to South Africa.",
                            2, "Soviet Union", False],    
        "Willy Brandt":["The USSR receives 1 VP and adds 1 Influence to West Germany. This Event cancels the effect(s) of the “#21 – NATO” Event for West Germany only. \nThis Event is prevented / canceled by Tear Down this Wall.",
                            2, "Soviet Union", True],     
        "Liberation Theology":["Add a total of 3 USSR Influence to any countries in Central America (adding no more than 2 Influence per country).",
                            2, "Soviet Union", False],                                                             
        "Allende":["Add 2 USSR Influence to Chile.",
                            1, "Soviet Union", True],
        "Lone Gunman":["The US reveals their hand of cards. The USSR may use the Operations value of this card to conduct Operations.",
                            1, "Soviet Union", True],
    ## US Mid War - 18 cards ##
        "Ussuri River Skirmish":["If the USSR has the “The China Card” card, the USSR must give the card to the US (face up and available for play). \
            \nIf the US already has the “The China Card” card, add a total of 4 US Influence to any countries in Asia (adding no more than 2 Influence per country).",
                            3, "U.S.A.", True], 
        "'Ask Not What Your Country…'":["The US may discard up to their entire hand of cards (including scoring cards) to the discard pile and draw replacements from the draw pile. \
            \nThe number of cards to be discarded must be decided before drawing any replacement cards from the draw pile.",
                            3, "U.S.A.", True], 
        "Alliance for Progress":["The US receives 1 VP for each US controlled Battleground country in Central and South America.",
                            3, "U.S.A.", True], 
        "Bear Trap":["On the USSR’s next action round, it must discard an Operations card with a value of 2 or more and roll 1-4 on a die to cancel this Event. Repeat this Event for each USSR action round until the USSR successfully rolls 1-4 on a die. \
                        \nIf the USSR is unable to discard an Operations card, it must play all of its scoring cards and then skip each action round for the rest of the turn.",
                            3, "U.S.A.", True],
        "Shuttle Diplomacy":["If this card’s Event is in effect, subtract (-1) a Battleground country from the USSR total and then discard this card during the next scoring of the Middle East or Asia (which ever comes first).",
                            3, "U.S.A.", False], 
        "The Voice of America":["Remove 4 USSR Influence from any countries NOT in Europe (removing no more than 2 Influence per country).",
                            2, "U.S.A.", False], 
        "Camp David Accords":["The US receives 1 VP and adds 1 Influence to Israel, Jordan and Egypt. \
            \nThis Event prevents the “Arab-Israeli War” card from being played as an Event.",
                            2, "U.S.A.", True], 
        "Nixon Plays the China Card":["If the USSR has the “The China Card” card, the USSR must give the card to the US (face down and unavailable for immediate play). \
            \nIf the US already has the “The China Card” card, the US receives 2 VP.",
                            2, "U.S.A.", True], 
        "Nuclear Subs":["US Operations used for Coup Attempts in Battleground countries, for the remainder of this turn, do not degrade the DEFCON level. \
                        \nThis card’s Event does not apply to any Event that would affect the DEFCON level (ex. the “Cuban Missile Crisis” Event).",
                            2, "U.S.A.", True],
        "Colonial Rear Guards":["Add 1 US Influence to each of any 4 countries in Africa and/or Southeast Asia.",
                            2, "U.S.A.", False],   
        "Puppet Governments":["The US may add 1 Influence to 3 countries that do not contain Influence from either the US or USSR.",
                            2, "U.S.A.", True], 
        "Grain Sales to Soviets":["The US randomly selects 1 card from the USSR’s hand (if available). The US must either play the card or return it to the USSR. \
            \nIf the card is returned, or the USSR has no cards, the US may use the Operations value of this card to conduct Operations.",
                            2, "U.S.A.", False], 
        "John Paul II Elected Pope":["Remove 2 USSR Influence from Poland and add 1 US Influence to Poland. \
            \nThis Event allows the “Solidarity” card to be played as an Event.",
                            2, "U.S.A.", True], 
        "Our Man in Tehran":["If the US controls at least one Middle East country, the US player uses this Event to draw the top 5 cards from the draw pile. \
            \nThe US may discard any or all of the drawn cards, after revealing the discarded card(s) to the USSR player, without triggering the Event(s). \
            \nAny remaining drawn cards are returned to the draw pile and the draw pile is reshuffled.",
                            2, "U.S.A.", True], 
        "OAS Founded":["Add a total of 2 US Influence to any countries in Central or South America.",
                            1, "U.S.A.", True], 
        "Sadat Expels Soviets":["Remove all USSR Influence from Egypt and add 1 US Influence to Egypt.",
                            1, "U.S.A.", True], 
        "Kitchen Debates":["If the US controls more Battleground countries than the USSR, the US player uses this Event to poke their opponent in the chest and receive 2 VP!",
                            1, "U.S.A.", True], 
        "Panama Canal Returned":["Add 1 US Influence to Panama, Costa Rica and Venezuela.",
                            1, "U.S.A.", True],  
    ## Neutral Mid War - 15 cards ##
        "Central America Scoring":["	Presence: 1; Domination: 3; Control: 5; +1 VP per controlled Battleground country in Region; +1 VP per country controlled that is adjacent to enemy superpower; MAY NOT BE HELD!",
                            0, "Neutral", False], 
        "Southeast Asia Scoring":["1 VP each for Control of Burma, Cambodia/Laos, Vietnam, Malaysia, Indonesia and the Philippines. 2 VP for Control of Thailand; MAY NOT BE HELD!",
                            0, "Neutral", True], 
        "South America Scoring":["Presence: 2; Domination: 5; Control: 6; +1 VP per controlled Battleground country in Region; MAY NOT BE HELD!",
                            0, "Neutral", False], 
        "Africa Scoring":["	Presence: 1; Domination: 4; Control: 6; +1 VP per controlled Battleground country in Region; MAY NOT BE HELD!",
                            0, "Neutral", False], 
        "ABM Treaty":["Improve the DEFCON level by 1 and then conduct Operations using the Operations value of this card.",
                            4, "Neutral", False], 
        "Brush War":["The player attacks any country with a stability number of 1 or 2. Roll a die and subtract (-1) from the die roll for every adjacent enemy controlled country. \
                    \nOn a modified die roll of 3-6, the player receives 1 VP and replaces all the opponent’s Influence in the target country with their Influence. The player adds 3 to its Military Operations Track.",
                            3, "Neutral", False], 
        "Arms Race":["Compare each player’s value on the Military Operations Track. If the phasing player has a higher value than their opponent on the Military Operations Track, that player receives 1 VP. \
            \nIf the phasing player has a higher value than their opponent, and has met the “required” amount, on the Military Operations Track, that player receives 3 VP instead.",
                            3, "Neutral", False], 
        "Cuban Missile Crisis":["Set the DEFCON level to 2. Any Coup Attempts by your opponent, for the remainder of this turn, will result in Global Thermonuclear War. Your opponent will lose the game. \
            \nThis card’s Event may be canceled, at any time, if the USSR removes 2 Influence from Cuba or the US removes 2 Influence from West Germany or Turkey.",
                            3, "Neutral", True], 
        "SALT Negotiations":["Improve the DEFCON level by 2. For the remainder of the turn, both players receive -1 to all Coup Attempt rolls. \
            \nThe player of this card’s Event may look through the discard pile, pick any 1 non-scoring card, reveal it to their opponent and then place the drawn card into their hand.",
                            3, "Neutral", True], 
        "How I Learned to Stop Worrying":["Set the DEFCON level to any level desired (1-5). The player adds 5 to its Military Operations Track.",
                            2, "Neutral", True], 
        "Junta":["Add 2 Influence to a single country in Central or South America. The player may make free Coup Attempts or Realignment rolls in either Central or South America using the Operations value of this card.",
                            2, "Neutral", False], 
        "Missile Envy":["Exchange this card for your opponent’s highest value Operations card. If 2 or more cards are tied, opponent chooses. \
            \nIf the exchanged card contains an Event applicable to yourself or both players, it occurs immediately. If it contains an opponent’s Event, use the Operations value (no Event). \
            \nThe opponent must use this card for Operations during their next action round.",
                            2, "Neutral", False], 
        "Latin American Death Squads":["All of the phasing player’s Coup Attempts in Central and South America, for the remainder of this turn, receive +1 to their die roll. \
            \nAll of the opponent’s Coup Attempts in Central and South America, for the remainder of this turn, receive -1 to their die roll.",
                            2, "Neutral", False], 
        "'One Small Step…'":["If you are behind on the Space Race Track, the player uses this Event to move their marker 2 spaces forward on the Space Race Track. \
            \nThe player receives VP only from the final space moved into.",
                            2, "Neutral", False], 
        "Summit":["Both players roll a die. Each player receives +1 to the die roll for each Region (Europe, Asia, etc.) they Dominate or Control. The player with the highest modified die roll receives 2 VP and may degrade or improve the DEFCON level by 1 (do not reroll ties).",
                            1, "Neutral", False], 
########################################
############# LATE WAR CARDS ############
########################################
    ## Soviet Late War - 10 cards ##
        "Glasnost":["Improve the DEFCON level by 1 and the USSR receives 2 VP. The USSR may make Realignment rolls or add Influence, using this card, if the “The Reformer” Event has already been played.",
                            4, "Soviet Union", True], 
        "Iranian Hostage Crisis":["Remove all US Influence and add 2 USSR Influence to Iran. \
                \nThis card’s Event requires the US to discard 2 cards, instead of 1 card, if the “Terrorism” Event is played.",
                            3, "Soviet Union", True], 
        "The Reformer":["Add 4 USSR Influence to Europe (adding no more than 2 Influence per country). If the USSR is ahead of the US in VP, 6 Influence may be added to Europe instead. The USSR may no longer make Coup Attempts in Europe.",
                            3, "Soviet Union", True], 
        "Aldrich Ames Remix":["The US reveals their hand of cards, face-up, for the remainder of the turn and the USSR discards a card from the US hand.",
                            3, "Soviet Union", True], 
        "Pershing II Deployed":["The USSR receives 1 VP. Remove 1 US Influence from any 3 countries in Western Europe.",
                            3, "Soviet Union", True], 
        "Marine Barracks Bombing":["Remove all US Influence in Lebanon and remove a total of 2 US Influence from any countries in the Middle East.",
                            2, "Soviet Union", True], 
        "Ortega Elected in Nicaragua":["Remove all US Influence from Nicaragua. The USSR may make a free Coup Attempt, using this card’s Operations value, in a country adjacent to Nicaragua.",
                            2, "Soviet Union", True], 
        "Iran-Contra Scandal":["All US Realignment rolls, for the remainder of this turn, receive -1 to their die roll.",
                            2, "Soviet Union", True], 
        "Latin American Debt Crisis":["The US must immediately discard a card with an Operations value of 3 or more or the USSR may double the amount of USSR Influence in 2 countries in South America.",
                            2, "Soviet Union", False], 
        "Yuri and Samantha":["The USSR receives 1 VP for each US Coup Attempt performed during the remainder of the Turn.",
                            2, "Soviet Union", True], 
    ## USA Late War - 10 cards ##
        "Soviets Shoot Down KAL-007":["Degrade the DEFCON level by 1 and the US receives 2 VP. \
            \nThe US may place influence or make Realignment rolls, using this card, if South Korea is US controlled.",
                            4, "U.S.A.", True], 
        "The Iron Lady":["Add 1 USSR Influence to Argentina and remove all USSR Influence from the United Kingdom. The US receives 1 VP. \
            \nThis Event prevents the “#7 – Socialist Governments” card from being played as an Event.",
                            3, "U.S.A.", True], 
        "North Sea Oil":["The US may play 8 cards (in 8 action rounds) for this turn only. \
            \nThis Event prevents the “OPEC” card from being played as an Event.",
                            3, "U.S.A.", True], 
        "Chernobyl":["The US must designate a single Region (Europe, Asia, etc.) that, for the remainder of the turn, the USSR cannot add Influence to using Operations points.",
                            3, "U.S.A.", True], 
        "Tear Down this Wall":["Add 3 US Influence to East Germany. The US may make free Coup Attempts or Realignment rolls in Europe using the Operations value of this card. \
            \nThis Event prevents / cancels the effect(s) of the “Willy Brandt” Event.",
                            3, "U.S.A.", True], 
        "'An Evil Empire'":["The US receives 1 VP. This Event prevents / cancels the effect(s) of the “Flower Power” Event.",
                            3, "U.S.A.", True], 
        "AWACS Sale to Saudis":["Add 2 US Influence to Saudi Arabia. This Event prevents the “Muslim Revolution” card from being played as an Event.",
                            3, "U.S.A.", True], 
        "Solidarity":["Add 3 US Influence to Poland. This card requires prior play of the “John Paul II Elected Pope” Event in order to be played as an Event.",
                            2, "U.S.A.", True], 
        "Reagan Bombs Libya":["The US receives 1 VP for every 2 USSR Influence in Libya.",
                            2, "U.S.A.", True], 
        "Star Wars":["If the US is ahead on the Space Race Track, the US player uses this Event to look through the discard pile, pick any 1 non-scoring card and play it immediately as an Event.",
                            2, "U.S.A.", True], 
    ## Neutral Late War - 3 cards ##
        "Wargames":["If the DEFCON level is 2, the player may immediately end the game after giving their opponent 6 VP. How about a nice game of chess?",
                            4, "Neutral", True], 
        "Terrorism":["The player’s opponent must randomly discard 1 card from their hand. \
                    \nIf the “Iranian Hostage Crisis” Event has already been played, a US player (if applicable) must randomly discard 2 cards from their hand.",
                            2, "Neutral", False], 
        "Iran-Iraq War":["Iran invades Iraq or vice versa (player’s choice). Roll a die and subtract (-1) from the die roll for every enemy controlled country adjacent to the target of the invasion (Iran or Iraq). \
                    \nOn a modified die roll of 4-6, the player receives 2 VP and replaces all the opponent’s Influence in the target country with their Influence. \
                    \nThe player adds 2 to its Military Operations Track.",
                            2, "Neutral", True], 
    }

######## ACTION FUNCTIONS ################
# Function to execute events on cards
def cardCode(Card):
    global currentPlayer, otherPlayer, DEFCON
    cardConditionTriggered = True # Remove starred events. Do not remove if condition wasn't triggered, though.

    if Card[-7:] == "Scoring": # All scoring cards go through a specialized function.
        scoringVP = scoreRegion(Card[:-8])
        if scoringVP > 0: # Rare exception - scoring can go either way, must specificy if US or USSR
            earnVP( scoringVP, 0 )
        elif scoringVP < 0:
            earnVP( abs(scoringVP), 1)

########################################
########### EARLY WAR CARDS ############
########################################

    elif Card == "The Cambridge Five":
        if warStage != "Late War":
            scoringCards = []
            for card in HANDS[0]:
                if card[-7:] == "Scoring":
                    scoringCards.append(card[:-8])
            
            swapSides("Soviet Union")
            doubleCheck = 1

            print(scoringCards)
            print(CARDS["The Cambridge Five"][0])
            target = input("Enter country in available Regions: ")
            while doubleCheck > 0:  

                if target not in COUNTRIES.keys():
                    print("ERROR. COUNTRY NOT FOUND. TRY AGAIN. \n")
                    target = input("Enter country in available Regions: ")
                    doubleCheck += 1

                elif COUNTRIES[target][3] not in scoringCards:
                    print("ERROR. That country is not in specified Regions. Try another.\n")
                    target = input("Enter country in available Regions: ")
                    doubleCheck += 1

                doubleCheck -= 1

            COUNTRIES[target][0][1] += 1
            swapSides(FACTION[phasingPlayer])


    elif Card == "De Gaulle Leads France":
        COUNTRIES["France"][0][0] -= 2
        COUNTRIES["France"][0][1] += 1
        SITUATIONS[Card][0] = True
        print("Charismatic De Gaulle has been elected in France!")
        checkControl(COUNTRIES, "France")


    elif Card == "Five Year Plan":
        if len(HANDS[1]) > 1:
            randomlyDrawn = HANDS[1][random.randint(0, len(HANDS[1])-1 )]
            while randomlyDrawn == "Five Year Plan": # Do not randomly select and discard FYP itself
                randomlyDrawn = HANDS[1][random.randint(0, len(HANDS[1])-1 )]

            randomlyDrawn = HANDS[1].index(randomlyDrawn) # Turn random card into its index - then remove it from the hand
            cardPlanned = HANDS[1].pop(randomlyDrawn)
            if CARDS[cardPlanned][2] == "Soviet Union" or CARDS[cardPlanned][2] == "Neutral":
                swapSides("Soviet Union") # Discard function must know who is current player - Soviet player will be discarded
                discardCard(cardPlanned, True, False)

            elif CARDS[cardPlanned][2] == "U.S.A.":
                removeCard = cardCode(cardPlanned) # Trigger event. Return True/False if to remove card
                swapSides("Soviet Union")
                discardCard(cardPlanned, True, removeCard)

            swapSides(FACTION[phasingPlayer])
            print("Five Year Planned has discarded %s" % (cardPlanned) )

        else:
            print("Five Year Planned has discarded nothing.")


    elif Card == "Marshall Plan":
        swapSides("U.S.A.")
        
        addedCountries = []
        for markers in range(7):

            doubleCheck = 1
            print("Add an influence to a non-USSR controlled country in Western Europe ("+str(7-markers),"remaining):")
            target = input("Enter country name: ")
            while doubleCheck > 0: # 

                if target not in COUNTRIES.keys():
                    print("ERROR. COUNTRY NOT FOUND. TRY AGAIN. \n")
                    target = input("Enter country name: ")
                    doubleCheck += 1

                elif "Western Europe" not in COUNTRIES[target][3]:
                    print("ERROR. That country is not in Western Europe. Try another.\n")
                    target = input("Enter country name: ")
                    doubleCheck += 1

                elif COUNTRIES[target][3] == "Soviet Union":
                    print("ERROR. The Soviets control that country. Try another.\n")
                    target = input("Enter country name: ")
                    doubleCheck += 1
                    
                elif target in addedCountries:
                    print("ERROR. You've already added one influence in that country with Marshall. Try another.\n")
                    target = input("Enter country name: ")
                    doubleCheck += 1

                doubleCheck -= 1
                
            COUNTRIES[target][0][0] += 1
            addedCountries.append(target)
            checkControl(COUNTRIES, target)
            
        if SITUATIONS["NATO"][0] == False:
            SITUATIONS[Card][0] = True
        swapSides(FACTION[phasingPlayer])


    elif Card == "Socialist Governments":
        swapSides("Soviet Union")
        
        addedCountries = []
        for markers in range(3):

            doubleCheck = 1
            print("Remove 1 US influence from any country in Western Europe, max 2 per country. ("+str(3-markers),"remaining):")
            target = input("Enter country name: ")
            while doubleCheck > 0: # 

                if target not in COUNTRIES.keys():
                    print("ERROR. COUNTRY NOT FOUND. TRY AGAIN. \n")
                    target = input("Enter country name: ")
                    doubleCheck += 1

                elif "Western Europe" not in COUNTRIES[target][3]:
                    print("ERROR. That country is not in Western Europe. Try another.\n")
                    target = input("Enter country name: ")
                    doubleCheck += 1

                elif COUNTRIES[target][0][0] == 0:
                    print("ERROR. There is no US influence in that country. Try another.\n")
                    target = input("Enter country name: ")
                    doubleCheck += 1
                    
                elif addedCountries.count(target) >= 2:
                    print("ERROR. You've removed the limit of 2 US influence from %s. Try another.\n" % (target))
                    target = input("Enter country name: ")
                    doubleCheck += 1

                doubleCheck -= 1
                
            COUNTRIES[target][0][0] -= 1
            addedCountries.append(target)
            checkControl(COUNTRIES, target)
            
        swapSides(FACTION[phasingPlayer])     


    elif Card == "Suez Crisis":
        swapSides("Soviet Union")

        USFilth = 0
        if COUNTRIES["France"][0][0] >= 2:
            USFilth += 2
        elif COUNTRIES["France"][0][0] >= 1:
            USFilth += 1

        if COUNTRIES["Israel"][0][0] >= 2:
            USFilth += 2
        elif COUNTRIES["Israel"][0][0] >= 1:
            USFilth += 1

        if COUNTRIES["UK"][0][0] >= 2:
            USFilth += 2
        elif COUNTRIES["UK"][0][0] >= 1:
            USFilth += 1
        
        if USFilth > 4: # If less than 4, you'll remove that many times
            USFilth = 4
        
        addedCountries = []
        for markers in range(USFilth):

            doubleCheck = 1
            print("Remove 1 US influence from Israel, France, or the UK. Max 2 per country. ("+str(3-markers),"remaining):")
            target = input("Enter country name: ")
            while doubleCheck > 0: # 

                if target not in COUNTRIES.keys():
                    print("ERROR. COUNTRY NOT FOUND. TRY AGAIN. \n")
                    target = input("Enter country name: ")
                    doubleCheck += 1

                elif target != "France" and target != "UK" and target != "Israel":
                    print("ERROR. You may only remove influence from France, Israel, or UK.\n")
                    target = input("Enter country name: ")
                    doubleCheck += 1                    

                elif COUNTRIES[target][0][0] == 0:
                    print("ERROR. There is no US influence in that country. Try another.\n")
                    target = input("Enter country name: ")
                    doubleCheck += 1
                    
                elif addedCountries.count(target) >= 2:
                    print("ERROR. You've removed the limit of 2 US influence from %s. Try another.\n" % (target))
                    target = input("Enter country name: ")
                    doubleCheck += 1

                doubleCheck -= 1
                
            COUNTRIES[target][0][0] -= 1
            addedCountries.append(target)
            checkControl(COUNTRIES, target)
            
        swapSides(FACTION[phasingPlayer])        


    elif Card == "NATO":
        if SITUATIONS["Marshall Plan"][0] == True:
            SITUATIONS["NATO"][0] = True
        elif SITUATIONS["Warsaw Pact Formed"][0] == True:
            SITUATIONS["NATO"][0] = True
        else:
            cardConditionTriggered = False

        if SITUATIONS["NATO"][0] == True: # Remove Marshall Plan and Warsaw Pact situations once NATO is in
            SITUATIONS["Marshall Plan"][0] = False
            SITUATIONS["Warsaw Pact Formed"][0] = False


    elif Card == "C.I.A. Created":
        print("*.* The C.I.A. has revealed the projects of the Soviets: *.*")
        for card in HANDS[1]:
            print(card)
        print("")

        swapSides("U.S.A.")
        conductOperations(["R","S","I","C"], CARDS[Card] , Card, 1, True, False)
        swapSides(FACTION[phasingPlayer])

    elif Card == "Duck and Cover":
        changeDEFCON(-1)
        print("Duck and cover, people!\nDEFCON NOW AT %d" % (DEFCON) )
        earnVP( (5 - DEFCON) , 0)


    elif Card == "Red Scare/Purge":
        SITUATIONS["Red Scare/Purge"][0] = True
        SITUATIONS["Red Scare/Purge"][1] = FACTION[currentPlayer]
        if currentPlayer == 0:
            print("The Soviets are purging their own ranks...")
        elif currentPlayer == 1:
            print("The paranoid Americans are under a Red Scare...")


    elif Card == "Containment":
        SITUATIONS["Containment"][0] = True
        print("'The communist menace must be contained within their own nations.'")


    elif Card == "Nuclear Test Ban":
        earnVP((DEFCON - 2), currentPlayer)
        changeDEFCON(2)


    elif Card == "Formosan Resolution":
        SITUATIONS["Formosan Resolution"][0] = True
        print("The U.S.A. has pledged its word for the island of Formosa!")


    elif Card == "Vietnam Revolts": # V.R. code for +1 Op not yet implemented
        SITUATIONS["Vietnam Revolts"][0] = True
        COUNTRIES["Vietnam"][0][1] += 2
        print("North Vietnam has won the revolutionary war against the South. Communism rules.")


    elif Card == "US/Japan Mutual Defense Pact":
        SITUATIONS["US/Japan Mutual Defense Pact"][0] = True
        COUNTRIES["Japan"][0][0] += COUNTRIES["Japan"][1] + COUNTRIES["Japan"][0][1] - COUNTRIES["Japan"][0][0]
        print("The U.S.A. and Japan will defend eachother from all adversaries!")


    elif Card == "NORAD":
        SITUATIONS["NORAD"][0] = True
        print("The Canadians have founded NORAD in a joint collaboration with the Americans.")


    elif Card == "Fidel":
        COUNTRIES["Cuba"][0][0] = 0
        COUNTRIES["Cuba"][0][1] = COUNTRIES["Cuba"][1]
        print("Fidel Castro has situated himself comfortably.")


    elif Card == "Romanian Abdication":
        COUNTRIES["Romania"][0][0] = 0
        COUNTRIES["Romania"][0][1] = COUNTRIES["Romania"][1]
        print("The monarch of Romania has abdicated. Communism forcibly seize assets.")


    elif Card == "Nasser":
        COUNTRIES["Egypt"][0][0] = math.floor( (COUNTRIES["Egypt"][0][0] / 2) )
        COUNTRIES["Egypt"][0][1] += 2
        print("Nasser takes helm of Egypt.")


    elif Card == "Decolonization":
        swapSides("Soviet Union")
        addedCountries = []
        for markers in range(4):

            doubleCheck = 1
            print("Add 1 USSR influence to a country in Africa or Southeast Asia ("+str(4-markers),"remaining):")
            target = input("Enter country name: ")
            while doubleCheck > 0: # 

                if target not in COUNTRIES.keys():
                    print("ERROR. COUNTRY NOT FOUND. TRY AGAIN. \n")
                    target = input("Enter country name: ")
                    doubleCheck += 1

                elif "Africa" not in COUNTRIES[target][3] and "Southeast Asia" not in COUNTRIES[target][3]:
                    print("ERROR. That country is not in Africa/SE Asia. Try another.\n")
                    target = input("Enter country name: ")
                    doubleCheck += 1
                    
                elif target in addedCountries:
                    print("ERROR. You've already added one influence in that country with De-col. Try another.\n")
                    target = input("Enter country name: ")
                    doubleCheck += 1

                doubleCheck -= 1
                
            COUNTRIES[target][0][1] += 1
            addedCountries.append(target)
            checkControl(COUNTRIES, target)
        swapSides(FACTION[phasingPlayer])


    elif Card == "Comecon":
        swapSides("Soviet Union")
        addedCountries = []
        for markers in range(4):

            doubleCheck = 1
            print("Add an influence to a non-US controlled country in Eastern Europe ("+str(4-markers),"remaining):")
            target = input("Enter country name: ")
            while doubleCheck > 0: # 

                if target not in COUNTRIES.keys():
                    print("ERROR. COUNTRY NOT FOUND. TRY AGAIN. \n")
                    target = input("Enter country name: ")
                    doubleCheck += 1

                elif "Eastern Europe" not in COUNTRIES[target][3]:
                    print("ERROR. That country is not in Eastern Europe. Try another.\n")
                    target = input("Enter country name: ")
                    doubleCheck += 1

                elif COUNTRIES[target][3] == "U.S.A.":
                    print("ERROR. The Americans control that country. Try another.\n")
                    target = input("Enter country name: ")
                    doubleCheck += 1
                    
                elif target in addedCountries:
                    print("ERROR. You've already added one influence in that country with Comecon. Try another.\n")
                    target = input("Enter country name: ")
                    doubleCheck += 1

                doubleCheck -= 1
                
            COUNTRIES[target][0][1] += 1
            addedCountries.append(target)
            checkControl(COUNTRIES, target)
        swapSides(FACTION[phasingPlayer])

    elif Card == "East European Unrest":
        swapSides("U.S.A")
        validCountries = []
        for easternEuropeCountry in COUNTRIES:
            if (COUNTRIES[easternEuropeCountry][0][1] > 0 and 
                "Eastern Europe" in COUNTRIES[easternEuropeCountry][3]):
                validCountries.append( easternEuropeCountry )
                    
        if len(validCountries) < 3:
            x = len(validCountries)
        else:
            x = 3

        print(CARDS[Card][0])
        for attempt in range(x):
            if len(validCountries) > 0:
                target = input("Enter country name: ")
                while target not in validCountries: 
                    print("ERROR. That is not a country in Eastern Europe. Try another.\n")
                    target = input("Enter country name: ")

                if warStage != "Late War":
                    COUNTRIES[target][0][1] -= 1
                elif warStage == "Late War":
                    COUNTRIES[target][0][1] -= 2
                checkControl(COUNTRIES, target)
            else:
                print("There are no more Eastern Europe countries with Soviet influence.")
                cardConditionTriggered = False

        swapSides(FACTION[phasingPlayer])


    elif Card == "Captured Nazi Scientists":
        spaceAction(1, "Captured Nazi Scientists")
        print("The captured scientists have boosted the development of %s." % (SPACE[currentPlayer][0]) )


    elif Card == "UN Intervention":
        doubleCheck = 1
        print(CARDS[Card][0])
        cardNum = input("\n - Choose card # from hand:\n")

        while doubleCheck > 0:

            if (cardNum.isdigit() == False or int(cardNum) < 1 or int(cardNum) > len(HANDS[currentPlayer])):
                print("ERROR. Invalid input. Enter only the card's ordering number in your hand.")
                cardNum = input("\n - Choose card # to play from hand:\n")   
                doubleCheck += 1  

            elif (CARDS[HANDS[currentPlayer][int(cardNum)-1]][2] == "Neutral" or
                    CARDS[HANDS[currentPlayer][int(cardNum)-1]][2] == FACTION[currentPlayer]):
                print("ERROR. Invalid input. You may only use UN Intervention with opponent-associated cards.")
                cardNum = input("\n - Choose card # to play from hand:\n")   
                doubleCheck += 1  

            doubleCheck -= 1

        # U2 Incident will score Soviet player 1 VP for UN
        if SITUATIONS["U2 Incident"][0] == True:
            earnVP(1, 1)
            SITUATIONS["U2 Incident"][0] = False
            print("The UN have reviewed the recent U2 Incident on its gathering.")

        cardName = HANDS[currentPlayer][int(cardNum)-1]
        card = CARDS[cardName]
        conductOperations(["R","S","I","C"], card, cardName, card[1], True, False)
        discardCard(cardName, False, False)
        print("The UN has intervened in the %s crisis. It is safely discarded." % (cardName) )


    elif Card == "Truman Doctrine":
        swapSides("U.S.A.")
        doubleCheck = 1
        print("Choose a country in Europe neither power has control of to remove all USSR influence:")
        target = input("Enter country name: ")
        while doubleCheck > 0: # 

            if target not in COUNTRIES.keys():
                print("ERROR. COUNTRY NOT FOUND. TRY AGAIN. \n")
                target = input("Enter country name: ")
                doubleCheck += 1

            elif "Europe" not in COUNTRIES[target][3]:
                print("ERROR. That country is not in Europe. Try another.\n")
                target = input("Enter country name: ")
                doubleCheck += 1

            elif COUNTRIES[target][4] != "None":
                print("ERROR. Truman cannot oust a controlled country.\n")
                target = input("Enter country name: ")
                doubleCheck += 1

            doubleCheck -= 1

        COUNTRIES[target][0][1] = 0
        checkControl(COUNTRIES, target)
        swapSides(FACTION[phasingPlayer])


    elif Card == "Independent Reds":
        swapSides("U.S.A")
        validCountries = []
        for slavicCountry in COUNTRIES:
            if (slavicCountry == "Romania" or slavicCountry == "Bulgaria" or
                slavicCountry == "Hungary" or slavicCountry == "Yugoslavia" or
                slavicCountry == "Czechoslovakia"):
                if COUNTRIES[slavicCountry][0][1] > 0:
                    validCountries.append( slavicCountry )
                    
        print(CARDS[Card][0])
        if len(validCountries) > 0:
            target = input("Enter country name: ")
            while target not in validCountries: 
                print("ERROR. That is not the requested country. Try another.\n")
                target = input("Enter country name: ")


            COUNTRIES[target][0][0] = COUNTRIES[target][0][1]
            checkControl(COUNTRIES, target)
        else:
            print("Not a single one of those countries have Soviet influence.")
            cardConditionTriggered = False
        swapSides(FACTION[phasingPlayer])


    elif Card == "Special Relationship":
        if COUNTRIES["UK"][4] == "U.S.A.":
            if SITUATIONS["NATO"][0] == True:
                swapSides("U.S.A.")
                print("The U.S. may add 2 U.S. influence to any country in Western Europe.")
                target = input("Choose country: ")
                while target not in COUNTRIES.keys() or "Western Europe" not in COUNTRIES[target][3]: 
                    print("ERROR. Invalid country. Try again.")
                    target = input("Choose country: ")

                COUNTRIES[target][0][0] += 2
                earnVP(2, 0)
                swapSides(FACTION[phasingPlayer])
                print("The Anglo-sphere have a benevolent vision for Europe.")

            elif SITUATIONS["NATO"][0] == False:
                swapSides("U.S.A.")
                for adj in COUNTRIES["UK"][-1]:
                    print(adj, end=", ")

                target = input("\nAdd 1 US influence to a country adjacent to the UK: ")
                while target not in COUNTRIES["UK"][-1]: 
                    print("ERROR. That is not adjacent to the UK. Try again.")
                    target = input("Add 1 US influence to a country adjacent to the UK: ")

                COUNTRIES[target][0][0] += 1
                swapSides(FACTION[phasingPlayer])
                print("Through and through, the U.S. and U.K. stick together!")
        else:
            print("Souring relations between the Queen and Uncle Sam prevent collaboration.")

        
    elif Card == "Olympic Games":
        host = FACTION[currentPlayer]
        swapSides("Swap")
        print("%s, you may either [P]articipate in the %s, or [B]oycott it." % (FACTION[currentPlayer], Card))
        decision = input("CHOOSE: ")
        while decision != "P" and decision != "p" and decision != "B" and decision != "b":
            decision = input("INPUT ERROR DETECTED. Try again. [P]/[B] \n")
        decision = decision.upper()

        swapSides("Swap")
        if decision == "P":
            USAmodifier = 0
            SOVIETmodifier = 0
            if host == "U.S.A.":
                USAmodifier += 2
            elif host == "Soviet Union":
                SOVIETmodifier += 2

            repeatRolls = True  # Repeat rolls if tied
            while repeatRolls == True:
                USAdice = random.randint(1, 6) + USAmodifier
                SOVIETdice = random.randint(1, 6) + SOVIETmodifier
                print("%s result: %d | %s result: %d" % ("U.S.A.", USAdice, "Soviet Union", SOVIETdice))
                if USAdice > SOVIETdice:
                    earnVP(2, 0)
                    repeatRolls = False
                elif SOVIETdice > USAdice:
                    earnVP(2, 1)
                    repeatRolls = False

        elif decision == "B":
            changeDEFCON(-1)
            conductOperations(["R","S","I","C"], CARDS[Card] , Card, 4, True, False)
            

    elif Card == "Korean War":
        enemyDefense = 0
        for adjEnemyCountry in COUNTRIES["South Korea"][-1]:
            if COUNTRIES[adjEnemyCountry][4] == "U.S.A.":
                enemyDefense += 1

        warResult = random.randint(1, 6)
        print("DICE:" , str(warResult) )
        if warResult > (3 + enemyDefense): # Victory
            print("North Korea has annexed its southern brother! It is now whole again, unified under hammer & sickle.")
            COUNTRIES["South Korea"][0][1] += COUNTRIES["South Korea"][0][0]
            COUNTRIES["South Korea"][0][0] = 0
            earnVP(2, 1)
        else:
            print("The invasion has failed! U.S. troops alongside UN forces have secured the 38th parallel!")

        MILOPS[1] += 2 # Create function for adding Milops IMO. Cant have more than 5.


    elif Card == "Arab-Israeli War":
        if SITUATIONS["Camp David Accords"][0] != True: # Camp David blocks Arab

            enemyDefense = 0
            for adjEnemyCountry in COUNTRIES["Israel"][-1]:
                if COUNTRIES[adjEnemyCountry][4] == "U.S.A.":
                    enemyDefense += 1

            warResult = random.randint(1, 6)
            print("DICE:" , str(warResult) )
            if warResult > (3 + enemyDefense): # Victory
                print("Muslim crusaders, backed by Soviet munition, have conquered Israel.")
                COUNTRIES["Israel"][0][1] += COUNTRIES["Israel"][0][0]
                COUNTRIES["Israel"][0][0] = 0
                earnVP(2, 1)
            else:
                print("Within a week, Israel concluded the war still standing.")

            MILOPS[1] += 2 # Create function for adding Milops IMO. Cant have more than 5.

        else:
            cardConditionTriggered = False
            print("The Camp David Accords are maintaining the peace between Israel and the Muslim world.")


    elif Card == "Indo-Pakistani War":
        target = input("Choose India, or Pakistan to be the target:\n")
        if target != "Pakistan" and target != "India":
            target = input("Input error. Enter India or Pakistan:\n")

        enemyDefense = 0
        for adjEnemyCountry in COUNTRIES[target][-1]:
            if COUNTRIES[adjEnemyCountry][4] == FACTION[otherPlayer]:
                enemyDefense += 1

        warResult = random.randint(1, 6)
        print("DICE:" , str(warResult) )
        if warResult > (3 + enemyDefense): # Victory
            print("Glittering idealogues, paid for in blood... %s now controls %s." % (FACTION[currentPlayer], target))
            COUNTRIES[target][0][currentPlayer] += COUNTRIES[target][0][otherPlayer]
            COUNTRIES[target][0][otherPlayer] = 0
            earnVP(2, currentPlayer)

        else:
            print("The infighting over in the Indian sub-continent has resulted in no gains.")

        MILOPS[currentPlayer] += 2 # Create function for adding Milops IMO. Cant have more than 5.
            

    elif Card == "Blockade":
        swapSides("U.S.A.")
        for count, card in enumerate(HANDS[currentPlayer]):
            if CARDS[card][2] == "U.S.A.":
                print("#%d -- %d *.* %s" % (count+1, CARDS[card][1], card))
            elif CARDS[card][2] == "Soviet Union":
                print("#%d -- %d |-/ %s" % (count+1, CARDS[card][1], card))
            elif CARDS[card][2] == "Neutral":
                print("#%d -- %d === %s" % (count+1, CARDS[card][1], card))

        repeating = True

        print("\n*.* US, you must discard a card of 3+ Op value, or lose all influence in West Germany. *.*")
        while repeating:
            chooseCard = input("Choose card # to discard, OR [D]o not discard.\n")
            
            if chooseCard.isdigit() == True:
                if int(chooseCard)-1 < 1 or int(chooseCard)-1 > len(HANDS[currentPlayer]):
                    print("ERROR. That is not a valid card number. Try again.")
                    chooseCard = input("Choose card # to discard, OR [D]o not discard.\n")

                elif CARDS[HANDS[currentPlayer][int(chooseCard)-1]][1] >= 3:
                    cardNameBlockade = HANDS[currentPlayer][int(chooseCard)-1]
                    DISCARD_PILE.append(cardNameBlockade)
                    HANDS[currentPlayer].remove(cardNameBlockade)
                    print("The Allies have dropped their plans for %s to save Berlin!" % (cardNameBlockade))
                    repeating = False
                
            else:
                if chooseCard != "D" and chooseCard != "d":
                    print("ERROR. That is not the discard command. Try again.")
                    chooseCard = input("Choose card # to discard, OR [D]o not discard.\n")

                else:
                    COUNTRIES["West Germany"][0][0] = 0
                    print("The Allies abandoned Berlin... German support shattered.")
                    checkControl(COUNTRIES, "West Germany")
                    repeating = False                                        

        swapSides(FACTION[phasingPlayer])


    elif Card == "Warsaw Pact Formed":
        swapSides("Soviet Union")

        choice = input("[R]emove all US influence from 4 Eastern Europe countries, OR [A]dd 5 Influence to Eastern Europe.")
        while choice != "R" and choice != "r" and choice != "A" and choice != "a":
            choice = input("Input error. Please try again. [R]emove US influence, or [A]dd USSR influence.")

        if choice == "A" or choice == "a":
            addedCountries = []
            for markers in range(5):

                doubleCheck = 1
                print("Add 1 Soviet influence to any country in Eastern Europe, max 2 per country. ("+str(5-markers),"remaining):")
                target = input("Enter country name: ")
                while doubleCheck > 0: # 

                    if target not in COUNTRIES.keys():
                        print("ERROR. COUNTRY NOT FOUND. TRY AGAIN. \n")
                        target = input("Enter country name: ")
                        doubleCheck += 1

                    elif "Eastern Europe" not in COUNTRIES[target][3]:
                        print("ERROR. That country is not in Eastern Europe. Try another.\n")
                        target = input("Enter country name: ")
                        doubleCheck += 1
                        
                    elif addedCountries.count(target) >= 2:
                        print("ERROR. You've added the limit of 2 USSR influence to %s. Try another.\n" % (target))
                        target = input("Enter country name: ")
                        doubleCheck += 1

                    doubleCheck -= 1
                    
                COUNTRIES[target][0][1] += 1
                addedCountries.append(target)
                checkControl(COUNTRIES, target)
                
                
        elif choice == "R" or choice == "r":
            USfilth = []
            for country in COUNTRIES:
                if "Eastern Europe" in COUNTRIES[country][3] and COUNTRIES[country][0][0] > 0:
                    USfilth.append( country )

            if len(USfilth) > 0:
                for instance in USfilth:
                    print(instance, end=", ")
                        
                repeatXtimes = len(USfilth) # If less than 4, you'll remove that many times
                if repeatXtimes > 4:
                    repeatXtimes = 4

                for markers in range(repeatXtimes):
                    doubleCheck = 1
                    print("Remove all US influence in an Eastern European country. ("+str(4-markers),"remaining):")
                    target = input("Enter country name: ")
                    while doubleCheck > 0: # 

                        if target not in COUNTRIES.keys():
                            print("ERROR. COUNTRY NOT FOUND. TRY AGAIN. \n")
                            target = input("Enter country name: ")
                            doubleCheck += 1

                        elif "Eastern Europe" not in COUNTRIES[target][3]:
                            print("ERROR. That country is not in Eastern Europe. Try another.\n")
                            target = input("Enter country name: ")
                            doubleCheck += 1

                        elif COUNTRIES[target][0][0] == 0:
                            print("ERROR. There is no US influence in that country.\n")
                            target = input("Enter country name: ")
                            doubleCheck += 1

                        doubleCheck -= 1

                    COUNTRIES[target][0][0] = 0
                    checkControl(COUNTRIES, target)

            #else:
                # If you can't remove, then make the USSR add influence instead. It makes it nicer.

        if SITUATIONS["NATO"][0] == False:
            SITUATIONS[Card][0] = True
            print("The Warsaw Pact has been established, clarifying the true hegemon.")
        swapSides(FACTION[phasingPlayer]) 


    elif Card == "De-Stalinization":
        swapSides("Soviet Union")        
        influenceRemoved = 0
        allowance = 4
        countriesAdded = []

        print(CARDS[Card][0]) # Description
        while allowance > 0:
            target = input("Take 1 influence from country, OR [S]top: ")
            while (target not in COUNTRIES.keys() or COUNTRIES[target][0][1] == 0
                    and (target != "S" or target != "s")):
                if target not in COUNTRIES.keys():
                    print("ERROR. COUNTRY NOT FOUND. TRY AGAIN. ")
                elif COUNTRIES[target][0][1] == 0:
                    print("ERROR. COUNTRY HAS NO SOVIET INFLUENCE. TRY AGAIN. ")
                target = input("Enter country name: ")

            if target == "S" or target == "s":
                break
            else:
                COUNTRIES[target][0][1] -= 1
                influenceRemoved += 1
                allowance -= 1
                checkControl(COUNTRIES, target)
                print("")

        while influenceRemoved > 0:
            doubleCheck = 1
            print("Add 1 influence to non-USA controlled countries (%d remaining)." % (influenceRemoved))
            target = input("Enter country name: ")
            while doubleCheck > 0: # 

                if target not in COUNTRIES.keys():
                    print("ERROR. COUNTRY NOT FOUND. TRY AGAIN. ")
                    target = input("Enter country name: ")
                    doubleCheck += 1

                elif COUNTRIES[target][3] == "U.S.A.":
                    print("ERROR. The Americans control that country. Try another.")
                    target = input("Enter country name: ")
                    doubleCheck += 1
                    
                elif countriesAdded.count(target) >= 2:
                    print("ERROR. You've already added 2 influence in %s. Try another." % (target))
                    target = input("Enter country name: ")
                    doubleCheck += 1

                doubleCheck -= 1
                
            COUNTRIES[target][0][1] += 1
            countriesAdded.append(target)
            checkControl(COUNTRIES, target)
            influenceRemoved -= 1
        
        print("\nWith the disillusionment of Stalin, a new era has begun in the socialist world!\n")
        swapSides(FACTION[phasingPlayer]) 
    
########################################
########### MID WAR CARDS ##############
########################################

# Bug -- As USA, triggering event and then using it for ops will instantly suffer -3 VP. Check must be done on NEXT turn 
    elif Card == "'We Will Bury You'":
        changeDEFCON(-1)
        print("'Whether you like it or not, history is on our side. We will bury you!'\nDEFCON NOW AT %d" % (DEFCON) )
        SITUATIONS["'We Will Bury You'"][0] = True


    elif Card == "Muslim Revolution":
        if SITUATIONS["AWACS Sale to Saudis"][0] == True:
            print("Saudi Arabia agrees to curtail revolutions in light of their new AWACS.")
        else:
            swapSides("Soviet Union") 
            muslimCountries = ["Sudan", "Libya", "Egypt", "Jordan", "Syria", "Iraq", "Saudi Arabia", "Iran"]
            USfilth = []
            for country in muslimCountries:
                if COUNTRIES[country][0][0] > 0:
                    USfilth.append(country)

            print(CARDS[Card][0])
            print(" ! Muslim countries that have US influence:")
            for x in USfilth:
                print(x, end=" | ")

            if len(USfilth) < 2:
                muslimRevs = len(USfilth)
            else:
                muslimRevs = 2

            while muslimRevs > 0:
                target = input("\nEnter country name: \n")
                if target not in USfilth:
                    target = input("ERROR. Not a valid country for a revolution. \nEnter country name: \n")

                COUNTRIES[target][0][0] = 0
                checkControl(COUNTRIES, target)
                
            print("The Western oppressors must die!")
            swapSides(FACTION[phasingPlayer]) 


    elif Card == "Flower Power":
        SITUATIONS["Flower Power"][0] = True
        print("Pacifist factions within the U.S. are protesting violence in war.")
    # HAVE NOT ADDED CODE FOR FLOWER POWER TO WORK PROPERLY


    elif Card == "Quagmire":
        SITUATIONS["Quagmire"][0] = True


    elif Card == "Breznev Doctrine":
        SITUATIONS["Breznev Doctrine"][0] = True


    elif Card == "U2 Incident":
        SITUATIONS["U2 Incident"][0] = True

    
    elif Card == "Cultural Revolution":
        if CARDS["The China Card"][3] == "Soviet Union":
            earnVP(1, 1)
        elif CARDS["The China Card"][3] == "U.S.A.":
            CARDS["The China Card"][3] = "Soviet Union"
            CARDS["The China Card"][4] = True

        print("Mao Zedong's vision for China has come to fruition - the eradication of the bourgeoisie.")

    
    elif Card == "OPEC":
        oilCountries = ["Venezuela","Libya","Egypt","Iraq","Iran","Saudi Arabia","Gulf States"]
        oilVP = 0

        if SITUATIONS["North Sea Oil"] != False: # OPEC activates, unless North Sea Oil is in play
            for country in oilCountries:
                if COUNTRIES[country][4] == "Soviet Union":
                    oilVP += 1

            if oilVP > 0:
                earnVP(oilVP, 1)
                print("The OPEC giants answer only to the Soviets.")
            else:
                print("The West enjoy favorable prices of their precious oil.")

        elif SITUATIONS["North Sea Oil"] == True:
            print("The oil reserves found in the North Sea are satisfying the demand for gasoline!")


    elif Card == "Che":
        swapSides("Soviet Union")
        print("Che has risen! The revolution is staged in...")

        doubleCoup = coupAction(CARDS["Che"][1], "Normal", "Che", True)
        if doubleCoup == True: # If US influence is removed, repeat the coup
            x = coupAction(CARDS["Che"][1], "Normal", "Che", True) # Placeholder variable to soak the result

        swapSides(FACTION[phasingPlayer]) 


    elif Card == "Portuguese Empire Crumbles":
        COUNTRIES["Angola"][0][1] += 2
        COUNTRIES["SE African States"][0][1] += 2
        print("The colonial slave masters have lost power within Africa.")


    elif Card == "South African Unrest":
        swapSides("Soviet Union")
        choice = input("#[1] Add 1 USSR influence to South Africa and 2 in an adjacent country, or #[2] Add 2 USSR influence to South Africa.")
        while choice != "1" and choice != "2":
            choice = input("Input error. Please try again. Enter [1] or [2].")

        if choice == "1":
            COUNTRIES["South Africa"][0][1] += 1
            for x in range(2):
                target = input("Add influence to [A]ngola or [B]otswana:\n")
                while target != "B" and choice != "b" and choice != "A" and choice != "a":
                    target = input("ERROR. Invalid input. Enter [A] or [B]:\n")

                if target == "A" or target == "a":
                    COUNTRIES["Angola"][0][1] += 1
                elif target == "B" or target == "b":
                    COUNTRIES["Botswana"][0][1] += 1
            print("Unrest in South Africa is boiling over to adjacent countries!")

        elif choice == "2":
            COUNTRIES["South Africa"][0][1] += 2
            print("Riot police in South Africa cannot get a handle on the situation!")

        swapSides(FACTION[phasingPlayer]) 


    elif Card == "Willy Brandt":
        earnVP(1, 1)
        COUNTRIES["West Germany"][0][1] += 1
        SITUATIONS["Willy Brandt"][0] = True
        print("Willy Brandt promises the reunification of Germany!")
    

    elif Card == "Liberation Theology":
        addedCountries = []
        for markers in range(3):

            doubleCheck = 1
            print("Add 1 Soviet influence to any country in Central America, max 2 per country. ("+str(3-markers),"remaining):")
            target = input("Enter country name: ")
            while doubleCheck > 0: 

                if target not in COUNTRIES.keys():
                    print("ERROR. COUNTRY NOT FOUND. TRY AGAIN. \n")
                    target = input("Enter country name: ")
                    doubleCheck += 1

                elif "Central America" not in COUNTRIES[target][3]:
                    print("ERROR. That country is not in Central America. Try another.\n")
                    target = input("Enter country name: ")
                    doubleCheck += 1
                    
                elif addedCountries.count(target) >= 2:
                    print("ERROR. You've added the limit of 2 USSR influence to %s. Try another.\n" % (target))
                    target = input("Enter country name: ")
                    doubleCheck += 1

                doubleCheck -= 1
                
            COUNTRIES[target][0][1] += 1
            addedCountries.append(target)
            checkControl(COUNTRIES, target)

        print("Influential debaters have made many catholic nations re-interpret the intentions of Jesus Christ.")


    elif Card == "Allende":
        COUNTRIES["Chile"][0][1] += 2
        print("Allende has nationalized the industries of Chile.")


    elif Card == "Lone Gunman":
        print("|-/ A Lone Gunman caused chaos within the U.S.: \-|")
        for card in HANDS[0]:
            print(card)
        print("")

        swapSides("Sovet Union")
        conductOperations(["R","S","I","C"], CARDS[Card] , Card, 1, True, False)
        swapSides(FACTION[phasingPlayer])


    elif Card == "Ussuri River Skirmish":
        if CARDS["The China Card"][3] == "Soviet Union":
            CARDS["The China Card"][3] = "U.S.A."
            CARDS["The China Card"][4] = True
        elif CARDS["The China Card"][3] == "U.S.A.":
            swapSides("U.S.A.")

            addedCountries = []
            for markers in range(4):

                doubleCheck = 1
                print("Add 1 US to any country in Asia, max 2 per country. ("+str(4-markers),"remaining):")
                target = input("Enter country name: ")
                while doubleCheck > 0: 

                    if target not in COUNTRIES.keys():
                        print("ERROR. COUNTRY NOT FOUND. TRY AGAIN. \n")
                        target = input("Enter country name: ")
                        doubleCheck += 1

                    elif "Asia" not in COUNTRIES[target][3]:
                        print("ERROR. That country is not in Asia. Try another.\n")
                        target = input("Enter country name: ")
                        doubleCheck += 1
                        
                    elif addedCountries.count(target) >= 2:
                        print("ERROR. You've added the limit of 2 US influence to %s. Try another.\n" % (target))
                        target = input("Enter country name: ")
                        doubleCheck += 1

                    doubleCheck -= 1
                    
                COUNTRIES[target][0][0] += 1
                addedCountries.append(target)
                checkControl(COUNTRIES, target)


            swapSides(FACTION[phasingPlayer])


        print("Differences between the Russian and Chinese counterparts are creating a schism.") 


    elif Card == "'Ask Not What Your Country…'":
        swapSides("U.S.A.")  

        numDiscarded = 0
        while True:
            for i, card in enumerate(HANDS[0]):
                print("#" + str(i+1) , card)
            print("\n" + CARDS[Card][0])

            print("\n*.* Discard card #, OR [S]top: *.*")
            choice = input("")

            while ( HANDS[0][int(choice)-1] == "'Ask Not What Your Country…'" or choice != "S" and choice != "s" and 
                (int(choice) < 1 or int(choice) > len(HANDS[0])) ):
                print("ERROR. Invalid input. Enter only the card's ordering number in your hand.")
                choice = input("")

            if "S" in choice or "s" in choice: # Player stopped discarding
                break

            cardName = HANDS[0][int(choice)-1]
            print("Discarded %s" % (cardName))
            discardCard(cardName, False, False)
            numDiscarded += 1

        if numDiscarded > 0:
            drawCards(DRAW_PILE, numDiscarded, HANDS[0])

        print("... can do for you... Ask what YOU can do for your country!")
        swapSides(FACTION[phasingPlayer])    


    elif Card == "Alliance for Progress":
        BGcontrolled = 0
        for latinCountry in COUNTRIES:
            if latinCountry[2] == True and "America" in latinCountry[3] and latinCountry[4] == "U.S.A.":
                BGcontrolled += 1

        if BGcontrolled > 0:
            earnVP(BGcontrolled, 0)
        else:
            cardConditionTriggered = False

        print("Monroe Doctrine echoes throughout the western hemisphere.")


    elif Card == "Bear Trap":
        SITUATIONS["Bear Trap"][0] = True
        print("The Soviets are bogged down in Afghanistan!")


    elif Card == "Shuttle Diplomacy":
        SITUATIONS["Shuttle Diplomacy"][0] = True


    elif Card == "The Voice of America":
        swapSides("U.S.A.")
        removedCountries = []
        for markers in range(4):

            doubleCheck = 1
            print("Remove 1 Soviet influence from any non-European country, max 2 per country. ("+str(4-markers),"remaining):")
            target = input("Enter country name: ")
            while doubleCheck > 0: 

                if target not in COUNTRIES.keys():
                    print("ERROR. COUNTRY NOT FOUND. TRY AGAIN. \n")
                    target = input("Enter country name: ")
                    doubleCheck += 1

                elif "Europe" in COUNTRIES[target][3]:
                    print("ERROR. You may not remove influence from Europe. Try another.\n")
                    target = input("Enter country name: ")
                    doubleCheck += 1
                    
                elif removedCountries.count(target) >= 2:
                    print("ERROR. You've removed the limit of 2 USSR influence from %s. Try another.\n" % (target))
                    target = input("Enter country name: ")
                    doubleCheck += 1

                doubleCheck -= 1
                
            COUNTRIES[target][0][1] -= 1
            removedCountries.append(target)
            checkControl(COUNTRIES, target)

        print("Underground radio stations tune into the un-filtered Western World.")
        swapSides(FACTION[phasingPlayer])


    elif Card == "Camp David Accords":
        earnVP(1, 0)
        SITUATIONS["Camp David Accords"][0] = True
        COUNTRIES["Israel"][0][0] += 1
        COUNTRIES["Egypt"][0][0] += 1
        COUNTRIES["Jordan"][0][0] += 1
        print("President Carter has made historic in-grounds within the Middle East.")


    elif Card == "Nixon Plays the China Card":
        if CARDS["The China Card"][3] == "Soviet Union":
            CARDS["The China Card"][3] = "U.S.A."
            CARDS["The China Card"][4] = False
        elif CARDS["The China Card"][3] == "U.S.A.":
            earnVP(2, 0)
        print("China will prove to be an important powerhouse, according to Nixon.")


    elif Card == "Nuclear Subs":
        SITUATIONS["Nuclear Subs"][0] = True
        print("Nautilus, the first Nuclear submarine, has launched itself from the Thames river.")


    elif Card == "Colonial Rear Guards":
        swapSides("U.S.A.")
        addedCountries = []
        for markers in range(4):

            doubleCheck = 1
            print("Add 1 US influence to a country in Africa or Southeast Asia ("+str(4-markers),"remaining):")
            target = input("Enter country name: ")
            while doubleCheck > 0: # 

                if target not in COUNTRIES.keys():
                    print("ERROR. COUNTRY NOT FOUND. TRY AGAIN. \n")
                    target = input("Enter country name: ")
                    doubleCheck += 1

                elif "Africa" not in COUNTRIES[target][3] and "Southeast Asia" not in COUNTRIES[target][3]:
                    print("ERROR. That country is not in Africa/SE Asia. Try another.\n")
                    target = input("Enter country name: ")
                    doubleCheck += 1
                    
                elif target in addedCountries:
                    print("ERROR. You've already added one influence in that country with Colonials. Try another.\n")
                    target = input("Enter country name: ")
                    doubleCheck += 1

                doubleCheck -= 1
                
            COUNTRIES[target][0][0] += 1
            addedCountries.append(target)
            checkControl(COUNTRIES, target)
        swapSides(FACTION[phasingPlayer])


    elif Card == "Puppet Governments":
        swapSides("U.S.A.")
        for markers in range(3):

            doubleCheck = 1
            print("Add 1 US influence to any country with no influence from either power ("+str(3-markers),"remaining):")
            target = input("Enter country name: ")
            while doubleCheck > 0: # 

                if target not in COUNTRIES.keys():
                    print("ERROR. COUNTRY NOT FOUND. TRY AGAIN. \n")
                    target = input("Enter country name: ")
                    doubleCheck += 1

                elif COUNTRIES[target][0][0] > 0 or COUNTRIES[target][0][1] > 0:
                    print("ERROR. THERE IS INFLUENCE IN THAT COUNTRY. TRY AGAIN. \n")
                    target = input("Enter country name: ")
                    doubleCheck += 1                    

                doubleCheck -= 1
                
            COUNTRIES[target][0][0] += 1
            checkControl(COUNTRIES, target)

        print("The puppets are now in place, the seeds of a new generation shall germinate.")
        swapSides(FACTION[phasingPlayer])


    elif Card == "Grain Sales to Soviets": # THIS NEEDS DEBUGGING
        swapSides("U.S.A.")
        if len(HANDS[1]) > 1:
            randomlyDrawn = HANDS[1][random.randint(0, len(HANDS[1])-1 )]
            while randomlyDrawn == "Grain Sales to Soviets": # Do not randomly select and discard Grain Sales itself
                randomlyDrawn = HANDS[1][random.randint(0, len(HANDS[1])-1 )]

            randomlyDrawn = HANDS[1].index(randomlyDrawn) # Turn random card into its index - then remove it from the hand
            cardPlanned = HANDS[1].pop(randomlyDrawn)
            card = CARDS[cardPlanned]

            print("Grain Sales has fished up %s." % (cardPlanned) )
            print("*.* U.S. - play the card, or return it back to Soviet's hand and play Grain Sales for ops.")
            returnOrPlay = input("ENTER: [P]lay or [R]eturn.")
            while returnOrPlay != "P" and returnOrPlay != "p" and returnOrPlay != "R" and returnOrPlay != "r":
                returnOrPlay = input("ERROR, INVALID INPUT. Enter [P] or [R].")

            if returnOrPlay == "P" or returnOrPlay == "p":
                conductOperations(["R","S","E","I","C"], card, cardPlanned, card[1], False, True)
            else:
                HANDS[1].append(cardPlanned)
                card = CARDS["Grain Sales to Soviets"]
                conductOperations(["R","S","E","I","C"], card, "Grain Sales to Soviets", card[1], True, False) 

        else: # No card to be taken; so use Grain Sales itself to do ops
            card = CARDS["Grain Sales to Soviets"]
            conductOperations(["R","S","E","I","C"], card, "Grain Sales to Soviets", card[1], True, False) 
            

        swapSides(FACTION[phasingPlayer])
    #dadw

    elif Card == "John Paul II Elected Pope":
        COUNTRIES["Poland"][0][1] -= 2
        COUNTRIES["Poland"][0][0] += 1
        SITUATIONS["John Paul II Elected Pope"][0] = True
        checkControl(COUNTRIES, "Poland")
        print("The Pope denounces Communism for being 'godless and immoral'!")


    elif Card == "Our Man in Tehran":
        swapSides("U.S.A.")
        OMITcards = []

        drawCards(DRAW_PILE, 5, OMITcards)
        for i, card in enumerate(OMITcards):
            print("#" + str(i+1) , card)
        print("\n" + CARDS[Card][0])

        while True:
            print("\n*.* Discard card #, OR [S]top: *.*")
            choice = input("")

            while choice != "S" or choice != "s" and (choice.isdigit() == False or int(choice) < 1 or int(choice) > len(OMITcards)):
                print("ERROR. Invalid input. Enter only the card's ordering number in your hand.")
                choice = input("")

            if "S" in choice or "s" in choice: # Player stopped discarding
                break

            cardName = OMITcards[int(choice)-1]
            discardCard(cardName, False, False)

        print("Our Man has informed us of Soviet plans.")
        swapSides(FACTION[phasingPlayer])


    elif Card == "OAS Founded":
        swapSides("U.S.A.")
        for markers in range(2):

            doubleCheck = 1
            print("Add 1 US influence to any country with in Central or South America ("+str(2-markers),"remaining):")
            target = input("Enter country name: ")
            while doubleCheck > 0:

                if target not in COUNTRIES.keys():
                    print("ERROR. COUNTRY NOT FOUND. TRY AGAIN. \n")
                    target = input("Enter country name: ")
                    doubleCheck += 1

                elif "America" not in COUNTRIES[target][3]:
                    print("ERROR. COUNTRY NOT IN AMERICAS. TRY AGAIN. \n")
                    target = input("Enter country name: ")
                    doubleCheck += 1                                       

                doubleCheck -= 1
                
            COUNTRIES[target][0][0] += 1
            checkControl(COUNTRIES, target)

        print("May this be a sign for closer ties between the countries of America and the U.S.")
        swapSides(FACTION[phasingPlayer])


    elif Card == "Sadat Expels Soviets":
        COUNTRIES["Egypt"][0][1] = 0
        COUNTRIES["Egypt"][0][0] += 1
        checkControl(COUNTRIES, "Egypt")
        print("The Soviets are fleeing Egypt like plague locusts.")


    elif Card == "Kitchen Debates":
        BGcontrolled = [0, 0]
        for country in COUNTRIES:
            if country[2] == True and country[4] == "U.S.A.":
                BGcontrolled[0] += 1
            elif country[2] == True and country[4] == "Soviet Union":
                BGcontrolled[1] += 1

        if BGcontrolled[0] > BGcontrolled[1]:
            earnVP(2, 0)
            print("Poke!")
        else:
            cardConditionTriggered = False


    elif Card == "Panama Canal Returned":
        COUNTRIES["Costa Rica"][0][0] += 1
        COUNTRIES["Panama"][0][0] += 1
        COUNTRIES["Venezuela"][0][0] += 1
        print("The Panama Canal is returned to its rightful owner.")


    elif Card == "ABM Treaty":
        changeDEFCON(1)
        conductOperations(["R","S","I","C"], CARDS[Card] , Card, 4, True, False)


    elif Card == "Brush War":
        target = input("Enter a 2 stability country to Brush War:\n")
    # USSR May not brush war Italy if NATO is active
        while COUNTRIES[target][1] > 2 or (target == "Italy" and SITUATIONS["NATO"][0] == True and currentPlayer == 1):
            target = input("INVALID TARGET. TOO HIGH STABILITY. Choose another country:\n") 

        enemyDefense = 0
        for adjEnemyCountry in COUNTRIES[target][-1]:
            if COUNTRIES[adjEnemyCountry][4] == FACTION[otherPlayer]:
                enemyDefense += 1

        warResult = random.randint(1, 6)
        print("DICE:" , str(warResult) )
        if warResult > (2 + enemyDefense): # Victory
            print("A guerilla squad funded by the %s has capitulated %s." % (FACTION[currentPlayer], target))
            COUNTRIES[target][0][currentPlayer] += COUNTRIES[target][0][otherPlayer]
            COUNTRIES[target][0][otherPlayer] = 0

            earnVP(1, currentPlayer)

        else: # Failure
            print("The guerilla forces failed! Local resistance has driven the invaders out.")

        MILOPS[currentPlayer] += 3


    elif Card == "Arms Race":
        if MILOPS[currentPlayer] > MILOPS[otherPlayer] and MILOPS[currentPlayer] >= DEFCON:
            earnVP(3, currentPlayer)
        elif MILOPS[currentPlayer] > MILOPS[otherPlayer]:
            earnVP(1, currentPlayer)
        else:
            print("%s are not impressed by your military." % (FACTION[otherPlayer]) )


    elif Card == "Cuban Missile Crisis":
        DEFCON = 2
        SITUATIONS["Cuban Missile Crisis"][0] = True
        SITUATIONS["Cuban Missile Crisis"][1] = FACTION[currentPlayer] # The Situation works in favor of current player
        print("Tensions are forming around Cuba. Minutes to midnight...")


    elif Card == "SALT Negotiations":
        changeDEFCON(2)
        SITUATIONS["SALT Negotiations"][0] == True
        for index, card in enumerate(DISCARD_PILE):
            print(" #d - %s" % (index+1, card) )
        reclaimCard = input("\nEnter card # from discards to put in your hand:\n")
        
 

    # Doublecheck influence situation with all countries
    checkControl(COUNTRIES, "All")
    if CARDS[Card][-1] == True and cardConditionTriggered == True:
        return True # Remove starred card whose condition was met.
    else:
        return False # Discard non-starred card, or starred card whose condition wasn't met.
    

# Realign Action.
# -- Number of rerolls dependent on operations.
# -- cardName is self explanatory.
def realignmentAction(operations, cardName):
    countriesRealigned = [] # Track countries for China Card bonus
    ChinaInfluence = False

    while operations > 0: # You roll as many times as the operation strength
        target = input("Choose target country to realign: \n")

        doubleCheck = 1
        while doubleCheck > 0:
            
            if target not in COUNTRIES.keys():
                print("ERROR. COUNTRY NOT FOUND. TRY AGAIN: \n")
                target = input("Choose target country to realign: \n")
                doubleCheck += 1

            if    ( (DEFCON < 5 and "Europe" in COUNTRIES[target][3]) or
                    (DEFCON < 4 and "Asia" in COUNTRIES[target][3]) or
                    (DEFCON < 3 and "Middle East" in COUNTRIES[target][3]) ):
                print("DEFCON DENIED. YOU MAY NOT COUP/REALIGN IN THIS REGION. RE-TRY: \n")
                target = input("Choose target country to realign: \n")
                doubleCheck += 1

            # NATO Prevents Realignment. De Gaulle and Willy opens up France/West Germany though
            if currentPlayer == 1 and "Europe" in COUNTRIES[target][3] and SITUATIONS["NATO"][0] == True:
                if target == "France" and SITUATIONS["De Gaulle Leads France"][0] == True:
                    pass
                elif target == "West Germany" and SITUATIONS["Willy Brandt"][0] == True:
                    pass
                else:
                    print("WARNING: NATO IN EFFECT. USSR MAY NOT COUP/REALIGN IN EUROPE. RE-TRY: \n")
                    target = input("Choose target country to coup: \n")
                    doubleCheck += 1     

            if ChinaInfluence == True and "Asia" not in COUNTRIES[target][3]:
                print("ERROR. BONUS REALIGN FROM CHINA CARD MUST GO TO ASIA. TRY AGAIN: \n")
                target = input("Choose target country to realign: \n")
                doubleCheck += 1    

            doubleCheck -= 1

        USA_modifier = 0
        RUSSIA_modifier = 0
        for adjacentCountry in COUNTRIES[target][-1]: # Adjacent countries who are controlled bonus
            if COUNTRIES[adjacentCountry][3] == "U.S.A.":
                USA_modifier += 1
            elif COUNTRIES[adjacentCountry][3] == "Soviet Union":
                RUSSIA_modifier += 1

        if "U.S.A." in COUNTRIES[target][-1]: # Superpower adjacency bonus
            USA_modifier += 1
        elif "Russia" in COUNTRIES[target][-1]:
            RUSSIA_modifier += 1

        if COUNTRIES[target][0][0] > COUNTRIES[target][0][1]: # Greater influence bonus
            USA_modifier += 1
        elif COUNTRIES[target][0][1] > COUNTRIES[target][0][0]:
            RUSSIA_modifier += 1
                
        print("USA:" , USA_modifier) #
        print("RUSSIA", RUSSIA_modifier) #

        # Add confirmation to roll here.

        USA_dice = random.randint(1, 6)
        Russia_dice = random.randint(1, 6)
        difference = abs( (USA_dice + USA_modifier) - (Russia_dice + RUSSIA_modifier) )
        print("U.S.A. rolled:", USA_dice, "+" , USA_modifier,  "||| Soviets rolled:", Russia_dice , "+" , RUSSIA_modifier )
        
        if (USA_dice + USA_modifier) > (Russia_dice + RUSSIA_modifier):
            COUNTRIES[target][0][1] -= difference
            print("The Soviets lost", difference, "influence in" , target + "!")
        elif (Russia_dice + RUSSIA_modifier) > (USA_dice + USA_modifier):
            COUNTRIES[target][0][0] -= difference
            print("The Americans lost", difference, "influence in" , target + "!")
        else:
            print("No one has lost any influence.")

        checkControl(COUNTRIES, target) # Update control if need be
        print(target + ": " + str(COUNTRIES[target][0]) )

        operations -= 1    

        countriesRealigned.append( COUNTRIES[target][3][0] )

        if operations == 0 and cardName == "The China Card":
            asianCountries = countriesRealigned.count("Asia")
            if asianCountries == len(countriesRealigned):
                operations += 1
                print("+1 Realign roll in Asia from China Card")
                ChinaInfluence = True
                countriesRealigned.append("CHINA") # Important. This stops China Card giving infinite bonus ops 


def spaceAction(operations, whatCondition):
    global VICTORYPOINTS
    # The checking if your card is strong enough for space happens before this function executes. 
    if SPACE[currentPlayer][-1] == True: # DEBUG - this is the 1 space per turn rule. This should be in the main action code, not here.
        
        # discard card function goes here
        currentMission = SPACE[currentPlayer][1]
        missionDifficulty = SPACE["Space Track"][currentMission][2]
        pointsDue = 0
        if whatCondition == "": # Roll dice if the card is nothing special
            dice = random.randint(1, 6)
            print("\nDice result:" , str(dice) )

        if whatCondition == "Captured Nazi Scientists" or dice <= missionDifficulty: # Success
            SPACE[currentPlayer][1] += 1
            if SPACE[currentPlayer][1] > SPACE[otherPlayer][1]: # If you were first, earn VP and claim abilities with your name
                
                if currentPlayer == 0:
                    pointsDue += SPACE["Space Track"][currentMission][3][0]
                    SPACE["Space Track"][currentMission][-1] = "U.S.A."
                elif currentPlayer == 1:
                    pointsDue -= SPACE["Space Track"][currentMission][3][0]
                    SPACE["Space Track"][currentMission][-1] = "Soviet Union"

            else: # If you were second, earn less VP and neutralize abilities
                
                if currentPlayer == 0: 
                    pointsDue += SPACE["Space Track"][currentMission][3][1]
                    SPACE["Space Track"][currentMission][-1] = "None"
                elif currentPlayer == 1:
                    pointsDue -= SPACE["Space Track"][currentMission][3][1]
                    SPACE["Space Track"][currentMission][-1] = "None"

            print("\n\n Space launch successful!" , SPACE[currentPlayer][0] , "has reached" , SPACE["Space Track"][currentMission][0] + "!")
            if pointsDue > 0:
                print("The Americans earned +" + str(pointsDue) , "VP from" , SPACE["Space Track"][currentMission][0] + ".")
                earnVP(pointsDue, 0)
            elif pointsDue < 0:
                print("The Soviets earned +" + str(abs(pointsDue)) , "VP from" , SPACE["Space Track"][currentMission][0] + ".")
                earnVP(pointsDue, 1)

        else: # Failure
            
            print("\n\n Failure..." , SPACE[currentPlayer][0] , "could not reach" , SPACE["Space Track"][currentMission][0] + ".")


# During a players turn, it'll pend for what youd like to do
# -- ActionsPermitted - List of actions available. By default, the list [R, S, E, I, C] is put in. Remove as appropriate.
# -- card - Card information
# -- cardName - Just the name of the card
# -- cardOps - Ops from the card
# -- recursionDiscard - Boolean value that determines if the card should be discarded 2x. True = Do not discard, False = do discard
# -- triggerEvent - Cards like UN Intervention will prevent the enemy event from triggering.
def conductOperations(ActionsPermitted, card, cardName, cardOps, recursionDiscard, triggerEvent):
    removeCard = False # Variable initialized. This doesn't affect anything yet.

    
    # Card Operations modified by Purging or Containment/Breznev
    if SITUATIONS["Containment"][0] == True and currentPlayer == 0:
        cardOps += 1
    elif SITUATIONS["Breznev Doctrine"][0] == True and currentPlayer == 1:
        cardOps += 1
    if SITUATIONS["Red Scare/Purge"][0] == True and FACTION[otherPlayer] == SITUATIONS["Red Scare/Purge"][1]: 
        cardOps -= 1
    if cardOps > 4: # Max 4 Ops, Min 1 ops
        cardOps = 4
    elif cardOps < 1 and cardName[-7:] != "Scoring":
        cardOps = 1

    
    enemyEvent = False      # If you have selected an enemy card, its event will trigger after you do your action
    if card[2] == FACTION[otherPlayer] and triggerEvent == True:
        enemyEvent = True
    enemyEventTriggered = False
    

    print("## Card: %s | Ops: %d | %s ##" % (cardName, cardOps, card[2]) )
    repeats = 1
    while repeats > 0:

        if cardName[-7:] == "Scoring":
            ActionsPermitted.remove("R")
            ActionsPermitted.remove("S")
            ActionsPermitted.remove("I")
            ActionsPermitted.remove("C")

        if cardName == "The China Card":
            ActionsPermitted.remove("E")

        if (SPACE[currentPlayer][-1] == False or # You already spaced a card earlier in the turn
            cardOps < SPACE["Space Track"][ SPACE[currentPlayer][1] ][1] or # cardOps < Next Space location Ops Requirement
            enemyEventTriggered == True): # You already triggered the enemy event - why space?
                                          # Animal in Space has been used up (MISSING)
            if "S" in ActionsPermitted:
                ActionsPermitted.remove("S")


        if currentPlayer == 0:
            print("\n *.* AVAILABLE ACTIONS *.*")
        elif currentPlayer == 1:
            print("\n /-| AVAILABLE ACTIONS |-\\")
        if "R" in ActionsPermitted:
            print("[R]ealignment", end=", ")
        if "S" in ActionsPermitted:
            print("[S]pace", end=", ")
        if "E" in ActionsPermitted and enemyEvent == True: # Warning that enemy event would trigger
            print("![E]vent!", end=", ")
        elif "E" in ActionsPermitted:
            print("[E]vent", end=", ")
        if "I" in ActionsPermitted:
            print("[I]nfluence", end=", ")
        if "C" in ActionsPermitted:
            print("[C]oup")

        chooseAction = input("\nSelect an action to take: ")
        chooseAction = chooseAction.upper()
        while chooseAction not in ActionsPermitted:
            chooseAction = input("ERROR. Invalid input. Only enter the first character of the action.\nSelect an action to take: ")
            chooseAction = chooseAction.upper()

    # Bug -- As USA, triggering event and then using it for ops will instantly suffer -3 VP. Check must be done on NEXT turn 
        # We Will Bury You will occur before ANY action, unless it's an event. In such a case, check later if it's UN event
        if currentPlayer == 0 and SITUATIONS["'We Will Bury You'"][0] == True and chooseAction != "E": 
            earnVP(3, 1)

        # Flower Power gives 2 VP automatically to Soviets, unless spaced
        if currentPlayer == 0 and SITUATIONS["Flower Power"][0] == True and chooseAction != "S" and cardName[-3:] == "War": 
            earnVP(2, 1)
            print("Protests are occuring over the US's involvement in the %s.\n" % cardName)
            
        if chooseAction == "R":
            realignmentAction( cardOps, cardName )
        elif chooseAction == "S":
            spaceAction( cardOps, "" )
            SPACE[currentPlayer][-1] = False
            enemyEvent = False
        elif chooseAction == "E":
        # Defuse We Will Bury You w/ UN, or suffer -3 VP
            if SITUATIONS["'We Will Bury You'"][0] == True and currentPlayer == 0 and cardName == "UN Intervention":
                SITUATIONS["'We Will Bury You'"][0] = False
            elif SITUATIONS["'We Will Bury You'"][0] == True and currentPlayer == 0:
                earnVP(3, 1)

            removeCard = cardCode( cardName )
            if enemyEvent == True:
                enemyEvent = False
                enemyEventTriggered = True
                ActionsPermitted.remove("E")
                repeats += 1
        elif chooseAction == "I":
            legalCountries = acknowledgeAdjacency( currentPlayer ) # ! Will break rules for leapfrogging. Adjacency only checked start of turn.
            influenceAction( cardOps, legalCountries, cardName )
        elif chooseAction == "C":
            coupAction( cardOps, "Normal", cardName, False )

        if enemyEvent == True:
            removeCard = cardCode( cardName )
            enemyEvent = False
            
        repeats -= 1

    # Discard card played
    discardCard(cardName, recursionDiscard, removeCard)


def influenceAction(operations, legalCountries, cardName):
    countriesInfluenced = [] # List's only purpose is to track country's region for China Card
    ChinaInfluence = False

    while operations > 0: # You place total influence equal to operations

        target = input("Choose target country to add influence in: \n")

        while target not in COUNTRIES.keys(): # Input validation
            target = input("ERROR. COUNTRY NOT FOUND. TRY AGAIN: \n")

        while ChinaInfluence == True and "Asia" not in COUNTRIES[target][3]: # 5th influence from China Card must go to Asia
            target = input("ERROR. BONUS INFLUENCE FROM CHINA CARD CAN ONLY BE PLACED IN ASIA: \n")        

        possible = False
        while possible == False:
            enemyCountry = False
            
            if target in legalCountries: # Check if target already has your influence or was adjacent to a country that does.
                possible = True

            if possible == True:                # Must pay at least 2 operations to add influence in enemy controlled country. 
                if COUNTRIES[target][3] == FACTION[otherPlayer]: 
                    enemyCountry = True
                    if operations < 2:
                        possible = False        # If you can't afford, try another country.

            
            if possible == False and enemyCountry == True:
                target = input("YOU DO NOT HAVE SUFFICIENT OPERATIONS TO ADD INFLUENCE IN ENEMY CONTROLLED COUNTRY. CHOOSE ANOTHER COUNTRY: \n")
            elif possible == False:
                target = input("COUNTRY NEITHER HAS INFLUENCE NOR ADJACENCY AT START OF ACTION ROUND. CHOOSE ANOTHER COUNTRY: \n")
                
        # Add additional rules for not leap frogging. Maybe remember targets?

        if enemyCountry == True:
            operations -= 2
        else:
            operations -= 1
        COUNTRIES[target][0][currentPlayer] += 1
        print("Influence added to" , target + ". Now at" , str(COUNTRIES[target][0]) )
        checkControl(COUNTRIES, target)
        countriesInfluenced.append( COUNTRIES[target][3][0] )

        if operations == 0 and cardName == "The China Card":
            asianCountries = countriesInfluenced.count("Asia")
            if asianCountries == len(countriesInfluenced):
                operations += 1
                print("+1 Influence in Asia from China Card")
                ChinaInfluence = True
                countriesInfluenced.append("CHINA") # Important. This stops China Card giving infinite bonus ops
                print(countriesInfluenced)
        
# Attempt a coup. 
# -- Coup strength is given through operations. 
# -- 'coupType' - Most coups are "Normal", but cards like Junta provide "Free" coups.
# -- eventCoup - Events that need the code of a coup, but with restrictions (I.E. 'Che'). False boolean normally, true boolean if special
def coupAction(operations, coupType, cardName, eventCoup):
    global DEFCON

    target = input("Choose target country to coup: \n")
    doubleCheck = 1
    while doubleCheck > 0: # Extra strong validation - check spelling, check if enemy exists at target, check if DEFCON restricted
            
        if target not in COUNTRIES.keys():
            print("ERROR. COUNTRY NOT FOUND. TRY AGAIN: \n")
            target = input("Choose target country to coup: \n")
            doubleCheck += 1

        if COUNTRIES[target][0][otherPlayer] == 0:
            print("ENEMY PRESENCE NOT FOUND IN COUNTRY. TRY AGAIN: \n")
            target = input("Choose target country to coup: \n")
            doubleCheck += 1

        if    ( (DEFCON < 5 and "Europe" in COUNTRIES[target][3]) or
                (DEFCON < 4 and "Asia" in COUNTRIES[target][3]) or
                (DEFCON < 3 and "Middle East" in COUNTRIES[target][3]) ) and coupType != "Free":
            print("DEFCON RESTRICTED. YOU MAY NOT COUP/REALIGN IN THIS REGION. RE-TRY: \n")
            target = input("Choose target country to coup: \n")
            doubleCheck += 1

        # NATO prevents couping in Europe. De Gaulle and Willy Brandt are exceptions, if they are active.
        if currentPlayer == 1 and "Europe" in COUNTRIES[target][3] and SITUATIONS["NATO"][0] == True:
            if target == "France" and SITUATIONS["De Gaulle Leads France"][0] == True:
                pass
            elif target == "West Germany" and SITUATIONS["Willy Brandt"][0] == True:
                pass
            else:
                print("WARNING: NATO IN EFFECT. USSR MAY NOT COUP/REALIGN IN EUROPE. RE-TRY: \n")
                target = input("Choose target country to coup: \n")
                doubleCheck += 1            

        # Che's coups are just like normal ones - but with additional restrictions and a parameter
        if cardName == "Che" and eventCoup == True and (COUNTRIES[target][2] == True or 
            "Europe" in COUNTRIES[target][3] or "Asia" in COUNTRIES[target][3] or "Middle East" in COUNTRIES[target][3]):
            print("ERROR. Che cannot lead a revolution in %s. Re-try:" % target)
            target = input("Choose target country to coup: \n")
            doubleCheck += 1

        doubleCheck -= 1

    # CUBAN MISSILE CRISIS = Game Over, victory to opponent
    if SITUATIONS["Cuban Missile Crisis"][0] == True and SITUATIONS["Cuban Missile Crisis"][1] == FACTION[otherPlayer]:
        victoryCheck("Cuban Missile Crisis", FACTION[otherPlayer])

    ChinaCardBonus = 0 
    if cardName == "The China Card":
        if "Asia" in COUNTRIES[target][3]:
            ChinaCardBonus = 1

    dice = random.randint(1, 6)
    power = operations + dice + ChinaCardBonus - ( COUNTRIES[target][1] * 2 ) # Coup strength
    
    oldState = COUNTRIES[target][0]
    print(FACTION[currentPlayer] , "has rolled a" , dice , "on a coup." ,
          "\nPREVIOUSLY  -\t", target, oldState)

    if power > 0:
        for x in range(power):      # Remove enemy influence until number is met. If no enemy influence, add your own influence 
            if COUNTRIES[target][0][otherPlayer] > 0:
                COUNTRIES[target][0][otherPlayer] -= 1
            elif COUNTRIES[target][0][otherPlayer] == 0:
                COUNTRIES[target][0][currentPlayer] += 1

        newState = COUNTRIES[target][0]
        print("\tNOW -\t", target, newState )

    else:
        print("Coup has failed...")

# Degrade DEFCON if target is a Battleground. 
    if COUNTRIES[target][2] == True:
        if currentPlayer == 0 and SITUATIONS["Nuclear Subs"][0] == True: # Nuclear subs prevents dropping DEFCON
            pass
        else:
            print("DEFCON reduced to", str(DEFCON-1) +"!\n")
            changeDEFCON(-1)

    if coupType != "Free":
        MILOPS[currentPlayer] += operations # Earn Milops if it wasn't a free coup
    checkControl(COUNTRIES, target)

    # 'Che' code. If coup success, return boolean to repeat coup
    if cardName == "Che" and eventCoup == True and power > 0:
        print("Che's charisma has inspired the workers of the world!")
        return True
    elif cardName == "Che" and eventCoup == True and power <= 0:
        print("Che's warcrimes have surfaced. People of the world are hesitant to follow his ideology.")
        return False
    

######## AUXILIARY FUNCTIONS #########
# Arguments:
#   - COUNTRIES - The COUNTRIES dictionary is always included.
#   - Range - A value/string that tells the function to check all countries, some, a continent, or just a singular one.
def checkControl(COUNTRIES, Range):
    if Range == "All": # Check all countries for control
            
        for name in COUNTRIES:
            if ( COUNTRIES[name][0][0] - COUNTRIES[name][0][1] ) >= COUNTRIES[name][1]:   # U.S.A. control
                COUNTRIES[name][4] = "U.S.A." 
                name = "*.* " + name + " *.*" # OPTIONAL - Give a little art to show control
            elif ( COUNTRIES[name][0][1] - COUNTRIES[name][0][0] ) >= COUNTRIES[name][1]: # Soviet control
                COUNTRIES[name][4] = "Soviet Union" 
                name = "|-/ " + name + " \-|"
            else:
                COUNTRIES[name][4] = "None" # No one controls the country

        for influence in range(2): # Impossible to have negative influence. Reset to 0.
            if COUNTRIES[name][0][influence] < 0: 
                COUNTRIES[name][0][influence] = 0


    elif Range in COUNTRIES: # Function used for checking one country. Near identical code to "All" check

        if ( COUNTRIES[Range][0][0] - COUNTRIES[Range][0][1] ) >= COUNTRIES[Range][1]:  
            COUNTRIES[Range][4] = "U.S.A." 
            #print("The Americans control" , Range) 
        elif ( COUNTRIES[Range][0][1] - COUNTRIES[Range][0][0] ) >= COUNTRIES[Range][1]:
            COUNTRIES[Range][4] = "Soviet Union" 
            #print("The Soviets control" , Range)
        else:
            COUNTRIES[Range][4] = "None" 

        for influence in range(2): 
            if COUNTRIES[Range][0][influence] < 0: 
                COUNTRIES[Range][0][influence] = 0

        print(Range + ":", COUNTRIES[Range][0], "-", COUNTRIES[Range][4], "controlled")
            
    
        # Possible to return this temporary name for future functions or prints

def swapSides(whoseTurn):
    global currentPlayer, otherPlayer
    # IMPORTANT! You MUST call the swapSides function twice in a card's code.
    #  If you don't, the player you swap to will have their turn instead of the phasing player.
    #  Call the swapsides to a player, and then revert back by calling swapSides(FACTION[phasingPlayer])
    
    if whoseTurn == "Swap":
        if currentPlayer == 0: 
            currentPlayer = 1
            otherPlayer = 0
        elif currentPlayer == 1:
            currentPlayer = 0
            otherPlayer = 1

    elif whoseTurn == "U.S.A.":
        currentPlayer = 0
        otherPlayer = 1

    elif whoseTurn == "Soviet Union":
        currentPlayer = 1
        otherPlayer = 0    

def drawCards(origin, number_drawn, destination):
    numb_drawn = 0
    while numb_drawn < number_drawn:
        if origin == DRAW_PILE and len(DRAW_PILE) == 0:
            random.shuffle(DISCARD_PILE)
            for discardCards in DISCARD_PILE:
                DRAW_PILE.append( DISCARD_PILE.pop(0) )
            print("\n **** Discards have been reshuffled! **** \n")
            
        else:
            destination.append( origin[0] )
            del origin[0]
            numb_drawn += 1


# cardName - name of the card; recursionDiscard - Boolean, explained in a comment; isCardRemoved - Boolean returned from cardCode
def discardCard(cardName, recursionDiscard, isCardRemoved):
    card = CARDS[cardName]
    if recursionDiscard == False:   # If a card code has a seperate conductOperations function, do not "double" discard
        if isCardRemoved == True and card[-1] == True: # Remove Card if event was starred
            REMOVED_PILE.append(cardName)
            HANDS[currentPlayer].remove(cardName)
        elif cardName == "The China Card":
            CARDS[cardName][3] = FACTION[otherPlayer]
            CARDS[cardName][4] = False
        else:
            DISCARD_PILE.append(cardName) # Otherwise, discard card
            HANDS[currentPlayer].remove(cardName)


## This function will find the shortest connection of countries to a destination (I.E. Thailand to India) and return a list of them.
def findShortestDistance(origin, target):
    truePath = []
    possiblePaths = []

    for X in range(100):
        testingPath = [origin]
        possibleLineage = True
        while possibleLineage:

            if testingPath[-1] == "U.S.A." or testingPath[-1] == "Soviet Union": # Never go through Superpowers
                break

            adjacentCountries = COUNTRIES[testingPath[-1]][-1] # Do not backtrack.
            for entity in reversed(adjacentCountries):
                if entity in testingPath:
                    adjacentCountries.remove(entity)
            
            if target in adjacentCountries: # Immediately leap for the target country, don't randomize it.
                testingPath.append( target )

            else:
                if len(adjacentCountries) > 0: # Randomly choose an adj. country not yet traversed. Dead end if not possible.
                    randomAdjCountry = random.choice( adjacentCountries )
                    if randomAdjCountry not in testingPath:
                        testingPath.append( randomAdjCountry ) 
                else:
                    break

            if target in testingPath:
                possiblePaths.append(testingPath)
                break
                

    if len(possiblePaths) > 0:
        shortestPaths = []
        for ITEM in possiblePaths:
            shortestPaths.append( len(ITEM) )
            
        min_value = min(shortestPaths)  
        choosePath = [i for i, x in enumerate(shortestPaths) if x == min_value] # Returns indexes of smallest possible paths

        truePath = possiblePaths[ random.choice(choosePath) ]
        return truePath
    else:
        return "None"
        

def acknowledgeAdjacency(currentPlayer):
    legalCountries = []
    
    for country in COUNTRIES:
        if COUNTRIES[country][0][currentPlayer] > 0: # Countries that have your influence
            if country not in legalCountries:
                legalCountries.append( country )

            for adjacentCountry in COUNTRIES[country][-1]: # Countries adjacent to other countries that have your influence
                if adjacentCountry not in legalCountries:
                    legalCountries.append( adjacentCountry )

        elif FACTION[currentPlayer] in COUNTRIES[country][-1]: # Superpower is always adjacent
            if country not in legalCountries:
                legalCountries.append( country )

    return legalCountries

def changeDEFCON(amount):
    global DEFCON
    
    DEFCON += amount
    if DEFCON > 5: # Maximum
        DEFCON = 5
    elif DEFCON < 1: # Minimum
        DEFCON = 1

    if amount > 0:
        print("DEFCON IMPROVED BY %d, NOW AT %d" % (amount, DEFCON))
    elif amount < 0:
        print("DEFCON REDUCED BY %d, NOW AT %d" % (amount, DEFCON))

    if DEFCON == 1:
        victoryCheck("DEFCON", "None")

    if DEFCON == 2 and SITUATIONS["NORAD"][0] == True and COUNTRIES["Canada"][-2] == "U.S.A.":
        print("*.* NORAD ALERT *.*")
        swapSides("U.S.A.")
        target = input("U.S.A., add 1 influence to a country with U.S. influence:\n")
        while target.isdigit() == True or target not in COUNTRIES.keys() or COUNTRIES[target][0][0] == 0:
            target = input("Invalid input and/or country. Try again:\n")

        COUNTRIES[target][0][0] += 1
        swapSides(FACTION[phasingPlayer])
        

def scoreRegion(Region):
    # Score +1 VP per battleground, +1 for adjacency
    # Then add points from presence, each region is different
    # score VP
    VPSowed = [0, 0]
    countriesControlled = [0, 0]
    BGcount = [0, 0]
    nonBGcontrolled = [False, False]
    powerStatus = ["None", "None"]
    BGinRegion = {
        "Europe":5 , "Middle East":6 , "Asia":6, "Africa":5 , "Central America":3 , "South America":4
        }
    
    if Region != "Southeast Asia": # EXCEPTION - Southeast Asia scored differently from others
        for player in range(0, 2):
            for countryName in COUNTRIES:
                country = COUNTRIES[countryName]
                
                if Region not in country[3]:
                    pass
                else:

                    if country[4] == FACTION[player]:
                        countriesControlled[player] += 1
                        if (countryName == "Taiwan" and player == 0 # Taiwan counts as BG only for US
                            and SITUATIONS["Formosan Resolution"][0] == True):
                            VPSowed[player] += 1
                            BGcount[player] += 1
                        elif country[2] == True: # Country is BG
                            VPSowed[player] += 1
                            BGcount[player] += 1
                        elif country[2] == False: # Country is NON-BG
                            nonBGcontrolled[player] = True

            # +1 VP per Adj. country on enemy border
                    if player == 0:
                        if (country[4] == FACTION[player]) and (FACTION[1] in country[-1]):
                            VPSowed[player] += 1
                    elif player == 1:                    
                        if (Region in country[3]) and (country[4] == FACTION[player]) and (FACTION[0] in country[-1]):
                            VPSowed[player] += 1

        # Determine presence status
        for player in range(0, 2):
            if player == 0:
                opponent = 1
            elif player == 1:
                opponent = 0

        # Shuttle Diplomacy kicks in against the Soviets before checking presence
            if player == 1 and SITUATIONS["Shuttle Diplomacy"] == True and (Region == "Asia" or Region == "Middle East"):
                SITUATIONS["Shuttle Diplomacy"] = False
                print("*.* Shuttle Diplomacy in %s! *.*" % (Region))
                if BGcount[1] > 0:
                    BGcount[1] -= 1
                    VPSowed[1] -= 1
                    countriesControlled[1] -= 1
                    if Region == "Asia" and COUNTRIES["Japan"][4] == "Soviet Union": # Japan is denied, so no +1 VP from adj.
                        VPSowed[1] -= 1

                
            if (BGcount[player] == BGinRegion[Region] and
                countriesControlled[player] > countriesControlled[opponent] ):
                powerStatus[player] = "Control"

            elif (BGcount[player] > BGcount[opponent] and
                  countriesControlled[player] > countriesControlled[opponent] and
                  nonBGcontrolled[player] == True ):
                powerStatus[player] = "Domination"

            elif countriesControlled[player] > 0:
                powerStatus[player] = "Presence"
        
    for player in range(0, 2):                    
        if Region == "Europe":
            if powerStatus[player] == "Presence":
                VPSowed[player] += 3
            elif powerStatus[player] == "Domination":
                VPSowed[player] += 7
            elif powerStatus[player] == "Control":
                victoryCheck("Europe Control", FACTION[player] )
                break
            
        elif Region == "Middle East":
            if powerStatus[player] == "Presence":
                VPSowed[player] += 3
            elif powerStatus[player] == "Domination":
                VPSowed[player] += 5
            elif powerStatus[player] == "Control":
                VPSowed[player] += 7
                
        elif Region == "Asia":
            if powerStatus[player] == "Presence":
                VPSowed[player] += 3
            elif powerStatus[player] == "Domination":
                VPSowed[player] += 7
            elif powerStatus[player] == "Control":
                VPSowed[player] += 9
                
        elif Region == "Southeast Asia":
            for player in range(0, 2):
                for countryName in COUNTRIES:
                    country = COUNTRIES[countryName]
                    
                    if Region not in country[3]:
                        pass
                    else:

                        if country[4] == FACTION[player]:
                            VPSowed[player] += 1
                            if country == "Thailand":
                                VPSowed[player] += 1

        elif Region == "Africa":
            if powerStatus[player] == "Presence":
                VPSowed[player] += 1
            elif powerStatus[player] == "Domination":
                VPSowed[player] += 4
            elif powerStatus[player] == "Control":
                VPSowed[player] += 6

        elif Region == "Central America":
            if powerStatus[player] == "Presence":
                VPSowed[player] += 1
            elif powerStatus[player] == "Domination":
                VPSowed[player] += 3
            elif powerStatus[player] == "Control":
                VPSowed[player] += 5
        
        elif Region == "South America":
            if powerStatus[player] == "Presence":
                VPSowed[player] += 2
            elif powerStatus[player] == "Domination":
                VPSowed[player] += 5
            elif powerStatus[player] == "Control":
                VPSowed[player] += 6

    print(" !== %s has been scored! ==!" % (Region) )
    VPSowed[1] = VPSowed[1] * -1 # Turn Soviet VP negative for easier calculation
    VPtoBeAwarded = VPSowed[0] + VPSowed[1]
    return VPtoBeAwarded

    
def earnVP(amount, currentPlayer):
    global VICTORYPOINTS
    VICTORYPOINTS += amount
    if currentPlayer == 0 and amount > 0:
        print("The U.S.A. earned %d points. VP is now at %d." % (amount, VICTORYPOINTS) )
    elif currentPlayer == 1 and amount > 0:
        print("The Soviet Union earned %d points. VP is now at %d." % (amount, VICTORYPOINTS) )
    elif amount == 0:
        print("Neither side has earned any points.")
        
    if VICTORYPOINTS >= 20:
        victoryCheck("Victory Points", "U.S.A.")
    elif VICTORYPOINTS <= -20:
        victoryCheck("Victory Points", "Soviet Union")


def victoryCheck(method, victor):
    
    if method == "Victory Points":
        print(" \n\n ###### THE GAME HAS ENDED DUE ACHIEVING 20 VICTORY POINTS! ######")

    elif method == "Wargames":
        pass
    
    elif method == "Final Scoring":
        pass
    
    elif method == "DEFCON":
        print(" \n\n ###### THE GAME HAS ENDED DUE TO DEFCON 1! ######")
        if phasingPlayer == 0: 
            victor = "Soviet Union"
        elif phasingPlayer == 1: 
            victor = "U.S.A."
        
    elif method == "Cuban Missile Crisis":
        print(" \n\n ###### THE GAME HAS ENDED DUE TO A COUP! THE CUBAN MISSILE CRISIS CAUSES NUCLEAR ANNIHILATION! ######")
    
    elif method == "Europe Control":
        print(" \n\n ###### THE GAME HAS ENDED DUE TO EUROPE CONTROL! ######")

    if victor == "U.S.A.": # American Victory
        print("Against all odds, the United States tiumphs over the socialist forces of the Soviet Union!")
    elif victor == "Soviet Union": # Soviet Victory
        print("The Soviet Union has successfully defeated the capitalist ideology of the United States!")


        
##### MASTER DATABASE OF PATHS ######
## BUG -- Fails too often at finding paths. Doesn't know how to reach adjacent country? Pakistan-Iran, Nigeria-Algeria?
##pathFinderDatabase = {}
##
##for countryX in COUNTRIES:
##    for countryY in COUNTRIES:
##        if countryX == countryY:
##            pass
##        else:
##
##            path = findShortestDistance(countryX, countryY)
##            name = countryX + "/" + countryY
##            pathFinderDatabase[name] = path
##            
##
##with open("TSpathFinder.txt", 'w') as f: 
##    for key, value in pathFinderDatabase.items(): 
##        f.write('%s:%s\n' % (key, value))
##
##f2 = open("TSpathFinder.txt", "r")
##print(f2.read())



######### GAMEPLAY ########
HANDS = {
        0: [],
        1: []
    }

DRAW_PILE = [] 
DISCARD_PILE = []
REMOVED_PILE = []
for index, card in enumerate(CARDS): # Add cards 1-37 (which are Early War cards)
    if index >= 0 and index <= 38:
        DRAW_PILE.append(card)


DRAW_PILE.remove("The China Card") # The China Card does not belong in Draw Pile
random.shuffle(DRAW_PILE)
checkControl(COUNTRIES, "All")
maximumActions, handSize = 6, 8

# in range(1, 11) is how it's supposed to be
for Turn in range(4, 11):
    
    if Turn == 4:
        warStage = "Mid War"
        maximumActions, handSize = 7, 9      # Players now take 7 actions, and draw +1
        for index, card in enumerate(CARDS): # Add cards 38-88 (mid-war cards)
            if index >= 39 and index <= 86:
                DRAW_PILE.append(card)
        random.shuffle(DRAW_PILE)

    elif Turn == 8:
        warStage = "Late War"
        for index, card in enumerate(CARDS): # Shuffle cards 88-109 (Late-war cards) 
            if index >= 87 and index <= 109:
                DRAW_PILE.append(card)
        random.shuffle(DRAW_PILE)

    while len(HANDS[0]) < handSize: # Americans draw cards
        drawCards( DRAW_PILE, 1, HANDS[0] )
        
    while len(HANDS[1]) < handSize: # Soviets draw Cards
        drawCards( DRAW_PILE, 1, HANDS[1] )
        

    SPACE[0][-1] = True # Space Action reset to True
    SPACE[1][-1] = True
    # Double Space action reset?
        
    # Headline Phase
        
    for ActionRound in range(1, (maximumActions + 1)*2 ):
        ActionRound = math.ceil(ActionRound / 2)
        phasingPlayer = currentPlayer
        legalSpaces = acknowledgeAdjacency(currentPlayer)

        print("\n============== TURN: "+str(Turn)+" ==================")
        print("======= ACTION "+str(ActionRound)+" | "+FACTION[currentPlayer]+" =======\n")

        for count, card in enumerate(HANDS[currentPlayer]):
            if CARDS[card][2] == "U.S.A.":
                print("#%d -- %d *.* %s" % (count+1, CARDS[card][1], card))
            elif CARDS[card][2] == "Soviet Union":
                print("#%d -- %d |-/ %s" % (count+1, CARDS[card][1], card))
            elif CARDS[card][2] == "Neutral":
                print("#%d -- %d === %s" % (count+1, CARDS[card][1], card))

        if CARDS["The China Card"][3] == FACTION[currentPlayer]: # China Card is not part of your hand, but has all the privileges of being so.
            if CARDS["The China Card"][4] == True:
                print("#China -- 4 === The China Card")
            elif CARDS["The China Card"][4] == False:
                print("#China -- 4 === The China Card (FACE DOWN)")

        # QUAGMIRE OR BEAR TRAP turn
        if ((SITUATIONS["Quagmire"][0] == True and currentPlayer == 0) or 
            SITUATIONS["Bear Trap"][0] == True and currentPlayer == 1):
            print("\nATTENTION. You must discard a card with an ops strength of 2 or higher.")
            cardNum = input(" - Choose card # to discard from hand:\n")
        # Op modifiers make getting out of trap easier or harder
            cardOps = CARDS[HANDS[currentPlayer][int(cardNum)-1]][1]
            if ((currentPlayer == 0 and SITUATIONS["Containment"][0] == True and cardOps < 4) or
                (currentPlayer == 1 and SITUATIONS["Breznev Doctrine"][0] == True and cardOps < 4)):
                cardOps += 1
            if SITUATIONS["Red Scare/Purge"][0] == True and FACTION[otherPlayer] == SITUATIONS["Red Scare/Purge"][1] and cardOps > 1: 
                cardOps -= 1


            while cardNum == "China" or (cardNum.isdigit() == False or int(cardNum) < 1 or int(cardNum) > len(HANDS[currentPlayer])
                    or cardOps < 2):
                print("ERROR. Invalid input. That is not a valid card to be discarded.")
                cardNum = input(" - Choose card # to discard from hand:\n")
                cardOps = CARDS[HANDS[currentPlayer][int(cardNum)-1]][1]
                if ((currentPlayer == 0 and SITUATIONS["Containment"][0] == True and cardOps < 4) or
                    (currentPlayer == 1 and SITUATIONS["Breznev Doctrine"][0] == True and cardOps < 4)):
                    cardOps += 1
                if SITUATIONS["Red Scare/Purge"][0] == True and FACTION[otherPlayer] == SITUATIONS["Red Scare/Purge"][1] and cardOps > 1: 
                    cardOps -= 1

            cardName = HANDS[currentPlayer][int(cardNum)-1]
            card = CARDS[cardName]
            discardCard(cardName, False, False)
            
            escape = random.randint(1, 6)
            print("ROLLED: %d" % (escape) )
            if escape > 4:
                escape = False
            else:
                escape = True

            if currentPlayer == 0:
                if escape == True:
                    print("SUCCESS. The quagmire of the Vietnam war is no more.")
                    SITUATIONS["Quagmire"][0] = False
                else:
                    print("FAILURE. Fear of communist takeover delays a withdrawal.")
            elif currentPlayer == 1:
                if escape == True:
                    print("SUCCESS. Mujahideen forces have been subdued.")
                    SITUATIONS["Bear Trap"][0] = False
                else:
                    print("FAILURE. Islam proves to be a tough nut to crack.")                

        # Normal turn - select card to do one of 5 actions
        else:
            # Cuban Missile Crisis prompt - give player a chance to remove it
            if SITUATIONS["Cuban Missile Crisis"][0] == True and SITUATIONS["Cuban Missile Crisis"][1] == FACTION[otherPlayer]:
                if currentPlayer == 0:
                    print("\n !- WARNING - Cuban Missile Crisis. Enter [CMC] to remove 2 influence from West Germany or Turkey and end the Crisis.\n")
                elif currentPlayer == 1:
                    print("\n !- WARNING - Cuban Missile Crisis. Enter [CMC] to remove 2 influence from Cuba and end the Crisis.\n")

            cardNum = input("\n - Choose card # to play from hand:\n") # Input validation for using card below. 
            if CARDS["The China Card"][4] == False and cardNum == "China": # China Card may not be used if facedown.
                while (cardNum == "China"
                        or (cardNum == "CMC" and SITUATIONS["Cuban Missile Crisis"][0] == False or 
                            (currentPlayer == 0 and COUNTRIES["Turkey"][0][0] < 2 and COUNTRIES["West Germany"][0][0] < 2) or
                            (currentPlayer == 1 and COUNTRIES["Cuba"][0][1] < 2) )
                        and (cardNum.isdigit() == False or int(cardNum) < 1 or int(cardNum) > len(HANDS[currentPlayer]))):
                    print("ERROR. Invalid input. Enter only the card's ordering number in your hand.")
                    cardNum = input("\n - Choose card # to play from hand:\n")
            else:
                while ( cardNum != "China" and (cardNum != "CMC" or SITUATIONS["Cuban Missile Crisis"][0] == False or 
                            (currentPlayer == 0 and COUNTRIES["Turkey"][0][0] < 2 and COUNTRIES["West Germany"][0][0] < 2) or
                            (currentPlayer == 1 and COUNTRIES["Cuba"][0][1] < 2) ) 
                        and (cardNum.isdigit() == False or int(cardNum) < 1 or int(cardNum) > len(HANDS[currentPlayer])) ):
                    print("ERROR. Invalid input. Enter only the card's ordering number in your hand.")
                    cardNum = input("\n - Choose card # to play from hand:\n")            

            if cardNum == "China":
                cardName = "The China Card"
            elif cardNum == "CMC":
                if currentPlayer == 0:
                    CMCinfluence = input("Enter [T] or [WG] to defuse the Cuban Missile Crisis:\n")
                    CMCinfluence = CMCinfluence.upper()
                    while ( (CMCinfluence != "T" or COUNTRIES["Turkey"][0][0] < 2) and 
                        (CMCinfluence != "WG" or COUNTRIES["West Germany"][0][0] < 2) ):
                        CMCinfluence = input("ERROR. Invalid input, or country does not have minimum 2 influence to lose. Try-again:\n")
                        CMCinfluence = CMCinfluence.upper()

                    if CMCinfluence == "T":
                        COUNTRIES["Turkey"][0][0] -= 2
                    elif CMCinfluence == "WG":
                        COUNTRIES["West Germany"][0][0] -= 2

                elif currentPlayer == 1:
                    COUNTRIES["Cuba"][0][1] -= 2

                SITUATIONS["Cuban Missile Crisis"][0] = False
                SITUATIONS["Cuban Missile Crisis"][1] = "None"
                print("The %s has defused the Cuban Missile Crisis!" % (FACTION[currentPlayer]) )

        # Removing Cuban Missile Crisis influence was a free action. Now, the user picks an actual card to play.
                cardNum = input("\n - Choose card # to play from hand:\n") # Input validation for using card below. 
                if CARDS["The China Card"][4] == False and cardNum == "China": # China Card may not be used if facedown.
                    while (cardNum == "China"
                            or (cardNum == "CMC" and SITUATIONS["Cuban Missile Crisis"][0] == False or 
                                (currentPlayer == 0 and COUNTRIES["Turkey"][0][0] < 2 and COUNTRIES["West Germany"][0][0] < 2) or
                                (currentPlayer == 1 and COUNTRIES["Cuba"][0][1] < 2) )
                            and (cardNum.isdigit() == False or int(cardNum) < 1 or int(cardNum) > len(HANDS[currentPlayer]))):
                        print("ERROR. Invalid input. Enter only the card's ordering number in your hand.")
                        cardNum = input("\n - Choose card # to play from hand:\n")
                else:
                    while ( cardNum != "China" and (cardNum != "CMC" or SITUATIONS["Cuban Missile Crisis"][0] == False or 
                                (currentPlayer == 0 and COUNTRIES["Turkey"][0][0] < 2 and COUNTRIES["West Germany"][0][0] < 2) or
                                (currentPlayer == 1 and COUNTRIES["Cuba"][0][1] < 2) ) 
                            and (cardNum.isdigit() == False or int(cardNum) < 1 or int(cardNum) > len(HANDS[currentPlayer])) ):
                        print("ERROR. Invalid input. Enter only the card's ordering number in your hand.")
                        cardNum = input("\n - Choose card # to play from hand:\n")  

                cardName = HANDS[currentPlayer][int(cardNum)-1] # Post-Cuban Crisis cardName

            else:
                cardName = HANDS[currentPlayer][int(cardNum)-1] # Normal cardName assignment
            card = CARDS[cardName] # In all cases, get info for card

            conductOperations(["R","S","E","I","C"], card, cardName, card[1], False, True)
        swapSides("Swap") # Switch player order over at end of action round

    CARDS["The China Card"][4] = True # Flip China Card

    for situation in SITUATIONS:    # Temporary situations that last for the turn are now removed
        if SITUATIONS[situation][2] == "Temporary" and SITUATIONS[situation][0] == True:
            SITUATIONS[situation][0] = False
            if situation == "Red Scare/Purge" or situation == "Cuban Missile Crisis":
                SITUATIONS[situation][1] = "None"

    changeDEFCON(1)

