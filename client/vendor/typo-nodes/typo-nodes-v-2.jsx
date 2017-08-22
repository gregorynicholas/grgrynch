/*
 * Copyright MIT © <2013> <Francesco Trillini>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
 * documentation files (the "Software"), to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
 * to permit persons to whom the Software is furnished to do so, subject to the following conditions:

 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
 * PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
 * FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
 * ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */


// see https://codepen.io/gregorynicholas/pen/XaWdgp


var $Typo = {};
var W = window;
var D = document;
var $W = $(W);
var $D = $(D);


(function($Typo, id, string) {

  var $Typo = W.$Typo || {};
  var canvas;
  var context;
  var raf;
  var mouse = {x:-99999, y:-99999};
  var nodes = [];
  var dirtyRegions = [];
  var inputForce = force = 0;
  var forceFactor = false;


  $Typo.settings = {
    text: string || 'artist,engineer,cto',
    fps: 30,
    interactive: true,
    node_friction: 0.92,
    // node_friction: 0.5,
    // node_friction: 0.35,

    // distance: 25,
    // distance: 50,
    distance: 75,
    // step: 12,
    step: 24,
    font_size: null,

    canvas: {
      x: null,
      y1: null,
      y2: null,
      y3: null,
      w: null,
      h: null
    }
  };



  /**
   * initializer.
   */
  $Typo.init = function() {
    //@ browser supports canvas?
    this._init_canvas_dom();
    if (!$Typo._supported()) {
      return console.error("browser doesn't support canvas.");
    }

    context = canvas.getContext('2d');

    //@ events
    if ('ontouchstart' in W || 'touchstart' in W) {
      canvas.addEventListener('touchstart', $Typo.onTouchStart, false);
      canvas.addEventListener('touchend',   $Typo.onTouchEnd,   false);
      canvas.addEventListener('touchcancel',$Typo.onTouchEnd,   false);
      canvas.addEventListener('touchmove',  $Typo.onTouchMove,  false);
    }

    else {
      canvas.addEventListener('mousedown', $Typo.onMouseDown, false);
      canvas.addEventListener('mouseup',   $Typo.onMouseUp,   false);
      canvas.addEventListener('mousemove', $Typo.onMouseMove, false);
    }

    //@ <TODO> buggy on chrome mobile ..
    if (!('ontouchstart' in W) && !('touchstart' in W)) {
      $W.on('resize', function(){
        $Typo._onresize();
      });
    }

    this._build_texture();

  };


  $Typo._init_canvas_dom = function() {
    var $body = D.querySelector('body');
    canvas = D.createElement('canvas');

    canvas.id = 'gregorynicholas-' + id;
    canvas.width  = W.innerWidth;
    canvas.height = W.innerHeight * 0.78;
    // canvas.height = W.innerHeight;

    // canvas.style.background = '-webkit-radial-gradient(#2bb0cc, #0079a5)';
    // canvas.style.background = '-moz-radial-gradient(#2bb0cc, #0079a5)';
    // canvas.style.background = '-ms-radial-gradient(#2bb0cc, #0079a5)';
    // canvas.style.background = '-o-radial-gradient(#2bb0cc, #0079a5)';
    // canvas.style.background = 'radial-gradient(#2bb0cc, #0079a5)';

    $Typo.settings.font_size = Math.floor(canvas.width / 8);
    $body.appendChild(canvas);
  };


  /**
   * checks if browser supports canvas element.
   */
  $Typo._supported = function() {
    return canvas.getContext && canvas.getContext('2d');
  };


  /**
   * window resize event.
   */
  $Typo._onresize = function(){
    canvas.width = W.innerWidth;
    canvas.height = W.innerHeight * 0.78;
    // canvas.height = W.innerHeight;
    nodes = [];
    dirtyRegions = [];
  };

  $Typo._set_force_factor = function(){
    forceFactor = true;
  };

  $Typo._unset_force_factor = function(){
    forceFactor = false;
  };


  /**
   * mouse-down event.
   */
  $Typo.onMouseDown = function(event) {
    event.preventDefault();
    $Typo._set_force_factor();
  };

  /**
   * mouse-up event.
   */
  $Typo.onMouseUp = function(event) {
    event.preventDefault();
    $Typo._unset_force_factor();
  };

  /**
   * mouse-move event.
   */
  $Typo.onMouseMove = function(event) {
    event.preventDefault();

    mouse.x = event.pageX - canvas.offsetLeft;
    mouse.y = event.pageY - canvas.offsetTop;
  };


  /**
   * touch-start event.
   */
  $Typo.onTouchStart = function(event) {
    event.preventDefault();
    $Typo._set_force_factor();
  };

  /**
   * touch-end event.
   */
  $Typo.onTouchEnd = function(event) {
    event.preventDefault();
    $Typo._unset_force_factor();
  };

  /**
   * touch-move event.
   */
  $Typo.onTouchMove = function(event) {
    event.preventDefault();

    mouse.x = event.touches[0].pageX - canvas.offsetLeft;
    mouse.y = event.touches[0].pageY - canvas.offsetTop;
  };



  /**
   * builds the text node-texture.
   */
  $Typo._build_texture = function() {
    $Typo._clear();

    //@ start by drawing the original texture ..
    if (nodes.length === 0) {

      $Typo.settings.canvas.x  = canvas.width  * 0.2;
      $Typo.settings.canvas.y1 = canvas.height * 0.25;
      $Typo.settings.canvas.y2 = canvas.height * 0.4;
      $Typo.settings.canvas.y2 = canvas.height * 0.65;

      $Typo.settings.canvas.w = canvas.width * 0.5;
      $Typo.settings.canvas.h = canvas.height * 0.75;

      context.font = $Typo.settings.font_size + 'px Arial';
      // context.fillStyle = 'rgba(0, 0, 0, 1.0)';
      // context.fillStyle = 'rgba(235, 235, 235, 1.0)';
      // context.textAlign = 'center';
      context.fillStyle = 'rgba(255,255,255, 1.0)';
      context.fontWeight = 'bold';

      context.fillText('artist',   $Typo.settings.canvas.x, $Typo.settings.canvas.y1);
      context.fillText('engineer', $Typo.settings.canvas.x, $Typo.settings.canvas.y2);
      context.fillText('cto',      $Typo.settings.canvas.x, $Typo.settings.canvas.y3);

      var _surface = context.getImageData(0, 0, canvas.width, canvas.height);

      $Typo._clear();

      for (var width = 0;  width < _surface.width;  width += $Typo.settings.step) {
        for (var height = 0;  height < _surface.height;  height += $Typo.settings.step) {

          //@ if pixel-color is white, then draw a node for it ..
          var _color = _surface.data[(height * _surface.width * 4) + (width * 4) - 1];

          if (_color !== 255)
            continue;

          var _x = $Typo.settings.canvas.w;
          var _y = $Typo.settings.canvas.h;

          var _radius = 1 + (Math.random() * 5);

          nodes.push({
            x: _x,
            y: _y,
            vx: 0,
            vy: 0,
            goalX: width + (Math.random() * 20),
            goalY: height + (Math.random() * 20),
            radius: _radius
          });

          dirtyRegions.push({
            x: _x,
            y: _y,
            radius: _radius
          });

        }
      }
    }

    //@ kick-off..!
    $Typo._clear_dirty();
    $Typo._update();
    $Typo._render();
    raf = requestAnimFrame($Typo._build_texture);
  };


  $Typo._clear = function() {
    context.clearRect(0, 0, canvas.width, canvas.height);
  };


  /**
   * clears regions marked as "dirty"
   */
  $Typo._clear_dirty = function() {

    [].forEach.call(dirtyRegions, function(dirty, idx) {
      var _w = (2 * dirty.radius) + 4;

      var _x = dirty.x - (_w / 2);
      var _y = dirty.y - (_w / 2);

      _w = Math.ceil(_w);
      _x = Math.floor(_x);
      _y = Math.floor(_y);

      context.clearRect(_x, _y, _w, _w);

    });

  };



  /**
   * updates the nodes.
   */
  $Typo._update = function() {
    var _force = 0.0001;
    var _texture_line_w = 2;
    var _texture_line_c = 'rgba(255,255,255, 0.9)';
    var _text_width = context.measureText($Typo.settings.text).width;
    var _node_length = nodes.length;


    [].forEach.call(nodes, function(node, _node_idx) {

      if (!$Typo.settings.interactive) {
        mouse.x = canvas.width * 0.5 + Math.sin(force) * _text_width * 0.5;
        mouse.y = canvas.height * 0.47;
        force += _force;
      }

      var _angle = Math.atan2(node.y - mouse.y, node.x - mouse.x);
      var _mouse_distance = $Typo._distance_to(mouse, node, true);

      //@ node velocity easing
      node.vx += Math.cos(_angle) * _mouse_distance + (node.goalX - node.x) * 0.1;
      node.vy += Math.sin(_angle) * _mouse_distance + (node.goalY - node.y) * 0.1;

      //@ node velocity friction
      node.vx *= $Typo.settings.node_friction;
      node.vy *= $Typo.settings.node_friction;

      node.x += node.vx;
      node.y += node.vy;

      if (!!forceFactor) {
        inputForce = Math.min(inputForce + 1, 5000);
      }
      else {
        inputForce = Math.max(inputForce - 1, 1000);
        // inputForce = Math.min(inputForce - 1, 500);
      }

      //@ check neighboring nodes..
      for (var _next_idx = _node_idx+1; _next_idx < _node_length; _next_idx++) {

        var _next_node = nodes[_next_idx];

        //@ oh we've found one ..

        var _next_distance = $Typo._distance_to(node, _next_node);
        if (_next_distance < $Typo.settings.distance) {
          var _alpha = 1 - (_next_distance / 100);

          context.save();
          context.beginPath();
          // context.globalCompositeOperation = 'destination-over';
          context.globalCompositeOperation = 'lighten';
          context.globalAlpha = _alpha;
          context.lineWidth = _texture_line_w;
          context.strokeStyle = _texture_line_c;
          context.moveTo(node.x, node.y);
          context.lineTo(_next_node.x, _next_node.y);
          context.stroke();
          context.closePath();
          context.restore();

        }
      }

    });
  };




  /*
   * renders the nodes.
   */
  $Typo._render = function() {

    [].forEach.call(nodes, function(node, index) {
      context.save();
      context.fillStyle = 'rgba(255,255,255, 0.2)';
      context.translate(node.x, node.y);
      context.beginPath();
      context.arc(0, 0, node.radius, 0, Math.PI * 2);
      context.fill();
      context.restore();

      //@ mark 'dirty' regions
      dirtyRegions[index].x = node.x;
      dirtyRegions[index].y = node.y;
      dirtyRegions[index].radius = node.radius;
    });

  };



  /**
   * distance between two points.
   */
  $Typo._distance_to = function(pointA, pointB, angle) {
    var absdx = Math.abs(pointA.x - pointB.x);
    var absdy = Math.abs(pointA.y - pointB.y);
    var sqrt = Math.sqrt(absdx * absdx + absdy * absdy);

    var result = sqrt;

    if (angle) {
      if ($Typo.settings.interactive) {
        result = 1000 + inputForce / sqrt;
      }
      else {
        result = 1000 / sqrt;
      }
    }

    return result;
  };



  /**
   * request new frame (by Paul Irish)
   * 60 FPS.
   */
  W.requestAnimFrame = (function() {
    return (
      W.requestAnimationFrame       ||
      W.webkitRequestAnimationFrame ||
      W.mozRequestAnimationFrame    ||
      W.oRequestAnimationFrame      ||
      W.msRequestAnimationFrame     ||
      function(_fn) {
        W.setTimeout(_fn, 1000 / $Typo.settings.fps);
      }
    );
  })();



  // window.addEventListener ? window.addEventListener('load', Typo.init, false) : window.onload = Typo.init;

  $D.ready(function(){
    $Typo.init();
  });


})($Typo, '01');


// $Typo('artist');
// $Typo('engineer');
// $Typo('cto');

