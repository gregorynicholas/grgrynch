
$window = $ window
$doc = $ document


# frames per second, for a nice, smooth buttox
fps = 60

# shim layer with setTimeout fallback
window.requestAnimFrame = (->
  window.requestAnimationFrame or window.webkitRequestAnimationFrame or window.mozRequestAnimationFrame or window.oRequestAnimationFrame or window.msRequestAnimationFrame or (callback) ->
    window.setTimeout callback, 1000 / fps
    return
)()


((win, doc) ->

  $ = doc.querySelector.bind doc

  blob1a = $ "#blob-1a"
  blob1b = $ "#blob-1b"
  blob1c = $ "#blob-1c"

  #@ act-i title
  blob2a = $ "#blob-2"

  blob3a = $ "#blob-3"
  blob4a = $ "#blob-4"
  blob5a = $ "#blob-5"
  blob6a = $ "#blob-6a"
  blob6b = $ "#blob-6b"

  #@ blew it.. jesus
  blob7a = $ "#blob-7"

  #@ act-ii title
  blob8a = $ "#blob-8"

  blob9a = $ "#blob-9"

  #@ act-iii title
  blob14 = $ "#blob-14"

  #@ act-iv title
  blob18 = $ "#blob-18"


  #@ lock for de-bouncing
  is_ticking = false

  #@ tracks window scroll pos.
  #@ also used to control easing effects
  scroll_x = 0
  scroll_y = 0

  #@ main method for fucking with parallax shiz..
  updateElements = ->
    ease_factor = 3000
    rel_x = scroll_x / ease_factor
    rel_y = scroll_y / ease_factor
    rel_z = 0

    prllx_y(blob1a,   0, pos(1, -700,   rel_y, 0, rel_z))
    prllx_y(blob1b,   0, pos(1, -400,   rel_y, 0, rel_z))
    prllx_y(blob1c,   0, pos(100, 500, rel_y, 0, rel_z))
    prllx_y(blob2a, 311, pos(-100, 575, rel_y, 0, rel_z))
    prllx_y(blob3a,   0, pos(100, -275, rel_y, 0, rel_z))
    prllx_y(blob4a,   0, pos(-170, 250, rel_y, 0, rel_z))
    prllx_y(blob6a,   0, pos(-275, 275, rel_y, 0, rel_z))

    #@ <TODO>
    #@     let's transform the map by scaling from smaller to larger..
    # prllx_scale(blob6b,   0, pos(-275, 275, rel_y, 0, rel_z))

    #@ <TODO> fuck you jesus, broken..
    # prllx blob7a, 0,  pos(-150, 150, rel_y, 0)
    # prllx blob8a, 10, pos(-250, 250, rel_y, 0)
    # prllx blob5a, 0,  pos(1730, -2900, rel_y, 0)
    # prllx blob6a, 0,  pos(2860, -4900, rel_y, 0)
    # prllx blob7a, 0,  pos(2550, -1900, rel_y, 0)
    # prllx blob8a, 0,  pos(2300, -700,  rel_y, 0)
    # prllx blob9a, 0,  pos(3700, -6000, rel_y, 0)

    # console.info('[app.js]', 'updateElements', blob1a, blob1b, blob1c, blob2a, blob3a, blob4a)
    is_ticking = false


  # the main algo for creating the parallax effects
  # params: base, range, relative-y, offset
  pos = (base, range, relative_y, offset) ->
    rv = base + limit(0, 1, relative_y - offset) * range
    # console.info 'relative_y:', relative_y, 'rv:', rv
    rv

  limit = (min, max, value) ->
    Math.max(min, Math.min(max, value))

  # prllx_fade = ($obj, alpha) ->
  #   prefix $obj.style, "opacity", alpha

  prllx_scale = ($obj, x, y, z) ->
    console.info('not implemented..')

  prllx_y = ($obj, x, y, z) ->
    if ! z?
      z = 0

    prefix $obj, "transform", "translate3d(#{x}px, #{y}px, #{z}px)"

  # cross browser prefixing for css declarations
  prefix = ($obj, prop, value) ->
    _style = ""
    prefs = ["-webkit-", "-moz-", "-o-", "-ms-", ""]

    for pref in prefs
      _key = prefs[pref] + prop
      _style += "#{pref}#{prop}: #{value};"

    # console.info('style:', _style)
    $obj.setAttribute 'style', _style
    # $obj.style = _style
    # $obj.style["#{prep}Style"] = _style
    # $obj.style["webkit#{prep}Style"] = _style


  # event bindings..

  onResize = ->
    updateElements win.scrollY


  onScroll = (evt) ->
    # console.info('[app.js]', 'onScroll..', evt)

    unless is_ticking
      is_ticking = true
      requestAnimFrame updateElements
      scroll_y = win.scrollY
      # console.info 'scroll_y:', scroll_y


  (->
    updateElements win.scrollY
    blob2a.classList.add "force-show"
    # blob6a.classList.add "force-show"
    blob6b.classList.add "force-show"
    blob7a.classList.add "force-show"
  )()

  win.addEventListener "resize", onResize, false
  win.addEventListener "scroll", onScroll, false

) window, document



$("#section-07").appear()
has_appeared = {}

$(document.body).on 'appear', '#section-07', (e, $affected) ->
  $el = $(@)
  id = $el.attr('id')
  return if has_appeared[id]
  has_appeared[id] = true

  $div = $el.find('div')
  $img = $div.find('img')
  $div.stop().animate({ opacity: 2 }, 2000)
  $img.stop().animate({ opacity: 1, marginTop: 0 }, 1550, 'easeInOutExpo')


$(document.body).on 'disappear', '#section-07', (e, $affected) ->
  $el = $(@)
  id = $el.attr('id')

  $div = $el.find('div')
  $img = $div.find('img')
  $div.stop().css opacity: 0
  $img.stop().css opacity: 0, marginTop: 200

  has_appeared[id] = false


$logo = $ '.animated-css3'
lock_animate = false


rotate = (callback) ->
  $logo.transition 'rotate': '0deg', duration: 0
  $logo.transition 'rotate': '+=180'
  $logo.transition 'rotate': '+=180', ->
    callback()


$logo.on 'mouseover', ->
  return if lock_animate
  lock_animate = true
  rotate ->
    # console.info 'unlocking animate'
    lock_animate = false



String.prototype.toProperCase = ()->
  _fn = (_txt)->
    _txt.charAt(0).toUpperCase() + _txt.substr(1).toLowerCase()

  @replace(/\w\S*/g, _fn)
