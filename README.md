# TONGUE-TWISTER

A tongue-twister is a phrase that is designed to be difficult to articulate properly, and can be used as a type of spoken word game. Additionally, they can be used as exercises to improve pronunciation and fluency, according to Wikipedia.

The Tongue Twister web application measure how much you can speak phrases and Google speech can understand. However, it is just for fun and cannot be considered as your real level of pronunciation or fluency.

## Technologies

- Python
- Flask
- HTML
- Javascript
- SQLite

## How to Install

1) Run the sqlite script below to create and populate the tables.
2) Run python/flask command to start the application.

## How to Use

You will need a microphone to speak in the application.

1) Enable your microphone in your browser;
2) Click on the button Start to record;
3) Speak what you see after the word "Say";
4) After finish speaking, click Stop to interrupt the recording;
5) Wait for the app checking your speech;
6) Your score to the current phrase will be shown;
7) Click Next to go to another phrase; Repeat from step 2.

## Create and Populate DB tables

-- user
DROP TABLE users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    username TEXT NOT NULL, 
    hash TEXT NOT NULL, 
    score NUMERIC DEFAULT 0.0
);

CREATE UNIQUE INDEX username ON users (username);

-- phrases
DROP TABLE phrases;
CREATE TABLE phrases (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    phrase TEXT NOT NULL
);

INSERT INTO phrases (phrase) VALUES 
("Peter Piper picked a peck of pickled peppers"),
("A peck of pickled peppers Peter Piper picked"),
("I saw Susie sitting in a shoe shine shop"),
("Where she sits she shines, and where she shines she sits"),
("Send toast to ten tense stout saints' ten tall tents"),
("Sheena leads, Sheila needs"),
("Seth at Sainsbury's sells thick socks"),
("You cuss, I cuss, we all cuss, for asparagus"),
("Roberta ran rings around the Roman ruins"),
("Clean clams crammed in clean cans"),
("I wish to wish the wish you wish to wish, but if you wish the wish the witch wishes, I won't wish the wish you wish to wish"),
("Picky people pick Peter Pan Peanut-Butter, 'tis the peanut-butter picky people pick"),
("Luke Luck likes lakes"),
("Luke's duck likes lakes"),
("Luke Luck licks lakes"),
("Luck's duck licks lakes"),
("Duck takes licks in lakes Luke Luck likes"),
("Luke Luck takes licks in lakes duck likes"),
("There those thousand thinkers were thinking how did the other three thieves go through"),
("I scream, you scream, we all scream for icecream"),
("One-one was a race horse"),
("Two-two was one too"),
("One-one won one race"),
("Two-two won one too"),
("Celibate celebrant, celibate celebrant, celibate celebrant, "),
("Willy's real rear wheel"),
("Gobbling gorgoyles gobbled gobbling goblins"),
("Pirates Private Property"),
("What a terrible tongue twister,"),
("When you write copy you have the right to copyright the copy you write "),
("A big black bug bit a big black dog on his big black nose"),
("Elizabeth's birthday is on the third Thursday of this month"),
("Ann and Andy's anniversary is in April"),
("Frogfeet, flippers, swimfins"),
("Hassock hassock, black spotted hassock Black spot on a black back of a black spotted hassock"),
("How much pot, could a pot roast roast, if a pot roast could roast pot"),
("Mary Mac's mother's making Mary Mac marry me"),
("My mother's making me marry Mary Mac"),
("She saw Sherif's shoes on the sofa"),
("Through three cheese trees three free fleas flew"),
("While these fleas flew, freezy breeze blew"),
("Freezy breeze made these three trees freeze"),
("Freezy trees made these trees' cheese freeze"),
("That's what made these three free fleas sneeze"),
("Two tried and true tridents"),
("Birdie birdie in the sky laid a turdie in my eye"),
("If cows could fly I'd have a cow pie in my eye"),
("Thirty-three thirsty, thundering thoroughbreds thumped Mr Thurber on Thursday"),
("Four furious friends fought for the phone"),
("Plymouth sleuths thwart Luther's slithering"),
("Bobby Bippy bought a bat"),
("Black background, brown background"),
("Tie twine to three tree twigs"),
("Rory the warrior and Roger the worrier were reared wrongly in a rural brewery"),
("Three short sword sheaths"),
("Rolling red wagons"),
("Green glass globes glow greenly"),
("I stood sadly on the silver steps of Burgess's fish sauce shop, mimicking him hiccuping, and wildly welcoming him within"),
("black back bat"),
("The queen in green screamed"),
("I thought, I thought of thinking of thanking you"),
("Roofs of mushrooms rarely mush too much"),
("He threw three balls"),
("The great Greek grape growers grow great Greek grapes"),
("Singing Sammy sung songs on sinking sand"),
("We're real rear wheels"),
("Rhys watched Ross switch his Irish wristwatch for a Swiss wristwatch"),
("I wish to wash my Irish wristwatch"),
("Near an ear, a nearer ear, a nearly eerie ear"),
("On a lazy laser raiser lies a laser ray eraser"),
("Scissors sizzle, thistles sizzle"),
("Tom threw Tim three thumbtacks"),
("He threw three free throws"),
("Fresh French fried fly fritters"),
("I was born on a pirate ship"),
("Say it while holding your tongue"),
("Little Mike left his bike like Tike at Spike's"),
("Eddie edited it"),
("Yellow butter, purple jelly, red jam, black bread"),
("Spread it thick, say it quick"),
("Wow, race winners really want red wine right away"),
("The ruddy widow really wants ripe watermelon and red roses when winter arrives"),
("I'll chew and chew until my jaws drop"),
("Two tiny tigers take two taxis to town"),
("Sounding by sound is a sound method of sounding sounds"),
("Willie's really weary"),
("Tommy Tucker tried to tie Tammy's Turtles tie"),
("Excited executioner exercising his excising powers excessively"),
("Double bubble gum, bubbles double"),
("Octopus ocular optics"),
("A slimey snake slithered down the sandy sahara"),
("Suzie Seaword's fish-sauce shop sells unsifted thistles for thistle-sifters to sift"),
("Nothing is worth thousands of deaths"),
("Casual clothes are provisional for leisurely trips across Asia"),
("She said she should sit"),
("I wish you were a fish in my dish"),
("She stood on the balcony, inexplicably mimicking him hiccuping, and amicably welcoming him in"),
("The big black bug bit the big black bear, but the big black bear bit the big black bug back"),
("Dust is a disk's worst enemy"),
("I see a sea down by the seashore"),
("As one black bug, bled blue, black blood The other black bug bled blue"),
("Aluminum, linoleum, molybdenum, aluminum, linoleum, molybdenum, aluminum, linoleum, molybdenum"),
("Thin grippy thick slippery"),
("The owner of the inside inn was inside his inside inn with his inside outside his inside inn"),
("She sees cheese"),
("I would if I could But I can't, so I won't"),
("But a harder thing still to do"),
("Silly sheep weep and sleep"),
("I slit a sheet, a sheet I slit, upon a slitted sheet I sit"),
("Round and round the rugged rock the ragged rascal ran"),
("Buckets of bug blood, buckets of bug blood, buckets of bug blood"),
("Shut up the shutters and sit in the shop"),
("Bake big batches of bitter brown bread"),
("Bake big batches of brown blueberry bread"),
("Whoever slit the sheets is a good sheet slitter"),
("Crush grapes, grapes crush, crush grapes"),
("A black bloke's back brake-block broke"),
("There was a minimum of cinnamon in the aluminum pan"),
("Her whole right hand really hurts"),
("Busy buzzing bumble bees"),
("A lump of red leather, a red leather lump"),
("While we were walking, we were watching window washers wash Washington's windows with warm washing water"),
("Sweet sagacious Sally Sanders said she sure saw seven segregated seaplanes sailing swiftly southward Saturday"),
("There are two minutes difference from four to two to two to two, from two to two to two, too"),
("Sally is a sheet slitter, she slits sheets"),
("You know New York"),
("Ripe white wheat reapers reap ripe white wheat right"),
("Blake's black bike's back brake bracket block broke"),
("She slits the sheet she sits on"),
("Miss Smith's fish-sauce shop seldom sells shellfish"),
("Great gray goats"),
("The batter with the butter is the batter that is better"),
("There's a sandwich on the sand which was sent by a sane witch"),
("Clowns grow glowing crowns"),
("The soldier's shoulder surely hurts"),
("She sees seas slapping shores"),
("A loyal warrior will rarely worry why we rule"),
("A proper cup of coffee from a proper copper coffee pot"),
("Don't trouble trouble, until trouble troubles you If you trouble trouble, triple trouble troubles you"),
("I slit a sheet, a sheet I slit, and on that slitted sheet I sit"),
("Don't spring on the inner-spring this spring or there will be an offspring next spring"),
("Sweater weather, leather weather"),
("One black beetle bled only black blood, the other black beetle bled blue"),
("The big black bug's blood ran blue"),
("We will learn why her lowly lone, worn yarn loom will rarely earn immoral money"),
("A nurse anesthetist unearthed a nest"),
("I thought a thought"),
("She sells sea shells on the seashore"),
("The seashells she sells are seashells she is sure"),
("Plain bun, plum bun, bun without plum"),
("Slick slim slippers sliding south"),
("Ah shucks, six stick shifts stuck shut"),
("The king would sing, about a ring that would go ding"),
("People pledging plenty of pennies"),
("Mares eat oats and does eat oats, but little lambs eat ivy"),
("I wish I were what I was when I wished I were what I am"),
("She had shoulder surgery"),
("The crow flew over the river with a lump of raw liver"),
("Flies fly but a fly flies"),
("No need to light a night-light on a light night like tonight"),
("A quick witted cricket critic"),
("The cat crept into the crypt, crapped and crept out"),
("Certified certificates from certified certificate certifiers"),
("On mules we find two legs behind and two we find before"),
("We stand behind before we find what those behind be for"),
("Susie sits shinning silver shoes"),
("Silly shoe-fly pie fans sell chilly shoe-fly pie pans"),
("The two-toed tree toad tried to tread where the three-toed tree toad trod"),
("You're behaving like a babbling, bumbling band of baboons"),
("I broke a brickbat and a brickbat broke me"),
("Give papa a cup of proper coffee in a copper coffee cup"),
("Nine nice night nurses nursing nicely"),
("A singly circularly linked list"),
("Thirty-three thousand feathers on a thrushes throat"),
("If practice makes perfect and perfect needs practice"),
("I’m perfectly practiced and practically perfect"),
("It's a nice night for a white rice fight"),
("Washington's wash woman washed Washington's wash while Washington's wife went west"),
("I gratefully gazed at the gracefully grazing gazelles"),
("She sat upon a balcony, inimicably mimicking him hiccuping and amicably welcoming him in"),
("chip shop chips"),
("Shine my city shoes"),
("Tell a tall tale of a tall tailed dog, that told Tim it tap a tall ale and thump the top of Tim's tomb"),
("They think that their teeth get thinner at times they want to taste thick meat"),
("Three tired tigers try to throw three trees"),
("I wish to wish the wish you wish to wish, but if you wish the wish the witch wishes, I won't wish the wish you wish to wish"),
("How many tow trucks could a tow truck tow if a tow truck could tow tow trucks"),
("I miss my Swiss miss"),
("She thrust three thousand thistles through the thick of her thumb"),
("A snake sneaks to seek a snack"),
("A synonym for cinnamon is a cinnamon synonym"),
("I see he sees high seas she sees"),
("I saw a kitten eating chicken in the kitchen"),
("My back black brake blocks are broken"),
("Four poor fools filled four pools full"),
("Quick queens quack quick quacks quicker than quacking quails"),
("Washing the washing machine while watching the washing machine washing washing"),
("She snapped a selfie with Sophie's silver cell phone"),
("She surely suits shiny sleek short skirts"),
("Tell Tom the ticket taker to take the ticket to the ticket wicket");

-- history
DROP TABLE history;
CREATE TABLE history (
    users_id INTEGER NOT NULL, 
    phrases_id INTEGER NOT NULL,
    user_speech TEXT NULL DEFAULT NULL,
    user_speech_html TEXT NULL DEFAULT NULL,
    original_phrase_html TEXT NULL DEFAULT NULL,
    score NUMERIC DEFAULT 0.0
);

## References

English Tongue Twisters - 1st International Collection of Tongue Twisters - www.tongue-twister.net/en.htm