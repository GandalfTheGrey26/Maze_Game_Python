# PROGRAM INFORMATION

## Credits

| Title                                           | Composer/Author                       | Websites                                                     |
| ----------------------------------------------- | ------------------------------------- | ------------------------------------------------------------ |
| Win.mp3                                         | Glenn Middleton                       | flat.io<br />onlinesequencer.net                             |
| Game_Over.mp3                                   |                                       | https://www.freesoundslibrary.com/game-over-piano-sound-effect/#google_vignette |
| For_Your_Life.mp3                               | Dubpixel                              | https://dubpixel.itch.io/pixel-madness-music-pack            |
| Pygame Template                                 |                                       | https://openbookproject.net/thinkcs/python/english3e/pygame.html |
| num2words (python library)                      |                                       | https://pypi.org/project/num2words/                          |
| text_rect = text.get_rect(center=(WIDTH//2, y)) | PythonProgrammi (Stack Overflow User) | https://stackoverflow.com/questions/23982907/how-to-center-text-in-pygame |
| Maze One                                        |                                       | https://atariage.com/forums/topic/185667-maze-example-program-with-pac-man-style-sprite/ |
| Turrent.png                                     |                                       | http://pixelartmaker.com/gallery?after=663863                |

## Classes

-Player
-Enemy
-Coin
-Bullet
-MenuSprite

## Functions

-game() 
-menu()
-settings()
-pHelp()
-win() 
-lose()
-mazeOutline() 
-drawMaze(mainSurface, squareSize, color)
-init(self, mainSurface, pos, alive, delayLength, color) [MenuSprite]
-draw(self) [MenuSprite]
-init(self, mainSurface, spritePos, othSpritePos) [Bullet]
-draw(self) [Bullet]
-init(self, mainSurface, playerCoordinates, scale, playerColor, squareSize, mazeLvl) [Player]
-drawPlayer(self) [Player]
-movePlayer(self, key) [Player]
-init(self, mainSurface, scale, enemyRect, enemyColor, squareSize, mazeLvl) [Enemy]
-drawEnemy(self) [Enemy]
-enemyBarrierCheck(self, direction) [Enemy]
-moveEnemy(self, playerCoordinates) [Enemy]
-updateEnemy(self) [Enemy]
-init(self, mainSurface, scale, squareSize, mazeLvl) [Coin]
-drawCoin(self) [Coin]

​	