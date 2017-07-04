
$win = $ window
$doc = $ document


$doc.on 'ready', ->
  $win.trigger 'scroll'
  $win.trigger 'resize'
  $win.trigger 'dScroll'
  $win.trigger 'dResize'
  console.info('[app.js]', 'document.ready..')


console.info('[app.js]', 'script load finished..')
