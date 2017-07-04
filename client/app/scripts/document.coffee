
$window = $ window
$doc = $ document


$doc.on 'ready', ->
  $window.trigger 'scroll'
  $window.trigger 'resize'
  $window.trigger 'dScroll'
  $window.trigger 'dResize'
  console.info('[app.js]', 'document.ready..')


console.info('[app.js]', 'script load finished..')
