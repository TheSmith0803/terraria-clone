tasks to complete:

- add random noise generator for surface DONE but needs to be better 
- change block behavior for dropping and picking up (grass drops dirt, mining takes a minute)
    - made grass drop dirt, and now grass dissapears when surrounded
- do pixel art (first tools and sword, extra blocks and stuff)
- give player health, and render health bar ✅
- get command console working to some extent 
- make interactible objects (new door, make placeable, maybe make chest openable)

- Make chests and chest inventories work!
 - Need to make chests spawnable in some fashion, preferably owned by the world class
 - Need to make chests interactable, by changing the function of the players right click action
 - Need to add different game states (in inventory browser, or not, stuff like that)

things to fix:
    Collisions!: We need to be able to index the new file in order to find particular tiles, and generate a position somehow.
    Brainstorming will be required for this task

    I made the debug world size SUPER small. 32x32, 4 chunks.

    Figure out why tiles are only rendering in one spot. (top left world tile)

ideas:

tbd lol

CHUNK ORGANIZATION:
    CHUNK_{0,0}
        tile | indx:
                   _______
        0,0     0         |
        1,0     1         | 
        2,0     2         |
        3,0     3         |       
        4,0     4         |
        5,0     5         |   
        6,0     6         |
        7,0     7         |
        8,0     8         | <- One row of one chunk
        9,0     9         |
        10,0    10        |
        11,0    11        |
        12,0    12        |
        13,0    13        |
        14,0    14        |
        15,0    15 _______|

        0,1     16
        1,1     17
        2,1     18   <- Next row and so on
        3,1     19

        etc...
