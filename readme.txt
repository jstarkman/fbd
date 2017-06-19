Free Body Diagram practice program

/*
 * THIS COPY MADE ON 2013-05-31 AND PRESERVED AS FINAL
 * Notes on this version:
 * - It works.
 * - It exists for distribution and history
 * - The .exe has been made (w/ cx_freeze)
 * - Minor changes to accomodate for how cx_freeze works.  Ordinary running of code has no change in results.
 * 	- This means little
 *
 * Bugs that were finally put to rest: arrows and click-and-drag on the interface
 * New features: local forces (see yo-yo for example) (implemented by invisible blocks); instructions map; map title displayed in-sim; degree sign.
 * 
 * Size estimate: 21-22kb of code, 10kb of non-media other (data, this file, options).
 * In lines: 400/classes.py ; 196/fbd.py ; 101/read.py ; 25/setup.py
 * Total: 722
 * 	- However, there are well-spaced parts, obfuscated parts, and all of pygame itself, so this is not a good measure
 * Actual amount typed is more, due to deletion.
 * This text was added after building the .exe, and is not part of that total.
 */

Notes on drawing:
	Computers number pixels like cells in Excel (R) - positive on the x-axis is right, while positive on the y is down.
	Do not put anything in the top 64px - the interface goes there.
	
	order of drawing, lowest layer to highest:
		map - in order of tags.  Put ropes first and text last.
		interface - the 64px at the top
		blocks - do not put too close together.  Bad things happen.
		arrows - order entered, newest on top

Notes on the data file, "data.txt":
	tags and syntax, to save empiricism
		pulley:x of ctr:y:radius
		ramp_r:incline, eg 30:x of upper-right point:y
		ramp_l:incline, eg 330:x or upper-left point:y
		table:x:y:width:height
		rope:x1:y1:x2:y2:x3:as needed, no limit
		text:<text to be rendered>:x of upper-left corner:y:R:G:B

		block
		force:name:angle it should be at (degrees, from East, upwards)
		size:side length, in px:mass
		pos:x of center:y:angle
		color:R:G:B

	Anything not in square brackets is a comment.  Do not use the open square bracket ("[") in your comments.  It tells the parser that a new tag is here, and will confuse it terribly.
	To temporarily remove a tag, replace the [] with () or {}.  The parser will then treat it like a comment, because it is.

	The map tags (e.g., pulley, table) defined above do not do anything; they merely make images.  As such, they can be used to draw - indeed, in the code, that is all they do.  




Notes on using the program (instructions)
	Click and drag to make an arrow.  Then click the correct type (from the menu) after releasing the arrow.  You can also hit the bound key (see options.txt for bindings) to select the type.  Repeat as needed until you think that all of the forces present are represented.  Then either press Enter or click the checkmark to check whether the forces are correct.  To dismiss the popup, press Enter.  Any bad arrows will be cleared; any good, kept.  When all of the needed arrows are present, the screen will exit to the homescreen.