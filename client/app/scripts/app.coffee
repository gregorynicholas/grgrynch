
$window = $ window
$doc = $ document


startDebounce = ->
  console.info 'startDebounce'

  $window = $ window

  debounceTimeScroll = 500
  debounceTimeResize = 250
  didScroll = false
  didResize = false


  # bind event handlers

  $window.on 'scroll', ->
    didScroll = true

  $window.on 'resize', ->
    didResize = true


  # rate limiting function hooks

  setInterval (->
    return if not didScroll

    didScroll = false
    $window.trigger 'dScroll'

  ), debounceTimeScroll


  setInterval (->
    return if not didResize

    didResize = false
    $window.trigger 'dResize'

  ), debounceTimeResize


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


startDebounce()


init = ->
  $root = $ "html, body"
  docHeight = $root.height()
  $wrap = $ ".fixed-wrapper"

  $head = $wrap.find ">header"
  $sections = $wrap.find ">section"

  $story = $ "#intro"
  $what = $ "#what"
  $where = $ "#where"
  $contact = $ "#contact"
  $footer = $ "#footer"

  storyOffset = $story.offset()
  storyHeight = $story.outerHeight()

  whatOffset = $what.offset()
  whatHeight = $what.outerHeight()
  whereOffset = $where.offset()
  whereHeight = $where.outerHeight()

  contactOffset = $contact.offset()
  contactHeight = $contact.outerHeight()

  winH = $window.height()
  winW = $window.width()
  scrollTop = $window.scrollTop()

  oldScroll = 0
  sectionExtraHeight = winH * 6
  cumExtraHeight = sectionExtraHeight * $sections.length
  centerBuffer = 100
  scaleFactor = 4
  scrollBottom = 780
  $fixWrapper = null

  $('body').css
    height: ($wrap.height() * scaleFactor) + cumExtraHeight + $footer.height()

  $story.on 'scrollInView', (e, start, end, prog) ->
    # console.log('scrollTop: ' + scrollTop, ' | start: ' + start, ' | end: ' + end, ' | prog: ' + prog )

  $window.on 'scroll', (e) ->
    scroll = $window.scrollTop()
    scrollPaused = false
    fauxScroll = -(scrollTop) / scaleFactor

    $sections.each (i, e) ->
      $this = $ @
      centerPos = $this.data 'centerPos'

      if scroll > centerPos - centerBuffer && scroll < centerPos + sectionExtraHeight + centerBuffer
        scrollPaused = true
        calcMarginTop = -1 * ((centerPos/scaleFactor) - ((sectionExtraHeight/scaleFactor) * i))

        if not $.support.transition
          $fixWrapper.css marginTop: calcMarginTop
        else
          $fixWrapper.transition
            marginTop: calcMarginTop,
            easing: 'ease-out',
            duration: 200,
            queue: false

        $this.trigger 'scrollInView', [centerPos - centerBuffer, centerPos + sectionExtraHeight + centerBuffer]

init()
