import flash.utils.Timer;
import flash.events.TimerEvent;
import flash.display.MovieClip;
import flash.display.Sprite;
import flash.display.Shape;

//Constant Variables
const gravity:Number = 10;
const jumpPowerBurst:Number = 25;
const obstacleSpeed:Number = 10;
const obTimeSpeed:Number = 1500;

//Initiate MovieClips
//var displayScore: MovieClip = new DisplayScore();
var gameTitle: MovieClip = new GameTitle();
var startMessage: MovieClip = new ClickToPlay();

//Variables 
var jumpPower:Number = 0;
var ground:Number = 400 - player.height - grass_Ground.height;
var score:Number = 0;
var gameState:Boolean = false;
var showScore:Boolean = false;
var isJumping:Boolean = false;
var gameStart:Boolean = false;
var stopObstacle:Boolean = false;

//Arrays
var allPipes: Array = []; //List of all PipesObstacle we have made so far
var allScoreCheckBlocks: Array = []; //List of all ScoreCheckBlocks we have made so far

//Timers
var obstacleTimer: Timer = new Timer(obTimeSpeed);

//Event Listeners
stage.addEventListener(Event.ENTER_FRAME, PlayGame);
stage.addEventListener(MouseEvent.MOUSE_DOWN, doJump);
obstacleTimer.addEventListener(TimerEvent.TIMER, onTimer);

/****************************************
* Main Funtion                          *
****************************************/
function PlayGame(Event)
{	
	if (gameState == false)
	{
		showTitle();
	}
	
	if (stopObstacle == false)
	{
		playerGravity(); //Applies gravity to player character
		
		moveAllObstacles(); //Moves Obstacles across stage
		
		removeObstacle();
		
		obstacleHitTest();
	}
	
	if (showScore == true)
	{
		dispScore();
	}
}


/***************************************
* Jump Funtions                        *
***************************************/
function doJump(event: MouseEvent)
{
	
	if(!gameStart)
		startGame();
		
	if(gameStart)
        jumpPower = jumpPowerBurst;
	
	gameState = true;
	
}

function playerGravity()
{
	if(isJumping)  
    {  
        player.y -= jumpPower;  
        jumpPower -= 2;
    }
	if(player.y + gravity < ground && gameStart)  
        player.y += gravity;
}

/***************************************
* Functions to spawn an obstacle every *
*    1 second                          *
***************************************/
function onTimer(event: TimerEvent)
{
	
	spawnObstacles(); //Spawns Obstacle
	
}

function spawnObstacles()
{
	var randNum:Number = 0; //Initiate random number variable
	var maxNum:Number = 400 - (player.height * 3);
	var minNum:Number = 0 + (player.height * 4.5);
	
	//Initiate MovieClips
	var PipeObstacleTop: MovieClip = new pipeObstacle();
	var PipeObstacleBottom: MovieClip = new pipeObstacle();
	var ScoreCheckBlock:Shape = new Shape;
	
	//Find y location of bottom pipes
	randNum = Math.floor(Math.random() * (maxNum - minNum + 1)) + minNum;
	
	//Build Bottom Pipe
	PipeObstacleBottom.x = 650; //Spawns pipe off stage
	PipeObstacleBottom.y = randNum;
	
	//Build Top Pipe
	PipeObstacleTop.rotation = 180;
	PipeObstacleTop.x = 650 + PipeObstacleTop.width;
	PipeObstacleTop.y = randNum - (player.height * 4);
	
	//Build Score Block
	ScoreCheckBlock.graphics.drawRect(2, 2, 2, 2);
	ScoreCheckBlock.y = -50;
    ScoreCheckBlock.x = 650 + PipeObstacleTop.width;
	
	//Add pipes to stage
	addChild(PipeObstacleBottom);
	addChild(PipeObstacleTop);
	addChild(ScoreCheckBlock);
	
	//Add pipes to array
	allPipes.push(PipeObstacleBottom);
	allPipes.push(PipeObstacleTop);
	allScoreCheckBlocks.push(ScoreCheckBlock);
}

function moveAllObstacles()
{
	//For every pipe in allPipes aray
	for each (var PipeObstacle:* in allPipes)
	{
		//Move across stage from right to left
		PipeObstacle.x -= obstacleSpeed;
	}
	
	//For every ScoreCheckBox in allScoreCheckBlocks aray
	for each (var ScoreCheckBlock:* in allScoreCheckBlocks)
	{
		//Move across stage from right to left
		ScoreCheckBlock.x -= obstacleSpeed;
	}
}

function removeObstacle()
{
	for each (var PipeObstacle:* in allPipes)
	{
		if (PipeObstacle.x < -100)
		{
			if (contains(PipeObstacle))
				removeChild(PipeObstacle);
		}
	}
	
	for each (var ScoreCheckBlock:* in allScoreCheckBlocks)
	{
		if (ScoreCheckBlock.x < player.x)
		{
			if (contains(ScoreCheckBlock))
			{
				removeChild(ScoreCheckBlock);
				score += 1;
				trace(score);
			}
		}
	}
}

/***************************************
* Function to start the game           *
***************************************/
function startGame()
{
	//Activate Ball
	gameStart = true;
	
	//Hide Title Screen
	removeChild(gameTitle);
	removeChild(startMessage);
	
	//Enable Ball Physics
	isJumping = true;
	
	//Satrt Obstacle Timer
	obstacleTimer.start();
	
}

/***************************************
* Function to test if ball hits        *
* an obstacle                          *
***************************************/
function obstacleHitTest()
{
	for each (var PipeObstacle:* in allPipes)
	{
		if (player.hitTestObject(PipeObstacle))
		{
			stopGame();
		}
	}
	
	if (player.y < 0 || player.y > ground)
		stopGame();
}

/***************************************
* Function to stop the game            *
***************************************/
function stopGame()
{
	stopObstacle = true;
	showScore = true;
}

/***************************************
* Function to show score               *
***************************************/
function dispScore()
{	
	//Initiate MovieClips
	var displayScore: MovieClip = new DisplayScore();
	
	//Add player score
	displayScore.pScore.text = String(score);
	
	//Locate Score on Stage
	displayScore.x = (550 - displayScore.width) / 2;
	displayScore.y = (400 - displayScore.height) / 2;
	
	//Add child to stage
	addChild(displayScore);
}

function showTitle()
{
	gameTitle.x = (550 - gameTitle.width) / 2;
	gameTitle.y = (400 - gameTitle.height) / 3;
	
	startMessage.x = (550 - startMessage.width) / 2;
	startMessage.y = ((400 - startMessage.height) / 3) * 2;
	
	addChild(gameTitle);
	addChild(startMessage);
} 