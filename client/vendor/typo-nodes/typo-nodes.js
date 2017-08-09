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


(function($Typo) {

  var $Typo = W.$Typo || {};
  var canvas;
  var context;
  var mouse = {x:-99999, y:-99999};
  var nodes = [];
  var dirtyRegions = [];
  var inputForce = force = 0;
  var input = forceFactor = false;
  var FPS = 60;
  var text = 'gregory' + 'nicholas';
  var interactive = true;
  var _node_friction = 0.7;



  /*
  // dat-gui settings.
  var Settings = function() {
    this.text = 'gregorynicholas';
    this.interactive = true;
    this.changeText = function(value) {
      text = value;
      nodes = [], dirtyRegions = [];
      input = true;
    };
    this.enableInteractivity = function(value) {
      !interactive ? interactive = true : interactive = false;
      mouse = { x: -99999, y: -99999 };
    };
  };
  */
  /*
  // dat-gui main
  // https://cdnjs.cloudflare.com/ajax/libs/dat-gui/0.5/dat.gui.min.js
  var GUI = new dat.GUI();
  var settings = new Settings();
  GUI.add(settings, 'text').onChange(settings.changeText);
  GUI.add(settings, 'interactive').onChange(settings.enableInteractivity);
  */




  /**
   * initializer.
   */
  $Typo.init = function() {
    this._init_canvas_dom();

    // browser supports canvas?
    if (!$Typo._supported()) {
      return console.error("browser doesn't support canvas.");
    }

    context = canvas.getContext('2d');

    // events
    if ('ontouchstart' in W) {
      canvas.addEventListener('touchstart', $Typo.onTouchStart, false);
      canvas.addEventListener('touchend', $Typo.onTouchEnd, false);
      canvas.addEventListener('touchmove', $Typo.onTouchMove, false);
    }

    else {
      canvas.addEventListener('mousedown', $Typo.onMouseDown, false);
      canvas.addEventListener('mouseup', $Typo.onMouseUp, false);
      canvas.addEventListener('mousemove', $Typo.onMouseMove, false);

    }

    $W.on('resize', function(){
      $Typo._onresize();
    });

    $Typo._build_texture();

  };


  $Typo._init_canvas_dom = function() {
    var $body = D.querySelector('body');
    canvas = D.createElement('canvas');

    canvas.id = 'gregorynicholas';
    canvas.width  = W.innerWidth;
    canvas.height = W.innerHeight * 0.75;

    canvas.style.position = 'absolute';
    canvas.style.top = 0;
    canvas.style.bottom = 0;
    canvas.style.left = 0;
    canvas.style.right = 0;
    canvas.style.zIndex = 1001;

    // canvas.style.background = '-webkit-radial-gradient(#2bb0cc, #0079a5)';
    // canvas.style.background = '-moz-radial-gradient(#2bb0cc, #0079a5)';
    // canvas.style.background = '-ms-radial-gradient(#2bb0cc, #0079a5)';
    // canvas.style.background = '-o-radial-gradient(#2bb0cc, #0079a5)';
    // canvas.style.background = 'radial-gradient(#2bb0cc, #0079a5)';

    $body.appendChild(canvas);
  };


  /**
   * window resize event.
   */
  $Typo._onresize = function(){
    canvas.width = W.innerWidth;
    canvas.height = W.innerHeight * 0.75;
    nodes = [], dirtyRegions = [];
  };


  /**
   * checks if browser supports canvas element.
   */
  $Typo._supported = function() {
    return canvas.getContext && canvas.getContext('2d');
  };


  /**
   * mouse-down event.
   */
  $Typo.onMouseDown = function(event) {
    event.preventDefault();
    forceFactor = true;
  };


  /**
   * mouse-up event.
   */
  $Typo.onMouseUp = function(event) {
    event.preventDefault();
    forceFactor = false;
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
    forceFactor = true;
  };



  /**
   * touch-end event.
   */
  $Typo.onTouchEnd = function(event) {
    event.preventDefault();
    forceFactor = false;
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
   * builds texture.
   */
  $Typo._build_texture = function() {
    context.clearRect(0, 0, canvas.width, canvas.height);

    // Let's start by drawing the original texture
    if (nodes.length === 0) {

      var _size = canvas.width / 10;
      var _step = 12;

      var _canvas = {
        width:  canvas.width * 0.5,
        height: canvas.height * 0.5
      };

      context.font = _size + 'px "Arial"';
      // context.fillStyle = 'rgba(0, 0, 0, 1)';
      context.fillStyle = 'rgba(235, 235, 235, 1)';
      context.textAlign = 'center';
      context.fontWeight = 'bold';
      context.fillText(
        text, _canvas.width, _canvas.height);


      var surface = context.getImageData(0, 0, canvas.width, canvas.height);

      context.clearRect(0, 0, canvas.width, canvas.height);

      for (var width = 0; width < surface.width; width += _step) {
        for (var height = 0; height < surface.height; height += _step) {

          var color = surface.data[(height * surface.width * 4) + (width * 4) - 1];

          // the pixel color is white? so draw on it...
          if (color === 255) {

            var x, y, radius;

            x = _canvas.width;
            y = _canvas.height;

            radius = 2 + Math.random() * 5;

            nodes.push({
              x: x,
              y: y,
              vx: 0,
              vy: 0,
              goalX: width,
              goalY: height,
              radius: radius
            });

            dirtyRegions.push({
              x: x,
              y: y,
              radius: radius
            });

          }
        }
      }
    }


    // kick-off
    $Typo._clear();
    $Typo._update();
    $Typo._render();
    requestAnimFrame($Typo._build_texture);
  };



  /**
   * clears only dirty regions.
   */
  $Typo._clear = function() {

    [].forEach.call(dirtyRegions, function(dirty, index) {
      var x, y, width, height;
      width = (2 * dirty.radius) + 4;
      height = width;
      x = dirty.x - (width / 2);
      y = dirty.y - (height / 2);

      context.clearRect(Math.floor(x), Math.floor(y), Math.ceil(width), Math.ceil(height));
    });

  };



  /**
   * updates the nodes.
   */
  $Typo._update = function() {
    var _force = 0.0001;
    var _distance = 25;

    [].forEach.call(nodes, function(node, index) {
      if (!interactive) {
        mouse.x = canvas.width * 0.5 + Math.sin(force) * context.measureText(text).width * 0.5;
        mouse.y = canvas.height * 0.47;
        force += _force;
      }

      var _angle = Math.atan2(node.y - mouse.y, node.x - mouse.x);

      // node-easing
      node.vx += Math.cos(_angle) * $Typo._distance_to(
        mouse, node, true) + (node.goalX - node.x) * 0.1;
      node.vy += Math.sin(_angle) * $Typo._distance_to(
        mouse, node, true) + (node.goalY - node.y) * 0.1;

      // node-friction
      node.vx *= _node_friction;
      node.vy *= _node_friction;

      node.x += node.vx;
      node.y += node.vy;


      if (!!forceFactor) {
        inputForce = Math.min(inputForce + 1, 5000);
      }
      else {
        inputForce = Math.max(inputForce - 1, 1000);
        // inputForce = Math.min(inputForce - 1, 500);
      }


      // check a neighborhood node
      for(var nextMolecule = index + 1; nextMolecule < nodes.length; nextMolecule++) {

        var _other_molecule = nodes[nextMolecule];

        // oh we've found one ..
        if ($Typo._distance_to(node, _other_molecule) < _distance) {
          context.save();
          context.beginPath();
          context.globalCompositeOperation = 'destination-over';
          context.globalAlpha = 1 - $Typo._distance_to(node, _other_molecule) / 100;
          context.lineWidth = 1;
          context.strokeStyle = 'rgba(255,255,255, 0.9)';
          context.moveTo(node.x, node.y);
          context.lineTo(_other_molecule.x, _other_molecule.y);
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
      context.fillStyle = 'rgba(255,255,255, 0.4)';
      context.translate(node.x, node.y);
      context.beginPath();
      context.arc(0, 0, node.radius, 0, Math.PI * 2);
      context.fill();
      context.restore();

      // dirty regions
      dirtyRegions[index].x = node.x;
      dirtyRegions[index].y = node.y;
      dirtyRegions[index].radius = node.radius;
    });

  };



  /**
   * distance between two points.
   */
  $Typo._distance_to = function(pointA, pointB, angle) {
    var dx = Math.abs(pointA.x - pointB.x);
    var dy = Math.abs(pointA.y - pointB.y);

    if (angle) {
      return (1000 + (interactive ? inputForce : 0)) / Math.sqrt(dx * dx + dy * dy);
    }
    else {
      return Math.sqrt(dx * dx + dy * dy);
    }
  };



  /**
   * request new frame (by Paul Irish)
   * 60 FPS.
   */
  W.requestAnimFrame = (function() {
    return (
      W.requestAnimationFrame   ||
      W.webkitRequestAnimationFrame ||
      W.mozRequestAnimationFrame    ||
      W.oRequestAnimationFrame      ||
      W.msRequestAnimationFrame     ||
      function(callback) {
        W.setTimeout(callback, 1000 / FPS);
      }
    );
  })();



  // window.addEventListener ? window.addEventListener('load', Typo.init, false) : window.onload = Typo.init;

  $D.ready(function(){
    $Typo.init();
  });


})($Typo);
