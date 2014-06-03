
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

  # act-i title
  blob2 = $ "#blob-2"

  blob3 = $ "#blob-3"
  blob4 = $ "#blob-4"
  blob5 = $ "#blob-5"
  blob6a = $ "#blob-6a"
  blob6b = $ "#blob-6b"

  # blew it.. jesus
  blob7 = $ "#blob-7"

  # act-ii title
  blob8 = $ "#blob-8"

  blob9 = $ "#blob-9"

  # act-iii title
  blob14 = $ "#blob-14"

  # act-iv title
  blob18 = $ "#blob-18"


  # lock for de-bouncing
  is_ticking = false

  # tracks window scroll pos.
  # also used to control easing effects
  scroll_y = 0


  # the main method for fucking with parallax shiz
  updateElements = ->
    ease_factor = 3000
    rel_y = scroll_y / ease_factor

    prllx blob1a, 0,  pos(1, -700,   rel_y, 0)
    prllx blob1b, 0,  pos(1, -400,   rel_y, 0)
    prllx blob1c, 0,  pos(1, -100,   rel_y, 0)

    prllx blob2, 311, pos(-100, 575, rel_y, 0)
    prllx blob3, 0, pos(100, -250, rel_y, 0)

    prllx blob4, 0,   pos(-170, 300, rel_y, 0)

    prllx blob6a, 0,  pos(-275, 275, rel_y, 0)

    # TODO: fuck you jesus, broken
    # prllx blob7, 0,  pos(-150, 150, rel_y, 0)

    # prllx blob8, 10, pos(-250, 250, rel_y, 0)

    # prllx blob5, 0,  pos(1730, -2900, rel_y, 0)
    # prllx blob6, 0,  pos(2860, -4900, rel_y, 0)
    # prllx blob7, 0,  pos(2550, -1900, rel_y, 0)
    # prllx blob8, 0,  pos(2300, -700,  rel_y, 0)
    # prllx blob9, 0,  pos(3700, -6000, rel_y, 0)

    is_ticking = false


  # the main algo for creating the parallax effects
  # params: base, range, relative-y, offset
  pos = (base, range, relative_y, offset) ->
    rv = base + limit(0, 1, relative_y - offset) * range
    # console.info 'relative_y:', relative_y, 'rv:', rv
    rv


  limit = (min, max, value) ->
    Math.max(min, Math.min(max, value))


  fade = (obj, alpha) ->
    prefix obj.style, "opacity", alpha


  prllx = (obj, x, y) ->
    prefix obj.style, "Transform", "translate3d(#{x}px, #{y}px, 0)"


  # cross browser prefixing for css declarations
  prefix = (obj, prop, value) ->
    prefs = ["webkit", "Moz", "o", "ms"]
    for pref of prefs
      obj[prefs[pref] + prop] = value


  # event bindings..

  onResize = ->
    updateElements win.scrollY


  onScroll = (evt) ->
    unless is_ticking
      is_ticking = true
      requestAnimFrame updateElements
      scroll_y = win.scrollY
      # console.info 'scroll_y:', scroll_y


  (->
    updateElements win.scrollY
    blob2.classList.add "force-show"
    # blob6a.classList.add "force-show"
    blob6b.classList.add "force-show"
    blob7.classList.add "force-show"
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
  $div.stop().animate({ opacity: 1 }, 1000)
  $img.stop().animate({ opacity: 1, marginTop: 0 }, 1250, 'easeInOutExpo')


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
    console.info 'unlocking animate'
    lock_animate = false
