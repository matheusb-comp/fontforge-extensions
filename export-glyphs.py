import fontforge
import pathlib

def loop(data, font):
	# Get input form 'data' or the UI
	if fontforge.hasUserInterface():
		# Directory path where files will be saved
		path = fontforge.saveFilename(
			"Export glyphs to folder...",
			font.fullname
		)
		if not path: return 0

		# File extension
		idx = fontforge.askChoices(
			"File Type",
			"Export glyphs as:",
			("SVG", "PNG", "PDF"),
			default=0
		)
		if idx < 0: return 0
		extension = ["svg", "png", "pdf"][idx]
	elif isinstance(data, dict):
		path = data['path']
		extension = data['extension']
	else:
		fontforge.postError("Error", "No data provided")
		return 1
	
	# Create the directory (equivalent to mkdir -p)
	pathlib.Path(path).mkdir(parents=True, exist_ok=True)

	# Iterate over the glyphs in the font
	glyphs = font.glyphs()
	for glyph in glyphs:
		# Ignore some glyphs
		if not glyph.isWorthOutputting(): continue

		# Append the filename to the path
		filename = "{path}/{unicode:04X}_{name}.{extension}".format(
			path=path,
			extension=extension,
			name=glyph.glyphname,
			unicode=glyph.unicode
		)

		# Export the glyph
		glyph.export(
			filename,
			pixelsize=400
		)

# Setup the 'loop' function in the Tools menu
if fontforge.hasUserInterface():
	fontforge.registerMenuItem(
		loop,
		None,
		None,
		"Font",
		None,
		"Export All Glyphs"
	)
