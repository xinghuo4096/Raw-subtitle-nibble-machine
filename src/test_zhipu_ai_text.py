import re

user_input1 = "Wednesday Ever since I can remember, the world has been ending somewhere.<字幕断句>Species extinction, deforestation, economic crises, environmental pollution, terrorism and climate change. Thanks a lot!<字幕断句>Pit stop? - Yes.<字幕断句>Somewhere there is always the next crisis, the next war - and mankind has but a few years left...<字幕断句>...to avert the apocalypse. You get used to it.<字幕断句>But on Slaborn? Nothing ever happens!<字幕断句>Everyone knows everyone, everyone is nice, beautiful landscape, dunes, meadows, cows, pensioners on sailboats. Boring? For sure!<字幕断句>But I'm only fifteen and newly in love.<字幕断句>I wouldn't mind if we could postpone the end of the world for a while, please!<字幕断句>Where is Evelin?<字幕断句>Sorry, I'm here.<字幕断句>Are you feeling better?<字幕断句>I don't know.<字幕断句>Everybody but Herm Sperm Show it! - Wait, do it again.<字幕断句>Wait. I want to film it, wait<字幕断句>Okay, you got it? - Yes.<字幕断句>Guys, guys, guys!<字幕断句>Dude, show me!<字幕断句>Enough already?<字幕断句>I'm fine.<字幕断句>What a twatface, dude!<字幕断句>You're all such idiots.<字幕断句>Dude, since when does Evelin like Miscarriage?<字幕断句>What do I know? Chicks... Whatever. - Did you break up?"
user_input2 = "Shut the fuck up!\nChill, dude.\nEvelin has left the group.\nIt can't go on like this, Herm.\nWhat'?I didn't do anything.- Exactly!\nYou really need to stop being such a victim.\nWow, great idea.I've only been trying that since forever?!\nTonight, at the Fisker-Party.\nYou're going with me.- No!I'm not suicidal.\nThen you can save your own ass in the future.\nI'll pick you up at nine.\nArrival Hello!- Hello!\nHello, Richard!- Hello!\nHello!- Hello!\nYes, she's coming, she's coming.\nRichard!\nMerit, hello!\nAre you picking up your daughter?\nKnuspa is picking her up, I'm just the driver.\nAnd you are picking up Luis?- Oh, God forbid, no.\nHe would be embarrassed.\nNo, I, uh, I'm waiting for Nikolai Wagner.\nTHE Nikolai Wagner?\"Zeugenzwerg\"?\nExactly.\nWow!- Yes.\nAuthor's reading and book signing session in my shop.\nMaybe even in the Pavilion.- And people say nothing\nhappens here culturally.\nHe's currently writing his new novel.Maybe he'll set part of\nit here on the island.\nWow.- Yes.\nOkay, you are right.The whole"
user_input3 = """
386
0:33:53,160 --> 0:33:54,680
You have to deal with me.

387
0:33:56,240 --> 0:33:59,280
Okay.Cool.I don't mind...Uh, I mean, great.

388
0:34:3,240 --> 0:34:4,760
You guys got this, right?

389
0:34:9,320 --> 0:34:11,920
Yeah, looks shit, right?- Nah, it's fine.

390
0:34:15,480 --> 0:34:16,920
May I?- Uh, yes.

391
0:34:46,920 --> 0:34:47,760
Yeah.

392
0:34:49,480 --> 0:34:50,960
Yeah, okay then...

393
0:34:52,760 --> 0:34:53,840
Shall we?- Yes.

394
0:35:44,480 --> 0:35:47,360
Okay.I'll take blow for fifty.

395
0:35:50,520 --> 0:35:51,800
I don't know you.

396
0:35:52,560 --> 0:35:53,280
So what?

397
0:35:54,560 --> 0:35:55,880
This is my party-

398
0:35:57,280 --> 0:35:58,440
You are not invited.

399
0:35:58,680 --> 0:36:0,640
I just want some coke.

400
0:36:2,160 --> 0:36:3,40
Isn't that...

401
0:36:4,320 --> 0:36:5,80
Illegal?

402
0:36:5,600 --> 0:36:8,920
I don't know.I'm not with the drug squad.

403
0:36:9,120 --> 0:36:12,440
Hey, my name is Nikolai Wagner.You can google me.

404
0:36:12,560 --> 0:36:13,440
And then?

405
0:36:13,760 --> 0:36:16,840
Well then you see that I have the Ingeborg Bachmann Award.

406
0:36:16,920 --> 0:36:18,760
And no, this is not a police medal.

407
0:36:18,840 --> 0:36:19,720
I am a writer.

408
0:36:19,920 --> 0:36:21,240
Listen, you big shot.

409
0:36:22,640 --> 0:36:24,80
I don't care who you are.

410
0:36:25,400 --> 0:36:27,560
You're not invited and that's it!

411
0:36:29,200 --> 0:36:29,960
Get lost!

412
0:36:36,760 --> 0:36:37,920
Where's Mom?

413
0:36:39,480 --> 0:36:42,560
Quickly back to the office.The real estate thing tomorrow

414
0:36:42,640 --> 0:36:43,440
for grandpa...

415
0:36:45,0 --> 0:36:46,360
ls there a free seat?

416
0:36:47,160 --> 0:36:48,40
Sure.

417
0:37:19,440 --> 0:37:20,360
Hey!

418
0:37:21,40 --> 0:37:21,960
How is it?

419
0:37:22,960 --> 0:37:23,760
Hi.

420
0:37:28,320 --> 0:37:31,40
How do we know you're not a snitch?- A what?
"""
user_input4 = """
417
0:34:9,240 --> 0:34:10,880
What'?
- I know what is happening

418
0:34:10,960 --> 0:34:11,960
in that hospital.
"""

user_input5 = """
552
0:45:25,160 --> 0:45:27,680
we have allocated you, the
residents, into groups according

553
0:45:27,760 --> 0:45:28,800
to blood test results.
"""
