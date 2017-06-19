Free Body Diagram practice program


/*
 * THIS COPY MADE ON 2013-05-28 AND PRESRVED AS HISTORY.  
 * Notes on this version:
 * - It works.
 * - It exists mostly as a backup.
 * - Numerous bugs are dead, including: bad rotations; strange initial arrow, bad win condition
 * - Options is more used, with new keybindings and force types
 *
 * Size estimate: 18kb of code, 7kb of other (e.g., data, options, this file, etc).
 * Actual amount typed is more, due to deletion.
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