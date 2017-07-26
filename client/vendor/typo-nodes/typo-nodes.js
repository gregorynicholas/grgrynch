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


var Typo = {};


(function(Typo) {

  var Typo = window.Typo || {};
  var canvas, context;
  var mouse = { x: -99999, y: -99999 };
  var nodes = [];
  var dirtyRegions = [];
  var inputForce = force = 0;
  var input = forceFactor = false;
  var FPS = 60;
  var text = 'gregory' + 'nicholas';
  var interactive = true;



  /*
   * Settings.
   */
  /*
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
    * Init.
   */
  Typo.init = function() {

    /*
    // Dat GUI main
    // https://cdnjs.cloudflare.com/ajax/libs/dat-gui/0.5/dat.gui.min.js
    var GUI = new dat.GUI();
    var settings = new Settings();
    GUI.add(settings, 'text').onChange(settings.changeText);
    GUI.add(settings, 'interactive').onChange(settings.enableInteractivity);
    */

    var body = document.querySelector('body');
    canvas = document.createElement('canvas');

    canvas.id = 'gregorynicholas';
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight * 0.75;

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

    body.appendChild(canvas);

    // Browser supports canvas?
    if(!!(Typo.gotSupport())) {

      context = canvas.getContext('2d');

      // Events
      if('ontouchstart' in window) {
        canvas.addEventListener('touchstart', Typo.onTouchStart, false);
        canvas.addEventListener('touchend', Typo.onTouchEnd, false);
        canvas.addEventListener('touchmove', Typo.onTouchMove, false);
      }

      else {
        canvas.addEventListener('mousedown', Typo.onMouseDown, false);
        canvas.addEventListener('mouseup', Typo.onMouseUp, false);
        canvas.addEventListener('mousemove', Typo.onMouseMove, false);

      }

      $(window).on('resize', function(){
        Typo.onResize();
      });

      Typo.buildTexture();

    }

    else {

      console.error("Sorry, your browser doesn't support canvas.");

    }

  };


  /*
   * On resize window event.
   */
  Typo.onResize = function(){
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight * 0.75;
    nodes = [], dirtyRegions = [];
  };


  /*
   * Check if browser supports canvas element.
   */
  Typo.gotSupport = function() {

    return canvas.getContext && canvas.getContext('2d');

  };

  /*
   * Mouse down event.
   */

  Typo.onMouseDown = function(event) {

    event.preventDefault();

    forceFactor = true;

  };

  /*
   * Mouse up event.
   */

  Typo.onMouseUp = function(event) {

    event.preventDefault();

    forceFactor = false;

  };



  /*
   * Mouse move event.
   */

  Typo.onMouseMove = function(event) {

    event.preventDefault();

    mouse.x = event.pageX - canvas.offsetLeft;
    mouse.y = event.pageY - canvas.offsetTop;

  };



  /*
   * Touch start event.
   */

  Typo.onTouchStart = function(event) {

    event.preventDefault();

    forceFactor = true;

  };



  /*
   * Touch end event.
   */

  Typo.onTouchEnd = function(event) {

    event.preventDefault();

    forceFactor = false;

  };



  /*
   * Touch move event.
   */

  Typo.onTouchMove = function(event) {

    event.preventDefault();

    mouse.x = event.touches[0].pageX - canvas.offsetLeft;
    mouse.y = event.touches[0].pageY - canvas.offsetTop;

  };



  /*
   * Building texture.
   */

  Typo.buildTexture = function() {

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


    // Logic
    Typo.clear();
    Typo.update();
    Typo.render();
    requestAnimFrame(Typo.buildTexture);
  };



  /*
   * Clear only dirty regions.
   */

  Typo.clear = function() {

    [].forEach.call(dirtyRegions, function(dirty, index) {
      var x, y, width, height;
      width = (2 * dirty.radius) + 4;
      height = width;
      x = dirty.x - (width / 2);
      y = dirty.y - (height / 2);

      context.clearRect(Math.floor(x), Math.floor(y), Math.ceil(width), Math.ceil(height));
    });

  };



  /*
   * Let's update the nodes.
   */
  Typo.update = function() {

    var _force = 0.0001;
    var _distance = 25;

    [].forEach.call(nodes, function(node, index) {
      if (!interactive) {
        mouse.x = canvas.width * 0.5 + Math.sin(force) * context.measureText(text).width * 0.5;
        mouse.y = canvas.height * 0.47;
        force += _force;
      }

      var angle = Math.atan2(node.y - mouse.y, node.x - mouse.x);

      // Ease
      node.vx += Math.cos(angle) * Typo.distanceTo(mouse, node, true) + (node.goalX - node.x) * 0.1;
      node.vy += Math.sin(angle) * Typo.distanceTo(mouse, node, true) + (node.goalY - node.y) * 0.1;

      // Friction
      node.vx *= 0.7;
      node.vy *= 0.7;

      node.x += node.vx;
      node.y += node.vy;


      if(!!forceFactor)
        inputForce = Math.min(inputForce + 1, 5000);
      else
        inputForce = Math.max(inputForce - 1, 1000);
        // inputForce = Math.min(inputForce - 1, 500);


      // check a neighborhood node
      for(var nextMolecule = index + 1; nextMolecule < nodes.length; nextMolecule++) {

        var otherMolecule = nodes[nextMolecule];

        // oh we've found one!
        if (Typo.distanceTo(node, otherMolecule) < _distance) {
          context.save();
          context.beginPath();
          context.globalCompositeOperation = 'destination-over';
          context.globalAlpha = 1 - Typo.distanceTo(node, otherMolecule) / 100;
          context.lineWidth = 1;
          // context.strokeStyle = 'rgba(0,0,0, 0.8)';
          context.strokeStyle = 'rgba(255,255,255, 0.9)';
          context.moveTo(node.x, node.y);
          context.lineTo(otherMolecule.x, otherMolecule.y);
          context.stroke();
          context.closePath();
          context.restore();

        }

      }

    });

  };




  /*
   * Let's render the nodes.
   */
  Typo.render = function() {
    [].forEach.call(nodes, function(node, index) {
      context.save();
      context.fillStyle = 'rgba(255,255,255, 0.4)';
      context.translate(node.x, node.y);
      context.beginPath();
      context.arc(0, 0, node.radius, 0, Math.PI * 2);
      context.fill();
      context.restore();

      // Dirty regions
      dirtyRegions[index].x = node.x;
      dirtyRegions[index].y = node.y;
      dirtyRegions[index].radius = node.radius;
    });

  };



  /*
   * Distance between two points.
   */

  Typo.distanceTo = function(pointA, pointB, angle) {

    var dx = Math.abs(pointA.x - pointB.x);
    var dy = Math.abs(pointA.y - pointB.y);

    if (angle)
      return (1000 + (interactive ? inputForce : 0)) / Math.sqrt(dx * dx + dy * dy);

    else
      return Math.sqrt(dx * dx + dy * dy);
  };



  /*
   * Request new frame by Paul Irish.
   * 60 FPS.
   */
  window.requestAnimFrame = (function() {
    return  window.requestAnimationFrame   ||
        window.webkitRequestAnimationFrame ||
        window.mozRequestAnimationFrame    ||
        window.oRequestAnimationFrame      ||
        window.msRequestAnimationFrame     ||
        function(callback) {
          window.setTimeout(callback, 1000 / FPS);
        };
      })();

  // window.addEventListener ? window.addEventListener('load', Typo.init, false) : window.onload = Typo.init;

  $(document).ready(function(){
    Typo.init();
  });

})(Typo);


console.info('Typo:', Typo);

