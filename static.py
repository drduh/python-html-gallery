"""Variables for gallery.py."""

root = '/home/drduh/www'  # path to jpgs or folders of jpgs and output root
tmp = '/tmp'              # temporary folder to move corrupt files to
index = 'index.html'      # filename for html files
n_thumbs = 3              # number of thumbnails to display on index page
min_size = 500,500        # minimum dimensions required to create thumbnail
thumb_size = 250,250      # dimensions of thumbnail to create

header = ("""<!doctype html>
<html>
<head>
  <title>%s</title>
  <meta charset="utf-8" />
  <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style type="text/css">
    body {
      background-color: #002b36;
      color: #839496;
      font-family: "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;
      margin: 0;
      padding: 0;
    }
    div {
      background-color: #073642;
      border-radius: 0.25em;
      margin: 1em auto;
      padding: 2em;
      width: 800px;
    }
    p {
      font-size: 16px;
      padding-bottom: 1.5em;
    }
    a:link, a:visited {
      color: #93a1a1;
      font-size: 24px;
      text-decoration: underline;
    }
    img {
      padding: 0.1em;
      border-radius: 0.25em;
    }
  </style>
</head>
<body>
<div>
""")

br = '\n<br>'
footer = '\n</div></body></html>'
img_src = '\n<img src="%s">'
timestamp = '\n<p>This page was created on %s</p>'
url_dir = '\n<p><a href="%s" target="_blank">%s</a></p>'
url_img = '\n<a href="%s" target="_blank"><img title="%s" src="%s"></a>'
