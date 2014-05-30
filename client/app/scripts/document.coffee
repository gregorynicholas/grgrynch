
$window = $ window
$doc = $ document


$doc.on 'ready', ->
  $window.trigger 'scroll'
  $window.trigger 'resize'
  $window.trigger 'dScroll'
  $window.trigger 'dResize'
